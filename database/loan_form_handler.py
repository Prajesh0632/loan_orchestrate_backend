import json
from json import JSONDecodeError

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import ValidationError

from config import settings


from .azure_blob_storage import store_in_blob, rollback_uploads

from .loan_application_models import (
    BaseLoanApplication,
    APPLICATION_MODELS
)

from .loan_document_models import (

    UploadedDocument,
    CommonLoanDocuments,
    DOCUMENT_MODELS
    
)

from .firebase_crud import (
    store_in_firebase, 
    get_doc_count, 
    rollback_writes
)


def get_requirements(model: type[BaseModel], doc : str) -> dict:
    requirements = {}

    for field_name, field in model.model_fields.items():
        field_type = field.annotation

        if isinstance(field_type, type) and issubclass(field_type, BaseModel) and doc == "application":
            requirements[field_name] = get_requirements(field_type, doc)
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
            await document.seek(0)

            document_data[title] = UploadedDocument(
                title=title,
                file_name=document.filename,
                content_type=document.content_type,
                size_bytes=len(file_bytes),
                required=None,
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

       application_requirements = get_requirements(APPLICATION_MODELS[loan_type], "application")
       document_requirements = get_requirements(DOCUMENT_MODELS[loan_type], 'document')

    except ValidationError:
        print("here")
        return False

    return await store_form_data(
                                 loan_type,
                                 application_model, 
                                 application_requirements,
                                 document_model, 
                                 document_requirements,
                                 documents,
                                 document_titles,
                                 current_user
                                 )



async def store_form_data(
                          loan_type : str,
                          application_model : BaseLoanApplication, 
                          application_requirements : dict,
                          document_model : CommonLoanDocuments,
                          document_requirements : dict,
                          documents : list[UploadFile],
                          document_titles : list[str],
                          current_user : str
                          )-> bool:
    
    doc_count = await get_doc_count(current_user)
    
    azure_response = azure_response =  await store_in_blob(
                                             loan_type,
                                             document_model, 
                                             documents,
                                             document_requirements,
                                             document_titles,
                                             current_user,
                                             doc_count
                                             )

    if  azure_response is None:
        await rollback_uploads(current_user, doc_count)
        return False


    firebase__response = await store_in_firebase(
                            application_model,
                            application_requirements,
                            document_model,
                            document_requirements,
                            document_titles,
                            azure_response,
                            current_user)
    
    if firebase__response is None:
        await rollback_uploads(current_user, doc_count)
        await rollback_writes(current_user, doc_count)
        return False
    
    
    return True
    








