# Models Documentation

*Note: All models include these standard fields:*
- id: Integer(primary_key=True)
- created_dt: DateTime(default=func.now())
- updated_dt: DateTime(default=func.now(), onupdate=func.now())
- created_user: User(nullable=True)
- updated_user: User(nullable=True)

## Location
- country: String(100, nullable=True)  // Country name (optional)
- province: String(100, nullable=True)  // Province/state (optional)
- city: String(100, nullable=True)  // City name (optional)
- region: String(100, nullable=True) // Region (optional)
- street: String(200, nullable=True)  // Street address (optional)
- address: String(200, nullable=True)  // Full address (optional)
- longitude: Float(nullable=True)  // GPS coordinate (optional)
- latitude: Float(nullable=True)  // GPS coordinate (optional)

## Company
// A company group that owns many subsidiaries
- name_eng: String(255, unique=True)  // Required unique English name
- name_chn: String(255, nullable=True)  // Optional Chinese name
- name_chn_abbr: String(50, nullable=True)  // Abbreviation of the company name
- location -> Location  // Optional location details

## BG (Business Group)
- name_eng: String(50, unique=True)  // Required unique English name
- name_chn: String(50, nullable=True)  // Optional Chinese name

## BU (Business Unit)
- name_eng: String(50, unique=True)  // Required unique English name
- name_chn: String(50, nullable=True)  // Optional Chinese name
- bg -> BG  // Optional business group reference

## PlantDistrict
- name_eng: String(50, unique=True)  // Required unique English name
- name_chn: String(50, nullable=True)  // Optional Chinese name
- company -> Company  // Optional company reference

## Plant
- plant_code: String(10, unique=True)  // Required unique plant code (e.g. SA03, QA08)
- plant_district -> PlantDistrict  // Optional plant district reference
- bu -> BU  // Optional business unit reference

## Supplier
- name_eng: String(100)
- name_chn: String(100)  // May be same as English name
- region: String(200)  // Headquarters location
- web_site: String(200)
- detail_info: Text

## SupplierPOD (Place of Delivery)
- alias: String(100)
- company -> Company
- supplier -> Supplier

## CurrencyEx (Currency Exchange)
- fr_curr: String(10)
- to_curr: String(10)
- ex_dt: DateTime  // Default: func.now()
- ex_rate: Float

## Machine
- floor: Float
- coordx: Float
- coordy: Float
- m_length: Float  // Machine length
- m_width: Float  // Machine width
- m_height: Float  // Machine height
- cover_length: Float  // Occupied area length
- cover_width: Float  // Occupied area width
- standard_name: String(100)
- verbose_name: String(100)  // Worker's common name
- m_model: String(100)
- verbose_num: Integer  // e.g. Drill machine #1
- detail_info: Text
- acuisition_date: Date
- supplier_pod -> SupplierPOD
- proxy_supplier_pod -> SupplierPOD
- plant -> Plant

## Asset
- num: String(100)
- tmp_num: String(100)
- asset_name: String(100)
- original_price: Float
- op_currency: String(10)  // Currency of original price
- op_date: Date  // Date of original price
- acquisition_price: Float
- ap_currency: String(10)  // Currency of acquisition price
- ap_date: Date  // Date of acquisition price
- machine -> Machine

## Customer
- name_eng: String(100)
- name_chn: String(100)  // May be same as English name
- region: String(200)  // Headquarters location
- web_site: String(200)
- detail_info: Text

## ShippingSite
- name_eng: String(100)
- name_chn: String(100)  // May be same as English name
- customer -> Customer
- company -> Company
- location -> Location

## Product
- cpn: String(50)  // Customer part number
- proj: String(50)  // Customer project
- pn: String(50)  // Part number
- semi_pn: String(100)  // Semi product part number
- detail_info: Text
- virtual: Boolean
- customer -> Customer

## ProductShareVer
- product1 -> Product
- product2 -> Product

## PDBUProduct
- rpn: String(50)
- detail_info: Text
- ignore_validate_rpn: Boolean
- bu -> BU
- plant_district -> PlantDistrict
- master_product -> Product
- sub_product -> Product

## YieldRate
- yr_date: Date
- yr: Float
- detail_info: Text
- pdbu_product -> PDBUProduct

## PartNum
- pn: String(20)
- ver: String(10)
- pn_create_dt: DateTime
- change_info: Text
- pre_part_num -> PartNum

## ProcCode
- p_code: String(10)
- p_name: String(20)
- p_normal_lt: Float

## SubProcCode
- p_code: String(10)
- p_name: String(20)

## PNLayer
- layer_code: Integer
- layer_name: String(20)
- part_num -> PartNum
- next_pn_layer -> PNLayer

## PNLayerProc
- seq: Integer
- proc_code_seq: Integer
- pn_layer -> PNLayer
- proc_code -> ProcCode
- proc_code_old -> ProcCode

## PNLayerSProc
- seq: Integer
- sub_proc_code_seq: Integer
- pcs_cnt: Integer
- detail_info: Text
- pn_layer_proc -> PNLayerProc
- sub_proc_code -> SubProcCode


## Material
- mpn: String(20) // material part number
- mtype: String(10) // material type
- supplier_pod -> SupplierPOD
- mdesc: String(50) // material description
- munit: String(10) // material unit

## SProcMaterial
- pn_layer_sproc -> PNLayerSProc
- material -> Material
- qpa: Float // Quantity Per Assembly, pcs base, like SH/PCS, SF/PCS, KG/PCS, according to the munit in Material

## User
- username: String(50)
- password: String(255)
- name_eng: String(50)
- name_chn: String(50)
- is_active: Boolean
- is_admin: Boolean

## Role
- name: String(50)
- description: String(255)

## UserRole
- user -> User
- role -> Role

## Permission
- name: String(50)
- description: String(255)

## RolePermission
- role -> Role
- permission -> Permission

## TopBarMenu
- name: String(255)
- menu_order: Integer

## SideBarMenu
- name: String(255)
- top_bar_menu -> TopBarMenu
- parent -> SideBarMenu
- url: String(255)
- menu_order: Integer

## MenuItemPermission
- side_bar_menu -> SideBarMenu
- permission -> Permission
