# -*- coding: utf-8 -*-
from aop.api.base import BaseApi
from aop.structure import Address, Cargo, Invoice


class AlibabaTradeFastCreateOrderParam(BaseApi):
    """快速创建1688大市场订单和1688代销订单，订单一步创建，不需要先调用订单预览，接口参数简单，地址参数传省市区街道的文本名，不需要额外查询地址码，系统默认选择最优惠下单方式，默认支付宝担保交易方式，详细地址必须不超过200个字，不要用地址做其他用途，需要留言或备注的有专门字段，留言和备注都支持500字

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.trade&n=alibaba.trade.fastCreateOrder&v=1&cat=aop.trade

    """

    def __init__(self, app_info, access_token, address: Address, cargo: Cargo, *, flow="general", domain=None,
                 sub_user_id=None, message="", invoice: Invoice = None, shop_promotion_id="", trade_type=""):
        BaseApi.__init__(self, app_info, domain)
        self.access_token = access_token
        self.flow = flow
        self.subUserId = sub_user_id
        self.message = message
        self.addressParam = address.get_data()
        self.cargoParamList = cargo.get_data()
        self.invoiceParam = invoice.get_data() if invoice else None
        self.shopPromotionId = shop_promotion_id
        self.tradeType = trade_type

    def get_api_uri(self):
        return '1/com.alibaba.trade/alibaba.trade.fastCreateOrder'

    def get_required_params(self):
        return ['flow', 'addressParam', 'cargoParamList']

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
