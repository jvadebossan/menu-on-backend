from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from database import users, menus
from routes.v1.auth import validate_user, get_current_user
from models.categories import categories_helper
from starlette import status
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson import ObjectId
from typing import Annotated, Dict
from utils import upload_photo, normalize_file_name
import logging


load_dotenv()

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    user: user_dependency,
    name: str = Form(...),
    description: str = Form(...),
    created_at: datetime = Form(...),
    establishment_id: str = Form(...),
    image: UploadFile = File(...),
):
    """
    Create a new category.
    """
    user_data = await validate_user(user)

    try:
        file_name = normalize_file_name(name)
        image_url = upload_photo(file_name, image)["response"]["url"]

        category = {
            "name": name,
            "description": description,
            "created_at": created_at,
            "owner_id": user_data["user_id"],
            "establishment_id": establishment_id,
            "image": image_url,
            "items": {},
        }

        new_category = menus.insert_one(category)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error creating category (image).",
        )

    return {
        "message": "Category created successfully",
        "category_id": str(new_category.inserted_id),
        "status_code": status.HTTP_201_CREATED,
    }


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(category_id: str):
    """
    Get a category by its ID.
    """
    try:
        category = menus.find_one({"_id": ObjectId(category_id)})

        return {
            "message": "Category found",
            "category": categories_helper(category),
            "status_code": status.HTTP_200_OK,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(
    category_id: str,
    user: user_dependency,
    name: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
):
    """
    Update a category.
    """
    user_data = await validate_user(user)

    update_fields = {
        "name": name,
        "description": description,
    }

    # Only update existing fields
    update_fields = {
        key: value for key, value in update_fields.items() if value is not None
    }

    if image:
        try:
            file_name = normalize_file_name(name)
            image_url = upload_photo(file_name, image)["response"]["url"]
            update_fields["image"] = image_url
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error updating category (image).",
            )

    try:
        teste = menus.update_one(
            {"_id": ObjectId(category_id)}, {"$set": update_fields}
        )
        print(teste)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error updating category.",
        )

    return {
        "message": "Category updated successfully",
        "status_code": status.HTTP_200_OK,
    }


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: str,
    user: user_dependency,
):
    """
    Delete a category.
    """
    user_data = await validate_user(user)

    try:
        menus.delete_one({"_id": ObjectId(category_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error deleting category.",
        )

    return {
        "message": "Category deleted successfully",
        "status_code": status.HTTP_200_OK,
    }
