from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def user_helper(user):
    return {
        "_id": str(user["_id"]),
        "email": user.get("email"),
    }
