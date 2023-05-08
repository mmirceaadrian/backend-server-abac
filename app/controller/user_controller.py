from fastapi import Depends, APIRouter

import app.services.user_service as user_service

user = APIRouter()


# register a new user
@user.post("/register", status_code=201)
def register(return_value: dict = Depends(user_service.register)):
    """Register a new user
    requires an email, password and email verification code
    """
    return return_value


# login
@user.post("/login", status_code=200)
def login(return_value: dict = Depends(user_service.login)):
    """Login a user and return a JWT token"""
    return return_value


@user.get("/verify", status_code=200)
def verify_token(return_value: dict = Depends(user_service.verify_token)):
    """Verify JWT token and return user data"""
    return return_value
