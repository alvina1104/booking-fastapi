from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import RoomImage
from myproject.database.schema import RoomImageInputSchema, RoomImageOutSchema
from myproject.database.db import SessionLocal

room_image_router = APIRouter(prefix="/room-image", tags=["Room Image CRUD"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_image_router.post("/", response_model=RoomImageOutSchema)
async def create_room_image(image: RoomImageInputSchema, db: Session = Depends(get_db)):
    # .dict() ордуна .model_dump() сунушталат (Pydantic v2 болсо)
    image_db = RoomImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db

@room_image_router.get("/", response_model=List[RoomImageOutSchema])
async def list_room_images(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()

@room_image_router.get("/{image_id}", response_model=RoomImageOutSchema)
async def detail_room_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Room image not found")
    return image

@room_image_router.put("/{image_id}", response_model=dict)
async def update_room_image(image_id: int, image: RoomImageInputSchema,
                             db: Session = Depends(get_db)):
    image_db = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail="Room image not found")

    for key, value in image.dict().items():
        setattr(image_db, key, value)

    db.commit()
    db.refresh(image_db)
    return {"message": "Room image updated"}

@room_image_router.delete("/{image_id}", response_model=dict)
async def delete_room_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail="Room image not found")

    db.delete(image_db)
    db.commit()
    return {"message": "Room image deleted"}