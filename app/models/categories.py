from pydantic import BaseModel
from datetime import datetime
from typing import Optional


def categories_helper(category):
    return {
        "_id": str(category["_id"]),
        "name": category["name"],
        "description": category["description"],
        "created_at": category["created_at"],
        "establishment_id": category["establishment_id"],
        "image": category["image"],
        "items": category["items"],
    }
