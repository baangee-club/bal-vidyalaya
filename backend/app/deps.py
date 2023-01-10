from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from app.config import get_settings
import secrets

auth = HTTPBasic()


def check_auth(
    cred: HTTPBasicCredentials = Depends(auth), config=Depends(get_settings)
):
    current_username_bytes = cred.username.encode("utf8")
    correct_username_bytes = config.username
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = cred.password.encode("utf8")
    correct_password_bytes = config.password
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_username or not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return cred.username
