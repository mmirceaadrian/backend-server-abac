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


@spaceship.get("/search_pieces", status_code=200)
def search_pieces(return_value: dict = Depends(spaceship_service.search_pieces)):
    """Search pieces for a spaceship"""
    return return_value


@spaceship.post("/add_piece", status_code=201)
def add_piece(return_value: dict = Depends(spaceship_service.add_piece)):
    """Add a piece to a spaceship"""
    return return_value
