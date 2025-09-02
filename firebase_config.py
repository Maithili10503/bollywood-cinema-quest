import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)

# Get Firestore DB instance
db = firestore.client()
