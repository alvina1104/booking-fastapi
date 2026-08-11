from myproject.api import review
from myproject.database.models import (Country,UserProfile,RefreshToken,City,Service,Hotel,
                                       HotelImage,Room,RoomImage,Booking,Review)
from sqladmin import ModelView


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id, Country.country_name]


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.token]


class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name]


class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.id, Service.service_name]


class HotelAdmin(ModelView, model=Hotel):
    column_list = [Hotel.id, Hotel.hotel_name]


class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = [HotelImage.id, HotelImage.hotel_image]


class RoomAdmin(ModelView, model=Room):
    column_list = [Room.id, Room.room_number]


class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [RoomImage.id, RoomImage.room_image]


class BookingAdmin(ModelView, model=Booking):
    column_list = [Booking.id, Booking.user]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.users]