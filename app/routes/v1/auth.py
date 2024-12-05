from fastapi import APIRouter, HTTPException, Depends
from database import users
from models.auth import CreateUserRequest, Token
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson import ObjectId
from typing import Annotated
from models.auth import user_helper

load_dotenv()

router = APIRouter()

# Setup jwt and bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Create a JWT token
def create_jwt_token(email: str, user_id: str, expires_delta: timedelta):
    payload = {"email": email, "user_id": user_id}
    expires = datetime.utcnow() + expires_delta
    payload.update({"exp": expires})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Validate the token and return the user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_helper(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# Validate the user
async def validate_user(user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return {"user": user}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    """
    Create a new user.
    """
    # Check if a user with the same email already exists
    existing_user = users.find_one({"email": create_user_request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    user = create_user_request.dict()
    user["password"] = bcrypt_context.hash(create_user_request.password)
    result = users.insert_one(user)

    print(f"Creating user: {user}")
    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.find_one({"email": form_data.username})
    if not user or not bcrypt_context.verify(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a JWT token
    expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token = create_jwt_token(user["email"], str(user["_id"]), expires)

    return {"access_token": token, "token_type": "bearer"}
