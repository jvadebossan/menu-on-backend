from bson import ObjectId
from fastapi.responses import JSONResponse
from passlib.context import CryptContext


def serialize_mongo_document(doc):
    """
    Serializes a single MongoDB document into a JSON-compatible format.
    """
    if not doc:
        return None
    return {
        key: (str(value) if isinstance(value, ObjectId) else value)
        for key, value in doc.items()
    }


def serialize_mongo_documents(docs):
    """
    Serializes a list of MongoDB documents into a JSON-compatible format.
    """
    return [serialize_mongo_document(doc) for doc in docs]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash a password
def hash_password(password: str):
    return pwd_context.hash(password)


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
