from fastapi import FastAPI
from app.api.endpoints import userRest
from app.api.endpoints import predavanjeRest

app = FastAPI()

app.include_router(userRest.router)
app.include_router(predavanjeRest.router)
# Define your routes here