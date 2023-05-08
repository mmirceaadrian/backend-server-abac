import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext


class AuthHandler:
    """Handles authentication and authorization and token generation"""
    security = HTTPBearer()

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret = os.getenv("AUTH_HANDLER_CODE")

    def get_password_hash(self, password: str) -> str:
        """Hashes the password using bcrypt"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies the password using bcrypt"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        """Decodes the token using the secret key and returns the payload"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def generate_auth_token(self, user_id) -> str:
        """Generates a token using the user id"""
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=10080),
            "iat": datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        payload = self.decode_token(auth.credentials)
        return payload["sub"]
