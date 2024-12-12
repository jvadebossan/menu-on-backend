from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from database import users, establishments
from models.establishments import (
    Create_establishment_request,
    Establishment_response,
    establishments_helper,
)
from routes.v1.auth import validate_user, get_current_user
from starlette import status
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson import ObjectId
from typing import Annotated
from utils import convert_file_to_base64

load_dotenv()

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_establishment(
    user: user_dependency,
    name: str = Form(...),
    created_at: datetime = Form(...),
    logo: UploadFile = File(...),
):
    """
    Create a new establishment.
    """
    user_data = await validate_user(user)
    logo_b64 = await convert_file_to_base64(logo)

    establishment = {
        "name": name,
        "created_at": created_at,
        "owner_id": user_data["user_id"],
        "logo": logo_b64,
    }
    new_establishment = establishments.insert_one(establishment)
    return {
        "message": "Establishment created successfully",
        "establishment_id": 123123,
        "status_code": status.HTTP_201_CREATED,
    }


@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_establishments(user: user_dependency):
    """
    Get all establishments.
    """
    user_data = await validate_user(user)
    try:

        establishments_list = establishments.find({"owner_id": user_data["user_id"]})
        return {
            "message": "Establishments found",
            "establishments": [
                establishments_helper(establishment)
                for establishment in list(establishments_list)
            ],
            "status_code": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No establishments found",
        )


@router.get("/{establishment_id}", status_code=status.HTTP_201_CREATED)
async def get_establishment(establishment_id: str, user: user_dependency):
    """
    Get a single establishment.
    """
    user_data = await validate_user(user)
    establishment_id = ObjectId(establishment_id)
    try:
        establishment = establishments.find_one({"_id": establishment_id})
        return {
            "message": "Establishment found",
            "establishment": establishments_helper(establishment),
            "status_code": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No establishment found",
        )


@router.put("/{establishment_id}", status_code=status.HTTP_201_CREATED)
async def update_establishment(
    establishment_id: str,
    user: user_dependency,
    name: str = Form(...),
    logo: UploadFile = File(...),
):
    """
    Update an establishment.
    """
    user_data = await validate_user(user)
    establishment_id = ObjectId(establishment_id)
    logo_b64 = await convert_file_to_base64(logo)
    try:
        establishment = {
            "name": name,
            "owner_id": user_data["user_id"],
            "logo": logo_b64,
        }
        establishments.update_one({"_id": establishment_id}, {"$set": establishment})
        return {
            "message": "Establishment updated successfully",
            "status_code": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No establishment found",
        )


@router.delete("/{establishment_id}", status_code=status.HTTP_201_CREATED)
async def delete_establishment(establishment_id: str, user: user_dependency):
    """
    Delete an establishment.
    """
    user_data = await validate_user(user)
    establishment_id = ObjectId(establishment_id)
    try:
        establishments.delete_one({"_id": establishment_id})
        return {
            "message": "Establishment deleted successfully",
            "status_code": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No establishment found",
        )
