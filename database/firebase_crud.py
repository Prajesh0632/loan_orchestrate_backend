from .firebase import get_db
from .loan_application_models import BaseLoanApplication

from .loan_document_models import CommonLoanDocuments
 


async def get_doc_count(current_user: str) -> int:
      try:
        db = get_db()

        doc = db.collection("form-data").document(current_user)
        doc_details = doc.get()

      

        doc_data = doc_details.to_dict() or {}
        return doc_data.get("count", 0)
      
      except Exception as error:
          return 0
          print(error)



async def store_in_firebase(
                             application_model : BaseLoanApplication, 
                             application_requirements : dict,
                             document_model : CommonLoanDocuments,
                             document_requirements : dict,
                             document_titles : list[str],
                             urls,
                             current_user : str):
    db = get_db()
    




    try:
        application_data = application_model.model_dump()

        
        doc = db.collection("form-data").document(current_user)
        doc_details = doc.get()
        
        doc_count = 0
        if doc_details.exists:
            doc_data = doc_details.to_dict() or {}
            doc_count = doc_data.get("count", 0)


        doc.set({
            "count" : doc_count + 1,
            
        })

        
        loan_doc = doc.collection(f"doc{doc_count + 1}")


        loan_doc.document("info").set(
            {
            "loan_type": application_data["loan_type"],
            "status": "pending",   
            }
        )
       


       
        loan_doc.document("loan_request").set(application_data["loan_request"])
        loan_doc.document("applicant_details").set(application_data["applicant_details"])
        loan_doc.document("employment").set(application_data["employment"])
        loan_doc.document("security").set(application_data["security"])
        loan_doc.document("financial_position").set(application_data["financial_position"])
        loan_doc.document("declarations").set(application_data["declarations"])


        loan_doc.document("application_requirements").set(application_requirements)


        document_data = document_model.model_dump()
        
        for index, title in enumerate(document_titles):
            document = document_data[title]
            document['url'] = urls[index]
            document['required'] = document_requirements[title]
           

        loan_doc.document("documents").set(document_data)   


        


        
    except Exception as error:
        print(error)
        return None    
    
    return True



async def rollback_writes(current_user : str, doc_count : int)->bool:

    db = get_db()

    try:
        
        document = db.collection('form-data').document(current_user)
        loan_collection = document.collection(f"doc{doc_count}")

        docs = loan_collection.stream()

        for doc in docs:
            doc.reference.delete()

        doc_data = document.get().to_dict() or {}
        current_count = doc_data.get("count", 0)

        document.update({
            "count" : max(0, current_count - 1)
        })    
        
        print(f"Rolled Back doc{doc_count}")
        return True


    except:
        print(f"Rollback failed")
        return False

