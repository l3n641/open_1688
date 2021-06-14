# -*- coding: utf-8 -*-
from aop.api.base import BaseApi


class AlibabaTradeReceiveAddressGetParam(BaseApi):
    """买家获取保存的收货地址信息列表

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.trade&n=alibaba.trade.receiveAddress.get&v=1&cat=aop.trade

    """

    def __init__(self, app_info, access_token, domain=None):
        super().__init__(app_info, domain)
        self.access_token = access_token

    def get_api_uri(self):
        return '1/com.alibaba.trade/alibaba.trade.receiveAddress.get'

    def get_required_params(self):
        return []

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def need_https(self):
        return False

    def is_inner_api(self):
        return False
