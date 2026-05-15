import firebase_admin
from firebase_admin import credentials, firestore
import json
from config import settings

db = None 

def init_firebase():
    global db
    
    if settings.FIREBASE_KEY_JSON:
        # Production: Use Key Vault secret (passed as env var)
        cred_dict = json.loads(settings.FIREBASE_KEY_JSON)
        cred = credentials.Certificate(cred_dict)
    else:
        # Development: Use local file
        cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(f"Firebase initialized in {settings.ENV} mode")

def get_db():
    return db