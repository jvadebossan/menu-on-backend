import requests
import os
from dotenv import load_dotenv
from fastapi import UploadFile

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
    headers = {"Authorization": square_api_key, "Content-Type": "application/json"}

    with file.file as file_stream:
        files = {"file": (file.filename, file_stream, file.content_type)}

        response = requests.post(
            url, files=files, headers=headers, params=querystring
        ).json()
    return response
