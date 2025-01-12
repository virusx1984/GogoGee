# Models Documentation

## Location
- country: String(100)
- province: String(100)
- city: String(100)
- street: String(200)
- address: String(200)
- longitude: Float
- latitude: Float

## Company
- name_eng: String(50)
- name_chn: String(50) (may equal english name)
- location_id: Integer (foreign key to Location)
- location: Relationship to Location

## BG (Business Group)
- name_eng: String(50)
- name_chn: String(50) (may equal english name)

## BU (Business Unit)
- name_eng: String(50)
- name_chn: String(50) (may equal english name)
- bg_id: Integer (foreign key to BG)
- bg: Relationship to BG

## Plant District
- name_eng: String(50)
- name_chn: String(50)
- company_id: Integer (foreign key to Company)
- company: Relationship to Company
- location_id: Integer (foreign key to Location)
- location: Relationship to Location

## Plant
- plant_code: String(10) (e.g., SA03, QA08)
- plant_district_id: Integer (foreign key to Plant District)
- plant_district: Relationship to Plant District
- bu_id: Integer (foreign key to BU)
- bu: Relationship to BU

## Supplier
- name_eng: String(100)
- name_chn: String(100) (may equal english name)
- region: String(200) (headquarters location)
- web_site: String(200)
- detail_info: Text

## Supplier POD (Place of Delivery)
- alias: String(100)
- location_id: Integer (foreign key to Location)
- location: Relationship to Location
- supplier_id: Integer (foreign key to Supplier)
- supplier: Relationship to Supplier

## Currency Exchange
- fr_curr: String(10)
- to_curr: String(10)
- ex_dt: DateTime (default: current time)
- ex_rate: Float

## Machine
- supplier_pod_id: Integer (foreign key to Supplier POD)
- supplier_pod: Relationship to Supplier POD
- proxy_supplier_pod_id: Integer (foreign key to Supplier POD)
- proxy_supplier_pod: Relationship to Supplier POD
- plant_id: Integer (foreign key to Plant)
- plant: Relationship to Plant
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

## Asset
- machine_id: Integer (foreign key to Machine)
- machine: Relationship to Machine
- num: String(100)
- tmp_num: String(100)
- asset_name: String(100)
- original_price: Float
- op_currency: String(10) (original price currency)
- op_date: Date (original price date)
- acquisition_price: Float
- ap_currency: String(10) (acquisition price currency)
- ap_date: Date (acquisition price date)

## Customer
- name_eng: String(100)
- name_chn: String(100) (may equal english name)
- region: String(200) (headquarters location)
- web_site: String(200)
- detail_info: Text

## Shipping Site
- customer_id: Integer (foreign key to Customer)
- customer: Relationship to Customer
- company_id: Integer (foreign key to Company)
- company: Relationship to Company
- location_id: Integer (foreign key to Location)
- location: Relationship to Location
- name_eng: String(100)
- name_chn: String(100) (may equal english name)

## Product
- customer_id: Integer (foreign key to Customer)
- customer: Relationship to Customer
- cpn: String(50) (customer part number)
- proj: String(50) (customer project)
- pn: String(50) (part number)
- semi_pn: String(100) (semi product part number)
- detail_info: String(50)
