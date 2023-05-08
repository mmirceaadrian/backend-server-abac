import os
import secrets
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth_handler import AuthHandler
from app.dataBase import get_db
from app.dataBase import models
from app.schema.user_sh import UserRegisterDDO, UserLoginDDO

auth_handler = AuthHandler()


def _email_exists(email: str, db: Session):
    return db.query(models.User).filter_by(email=email).first()


def register(user_register: UserRegisterDDO, db: Session = Depends(get_db)):
    if _email_exists(user_register.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    user_model = models.User(password=auth_handler.get_password_hash(user_register.password),
                             email=user_register.email)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "User created"}


def login(user_login: UserLoginDDO, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter_by(email=user_login.email).first()
    if not user_model or not auth_handler.verify_password(user_login.password, user_model.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            )
    token = auth_handler.generate_auth_token(user_model.user_id)
    return {"token": token}


def verify_token(user_id: int = Depends(auth_handler.auth_wrapper)):
    return {"message": "Token verified"}

