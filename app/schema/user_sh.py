from pydantic import BaseModel


class UserDDO(BaseModel):
    user_id: int
    password: str
    email: str


class UserLoginDDO(BaseModel):
    email: str
    password: str


class UserRegisterDDO(BaseModel):
    password: str
    email: str
