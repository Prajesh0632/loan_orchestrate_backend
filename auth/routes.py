from fastapi import APIRouter,HTTPException,status
from auth.models import UserLogin, UserSignup,Token
from datetime import timedelta,datetime,timezone
from database.users import get_user, create_user
from auth.firebase_db import user_exists_in_firebase
from auth.security import get_hash_password,authenticate_user,create_access_token
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES

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
            detail=f"Signup failed: {str(e)}"
        )


    