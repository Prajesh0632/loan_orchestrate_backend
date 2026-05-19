from fastapi import UploadFile
from azure.storage.blob import BlobServiceClient
from .loan_document_models import UploadedDocument
from config import settings



from .loan_document_models import  CommonLoanDocuments
    


blob_service_client = None

async def init_blob():
    global blob_service_client
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    if not connection_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not configured")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)


async def store_in_blob(
                        loan_type : str,
                        document_model : CommonLoanDocuments,
                        documents : list[UploadFile],
                        document_requirements : dict,
                        document_titles : list[str],
                        current_user : str,
                        doc_count : int,
                        )->list[str]:
    
    await init_blob()
    urls : str = []


    try:
        for index, document in enumerate(documents):
            file_bytes = await document.read()
            filename = document_titles[index]
            container_name = settings.AZURE_BLOB_CONTAINER_NAME
            blob_path =  f"{current_user}/doc{doc_count + 1}/{loan_type}/{filename}" 

            azure_url =  await upload_file(file_bytes, filename, container_name, blob_path)

            if not azure_url:
                return None
            
            urls.append(azure_url)

        
    
    except:
        return None

    return urls 
        


    


    



async def upload_file(
                      file_bytes,
                      filename : str,
                      container_name : str,
                      blob_path : str,
                               )->str:
    global blob_service_client

    try:
        if not blob_service_client:
            await init_blob()

        blob_client = blob_service_client.get_blob_client(
            container = container_name,
            blob = blob_path
        )    
        blob_client.upload_blob(file_bytes, overwrite=True)
        return blob_client.url


    except Exception as err:
        print(err)
        return None     




async def rollback_uploads(current_user : str, doc_count : int)->bool:
    
    directory = f"{current_user}/doc{doc_count}"
    
    try:
        container_client = blob_service_client.get_container_client(settings.AZURE_BLOB_CONTAINER_NAME)
        blobs = container_client.list_blobs(name_starts_with=directory)

        for blob in blobs:
            container_client.delete_blob(blob.name)

        return True    

    except:
        return None        

    
    
   















