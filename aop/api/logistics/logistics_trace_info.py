# -*- coding: utf-8 -*-
from aop.api.base import BaseApi


class AlibabaTradeGetLogisticsTraceInfoBuyerViewParam(BaseApi):
    """该接口需要获取订单买家的授权，获取买家的订单的物流跟踪信息，在采购或者分销场景中，作为买家也有获取物流详情的需求。该接口能查能根据物流单号查看物流单跟踪信息。由于物流单录入的原因，可能跟踪信息的API查询会有延迟。该API需要向开放平台申请权限才能访问。In the procurement or distribution scenario, buyers can obtain information on logistics tracking. The interface can view the logistics tracking information according to the logistics tacking number. Depending on the logistics information entry time, there may be a delay in API queries regarding the information tracking.

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.logistics&n=alibaba.trade.getLogisticsTraceInfo.buyerView&v=1&cat=wuliu

    """

    def __init__(self, app_info, access_token, order_id, *, domain=None, web_site='1688', logistics_id=''):
        BaseApi.__init__(self, app_info, domain)
        self.access_token = access_token
        self.logisticsId = logistics_id
        self.orderId = order_id
        self.webSite = web_site

    def get_api_uri(self):
        return '1/com.alibaba.logistics/alibaba.trade.getLogisticsTraceInfo.buyerView'

    def get_required_params(self):
        return ['orderId', 'webSite']

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
