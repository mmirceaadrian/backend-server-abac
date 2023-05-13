from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Double

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


class Service(Base):
    __tablename__ = "service"
    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    cost = Column(Integer)
    image = Column(String)
    rating = Column(Double)
    reviews = Column(Integer)


class Piece(Base):
    __tablename__ = "piece"
    piece_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.user_id"))
