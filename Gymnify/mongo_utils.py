from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")
MONGO_COLLECTION_NAME_2 = os.getenv("MONGO_COLLECTION_NAME_2")
MONGO_COLLECTION_NAME_3 = os.getenv("MONGO_COLLECTION_NAME_3")
MONGO_COLLECTION_NAME_4 = os.getenv("MONGO_COLLECTION_NAME_4")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def get_gymers_collection():
    return db[MONGO_COLLECTION_NAME]

def get_bills_collection():
    return db[MONGO_COLLECTION_NAME_2]

def get_foods_collection():
    return db[MONGO_COLLECTION_NAME_3]

def get_exercises_collection():
    return db[MONGO_COLLECTION_NAME_4]
