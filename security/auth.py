from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, api_key
import secrets, os
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER')
BASIC_AUTH_PWD = os.getenv('BASIC_AUTH_PWD')
API_KEY = os.getenv('API_KEY')

security = HTTPBasic()
api_key_header = api_key.APIKeyHeader(name="X-API-KEY")

def check_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(BASIC_AUTH_USER,'utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(BASIC_AUTH_PWD,'utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

def check_api_key(key: Annotated[str, Security(api_key_header)]):
    correct_api_key = bytes(API_KEY,'utf-8')
    current_api_key = key.encode("utf8")
    is_correct_api_key = secrets.compare_digest(
        current_api_key, correct_api_key
    )
    if not is_correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ApiKey"
        )
    