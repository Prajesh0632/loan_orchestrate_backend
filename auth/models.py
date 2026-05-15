from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserSignup(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class User(BaseModel):
    username:str
    disabled:bool
    
class TokenData(BaseModel):
    username:str
