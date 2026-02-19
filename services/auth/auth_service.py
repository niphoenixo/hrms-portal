import jwt
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from config.config import TOKEN_ALGORITHM,TOKEN_SECRET_KEY,TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()

class AuthService():

    def verify_password(plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)


    def get_password_hash(password):
        return password_hash.hash(password)
    
    def create_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
        return encoded_jwt
    
    def verify_token():
        pass
