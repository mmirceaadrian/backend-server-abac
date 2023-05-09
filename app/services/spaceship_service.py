from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dataBase import get_db, models
from app.schema.spaceship_sh import SpaceshipCreateDDO
from app.services.user_service import auth_handler


def add_spaceship(spaceship: SpaceshipCreateDDO,
                  user_id: int = Depends(auth_handler.auth_wrapper),
                  db: Session = Depends(get_db)):
    spaceship_model = models.Spaceship(**spaceship.dict())
    spaceship_model.user_id = user_id
    db.add(spaceship_model)
    db.commit()
    db.refresh(spaceship_model)
    return {"message": "Spaceship added"}


def get_user_spaceships(user_id: int = Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    return db.query(models.Spaceship).filter_by(user_id=user_id).all()


def delete_spaceship(spaceship_id: int,
                     user_id: int = Depends(auth_handler.auth_wrapper),
                     db: Session = Depends(get_db)):
    spaceship = db.query(models.Spaceship).filter_by(spaceship_id=spaceship_id).first()
    if spaceship.user_id != user_id:
        raise HTTPException(status_code=400, detail="You can only delete your own spaceships")
    db.delete(spaceship)
    db.commit()
    return {"message": "Spaceship deleted"}


def search_pieces(search_string: str, user_id: int = Depends(auth_handler.auth_wrapper),
                  db: Session = Depends(get_db)):
    search_query = "%" + search_string + "%"
    selected_pieces = db.query(models.Piece).filter(models.Piece.name.like(search_query)).all()
    result = []
    for piece in selected_pieces:
        piece_ddo = {"piece_id": piece.piece_id, "name": piece.name,
                     "price": piece.price}
        result.append(piece_ddo)
    return result


def add_piece(name: str, price: int,user_id: int = Depends(auth_handler.auth_wrapper),
              db: Session = Depends(get_db)):
    piece = models.Piece(name=name, price=price)
    db.add(piece)
    db.commit()
    db.refresh(piece)
    return {"message": "Piece added"}
