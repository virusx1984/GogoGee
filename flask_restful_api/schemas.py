from marshmallow import Schema, fields
from datetime import datetime

class LocationSchema(Schema):
    id = fields.Integer(dump_only=True)
    country = fields.String()
    province = fields.String()
    city = fields.String()
    street = fields.String()
    address = fields.String()
    longitude = fields.Float()
    latitude = fields.Float()

class CompanySchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name
    location_id = fields.Integer(required=True)
    location = fields.Nested(LocationSchema)

class BGSchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name

class BUSchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name
    bg_id = fields.Integer(required=True)
    bg = fields.Nested(BGSchema)

class PlantDistrictSchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()
    company_id = fields.Integer(required=True)
    company = fields.Nested(CompanySchema)
    location_id = fields.Integer(required=True)
    location = fields.Nested(LocationSchema)

class PlantSchema(Schema):
    id = fields.Integer(dump_only=True)
    plant_code = fields.String(required=True)  # like SA03, QA08 etc.
    plant_district_id = fields.Integer(required=True)
    plant_district = fields.Nested(PlantDistrictSchema)
    bu_id = fields.Integer(required=True)  # may be one building owned by multi BUs
    bu = fields.Nested(BUSchema)

class SupplierSchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name
    region = fields.String()  # the location of headquarters
    web_site = fields.String()
    detail_info = fields.String()

class SupplierPODSchema(Schema):
    id = fields.Integer(dump_only=True)
    alias = fields.String(required=True)
    location_id = fields.Integer(required=True)
    location = fields.Nested(LocationSchema)
    supplier_id = fields.Integer(required=True)
    supplier = fields.Nested(SupplierSchema)

class CurrencyExSchema(Schema):
    id = fields.Integer(dump_only=True)
    fr_curr = fields.String(required=True)
    to_curr = fields.String(required=True)
    ex_dt = fields.DateTime(default=datetime.now)
    ex_rate = fields.Float(required=True)

class MachineSchema(Schema):
    id = fields.Integer(dump_only=True)
    supplier_pod_id = fields.Integer(required=True)
    supplier_pod = fields.Nested(SupplierPODSchema)
    proxy_supplier_pod_id = fields.Integer()
    proxy_supplier_pod = fields.Nested(SupplierPODSchema)
    plant_id = fields.Integer(required=True)
    plant = fields.Nested(PlantSchema)
    floor = fields.Float()
    coordx = fields.Float()
    coordy = fields.Float()
    m_length = fields.Float()  # the length of the machine
    m_width = fields.Float()  # the width of the machine
    m_height = fields.Float()  # the height of the machine
    cover_length = fields.Float()  # include operation area, repairing area etc.
    cover_width = fields.Float()  # include operation area, repairing area etc.
    standard_name = fields.String(required=True)
    verbose_name = fields.String()  # the machine called by the worker normally
    m_model = fields.String()
    verbose_num = fields.Integer()  # like Drill machine #1
    detail_info = fields.String()
    acuisition_date = fields.Date()

class AssetSchema(Schema):
    id = fields.Integer(dump_only=True)
    machine_id = fields.Integer(required=True)
    machine = fields.Nested(MachineSchema)
    num = fields.String(required=True)
    tmp_num = fields.String()
    asset_name = fields.String(required=True)
    original_price = fields.Float()
    op_currency = fields.String()  # currency of original price
    op_date = fields.Date()  # date of original price
    acquisition_price = fields.Float()
    ap_currency = fields.String()  # currency of acquisition price
    ap_date = fields.Date()  # date of acquisition price

class CustomerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name
    region = fields.String()  # the location of headquarters
    web_site = fields.String()
    detail_info = fields.String()

class ShippingSiteSchema(Schema):
    id = fields.Integer(dump_only=True)
    customer_id = fields.Integer(required=True)
    customer = fields.Nested(CustomerSchema)
    company_id = fields.Integer(required=True)  # the company to send the bill to
    company = fields.Nested(CompanySchema)
    location_id = fields.Integer(required=True)
    location = fields.Nested(LocationSchema)
    name_eng = fields.String(required=True)
    name_chn = fields.String()  # maybe there is no chinese name, just let it equals to english name

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    customer_id = fields.Integer(required=True)
    customer = fields.Nested(CustomerSchema)
    cpn = fields.String()  # customer part number
    proj = fields.String()  # customer project
    pn = fields.String()  # part number
    semi_pn = fields.String()  # semi product part number
    detail_info = fields.String()

