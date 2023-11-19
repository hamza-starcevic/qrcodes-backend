from fastapi import FastAPI
from app.api.endpoints import userRest
from app.api.endpoints import predmetRest, userRest, predavanjeRest


app = FastAPI()

app.include_router(userRest.router)
app.include_router(predavanjeRest.router)
app.include_router(predmetRest.router)

# Define your routes here