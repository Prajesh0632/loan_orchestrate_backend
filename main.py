from fastapi import FastAPI
from auth import router as auth_router
from database import init_firebase

app = FastAPI(title="Loan Orchestrate API", version="1.0.0")

# Initialize Firebase
init_firebase()

# Include auth routes
app.include_router(auth_router, prefix="/api", tags=["auth"])










