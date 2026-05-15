from database.firebase import get_db
from auth.models import UserSignup, UserLogin
from fastapi import HTTPException,status


async def create_user(user: UserSignup, hashed_password: str):
    try:
        db = get_db()
        user_data = {
            "username": user.username,
            "password": hashed_password
        }
        db.collection("credentials").document(user.username).set(user_data)

        return {
            "status": True,
            "message": "User Created"
        }
    except Exception as e:
        return {
            "status": False,
            "message": f"Failed to create user: {str(e)}"
        }

async def get_user(username:str):
    
    db = get_db()
    doc = db.collection("credentials").document(username).get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
        
    
   
