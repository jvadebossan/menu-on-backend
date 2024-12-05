import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# Database connection variables
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

client = MongoClient(MONGODB_URL, server_api=ServerApi("1"))

db = client[MONGODB_DB_NAME]
users = db["users"]
