from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from database import init_firebase
from config import settings

app = FastAPI(
    title="Loan Orchestrate API",
    version="1.0.0",
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
init_firebase()

# Include auth routes
app.include_router(auth_router, prefix="/api", tags=["auth"])












