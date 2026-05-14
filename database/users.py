from database.firebase import get_db
from auth.models import UserSignup, UserLogin


async def create_user(user:UserSignup):
    
    db = get_db()
    user_data = user.dict()

    db.collection("credentials").document(user.username).set(user_data)
    return {
            "status"  : True,
            "message" : "User Created"
        }



async def get_user(username:str):
    
    db = get_db()
    doc = db.collection("credentials").document(username).get()

    if doc.exists:
        return doc.to_dict()
    
    return None
    
   
