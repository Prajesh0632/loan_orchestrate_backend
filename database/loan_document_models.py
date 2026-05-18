from typing import Literal, Optional
from pydantic import BaseModel


class UploadedDocument(BaseModel):
    title: str
    file_name: str
    content_type: str
    size_bytes: int
    storage_path: Optional[str] = None


class CommonLoanDocuments(BaseModel):
    citizenship_or_national_id: UploadedDocument
    passport_size_photo: UploadedDocument
    pan_or_tax_registration: UploadedDocument
    bank_statement: UploadedDocument
    income_proof: UploadedDocument


class HousingLoanDocuments(CommonLoanDocuments):
    loan_type: Literal["housing"]
    title_deed_lalpurja: UploadedDocument
    land_or_property_tax_receipt: UploadedDocument
    site_plan_or_map: UploadedDocument
    valuation_report: UploadedDocument
    construction_estimate_or_quotation: Optional[UploadedDocument] = None


class ApartmentLoanDocuments(CommonLoanDocuments):
    loan_type: Literal["apartment"]
    booking_or_allotment_letter: UploadedDocument
    project_quotation: UploadedDocument
    building_or_project_approval_papers: UploadedDocument
    unit_or_floor_plan: UploadedDocument
    developer_ownership_papers: Optional[UploadedDocument] = None


class LandLoanDocuments(CommonLoanDocuments):
    loan_type: Literal["land"]
    title_deed_lalpurja: UploadedDocument
    plot_or_kitta_map: UploadedDocument
    land_tax_receipt: UploadedDocument
    purchase_agreement: UploadedDocument
    valuation_report: UploadedDocument


class VehicleLoanDocuments(CommonLoanDocuments):
    loan_type: Literal["vehicle"]
    dealer_quotation_or_proforma_invoice: UploadedDocument
    vehicle_specification_sheet: UploadedDocument
    purchase_agreement: UploadedDocument
    used_vehicle_valuation: Optional[UploadedDocument] = None
    driving_license: Optional[UploadedDocument] = None


class AgricultureLoanDocuments(CommonLoanDocuments):
    loan_type: Literal["agriculture"]
    land_ownership_or_lease_agreement: UploadedDocument
    agricultural_plan: UploadedDocument
    supplier_quotation: UploadedDocument
    irrigation_or_utility_document: Optional[UploadedDocument] = None
    farm_registration_or_pan: Optional[UploadedDocument] = None



DOCUMENT_MODELS = {
      "vehicle": VehicleLoanDocuments,
      "housing": HousingLoanDocuments,
      "apartment": ApartmentLoanDocuments,
      "land": LandLoanDocuments,
      "agriculture": AgricultureLoanDocuments,
  }