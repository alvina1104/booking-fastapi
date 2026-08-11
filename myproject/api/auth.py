from fastapi import APIRouter, Depends, HTTPException
from myproject.database.db import SessionLocal
from myproject.database.models import UserProfile,RefreshToken
from myproject.database.schema import UserProfileInputSchema,UserProfileOutSchema, UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from myproject.config import (SECRET_KEY,ALGORITHM,ACCESS_TOKEN_LIFETIME,REFRESH_TOKEN_LIFETIME)
from datetime import datetime, timedelta
from jose import jwt
from  typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



#def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#    to_encode = data.copy()
#    if expires_delta:
#        expire = datetime.utcnow() + expires_delta
#    else:
#        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
#    to_encode.update({"exp": expire})
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))



@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Username or email already exists', status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        user_image=user.user_image,
        country_id=user.country_id,
        password=hash_password,
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"message": "User created successfully"}

@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='The information is incorrect', status_code=401)

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_access_token({'sub': user_db.username})

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()



    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/logout/')
async def logout(refresh_token: str, db: Session = Depends(get_db)):

    booking_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not booking_token:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

    db.delete(booking_token)
    db.commit()

    return {'message': 'User logged out'}

@auth_router.post('/refresh')
async def refresh(refresh_token: str,db: Session = Depends(get_db)):
    booking_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not booking_token:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

    access_token = create_access_token({'sub': booking_token.id})
    return {'access_token': access_token, 'token_type': 'Bearer'}








