import time
import hmac
import hashlib
import requests
import json
from aop.structure import AppInfo
from aop.exceptions import AopError, ApiError
from abc import abstractmethod, ABCMeta
from requests.exceptions import HTTPError

# constants
P_OPENAPI = 'openapi'
P_API = 'api'
P_PARAM2 = 'param2'

# system parameters
P_ACCESS_TOKEN = 'access_token'
P_TIMESTAMP = '_aop_timestamp'
P_SIGN = '_aop_signature'

P_ERROR_CODE = 'error_code'
P_ERROR_MESSAGE = 'error_message'
P_EXCEPTION = 'exception'
P_REQUEST_ID = 'request_id'

P_SYS_PARAMS = [P_TIMESTAMP, P_SIGN, P_ACCESS_TOKEN]


class FileItem(metaclass=ABCMeta):
    def __init__(self, filename=None, content=None):
        """
        Parameters
        ----------
        content : file-like-object(str/bytes/bytearray or an object that has read attribute)
            e.g. f = open('filepath', 'rb') ... fileitem = aop.api.FileItem('filename', f)
            e.g. fileitem = aop.api.FileItem('filename', 'file_content_str')

        """
        self.filename = filename
        self.content = content


class BaseApi(object):
    """"Base class of APIs.

    """

    def __init__(self, app_info: AppInfo, domain=None):
        """
        初始化接口
        :param app_info:
        :param domain:
        """
        self.__domain = domain or "gw.open.1688.com"
        self.__http_method = "POST"
        self.__app_key = app_info.app_key
        self.__secret = app_info.secret

    def raise_aop_error(self, *args):
        _args = ['API: ' + self.get_api_uri()]
        if args:
            _args.extend(args)
        raise AopError(*_args)

    def sign(self, url_path, params, secret):
        """
        Method to generate _aop_signature.
        Parameters
        ----------
        url_path : str param2/version/namespace/name/appkey
        params : dict-like
        secret : str
        References
        ----------
        https://open.1688.com/api/sysSignature.htm

        """
        if not url_path:
            self.raise_aop_error('sign error: urlPath missing')
        if not secret:
            self.raise_aop_error('sign error: secret missing')

        param_list = []
        if params:
            if not hasattr(params, "items"):
                self.raise_aop_error('sign error: params must be dict-like')
            param_list = [k + v for k, v in params.items()]
            param_list = sorted(param_list)

        msg = bytearray(url_path.encode('utf-8'))
        for param in param_list:
            msg.extend(bytes(param.encode('utf-8')))

        sha = hmac.new(bytes(secret.encode('utf-8')), None, hashlib.sha1)
        sha.update(msg)
        return sha.hexdigest().upper()

    @abstractmethod
    def get_api_uri(self):
        pass

    def need_sign(self):
        """True if _aop_signature is needed"""
        return False

    def need_timestamp(self):
        """True if _aop_timestamp is needed"""
        return False

    def need_auth(self):
        """True if access_token is needed"""
        return False

    def need_https(self):
        """True if to send a https request"""
        return False

    def is_inner_api(self):
        """True if not an open api. Usually false."""
        return False

    def get_multipart_params(self):
        """
        Returns
        -------
        list
            API parameters with type of byte[].
            A multipart request will be sent if not empty.
            e.g. returns ['image'] if the 'image' parameter's type is byte[].
                Then assign it as req.image = aop.api.FileItem('imagename.png', imagecontent)

        """
        return []

    def get_required_params(self):
        """
        Names of required API parameters.
        System parameters(access_token/_aop_timestamp/_aop_signature) excluded.

        An AopError with message 'Required params missing: {"missing_param1_name", ...}'
        will be thrown out if some of the required API parameters are missing before a
        request sent to the remote server.

        """
        return []

    def __get_url_protocol(self):
        return 'https' if self.need_https() else 'http'

    def _build_sign_url_path(self):
        return '%s/%s/%s' % (P_PARAM2, self.get_api_uri(), self.__app_key)

    def _build_url(self, sign_url_path):
        return '%s://%s/%s/%s' % (self.__get_url_protocol(), self.__domain,
                                  P_API if self.is_inner_api() else P_OPENAPI, sign_url_path)

    def _check_sign(self):
        if self.need_sign():
            if not self.__app_key:
                self.raise_aop_error('AppKey missing')
            if not self.__secret:
                self.raise_aop_error('App secret missing')

    def _check_auth(self, **kwargs):
        if self.need_auth():
            if not kwargs.get(P_ACCESS_TOKEN):
                self.raise_aop_error('access_token missing')

    def _check_required_params(self, **kwargs):
        missing_params = set(self.get_required_params()) - set(kwargs.keys())
        if missing_params:
            self.raise_aop_error('Required params missing: %s' % (str(missing_params)))

    @staticmethod
    def _gen_timestamp():
        return int(time.time() * 1000)

    def get_response(self, timeout=5, **kwargs):

        params = self._get_nonnull_biz_params()
        if kwargs:
            params.update(kwargs)

        if self.need_sign():
            self._check_sign()
        if self.need_auth():
            self._check_auth(**params)
        if self.get_required_params():
            self._check_required_params(**params)
        if self.need_timestamp() and (not params.get(P_TIMESTAMP)):
            params[P_TIMESTAMP] = self._gen_timestamp(self.__domain)

        for multipart_param in self.get_multipart_params():
            params.pop(multipart_param)

        sign_url_path = self._build_sign_url_path()
        if self.need_sign() and (not params.get(P_SIGN)):
            params[P_SIGN] = self.sign(sign_url_path, params, self.__secret)

        url = self._build_url(sign_url_path)
        headers = self._get_request_header();

        files = {}
        if self.get_multipart_params():
            for key in self.get_multipart_params():
                fileitem = getattr(self, key)
                if (fileitem and isinstance(fileitem, FileItem)):
                    files[key] = (fileitem.filename, fileitem.content)
                else:
                    self.raise_aop_error(key + ' not a FileItem')
        response = self._do_request(url, params, files, headers=headers, timeout=timeout)

        return response

    def _do_request(self, url, data=None, files=None, **kwargs):
        try:
            if files:
                response = requests.post(url, data=data, files=files, **kwargs)
            else:
                response = requests.post(url, data=data, **kwargs)

            response.raise_for_status()
            return response.json()

        except HTTPError as e:
            if not (response.status_code >= 200 and response.status_code < 400):
                param = {
                    "api": self.get_api_uri(),
                    "error_code": response.get(P_ERROR_CODE),
                    'error_message': response.get(P_ERROR_MESSAGE),
                    "exception": response.get(P_EXCEPTION),
                    'request_id': response.get(P_REQUEST_ID)
                }
                raise ApiError(**param)

            raise e
        except requests.RequestException as e:
            self.raise_aop_error(str(e))

    @staticmethod
    def _get_request_header():
        return {
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Ocean-SDK-Client'
        }

    @staticmethod
    def _is_nonnull_biz_param(param_name, param_value):
        if param_name in P_SYS_PARAMS:
            return True
        return (not param_name.startswith("__")) and (not param_name.startswith("_BaseApi__")) and param_value

    def _get_nonnull_biz_params(self):
        biz_params = {}
        for key, value in self.__dict__.items():
            if self._is_nonnull_biz_param(key, value):
                biz_params[key] = value
        return biz_params
