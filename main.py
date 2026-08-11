from dis import code_info

from fastapi import FastAPI
from myproject.api import (country, user, city, service, hotel, hotelimage,
                           room, roomimage,booking, review,auth)
import uvicorn
from myproject.admin.setup import setup_admin

hotel_app = FastAPI(title="Hotel API")
hotel_app.include_router(country.country_router)
hotel_app.include_router(user.user_router)
hotel_app.include_router(city.city_router)
hotel_app.include_router(service.service_router)
hotel_app.include_router(hotel.hotel_router)
hotel_app.include_router(hotelimage.hotel_image_router)
hotel_app.include_router(room.room_router)
hotel_app.include_router(roomimage.room_image_router)
hotel_app.include_router(booking.booking_router)
hotel_app.include_router(review.review_router)
hotel_app.include_router(auth.auth_router)
setup_admin(hotel_app)




if __name__ == "__main__":
    uvicorn.run(hotel_app, host="127.0.0.1", port=8000)