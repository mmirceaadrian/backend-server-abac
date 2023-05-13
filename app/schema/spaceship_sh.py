import datetime

from pydantic import BaseModel


class SpaceshipCreateDDO(BaseModel):
    name: str
    model: str
    image: str
    year: int


class AppointmentCreateDDO(BaseModel):
    date: datetime.datetime


class ServiceCreateDDO(BaseModel):
    name: str
    location: str
    cost: int
    image: str
    rating: float
    reviews: int

