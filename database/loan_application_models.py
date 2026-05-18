from typing import Literal, Optional
from pydantic import BaseModel

class LoanRequest(BaseModel):
    loanType: str
    requested_amount: str
    requested_amount_words: Optional[str] = None
    purpose: str
    repayment_period_years: str
    loan_tenure_start_date: Optional[str] = None


class ApplicantDetails(BaseModel):
    applicant_name: str
    dob_or_establishment: str
    calendar_type: str
    permanent_house_no: Optional[str] = None
    ward_no: str
    street_name: Optional[str] = None
    city: str
    district: str
    po_box: Optional[str] = None
    telephone_office: Optional[str] = None
    telephone_residence: Optional[str] = None
    mobile: str
    fax: Optional[str] = None
    email: Optional[str] = None
    father_name: str
    grandfather_name: str
    spouse_name: Optional[str] = None
    dependents_parents: Optional[str] = None
    dependents_children: Optional[str] = None


class Employment(BaseModel):
    occupation: str
    company_name: Optional[str] = None
    work_address: Optional[str] = None
    years_there: Optional[str] = None
    previous_employer: Optional[str] = None
    business_nature: Optional[str] = None


class FinancialPosition(BaseModel):
    deposit_nmb: Optional[str] = None
    deposit_other_bank: Optional[str] = None
    shares_bonds: Optional[str] = None
    assets_land_building: Optional[str] = None
    assets_vehicle: Optional[str] = None
    furniture_appliances: Optional[str] = None
    other_assets: Optional[str] = None
    loan_nmb: Optional[str] = None
    loan_other_bank: Optional[str] = None
    loan_employer: Optional[str] = None
    credit_card_limit: Optional[str] = None
    loan_other_sources: Optional[str] = None
    rent: Optional[str] = None
    land_building_tax: Optional[str] = None
    income_tax: Optional[str] = None
    total_income: str
    living_expenses: str
    net_disposable_income: str


class Declarations(BaseModel):
    declaration_truth: str
    declaration_authorization: str
    declaration_date: Optional[str] = None
    signature_name: Optional[str] = None


class HousingSecurity(BaseModel):
    property_address: str
    land_area: str
    built_up_area: Optional[str] = None
    no_of_floors: Optional[str] = None
    ownership_type: str
    estimated_property_value: str
    developer_contractor: Optional[str] = None
    cash_margin: Optional[str] = None
    guarantee_of: Optional[str] = None
    other_security: Optional[str] = None
    years_at_current_residence: Optional[str] = None


class ApartmentSecurity(BaseModel):
    project_name: str
    unit_no: str
    floor_no: Optional[str] = None
    apartment_built_up_area: str
    parking_slot: Optional[str] = None
    apartment_ownership_type: str
    estimated_apartment_value: str
    expected_handover_date: Optional[str] = None
    cash_margin: Optional[str] = None
    guarantee_of: Optional[str] = None
    other_security: Optional[str] = None


class LandSecurity(BaseModel):
    kitta_no: str
    land_location: str
    land_area_land: str
    road_access: str
    land_ownership_type: str
    intended_use: str
    estimated_market_value: str
    cash_margin: Optional[str] = None
    guarantee_of: Optional[str] = None
    other_security: Optional[str] = None


class VehicleSecurity(BaseModel):
    vehicle_type: str
    vehicle_model: str
    vehicle_year: str
    vehicle_seller: str
    vehicle_invoice_no: Optional[str] = None
    vehicle_purchase_price: str
    vehicle_down_payment: str
    vehicle_loan_amount: str
    vehicle_chassis_no: Optional[str] = None
    vehicle_engine_no: Optional[str] = None
    vehicle_registration_no: Optional[str] = None


class AgricultureSecurity(BaseModel):
    farm_project_name: str
    crop_activity_type: str
    agri_land_area: str
    agri_land_location: str
    agri_ownership_type: str
    irrigation_source: Optional[str] = None
    farm_equipment: Optional[str] = None
    agri_project_cost: str
    harvest_cycle: Optional[str] = None


class BaseLoanApplication(BaseModel):
    schema_version: Literal[1]
    loan_request: LoanRequest
    applicant_details: ApplicantDetails
    employment: Employment
    financial_position: FinancialPosition
    declarations: Declarations


class HousingLoanApplication(BaseLoanApplication):
    loan_type: Literal["housing"]
    security: HousingSecurity


class ApartmentLoanApplication(BaseLoanApplication):
    loan_type: Literal["apartment"]
    security: ApartmentSecurity


class LandLoanApplication(BaseLoanApplication):
    loan_type: Literal["land"]
    security: LandSecurity


class VehicleLoanApplication(BaseLoanApplication):
    loan_type: Literal["vehicle"]
    security: VehicleSecurity


class AgricultureLoanApplication(BaseLoanApplication):
    loan_type: Literal["agriculture"]
    security: AgricultureSecurity



APPLICATION_MODELS = {
      "vehicle": VehicleLoanApplication,
      "housing": HousingLoanApplication,
      "apartment": ApartmentLoanApplication,
      "land": LandLoanApplication,
      "agriculture": AgricultureLoanApplication,
  }