from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from models import (
    Location, Company, BG, BU, PlantDistrict, Plant, 
    Supplier, SupplierPOD, CurrencyEx, Machine, Asset,
    Customer, ShippingSite, Product, ProductShareVer,
    PDBUProduct, YieldRate, PartNum, PNLayer, ProcCode,
    SubProcCode, PNLayerProc, PNLayerSProc, Role,
    UserRole, User, Permission, RolePermission,
    Material, SProcMaterial, TopBarMenu, SideBarMenu, MenuItemPermission
)

class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_relationships = True
        load_instance = True

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True

class BGSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BG
        include_relationships = True
        load_instance = True

class BUSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BU
        include_relationships = True
        load_instance = True

class PlantDistrictSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlantDistrict
        include_relationships = True
        load_instance = True

class PlantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plant
        include_relationships = True
        load_instance = True

class SupplierSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Supplier
        include_relationships = True
        load_instance = True

class SupplierPODSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SupplierPOD
        include_relationships = True
        load_instance = True

class CurrencyExSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CurrencyEx
        include_relationships = True
        load_instance = True

class MachineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Machine
        include_relationships = True
        load_instance = True

class AssetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        include_relationships = True
        load_instance = True

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True

class ShippingSiteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingSite
        include_relationships = True
        load_instance = True

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True

class ProductShareVerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductShareVer
        include_relationships = True
        load_instance = True

class PDBUProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PDBUProduct
        include_relationships = True
        load_instance = True

class YieldRateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = YieldRate
        include_relationships = True
        load_instance = True

class PartNumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PartNum
        include_relationships = True
        load_instance = True

class PNLayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PNLayer
        include_relationships = True
        load_instance = True

class ProcCodeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProcCode
        include_relationships = True
        load_instance = True

class SubProcCodeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubProcCode
        include_relationships = True
        load_instance = True

class PNLayerProcSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PNLayerProc
        include_relationships = True
        load_instance = True

class PNLayerSProcSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PNLayerSProc
        include_relationships = True
        load_instance = True

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True

class UserRoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    # Define a password field for input/output
    password = fields.String(required=True, load_only=True)  # load_only means it won't be included in serialized output
    
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ('password_hash',)  # Exclude password_hash from the schema

class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        include_relationships = True
        load_instance = True

class RolePermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RolePermission
        include_relationships = True
        load_instance = True

class MaterialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Material
        include_relationships = True
        load_instance = True

class SProcMaterialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SProcMaterial
        include_relationships = True
        load_instance = True

class TopBarMenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TopBarMenu
        include_relationships = True
        load_instance = True

class SideBarMenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SideBarMenu
        include_relationships = True
        load_instance = True

    # 添加嵌套的 TopBarMenu 关系
    top_bar_menu = fields.Nested(TopBarMenuSchema, exclude=('side_bar_menus',))
    
    # 添加自引用关系
    parent = fields.Nested('self', exclude=('parent',), allow_none=True)

class MenuItemPermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemPermission
        include_relationships = True
        load_instance = True

    # 添加嵌套的 SideBarMenu 和 Permission 关系
    side_bar_menu = fields.Nested(SideBarMenuSchema, exclude=('menu_item_permissions',))
    permission = fields.Nested('PermissionSchema', exclude=('menu_item_permissions',))