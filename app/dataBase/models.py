from sqlalchemy import Column, Integer, String, ForeignKey

from app.dataBase.database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(Integer, unique=True, index=True)
    password = Column(String)


class Spaceship(Base):
    __tablename__ = "spaceship"
    spaceship_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    model = Column(String)
    year = Column(Integer)
    image = Column(String)
    user_id = Column(Integer, ForeignKey("user.user_id"))
