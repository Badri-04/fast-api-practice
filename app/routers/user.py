from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(user: schemas.UserBase, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.id == id)
    user = db.execute(stmt).scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user