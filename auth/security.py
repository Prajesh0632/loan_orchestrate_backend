from typing import Optional
from database.users import get_user
from datetime import datetime,timedelta,timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from auth.config import SECRET_KEY,ALGORITHM

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

## to verify the password
def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

# generate a hashed password
def get_hash_password(password:str):
    return password_hash.hash(password)

# autheticate if user exits in database
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user['password']):
        return False
    return user
def create_access_token(data,expires_delta:timedelta |None=None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes= 15)
    
    to_encode.update({
        "exp": expire,
        "sub": data.get("sub")
    })
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        print(f"Token decode Error {e}")
        return None
    

    
    

