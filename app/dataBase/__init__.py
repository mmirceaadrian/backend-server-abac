from .database import sessionmanager
from . import models
from sqlalchemy.orm import Session


def get_db() -> Session:
    with sessionmanager.session() as session:
        yield session
