from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from  typing import List
from myproject.database.models import Room
from myproject.database.schema import RoomInputSchema,RoomOutSchema
from myproject.database.db import SessionLocal

room_router = APIRouter(prefix="/room", tags=["Room CRUD"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post("/", response_model=RoomOutSchema)
async def create_room(room: RoomInputSchema, db: Session = Depends(get_db)):
    room_db = Room(**room.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get("/", response_model=List[RoomInputSchema])
async def get_room(db: Session = Depends(get_db)):
    return db.query(Room).all()


@room_router.get("/{room_id}", response_model=RoomOutSchema)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@room_router.put("/{room_id}", response_model=dict)
async def update_room(room_id: int, room: RoomInputSchema,
                      db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in room.dict().items():
        setattr(room_db, key, value)

        db.commit()
        db.refresh(room_db)
        return {"massage": "Room updated"}

@room_router.delete("/{room_id}", response_model=dict)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room_db)
    db.commit()
    return {"massage": "Room deleted"}