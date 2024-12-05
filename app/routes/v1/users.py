from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from bson import ObjectId
from database import users
from models.users import UserCreate, UserUpdate

# Define router
router = APIRouter()


# Routes
@router.post("/")
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    result = users.insert_one(user.dict())
    return {"id": str(result.inserted_id), "message": "User created successfully"}


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """
    Delete a user by ID.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    result = users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.patch("/{user_id}")
async def edit_user(
    user_id: str,
    user: UserUpdate,
):
    print(user_id, user)
    """
    Edit a user by ID.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Get a user by ID.
    """
    print(user_id)
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user
