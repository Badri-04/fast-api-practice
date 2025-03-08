from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    stmt = select(models.User).where(models.User.email == user_credentials.username)
    user = db.execute(stmt).scalar()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}