import json


class AppInfo(object):
    def __init__(self, app_key, secret):
        self.app_key = app_key
        self.secret = secret


class Address(object):
    def __init__(self, address_id, full_name, mobile, phone, post_code, city, province, area, town, address,
                 district_code):
        self.addressId = address_id
        self.fullName = full_name
        self.mobile = mobile
        self.phone = phone
        self.postCode = post_code
        self.cityText = city
        self.provinceText = province
        self.areaText = area
        self.townText = town
        self.address = address
        self.districtCode = district_code

    def get_data(self):
        data = {}
        for key, value in self.__dict__.items():
            data[key] = value
        return json.dumps(data)


class Cargo(object):
    def __init__(self):
        self.param_list = []

    def add(self, offer_id, spec_id, quantity):
        data = {
            "offerId": offer_id,
            "specId": spec_id,
            "quantity": quantity,
        }
        self.param_list.append(data)

    def get_data(self):
        return json.dumps(self.param_list)


class Invoice(object):
    def __init__(self, invoice_type, province, city, area, town, address, post_code, district_code, full_name, phone,
                 mobile, company_name, tax_payer_identifier, bank_account, local_invoice_id):
        self.invoiceType = invoice_type
        self.fullName = full_name
        self.mobile = mobile
        self.phone = phone
        self.postCode = post_code
        self.cityText = city
        self.provinceText = province
        self.areaText = area
        self.townText = town
        self.address = address
        self.districtCode = district_code
        self.companyName = company_name
        self.taxpayerIdentifier = tax_payer_identifier
        self.bankAndAccount = bank_account
        self.localInvoiceId = local_invoice_id

    def get_data(self):
        data = {}
        for key, value in self.__dict__.items():
            data[key] = value
        return json.dumps(data)
