from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Create_establishment_request(BaseModel):
    name: str
    created_at: datetime
    
class Establishment_response(BaseModel):
    name: str
    owner_id: str
    logo: str
    created_at: datetime


def establishments_helper(establishment):
    return {
        "_id": str(establishment["_id"]),
        "name": establishment.get("name"),
        "owner_id": establishment.get("owner_id"),
        "logo": establishment.get("logo"),
        "created_at": establishment.get("created_at"),
    }
