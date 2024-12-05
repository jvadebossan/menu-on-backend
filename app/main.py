import uvicorn
from fastapi import FastAPI, Depends
from routes.v1.users import router as v1_users_router
from dotenv import load_dotenv

from utils import format_response
from database import users, db
from bson import ObjectId

# Load environment variables
load_dotenv()

# Initialize the FastAPI application with the lifespan function
app = FastAPI()

# Include routers
app.include_router(v1_users_router, prefix="/v1/users", tags=["users-v1"])

@app.get("/")
async def root():
    """
    Root endpoint. Return the current API version.
    """
    version = os.getenv("VERSION")
    if not version:
        return format_response("Internal server error", 500)
    return format_response(version, 200)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
    )
