from fastapi import APIRouter
from auth.models import UserLogin, UserSignup
from database.users import get_user, create_user

router = APIRouter()

@router.post("/login")
async def login(user:UserLogin):
    
    exists = await get_user(user.username)

    if exists and exists["password"] == user.password:
        return {
            "status" : True,
            "message": "Login Successful"
        }
        
        

    return {
        "status" : False,
        "message" : "Incorrect Username or Password"
    }



@router.post("/signup")
async def signup(user:UserSignup):

    exists = await get_user(user.username)

    if exists:
        return {
            "status": False,
            "message" : "User already exists"

            }
    return await create_user(user)