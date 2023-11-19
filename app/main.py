from fastapi import FastAPI
from app.api.endpoints import userRest
from app.api.endpoints import predmetRest, userRest, predavanjeRest


app = FastAPI()

app.include_router(userRest.router, prefix="/api/user")
app.include_router(predavanjeRest.router, prefix="/api/predavanje")
app.include_router(predmetRest.router, prefix="/api/predmet")

# Define your routes here