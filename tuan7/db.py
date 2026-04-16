import os
from pymongo import MongoClient

_client = None
_db = None


def init_db() -> None:
    global _client, _db
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB", "tuan7_products")

    _client = MongoClient(mongo_uri)
    _db = _client[db_name]


def get_products_collection():
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db["products"]
