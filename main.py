from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Details(BaseModel):
    username:str 
    password:str

@app.post("/api/login")
async def login(item: Details):
    return {
        "username": item.username,
        "password" : item.password
            }

