from fastapi import FastAPI
from app.api.endpoints import userRest
from app.api.endpoints import predmetRest, userRest, predavanjeRest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRest.router, prefix="/api/user")
app.include_router(predavanjeRest.router, prefix="/api/predavanje")
app.include_router(predmetRest.router, prefix="/api/predmet")

# Define your routes here