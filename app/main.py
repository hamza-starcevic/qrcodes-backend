from fastapi import FastAPI
from app.api.endpoints import userRest

app = FastAPI()

app.include_router(userRest.router)
# Define your routes here