from fastapi import FastAPI
from app.api.endpoints import predmetRest, userRest

app = FastAPI()

app.include_router(userRest.router)
app.include_router(predmetRest.router)
# Define your routes here