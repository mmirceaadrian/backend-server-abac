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
