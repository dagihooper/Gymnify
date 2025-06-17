from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")


client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def get_gymers_collection():
    return db[MONGO_COLLECTION_NAME]
