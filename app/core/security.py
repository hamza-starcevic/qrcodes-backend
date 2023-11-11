from fastapi.datastructures import Headers
from passlib.context import CryptContext
import jwt, os
from dotenv import load_dotenv
 
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def check_role(headers: Headers, roleToBe):
    role=False
    try:
        jwt_token = headers.get("Authorization").split(" ")[1]
        decoded = jwt.decode(jwt_token, os.getenv("jwt_secret"), algorithms=["HS256"])
        role = decoded["role"]
    except Exception as e:
        return False
    finally:
        if role == roleToBe:
            return True
        else:
            return False