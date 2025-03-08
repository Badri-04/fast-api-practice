from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


# @router.get("/", response_model=list[schemas.ItemResponse])
@router.get("/", response_model=list[schemas.ItemVoteResponse])
def getItems(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), skip: int = 0, limit: int = 3, search: Optional[str] = ''):
    # stmt = select(models.Item).where(models.Item.name.icontains(search)).offset(skip).limit(limit)
    stmt = (
        select(models.Item, func.count(models.Vote.user_id).label('votes'))
        .join(models.Vote, models.Item.id == models.Vote.item_id, isouter=True)
        .group_by(models.Item.id)
        .where(models.Item.name.icontains(search))
        .offset(skip)
        .limit(limit)
    )
    items = db.execute(stmt).mappings().all()
    print(items)
    return items


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def getItem(item_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    stmt = select(models.Item).where(models.Item.id == item_id)
    item = db.execute(stmt).scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def addItem(payload: schemas.CreateItem, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_item = models.Item(name=payload.name, count=payload.count, rating=payload.rating)
    new_item = models.Item(owner_id = current_user.id, **payload.model_dump()) # this is the same as above
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteItem(item_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    fetch_stmt = select(models.Item).where(models.Item.id == item_id)
    item = db.execute(fetch_stmt).scalar()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this item")
    
    delete_stmt = delete(models.Item).where(models.Item.id == item_id)
    result = db.execute(delete_stmt)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # when 204 is statuscode we shouldn't send any other data


@router.put("/{item_id}", response_model=schemas.ItemResponse)
def updateItem(item_id: int, payload: schemas.CreateItem, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    stmt = select(models.Item).where(models.Item.id == item_id)
    item = db.execute(stmt).scalar()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this item")
    
    update_stmt = update(models.Item).where(models.Item.id == item_id).values(**payload.model_dump())
    db.execute(update_stmt)
    db.commit()

    item = db.execute(stmt).scalar()
    return item