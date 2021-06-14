# -*- coding: utf-8 -*-
from aop.api.base import BaseApi


class AlibabaTradeGetBuyerOrderListParam(BaseApi):
    """获取买家的订单列表，也就是用户的memberId必须等于订单里的买家memberId。该接口仅仅返回订单基本信息，不会返回订单的物流信息和发票信息；如果需要获取物流信息，请调用获取订单详情接口；如果需要获取发票信息，请调用获取发票信息的API

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.trade&n=alibaba.trade.getBuyerOrderList&v=1&cat=order_category

    """

    def __init__(self, app_info, access_token, domain=None, *, biz_types=None, create_end_time=None,
                 create_start_time=None, is_his=None, modify_end_time=None, modify_start_time=None, order_status=None,
                 page=None, page_size=None, refund_status=None, seller_member_id=None, seller_login_id=None,
                 seller_rate_status=None, trade_type=None, product_name=None, need_buyer_address_and_phone=None,
                 need_memo_info=None):
        BaseApi.__init__(self, app_info, domain)
        self.access_token = access_token
        self.bizTypes = biz_types
        self.createEndTime = create_end_time
        self.createStartTime = create_start_time
        self.isHis = is_his
        self.modifyEndTime = modify_end_time
        self.modifyStartTime = modify_start_time
        self.orderStatus = order_status
        self.page = page
        self.pageSize = page_size
        self.refundStatus = refund_status
        self.sellerMemberId = seller_member_id
        self.sellerLoginId = seller_login_id
        self.sellerRateStatus = seller_rate_status
        self.tradeType = trade_type
        self.productName = product_name
        self.needBuyerAddressAndPhone = need_buyer_address_and_phone
        self.needMemoInfo = need_memo_info

    def get_api_uri(self):
        return '1/com.alibaba.trade/alibaba.trade.getBuyerOrderList'

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
