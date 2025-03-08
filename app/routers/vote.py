from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def createVote(payload: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if payload.dir == 1:
        new_vote = models.Vote(user_id=current_user.id, item_id=payload.item_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    else:
        stmt = select(models.Vote).where(models.Vote.user_id == current_user.id, models.Vote.item_id == payload.item_id)
        vote = db.execute(stmt).scalar()
        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        db.delete(vote)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
