import os
from fastapi import APIRouter,HTTPException,status,Depends
from auth.models import UserLogin, UserSignup,Token,User
from datetime import timedelta,datetime,timezone
from database.users import get_user, create_user
from auth.firebase_db import user_exists_in_firebase
from auth.security import get_hash_password,authenticate_user,create_access_token
from auth.dependencies import get_current_user
import jwt
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


router = APIRouter()

@router.post("/login")
async def login(item:UserLogin):
    """
    Login endpoint - receives credentials from frontend (JSON)
    Returns JWT access token if authentication is successful
    """
    
    user = await authenticate_user(item.username,item.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user['username']}, expires_delta=access_token_expires)
    return  {
    "status": True,
    "message": "Login successful",
    "access_token": access_token,
    "token_type": "bearer"
    }

@router.post("/signup")
async def signup(user: UserSignup):
        exists = await user_exists_in_firebase(user.username)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        try:
            hashed_password = get_hash_password(user.password)

            result = await create_user(user, hashed_password)

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Signup failed: {str(e)}")

@router.post('/token')
async def token(item:UserLogin):
    """
    Login endpoint - receives credentials from frontend (JSON)
    Returns JWT access token if authentication is successful
    """
    
    user = await authenticate_user(item.username,item.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user['username']}, expires_delta=access_token_expires)
    return Token(access_token=access_token,token_type='bearer')
    
@router.get("/dashboard")
async def dashboard(current_user:User = Depends(get_current_user)):
    return {'username':current_user.username}

# @router.post("/decodetoken")
# def decode_token(token:str):
#     try:
#         payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         return payload
#     except Exception as e:
#         print(f"Token decode Error {e}")
#         return None        