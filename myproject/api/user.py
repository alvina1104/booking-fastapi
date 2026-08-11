from starlette import status
from myproject.database.models import UserProfile
from myproject.database.schema import UserProfileInputSchema, UserProfileOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

user_router = APIRouter(prefix='/user', tags=['UserProfile CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@user_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай id жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'message': 'Id ийгиликтуу очурулду'}