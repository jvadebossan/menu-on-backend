import uvicorn
import os
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from database import db
from typing import Annotated
from starlette import status

# Import routers
from routes.v1.auth import router as v1_auth_router
from routes.v1.auth import validate_user, get_current_user
from routes.v1.establishments import router as v1_establishments_router

# Load environment variables
load_dotenv()

# Initialize the FastAPI
app = FastAPI()
user_dependency = Annotated[dict, Depends(get_current_user)]

# Include routers
app.include_router(v1_auth_router, prefix="/v1/auth", tags=["auth-v1"])
app.include_router(
    v1_establishments_router, prefix="/v1/establishments", tags=["establishments-v1"]
)


@app.get("/test-user", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency):
    """
    Get current users.
    """
    user_data = await validate_user(user)

    return {"message": "User found", "user": user_data}


@app.get("/")
async def root():
    """
    Root endpoint. Return the current API version.
    """
    version = os.getenv("VERSION")
    if not version:
        return {"message": "No version found.", "status": status.HTTP_400_BAD_REQUEST}
    return {"version": version, "status": status.HTTP_200_OK}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
    )
