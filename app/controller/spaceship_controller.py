from fastapi import Depends, APIRouter

import app.services.spaceship_service as spaceship_service

spaceship = APIRouter()


@spaceship.post("/add", status_code=201)
def add_spaceship(return_value: dict = Depends(spaceship_service.add_spaceship)):
    """Add a new spaceship"""
    return return_value


@spaceship.get("/get", status_code=200)
def get_user_spaceships(return_value: dict = Depends(spaceship_service.get_user_spaceships)):
    """Get all spaceships of a user"""
    return return_value
