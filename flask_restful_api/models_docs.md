# Models Documentation

## Location
### Fields
- country: String(100)
- province: String(100)
- city: String(100)
- street: String(200)
- address: String(200)
- longitude: Float
- latitude: Float

## Company
### Fields
- name_eng: String(50)
- name_chn: String(50) (may equal english name)

### Relationships
- location_id -> Location

## BG (Business Group)
### Fields
- name_eng: String(50)
- name_chn: String(50) (may equal english name)

## BU (Business Unit)
### Fields
- name_eng: String(50)
- name_chn: String(50) (may equal english name)

### Relationships
- bg_id -> BG

## PlantDistrict
### Fields
- name_eng: String(50)
- name_chn: String(50)

### Relationships
- company_id -> Company
- location_id -> Location

## Plant
### Fields
- plant_code: String(10) (e.g., SA03, QA08)

### Relationships
- plant_district_id -> PlantDistrict
- bu_id -> BU

## Supplier
### Fields
- name_eng: String(100)
- name_chn: String(100) (may equal english name)
- region: String(200) (headquarters location)
- web_site: String(200)
- detail_info: Text

## SupplierPOD (Place of Delivery)
### Fields
- alias: String(100)

### Relationships
- location_id -> Location
- supplier_id -> Supplier

## CurrencyExchange
### Fields
- fr_curr: String(10)
- to_curr: String(10)
- ex_dt: DateTime (default: current time)
- ex_rate: Float

## Machine
### Fields
- floor: Float
- coordx: Float
- coordy: Float
- m_length: Float (machine length)
- m_width: Float (machine width)
- m_height: Float (machine height)
- cover_length: Float (including operation/repair areas)
- cover_width: Float (including operation/repair areas)
- standard_name: String(100)
- verbose_name: String(100) (worker's common name)
- m_model: String(100)
- verbose_num: Integer (e.g., Drill machine #1)
- detail_info: Text
- acquisition_date: Date

### Relationships
- supplier_pod_id -> SupplierPOD
- proxy_supplier_pod_id -> SupplierPOD
- plant_id -> Plant

## Asset
### Fields
- num: String(100) (there is anoter test comment)
- tmp_num: String(100)
- asset_name: String(100)
- original_price: Float
- op_currency: String(10) (original price currency)
- op_date: Date (original price date)
- acquisition_price: Float
- ap_currency: String(10) (acquisition price currency)
- ap_date: Date (acquisition price date)

### Relationships
- machine_id -> Machine

## Customer
### Fields
- name_eng: String(100)
- name_chn: String(100) (may equal english name)
- region: String(200) (headquarters location)
- web_site: String(200)
- detail_info: Text

## ShippingSite
### Fields
- name_eng: String(100)
- name_chn: String(100) (may equal english name)

### Relationships
- customer_id -> Customer
- company_id -> Company
- location_id -> Location

## Product
### Fields
- cpn4444: String(50) (customer part number)
- proj: String(50) (customer project)
- pn: String(50) (part number)
- semi_pn: String(100) (semi product part number)
- detail_info: String(50)

### Relationships
- customer_id -> Customer

## TestForeignKey
### Relationships
- product_id -> Product
