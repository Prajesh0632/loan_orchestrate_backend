from fastapi import FastAPI,Depends,status
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from database import init_firebase
from config import settings
from auth.security import authenticate_user
import sys

app = FastAPI(
    title="Loan Orchestrate API",
    version="1.0.0",
    debug=settings.DEBUG 
)

print(f"Starting app in {settings.ENV} mode", file=sys.stderr)

try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("CORS middleware added", file=sys.stderr)
except Exception as e:
    print(f"CORS middleware error: {e}", file=sys.stderr)

# Initialize Firebase
try:
    init_firebase()
    print("Firebase initialized successfully", file=sys.stderr)
except Exception as e:
    print(f"Firebase initialization error: {e}", file=sys.stderr)
    raise

# Include auth routes
try:
    app.include_router(auth_router, prefix="/api", tags=["auth"])
    print("Auth router included", file=sys.stderr)
except Exception as e:
    print(f"Auth router error: {e}", file=sys.stderr)
    raise

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.ENV
    }












