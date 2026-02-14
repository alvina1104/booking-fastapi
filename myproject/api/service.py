from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Service
from myproject.database.schema import ServiceInputSchema, ServiceOutSchema
from myproject.database.db import SessionLocal

service_router = APIRouter(prefix='/service', tags=['Service CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@service_router.post('/', response_model=ServiceOutSchema)
async def create_service(service: ServiceInputSchema, db: Session = Depends(get_db)):
    service_db = Service(**service.dict())
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db


@service_router.get('/', response_model=List[ServiceOutSchema])
async def list_service(db: Session = Depends(get_db)):
    return db.query(Service).all()

@service_router.get('/{service_id}', response_model=ServiceOutSchema)
async def detail_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')
    return service


@service_router.put('/{service_id}', response_model=dict)
async def update_service(service_id: int, service_: ServiceInputSchema,
                         db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=404, detail='Service not found')

    for key, value in service_.dict().items():
        setattr(service_db, key, value)

    db.commit()
    db.refresh(service_db)
    return {"message": "Service updated"}


@service_router.delete('/{service_id}', response_model=dict)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=404, detail='Service not found')

    db.delete(service_db)
    db.commit()
    return {"message": "Service deleted"}