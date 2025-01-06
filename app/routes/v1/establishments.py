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
from typing import Annotated, Dict
from utils import upload_photo
import logging


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
    file_name = name.lower().replace(" ", "_")

    try:
        logo_url = upload_photo(file_name, logo)["response"]["url"]
        establishment = {
            "name": name,
            "created_at": created_at,
            "owner_id": user_data["user_id"],
            "logo": logo_url,
        }
        new_establishment = establishments.insert_one(establishment)
        return {
            "message": "Establishment created successfully",
            "establishment_id": str(new_establishment.inserted_id),
            "status_code": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error creating establishment (image).",
        )


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


@router.put("/{establishment_id}", status_code=status.HTTP_200_OK)
async def update_establishment(
    establishment_id: str,
    user: user_dependency,
    name: str = Form(...),
    logo: UploadFile = File(None),
):
    """
    Update an establishment.
    """

    user_data = await validate_user(user)

    # Validate establishment_id
    if not ObjectId.is_valid(establishment_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid establishment ID format",
        )
    establishment_id = ObjectId(establishment_id)

    update_fields = {
        "name": name,
    }

    if logo:
        try:
            file_name = name.lower().replace(" ", "_")
            logo_url = upload_photo(file_name, logo)["response"]["url"]
            update_fields["logo"] = logo_url
        except Exception as e:
            logging.error(f"Error uploading logo: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading logo",
            )

    update_result = establishments.update_one(
        {"_id": establishment_id}, {"$set": update_fields}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Establishment not found",
        )

    return {
        "message": "Establishment updated successfully",
        "updated_fields": update_fields,
        "status_code": status.HTTP_200_OK,
    }


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
