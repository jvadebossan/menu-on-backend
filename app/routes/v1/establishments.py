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
    print(user_data)
    print(name)
    logo_b64 = await convert_file_to_base64(logo)

    establishment = {
        "name": name,
        "created_at": created_at,
        "owner_id": user_data["user_id"],
        "logo": logo_b64,
    }
    new_establishment = establishments.insert_one(establishment)
    print(new_establishment, new_establishment.inserted_id)
    return {
        "message": "Establishment created successfully",
        "establishment id": 123123,
    }
