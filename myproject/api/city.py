from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import City
from myproject.database.schema import CityInputSchema,CityOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

city_router = APIRouter(prefix='/city',tags=['City CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post('/',response_model=CityOutSchema )
async def create_city(city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/', response_model=List[CityOutSchema])
async def list_city(db: Session = Depends(get_db)):
    return db.query(City).all()


@city_router.get('/{city_id}', response_model=CityOutSchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=400, detail='City not found')
    return city


@city_router.put('/{city_id}',response_model=dict)
async def update_city(city_id: int, city_: CityInputSchema,
                         db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='City not found')
    for city_key, city_value in city_.dict().items():
        setattr(city_db, city_key, city_value)
        db.commit()
        db.refresh(city_db)
        return {"message": "City updated"}


@city_router.delete('/{city_id}', response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=400, detail='City not found')
    db.delete(city_db)
    db.commit()
    return {"message": "City deleted"}