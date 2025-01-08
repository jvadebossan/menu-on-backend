import requests
import os
from dotenv import load_dotenv
from fastapi import UploadFile
from random import choices
import re

# Load env variables
load_dotenv()
square_api_key = os.getenv("SQUARE_API_KEY")


def upload_photo(file_name: str, file: UploadFile):
    """
    Upload a photo to the Square Cloud Blob Storage.
    """
    url = "https://blob.squarecloud.app/v1/objects"

    querystring = {"name": str(file_name)}
    payload = {"file": file}
    headers = {"Authorization": square_api_key}

    with file.file as file_stream:
        files = {"file": (file.filename, file_stream, file.content_type)}

        response = requests.post(
            url, files=files, headers=headers, params=querystring
        ).json()
    return response


def normalize_file_name(file_name: str):
    """
    Normalize the file name.
    """
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", file_name)
    if len(normalized) < 3 or len(normalized) > 31:
        normalized = "".join(choices("abcdefghijklmnopqrstuvwxyz0123456789", k=31))

    return normalized[:31].lower()


def validate_id(id: str, db):
    if not ObjectId.is_valid(id) or not db.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid ID",
        )
