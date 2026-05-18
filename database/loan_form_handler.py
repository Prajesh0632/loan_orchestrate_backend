import json
from json import JSONDecodeError

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import ValidationError

from .firebase import get_db
from .loan_application_models import (
    BaseLoanApplication,
    APPLICATION_MODELS
)

from .loan_document_models import (

    UploadedDocument,
    CommonLoanDocuments,
    DOCUMENT_MODELS
    
)


def get_requirements(model: type[BaseModel]) -> dict:
    requirements = {}

    for field_name, field in model.model_fields.items():
        field_type = field.annotation

        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            requirements[field_name] = get_requirements(field_type)
        else:
            requirements[field_name] = field.is_required()

    return requirements





async def handle_form_data(
                            loan_type:str,
                            application:str,
                            documents_metadata:str,
                            documents:list[UploadFile],
                            document_titles:list[str],
                            current_user:str
                            )->bool:
    try:
        application_data = json.loads(application)

        document_data = {
            "loan_type" : loan_type
        }
       
        
        for index, document in enumerate(documents):
            title = document_titles[index]

            file_bytes = await document.read()

            document_data[title] = UploadedDocument(
                title=title,
                file_name=document.filename,
                content_type=document.content_type,
                size_bytes=len(file_bytes),
                required=False,
                storage_path=None,
            )

    except (JSONDecodeError, TypeError, ValidationError):
        return False

    if "sections" in application_data:
        sections = application_data.get("sections") or {}
        application_data = {
            "schema_version": application_data.get("schema_version"),
            "loan_type": application_data.get("loan_type"),
            "loan_request": sections.get("loan_request"),
            "applicant_details": sections.get("applicant_details"),
            "employment": sections.get("employment"),
            "security": sections.get("security"),
            "financial_position": sections.get("financial_position"),
            "declarations": sections.get("declarations"),
        }

    try:
        
       application_model = APPLICATION_MODELS[loan_type](**application_data)
       document_model = DOCUMENT_MODELS[loan_type](**document_data)

       application_requirements = get_requirements(APPLICATION_MODELS[loan_type])
       document_requirements = get_requirements(DOCUMENT_MODELS[loan_type])

    except ValidationError:
        return False

    return await store_form_data(
                                 application_model, 
                                 application_requirements,
                                 document_model, 
                                 document_requirements,
                                 current_user
                                 )



async def store_form_data(
                          application_model : BaseLoanApplication, 
                          application_requirements : dict,
                          document_model : CommonLoanDocuments,
                          document_requirements : dict,
                          current_user : str
                          )-> bool:
    db = get_db()

    try:
        username = getattr(current_user, "username", current_user)

        doc = db.collection("form-data").document(username)
        doc_details = doc.get()
        
        doc_count = 0
        if doc_details.exists:
            doc_data = doc_details.to_dict() or {}
            doc_count = doc_data.get("count", 0)

        doc.set({
            "count" : doc_count + 1
        })
        loan_doc = doc.collection(f"doc{doc_count + 1}")
        application_data = application_model.model_dump()

        loan_doc.document("info").set({
            "loan_type": application_data["loan_type"],
            "status": "pending",
        })

       
        loan_doc.document("loan_request").set(application_data["loan_request"])
        loan_doc.document("applicant_details").set(application_data["applicant_details"])
        loan_doc.document("employment").set(application_data["employment"])
        loan_doc.document("security").set(application_data["security"])
        loan_doc.document("financial_position").set(application_data["financial_position"])
        loan_doc.document("declarations").set(application_data["declarations"])



        loan_doc.document("requirements").set(application_requirements)
        
    except Exception as error:
        print(f"Failed to store form data: {error}")
        return False    
    
    return True
