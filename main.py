import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.api_controller import api_controller_router
from controllers.user_controller import user_controller_router

app = FastAPI()

# Load the environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Add the tags metadata
tags_metadata = [
    {"name": "Users", "description": "Operations related to user management"}
]

# Include the routers from controller modules
app.include_router(user_controller_router, prefix="/users", tags=["Users"])
app.include_router(api_controller_router, prefix="/apis", tags=["Ads APIs"])

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run the application
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
