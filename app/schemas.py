from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str
    count: int = 0
    rating: Optional[int] = None

class CreateItem(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: datetime    
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class ItemVoteResponse(BaseModel):
    Item: ItemResponse
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    item_id: int
    dir: int