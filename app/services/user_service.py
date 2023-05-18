import os
import secrets
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth_handler import AuthHandler
from app.dataBase import get_db
from app.dataBase import models
from app.schema.user_sh import UserRegisterDDO, UserLoginDDO
import boto3

auth_handler = AuthHandler()
topic_arn = os.getenv("TOPIC_ARN")


def send_subscription_email(email_address, topic_arn):
    client = boto3.client('sns', region_name='us-east-1')

    response = client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email_address,
        ReturnSubscriptionArn=True
    )

    subscription_arn = response['SubscriptionArn']

    confirmation_link = f"https://sns.console.aws.amazon.com/sns/v3/opt-in?token={subscription_arn}"

    message = f"Please confirm your subscription by clicking the link: {confirmation_link}"

    response = client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Subscription Confirmation'
    )
    print(response)
    print(f"Subscription email sent to {email_address}.")


def _email_exists(email: str, db: Session):
    return db.query(models.User).filter_by(email=email).first()


def register(user_register: UserRegisterDDO, db: Session = Depends(get_db)):
    if _email_exists(user_register.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    user_model = models.User(password=auth_handler.get_password_hash(user_register.password),
                             email=user_register.email)
    send_subscription_email(user_register.email, topic_arn)
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

