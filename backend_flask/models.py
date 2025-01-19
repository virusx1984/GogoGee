from sqlalchemy import Column, Integer, String, func, Date, DateTime, Float, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from . import db

class Location(db.Model):
    __tablename__ = 'oog_location'

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    country = Column(String(100))
    province = Column(String(100))
    city = Column(String(100))
    street = Column(String(200))
    address = Column(String(200))
    longitude = Column(Float)
    latitude = Column(Float)

    def __repr__(self):
        return f'<Location {self.address}>'
    
class Company(db.Model):
    __tablename__ = 'oog_company'
    __table_args__ = {'comment': 'a company group that owns many subsidiaries'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    name_eng = Column(String(50))
    name_chn = Column(String(50), comment='If there is no Chinese name, it will default to the English name.')

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    def __repr__(self):
        return f'<Company {self.name_eng}>'

class BG(db.Model):
    __tablename__ = 'oog_bg'
    __table_args__ = {'comment': 'Business Group (BG1, BG2, BG3 etc)'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name_eng = Column(String(50))
    name_chn = Column(String(50), comment='If there is no Chinese name, it will default to the English name.')

    def __repr__(self):
        return f'<BG {self.name_eng}>'

class BU(db.Model):
    __tablename__ = 'oog_bu'
    __table_args__ = {'comment': 'Business Unit (HDI, FPC, MSAP, RPCB, BTK etc)'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name_eng = Column(String(50))
    name_chn = Column(String(50), comment='If there is no Chinese name, it will default to the English name.')

    bg_id = Column(Integer, ForeignKey('oog_bg.id'))
    bg = relationship('BG')

    def __repr__(self):
        return f'<BU {self.name_eng}>'
    
class PlantDistrict(db.Model):
    __tablename__ = 'oog_plant_district'
    __table_args__ = {'comment': 'place where many plants located (SA, SB, HA, HB, QA etc)'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name_eng = Column(String(50))
    name_chn = Column(String(50))

    company_id = Column(Integer, ForeignKey('oog_company.id'))
    company = relationship('Company')

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    def __repr__(self):
        return f'<PlantDistrict {self.name_eng}>'
    
class Plant(db.Model):
    __tablename__ = 'oog_plant'
    __table_args__ = {'comment': 'specific building of a factory (SA03, SA02)'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    plant_code = Column(String(10), comment = 'like SA03, QA08 etc.')

    plant_district_id = Column(Integer, ForeignKey('oog_plant_district.id'))
    plant_district = relationship('PlantDistrict')

    bu_id = Column(Integer, ForeignKey('oog_bu.id'), comment = 'may be one building owned by multi bus. like part of SA02 is owned by FPC and the left part is owned by HDI.')
    bu = relationship('BU')

    def __repr__(self):
        return f'<Plant {self.plant_code}>'
    
class Supplier(db.Model):
    __tablename__ = 'oog_supplier'
    __table_args__ = {'comment': 'machine, material, and outsourcing suppliers'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name_eng = Column(String(100))
    name_chn = Column(String(100), comment = 'maybe there is no chinese name, just let it equals to english name')
    region = Column(String(200), comment = 'the localtion of headquarters. like China HK, China Taiwan, Japan etc.')
    web_site = Column(String(200))
    detail_info = Column(Text)

    def __repr__(self):
        return f'<Supplier {self.name_eng}>'
    
class SupplierPOD(db.Model):
    __tablename__ = 'oog_supplier_pod'
    __table_args__ = {'comment': 'Place of Delivery (supplier may have multiple delivery places)'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    alias = Column(String(100))

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    supplier_pod = relationship('SupplierPOD')

    def __repr__(self):
        return f'<Supplier {self.alias}>'
    

class CurrencyEx(db.Model):
    __tablename__ = 'oog_currency_ex'
    __table_args__ = {'comment': 'currency exchange rate data'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    fr_curr = Column(String(10))
    to_curr = Column(String(10))
    ex_dt = Column(DateTime, default = func.now())
    ex_rate = Column(Float)

    def __repr__(self):
        return f'<CurrencyEx {self.fr_curr}>'


class Machine(db.Model):
    __tablename__ = 'oog_machine'
    __table_args__ = {'comment': 'the meta data of each machine'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    supplier_pod = relationship('SupplierPOD', foreign_keys=[supplier_pod_id])

    proxy_supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    proxy_supplier_pod = relationship('SupplierPOD', foreign_keys=[proxy_supplier_pod_id])

    plant_id = Column(Integer, ForeignKey('oog_plant.id'))
    plant = relationship('Plant')


    floor = Column(Float)
    coordx = Column(Float)
    coordy = Column(Float)

    m_length = Column(Float, comment = 'the length of the machine')
    m_width = Column(Float, comment = 'the width of the machine')
    m_height = Column(Float, comment = 'the height of the machine')
    cover_length = Column(Float, comment = 'the length of the area of the machine occupied, include operation area, repairing are etc.')
    cover_width = Column(Float, comment = 'the width of the area of the machine occupied, include operation area, repairing are etc.')
    standard_name = Column(String(100))
    verbose_name = Column(String(100), comment = 'the machine called by the worker normally')
    m_model = Column(String(100))
    verbose_num = Column(Integer, comment = 'like Drill machine #1. the number 1 is the verbose num')
    detail_info = Column(Text)
    acuisition_date = Column(Date)

    def __repr__(self):
        return f'<Machine {self.verbose_name}>'
    
class Asset(db.Model):
    __tablename__ = 'oog_asset'
    __table_args__ = {'comment': 'one machine may have more than one asset'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    machine_id = Column(Integer, ForeignKey('oog_machine.id'))
    machine = relationship('Machine')

    num = Column(String(100), comment='there is anoter test comment')
    tmp_num = Column(String(100))
    asset_name = Column(String(100))
    original_price = Column(Float)
    op_currency = Column(String(10), comment = 'currency of original price')
    op_date = Column(Date, comment = 'date of original price')
    acquisition_price = Column(Float)
    ap_currency = Column(String(10), comment = 'currency of acquisition price')
    ap_date = Column(Date, comment = 'date of acquisition price')

    def __repr__(self):
        return f'<Asset {self.asset_name}>'
    
class Customer(db.Model):
    __tablename__ = 'oog_customer'
    __table_args__ = {'comment': 'company group can be a customer'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name_eng = Column(String(100))
    name_chn = Column(String(100), comment = 'maybe there is no chinese name, just let it equals to english name')
    region = Column(String(200), comment = 'the localtion of headquarters. like China HK, China Taiwan, Japan etc.')
    web_site = Column(String(200))
    detail_info = Column(Text)

    def __repr__(self):
        return f'<Customer {self.name_eng}>'

class ShippingSite(db.Model):
    __tablename__ = 'oog_shipping_site'
    __table_args__ = {'comment': 'customer may have multiple receiving sites'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    customer_id = Column(Integer, ForeignKey('oog_customer.id'))
    customer = relationship('Customer')

    company_id = Column(Integer, ForeignKey('oog_company.id'), comment = 'the company you should send the bill to')
    company = relationship('Company')

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    name_eng = Column(String(100))
    name_chn = Column(String(100), comment = 'maybe there is no chinese name, just let it equals to english name')
    

    def __repr__(self):
        return f'<ShippingSite {self.name_eng}>'
    
class Product(db.Model):
    __tablename__ = 'oog_product'
    __table_args__ = {'comment': 'includes semi-products'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    customer_id = Column(Integer, ForeignKey('oog_customer.id'))
    customer = relationship('Customer')

    cpn = Column(String(50), comment = 'customer part number')
    proj = Column(String(50), comment = 'customer project')
    pn = Column(String(50), comment = 'part number')
    semi_pn = Column(String(100), comment = 'semi product part number')
    detail_info = Column(Text)
    virtual = Column(Boolean)

    def __repr__(self):
        return f'<Product {self.pn}>'

class ProductShareVer(db.Model):
    __tablename__ = 'oog_product_share_ver'
    __table_args__ = {'comment': 'share version'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    product1_id = Column(Integer, ForeignKey('oog_product.id'))
    product1 = relationship('Product', foreign_keys=[product1_id])
    
    product2_id = Column(Integer, ForeignKey('oog_product.id'))
    product2 = relationship('Product', foreign_keys=[product2_id])

    def __repr__(self):
        return f'<ProductShareVer {self.id}>'

class PDBUProduct(db.Model):
    __tablename__ = 'oog_pdbu_product'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    rpn = Column(String(50))
    detail_info = Column(Text)
    ignore_validate_rpn = Column(Boolean)
    
    bu_id = Column(Integer, ForeignKey('oog_bu.id'))
    bu = relationship('BU')
    
    plant_district_id = Column(Integer, ForeignKey('oog_plant_district.id'))
    plant_district = relationship('PlantDistrict')
    
    master_product_id = Column(Integer, ForeignKey('oog_product.id'))
    master_product = relationship('Product', foreign_keys=[master_product_id])
    
    sub_product_id = Column(Integer, ForeignKey('oog_product.id'))
    sub_product = relationship('Product', foreign_keys=[sub_product_id])

    def __repr__(self):
        return f'<PDBUProduct {self.rpn}>'

class YieldRate(db.Model):
    __tablename__ = 'oog_yield_rate'
    __table_args__ = {'comment': 'yield rate data'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    yr_date = Column(Date)
    yr = Column(Float)
    detail_info = Column(Text)
    
    pdbu_product_id = Column(Integer, ForeignKey('oog_pdbu_product.id'))
    pdbu_product = relationship('PDBUProduct')

    def __repr__(self):
        return f'<YieldRate {self.yr_date}>'

class PartNum(db.Model):
    __tablename__ = 'oog_part_num'
    __table_args__ = {'comment': 'part number version tracking'}

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    pn = Column(String(20))
    ver = Column(String(10))
    pn_create_dt = Column(DateTime)
    change_info = Column(Text)
    
    pre_part_num_id = Column(Integer, ForeignKey('oog_part_num.id'))
    pre_part_num = relationship('PartNum')

    def __repr__(self):
        return f'<PartNum {self.pn}>'

class PNLayer(db.Model):
    __tablename__ = 'oog_pn_layer'

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    layer_code = Column(Integer)
    layer_name = Column(String(20))
    
    part_num_id = Column(Integer, ForeignKey('oog_part_num.id'))
    part_num = relationship('PartNum')
    
    next_pn_layer_id = Column(Integer, ForeignKey('oog_pn_layer.id'))
    next_pn_layer = relationship('PNLayer')

    def __repr__(self):
        return f'<PNLayer {self.layer_name}>'

class ProcCode(db.Model):
    __tablename__ = 'oog_proc_code'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    p_code = Column(String(10))
    p_name = Column(String(20))
    p_normal_lt = Column(Float)

    def __repr__(self):
        return f'<ProcCode {self.p_code}>'

class SubProcCode(db.Model):
    __tablename__ = 'oog_sub_proc_code'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    p_code = Column(String(10))
    p_name = Column(String(20))

    def __repr__(self):
        return f'<SubProcCode {self.p_code}>'

class PNLayerProc(db.Model):
    __tablename__ = 'oog_pn_layer_proc'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    seq = Column(Integer)
    proc_code_seq = Column(Integer)
    
    pn_layer_id = Column(Integer, ForeignKey('oog_pn_layer.id'))
    pn_layer = relationship('PNLayer')
    
    proc_code_id = Column(Integer, ForeignKey('oog_proc_code.id'))
    proc_code = relationship('ProcCode', foreign_keys=[proc_code_id])
    
    proc_code_old_id = Column(Integer, ForeignKey('oog_proc_code.id'))
    proc_code_old = relationship('ProcCode', foreign_keys=[proc_code_old_id])

    def __repr__(self):
        return f'<PNLayerProc {self.seq}>'

class PNLayerSProc(db.Model):
    __tablename__ = 'oog_pn_layer_sproc'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    seq = Column(Integer)
    sub_proc_code_seq = Column(Integer)
    pcs_cnt = Column(Integer)
    detail_info = Column(Text)
    
    pn_layer_proc_id = Column(Integer, ForeignKey('oog_pn_layer_proc.id'))
    pn_layer_proc = relationship('PNLayerProc')
    
    sub_proc_code_id = Column(Integer, ForeignKey('oog_sub_proc_code.id'))
    sub_proc_code = relationship('SubProcCode')

    def __repr__(self):
        return f'<PNLayerSProc {self.seq}>'

class Role(db.Model):
    __tablename__ = 'oog_role'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name = Column(String(50))
    description = Column(String(255))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class UserRole(db.Model):
    __tablename__ = 'oog_user_role'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    user_id = Column(Integer, ForeignKey('oog_user.id'))
    user = relationship('User', foreign_keys=[user_id])
    
    role_id = Column(Integer, ForeignKey('oog_role.id'))
    role = relationship('Role', foreign_keys=[role_id])
    
    def __repr__(self):
        return f'<UserRole {self.id}>'

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'oog_user'

    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'), nullable=True)
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'), nullable=True)
    updated_user = relationship('User', foreign_keys=[updated_user_id])

    user_name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name_eng = Column(String(50))
    name_chn = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.user_name}>'

class Permission(db.Model):
    __tablename__ = 'oog_permission'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    name = Column(String(50))
    description = Column(String(255))
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class RolePermission(db.Model):
    __tablename__ = 'oog_role_permission'
    
    id = Column(Integer, primary_key = True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    role_id = Column(Integer, ForeignKey('oog_role.id'))
    role = relationship('Role')
    
    permission_id = Column(Integer, ForeignKey('oog_permission.id'))
    permission = relationship('Permission')
    
    def __repr__(self):
        return f'<RolePermission {self.id}>'

class Material(db.Model):
    __tablename__ = 'oog_material'
    __table_args__ = {'comment': 'Material information'}
    
    id = Column(Integer, primary_key=True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    mpn = Column(String(20), comment='Material part number')
    mtype = Column(String(10), comment='Material type')
    supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    supplier_pod = relationship('SupplierPOD')
    mdesc = Column(String(50), comment='Material description')
    munit = Column(String(10), comment='Material unit')
    
    def __repr__(self):
        return f'<Material {self.mpn}>'


class SProcMaterial(db.Model):
    __tablename__ = 'oog_sproc_material'
    __table_args__ = {'comment': 'Material usage in sub-processes'}
    
    id = Column(Integer, primary_key=True)
    created_dt = Column(DateTime, default=func.now())
    updated_dt = Column(DateTime, default=func.now(), onupdate=func.now())
    created_user_id = Column(Integer, ForeignKey('oog_user.id'))
    updated_user_id = Column(Integer, ForeignKey('oog_user.id'))
    created_user = relationship('User', foreign_keys=[created_user_id])
    updated_user = relationship('User', foreign_keys=[updated_user_id])
    
    pn_layer_sproc_id = Column(Integer, ForeignKey('oog_pn_layer_sproc.id'))
    pn_layer_sproc = relationship('PNLayerSProc')
    
    material_id = Column(Integer, ForeignKey('oog_material.id'))
    material = relationship('Material')
    
    qpa = Column(Float, comment='Quantity Per Assembly (pcs base, like SH/PCS, SF/PCS, KG/PCS)')
    
    def __repr__(self):
        return f'<SProcMaterial {self.id}>'
