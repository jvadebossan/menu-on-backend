import base64
from fastapi import File, UploadFile


async def convert_file_to_base64(file: UploadFile) -> str:
    """
    Converts an UploadFile object to a Base64-encoded string.

    Args:
        file (UploadFile)

    Returns:
        str: Base64-encoded string
    """
    try:
        file_content = await file.read()

        base64_encoded = base64.b64encode(file_content).decode("utf-8")

        return base64_encoded
    except:
        return None
