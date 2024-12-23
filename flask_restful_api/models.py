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

class BG(db.Model):
    __tablename__ = 'oog_bg'

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(50))
    name_chn = Column(String(50))

    def __repr__(self):
        return f'<BG {self.name_eng}>'

class BU(db.Model):
    __tablename__ = 'oog_bu'

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(50))
    name_chn = Column(String(50))

    bg_id = Column(Integer, ForeignKey('oog_bg.id'))
    bg = relationship('BG')

    def __repr__(self):
        return f'<BU {self.name_eng}>'
    
class PlantDistrict(db.Model):
    __tablename__ = 'oog_plant_district'

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(50))
    name_chn = Column(String(50))

    location_id = Column(Integer, ForeignKey('oog_location.id'))
    location = relationship('Location')

    def __repr__(self):
        return f'<PlantDistrict {self.name_eng}>'
    
class Plant(db.Model):
    __tablename__ = 'oog_plant'

    id = Column(Integer, primary_key = True)
    plant_code = Column(String(10))

    plant_district_id = Column(Integer, ForeignKey('oog_plant_district.id'))
    plant_district = relationship('PlantDistrict')

    bu_id = Column(Integer, ForeignKey('oog_bu.id'))
    bu = relationship('BU')

    def __repr__(self):
        return f'<Plant {self.name_eng}>'
    
class Supplier(db.Model):
    __tablename__ = 'oog_supplier'

    id = Column(Integer, primary_key = True)
    name_eng = Column(String(100))
    name_chn = Column(String(100))
    region = Column(String(200))
    web_site = Column(String(200))
    detail_info = Column(Text)

    def __repr__(self):
        return f'<Supplier {self.name_eng}>'
    
class SupplierPOD(db.Model): # POD: Place Of Delivery
    __tablename__ = 'oog_supplier_pod'

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

    id = Column(Integer, primary_key = True)

    fr_curr = Column(String(10))
    to_curr = Column(String(10))
    ex_dt = Column(DateTime, default = func.now())
    ex_rate = Column(Float)

    def __repr__(self):
        return f'<CurrencyEx {self.fr_curr}>'


class Machine(db.Model):
    __tablename__ = 'oog_machine'

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

    m_length = Column(Float)
    m_width = Column(Float)
    m_height = Column(Float)
    cover_length = Column(Float)
    cover_width = Column(Float)
    standard_name = Column(String(100))
    verbose_name = Column(String(100))
    m_model = Column(String(100))
    verbose_num = Column(Integer)
    detail_info = Column(Text)
    acuisition_date = Column(Date)

    def __repr__(self):
        return f'<Supplier {self.verbose_name}>'