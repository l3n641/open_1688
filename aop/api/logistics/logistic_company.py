# -*- coding: utf-8 -*-
from aop.api.base import BaseApi


class AlibabaLogisticsOpQueryLogisticCompanyListParam(BaseApi):
    """获取所有的物流公司名称

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.logistics&n=alibaba.logistics.OpQueryLogisticCompanyList&v=1&cat=aop.logistics

    """

    def __init__(self, app_info, access_token, *, domain=None):
        BaseApi.__init__(self, app_info, domain)
        self.access_token = access_token

    def get_api_uri(self):
        return '1/com.alibaba.logistics/alibaba.logistics.OpQueryLogisticCompanyList'

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
