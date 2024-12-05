from pydantic import BaseModel, EmailStr
from typing import Optional


# Input model for creating a user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Response model for returning user data
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr


# Input model for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# Helper to format MongoDB documents
def user_helper(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
    }
