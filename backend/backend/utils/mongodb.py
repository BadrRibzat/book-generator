# backend/utils/mongodb.py
from pymongo import MongoClient
from django.conf import settings

# Reuse connection across requests (optional: add connection pooling if needed)
_client = None
_db = None

def get_mongodb_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
    return _client

def get_mongodb_db():
    global _db
    if _db is None:
        client = get_mongodb_client()
        _db = client[settings.MONGODB_DB_NAME]
    return _db
