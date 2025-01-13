from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func, Date, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'oog_location'

    id = Column(Integer, primary_key = True)
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

    name_eng = Column(String(50))
    name_chn = Column(String(50), comment = 'maybe there is no chinese name, just let it equals to english name')

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    def __repr__(self):
        return f'<Company {self.name_eng}>'

class BG(db.Model):
    __tablename__ = 'oog_bg'
    __table_args__ = {'comment': 'Business Group. BG1, BG2, BG3 etc'}

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(50))
    name_chn = Column(String(50), comment = 'maybe there is no chinese name, just let it equals to english name')

    def __repr__(self):
        return f'<BG {self.name_eng}>'

class BU(db.Model):
    __tablename__ = 'oog_bu'
    __table_args__ = {'comment': 'Business Unit. HDI, FPC, MSAP, RPCB, BTK etc'}

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(50))
    name_chn = Column(String(50), comment = 'maybe there is no chinese name, just let it equals to english name')

    bg_id = Column(Integer, ForeignKey('oog_bg.id'))
    bg = relationship('BG')

    def __repr__(self):
        return f'<BU {self.name_eng}>'
    
class PlantDistrict(db.Model):
    __tablename__ = 'oog_plant_district'
    __table_args__ = {'comment': 'the place where many plants located. like SA, SB, HA, HB, QA etc.'}

    id = Column(Integer, primary_key = True)
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
    __table_args__ = {'comment': 'specific building of a factory. like SA03, SA02'}

    id = Column(Integer, primary_key = True)
    plant_code = Column(String(10), comment = 'like SA03, QA08 etc.')

    plant_district_id = Column(Integer, ForeignKey('oog_plant_district.id'))
    plant_district = relationship('PlantDistrict')

    bu_id = Column(Integer, ForeignKey('oog_bu.id'), comment = 'may be one building owned by multi bus. like part of SA02 is owned by FPC and the left part is owned by HDI.')
    bu = relationship('BU')

    def __repr__(self):
        return f'<Plant {self.plant_code}>'
    
class Supplier(db.Model):
    __tablename__ = 'oog_supplier'
    __table_args__ = {'comment': 'not only machine suppliers, but also material suppliers, out outsourcing suppliers etc.'}

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(100))
    name_chn = Column(String(100), comment = 'maybe there is no chinese name, just let it equals to english name')
    region = Column(String(200), comment = 'the localtion of headquarters. like China HK, China Taiwan, Japan etc.')
    web_site = Column(String(200))
    detail_info = Column(Text)

    def __repr__(self):
        return f'<Supplier {self.name_eng}>'
    
class SupplierPOD(db.Model):
    __tablename__ = 'oog_supplier_pod'
    __table_args__ = {'comment': 'POD: Place Of Delivery. A supplier many have many place to delivery the products.'}

    id = Column(Integer, primary_key = True)

    alias = Column(String(100))

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    supplier_id = Column(Integer, ForeignKey('oog_supplier.id'))
    supplier = relationship('Supplier')

    def __repr__(self):
        return f'<Supplier {self.alias}>'
    

class CurrencyEx(db.Model):
    __tablename__ = 'oog_currency_ex'
    __table_args__ = {'comment': 'currency exchange rate data'}

    id = Column(Integer, primary_key = True)

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

    supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    supplier_pod = relationship('SupplierPOD')

    proxy_supplier_pod_id = Column(Integer, ForeignKey('oog_supplier_pod.id'))
    proxy_supplier_pod = relationship('SupplierPOD')

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
    __table_args__ = {'comment': 'a company of our company group can be a customer. but need to add new customer to represent it.'}

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(100))
    name_chn = Column(String(100), comment = 'maybe there is no chinese name, just let it equals to english name')
    region = Column(String(200), comment = 'the localtion of headquarters. like China HK, China Taiwan, Japan etc.')
    web_site = Column(String(200))
    detail_info = Column(Text)

    def __repr__(self):
        return f'<Customer {self.name_eng}>'

class ShippingSite(db.Model):
    __tablename__ = 'oog_shipping_site'
    __table_args__ = {'comment': 'a customer may have may sites to receive you products'}

    id = Column(Integer, primary_key = True)

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
    __table_args__ = {'comment': 'include semi-prodcut'}

    id = Column(Integer, primary_key = True)

    customer_id = Column(Integer, ForeignKey('oog_customer.id'))
    customer = relationship('Customer')

    cpn4444 = Column(String(50), comment = 'customer part number')
    proj = Column(String(50), comment = 'customer project')
    pn = Column(String(50), comment = 'part number')
    semi_pn = Column(String(100), comment = 'semi product part number')
    detail_info = Column(String(50))

    def __repr__(self):
        return f'<Product {self.pn}>'

class TestForeignKey(db.Model):
    __tablename__ = 'oog_test_foreign_key'
    __table_args__ = {'comment': 'Test foreign key relationship'}

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('oog_product.id'))
    product = relationship('Product')

    def __repr__(self):
        return f'<TestForeignKey {self.id}>'
