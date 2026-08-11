from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Enum, Date, Text, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'


class RoomTypeChoices(str, PyEnum):
    LUX = "Luxury"
    FAMILY = "Family"
    STANDARD = "Standard"
    DOUBLE = "Double"


class RoomStatusChoices(str, PyEnum):
    AVAILABLE = "available"
    BOOKED = "booked"
    OCCUPIED = "occupied"


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_image: Mapped[str] = mapped_column(String)
    country_name: Mapped[str] = mapped_column(String(50), unique=True)

    country_users: Mapped[List['UserProfile']] = relationship(back_populates='country', cascade='all, delete-orphan')
    country_cities: Mapped[List['City']] = relationship(back_populates='countries', cascade='all, delete-orphan')
    country_hotels: Mapped[List['Hotel']] = relationship(back_populates='country_hotel', cascade='all, delete-orphan')


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country: Mapped[Country] = relationship(back_populates='country_users')

    owner_hotels: Mapped[List['Hotel']] = relationship(back_populates='owner', cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship(back_populates='user', cascade='all, delete-orphan')
    user_reviews: Mapped[List['Review']] = relationship(back_populates='users', cascade='all, delete-orphan')
    owner_images: Mapped[List['HotelImage']] = relationship(back_populates='useries', cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(50))
    city_image: Mapped[str] = mapped_column(String)

    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    countries: Mapped[Country] = relationship(back_populates='country_cities')
    hotels: Mapped[List['Hotel']] = relationship(back_populates='city', cascade='all, delete-orphan')


class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_image: Mapped[str] = mapped_column(String)
    service_name: Mapped[str] = mapped_column(String(50))
    hotels: Mapped[List['Hotel']] = relationship(back_populates='serviced', cascade='all, delete-orphan')


class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(50))
    hotel_stars: Mapped[int] = mapped_column(Integer)
    postal_code: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)

    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country_hotel: Mapped[Country] = relationship(back_populates='country_hotels')

    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    serviced: Mapped[Service] = relationship(back_populates='hotels')

    owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    owner: Mapped[UserProfile] = relationship(back_populates='owner_hotels')

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(back_populates='hotels')

    images: Mapped[List['HotelImage']] = relationship(back_populates='hotel', cascade='all, delete-orphan')
    rooms: Mapped[List['Room']] = relationship(back_populates='hotels', cascade='all, delete-orphan')

    hotel_bookings: Mapped[List['Booking']] = relationship(back_populates='hotel_book', cascade='all, delete-orphan')
    hotel_reviews: Mapped[List['Review']] = relationship(back_populates='hotel_rev', cascade='all, delete-orphan')


class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_image: Mapped[str] = mapped_column(String)

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped["Hotel"] = relationship(back_populates='images')

    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    useries: Mapped[UserProfile] = relationship(back_populates='owner_images')




class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_number: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices))
    room_status: Mapped[RoomStatusChoices] = mapped_column(Enum(RoomStatusChoices))
    description: Mapped[str] = mapped_column(Text)

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotels: Mapped[Hotel] = relationship(back_populates='rooms')

    room_images: Mapped[List['RoomImage']] = relationship(back_populates='room', cascade='all, delete-orphan')
    room_bookings: Mapped[List['Booking']] = relationship(back_populates='room', cascade='all, delete-orphan')


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_image: Mapped[str] = mapped_column(String)

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(back_populates='room_images')




class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user: Mapped[UserProfile] = relationship(back_populates='bookings')

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_book: Mapped[Hotel] = relationship(back_populates='hotel_bookings')

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(back_populates='room_bookings')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    users: Mapped[UserProfile] = relationship(back_populates='user_reviews')

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_rev: Mapped[Hotel] = relationship(back_populates='hotel_reviews')