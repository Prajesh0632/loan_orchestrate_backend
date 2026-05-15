from database.firebase import get_db
from auth.models import UserSignup, UserLogin

async def user_exists_in_firebase(username:str)->bool:
    try:
        db = get_db()
        doc = db.collection("credentials").document(username).get()
        if doc.exists:
            return doc.to_dict() is not None
        else:
            return False
    except Exception as e:
        print(f"{username} doesnt exist")
        return False
    
         
    