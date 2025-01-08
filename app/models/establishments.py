from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Create_establishment_request(BaseModel):
    name: str
    created_at: datetime


class Establishment_response(BaseModel):
    name: str
    name_alias: str
    owner_id: str
    logo: str
    created_at: datetime


def establishments_helper(establishment):
    return {
        "_id": str(establishment["_id"]),
        "name": establishment["name"],
        "name_alias": establishment["name_alias"],
        "owner_id": establishment["owner_id"],
        "logo": establishment["logo"],
        "created_at": establishment["created_at"],
    }
