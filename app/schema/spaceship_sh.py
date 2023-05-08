from pydantic import BaseModel


class SpaceshipCreateDDO(BaseModel):
    name: str
    model: str
    image: str
    year: int
