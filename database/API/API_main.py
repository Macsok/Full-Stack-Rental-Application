from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models as models
from bases import *
from database_connection import engine_master, engine_slave, SessionLocal_Master, SessionLocal_Slave
from sqlalchemy.orm import Session
from sqlalchemy import text
import hashlib

# To test API visit http://localhost:8000/docs#

app = FastAPI()
models.Base.metadata.create_all(bind=engine_master)

# Sessions management
def get_db_master():
    db = SessionLocal_Master()
    try:
        yield db
    finally:
        db.close()

def get_db_slave():
    db = SessionLocal_Slave()
    try:
        yield db
    finally:
        db.close()

db_master_dependency = Annotated[Session, Depends(get_db_master)]
db_slave_dependency = Annotated[Session, Depends(get_db_slave)]

#------------------------- API Endpoints on Slave Database (Vulnerable) ------------#
@app.get("/api/v1/cars_vulnerable", status_code=status.HTTP_200_OK)
# This endpoint is vulnerable to SQL Injection
async def read_cars_vulnerable(
    db: db_slave_dependency,
    car_id: int = None,
    brand: str = None,
    model: str = None,
    year: int = None
):
    query = []
    if car_id:
        query = db.execute(text(f"SELECT * FROM cars WHERE id = {car_id}")).fetchall()
    if brand:
        query = db.execute(text(f"SELECT * FROM cars WHERE brand = '{brand}'")).fetchall()
    if model:
        query = db.execute(text(f"SELECT * FROM cars WHERE model = '{model}'")).fetchall()
    if year:
        query = db.execute(text(f"SELECT * FROM cars WHERE year = {year}")).fetchall()
    if not query:
        raise HTTPException(status_code=404, detail='Car was not found')
    return [dict(car._mapping) for car in query]

#------------------------- API Endpoints on Slave Database -------------------------#
@app.get("/api/v1/cars", status_code=status.HTTP_200_OK)
async def read_cars(
    db: db_slave_dependency,
    car_id: int = None,
    brand: str = None,
    model: str = None,
    year: int = None
):
    query = db.query(models.Car)
    if car_id:
        query = query.filter(models.Car.id == car_id)
    if brand:
        query = query.filter(models.Car.brand == brand)
    if model:
        query = query.filter(models.Car.model == model)
    if year:
        query = query.filter(models.Car.year == year)
    cars = query.all()
    if not cars:
        raise HTTPException(status_code=404, detail='Car was not found')
    return cars

@app.get("/api/v1/locations", status_code=status.HTTP_200_OK)
async def read_locations(
    db: db_slave_dependency,
    location_id: int = None,
    address_id: int = None,
    name: str = None
):
    query = db.query(models.Location)
    if location_id:
        query = query.filter(models.Location.id == location_id)
    if address_id:
        query = query.filter(models.Location.address_id == address_id)
    if name:
        query = query.filter(models.Location.name == name)
    locations = query.all()
    if not locations:
        raise HTTPException(status_code=404, detail='Locations not found')
    return locations


@app.get("/api/v1/passwords", status_code=status.HTTP_200_OK)
async def get_passwords(
    db: db_slave_dependency,
    user_id: int = None
):
    query = db.query(models.Password)
   
    # Jeśli podano user_id, filtruj wyniki
    if user_id is not None:
        query = query.filter(models.Password.user_id == user_id)
   
    passwords = query.all()
   
    if not passwords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nie znaleziono żadnych haseł dla podanego user_id."
        )
   
    return passwords


@app.get("/api/v1/users", status_code=status.HTTP_200_OK)
async def read_users(
    db: db_slave_dependency,
    user_id: int = None,
    username: str = None
):
    query = db.query(models.User)
    if user_id:
        query = query.filter(models.User.id == user_id)
    if username:
        query = query.filter(models.User.username == username)
    users = query.all()
    if not users:
        raise HTTPException(status_code=404, detail='Users not found')
    return users

@app.get("/api/v1/passwords", status_code=status.HTTP_200_OK)
async def read_passwords(
    db: db_slave_dependency,
    user_id: int = None
):
    query = db.query(models.Password)
    if user_id:
        query = query.filter(models.Password.user_id == user_id)
    passwords = query.all()
    if not passwords:
        raise HTTPException(status_code=404, detail='Passwords not found')
    return passwords

@app.get("/api/v1/rentals", status_code=status.HTTP_200_OK)
async def read_rentals(
    db: db_slave_dependency,
    rental_id: int = None,
    car_id: int = None,
    rental_date: str = None,
    return_date: str = None
):
    query = db.query(models.Rental)
    if rental_id:
        query = query.filter(models.Rental.id == rental_id)
    if car_id:
        query = query.filter(models.Rental.car_id == car_id)
    if rental_date:
        query = query.filter(models.Rental.rental_date == rental_date)
    if return_date:
        query = query.filter(models.Rental.return_date == return_date)
    rentals = query.all()
    if not rentals:
        raise HTTPException(status_code=404, detail='Rentals not found')
    return rentals

@app.get("/api/v1/addresses", status_code=status.HTTP_200_OK)
async def read_addresses(
    db: db_slave_dependency,
    address_id: int = None,
    address: str = None,
    city: str = None,
    country: str = None
):
    query = db.query(models.Address)
    if address_id:
        query = query.filter(models.Address.id == address_id)
    if address:
        query = query.filter(models.Address.address == address)
    if city:
        query = query.filter(models.Address.city == city)
    if country:
        query = query.filter(models.Address.country == country)
    addresses = query.all()
    if not addresses:
        raise HTTPException(status_code=404, detail='Addresses not found')
    return addresses

@app.get("/api/v1/car_details", status_code=status.HTTP_200_OK)
async def read_car_details(
    db: db_slave_dependency,
    car_detail_id: int = None,
    location_id: int = None,
    price_per_day: int = None,
    horse_power: int = None
):
    query = db.query(models.CarDetails)
    if car_detail_id:
        query = query.filter(models.CarDetails.id == car_detail_id)
    if location_id:
        query = query.filter(models.CarDetails.location_id == location_id)
    if price_per_day:
        query = query.filter(models.CarDetails.price_per_day == price_per_day)
    if horse_power:
        query = query.filter(models.CarDetails.horse_power == horse_power)
    car_details = query.all()
    if not car_details:
        raise HTTPException(status_code=404, detail='Car details not found')
    return car_details

@app.get("/api/v1/rental_details", status_code=status.HTTP_200_OK)
async def read_rental_details(
    db: db_slave_dependency,
    rental_detail_id: int = None,
    customer_id: int = None,
    total_price: int = None
):
    query = db.query(models.RentalDetails)
    if rental_detail_id:
        query = query.filter(models.RentalDetails.id == rental_detail_id)
    if customer_id:
        query = query.filter(models.RentalDetails.customer_id == customer_id)
    if total_price:
        query = query.filter(models.RentalDetails.total_price == total_price)
    rental_details = query.all()
    if not rental_details:
        raise HTTPException(status_code=404, detail='Rental details not found')
    return rental_details

@app.get("/api/v1/user_details", status_code=status.HTTP_200_OK)
async def read_user_details(
    db: db_slave_dependency,
    user_detail_id: int = None,
    address_id: int = None,
    is_active: bool = None,
    role: str = None,
    email: str = None,
    phone: str = None
):
    query = db.query(models.UserDetail)
    if user_detail_id:
        query = query.filter(models.UserDetail.id == user_detail_id)
    if address_id:
        query = query.filter(models.UserDetail.address_id == address_id)
    if is_active is not None:
        query = query.filter(models.UserDetail.is_active == is_active)
    if role:
        query = query.filter(models.UserDetail.role == role)
    if email:
        query = query.filter(models.UserDetail.email == email)
    if phone:
        query = query.filter(models.UserDetail.phone == phone)
    user_details = query.all()
    if not user_details:
        raise HTTPException(status_code=404, detail='User details not found')
    return user_details

@app.get("/api/v1/payments", status_code=status.HTTP_200_OK)
async def read_payments(
    db: db_slave_dependency,
    payment_id: int = None,
    rental_id: int = None
):
    query = db.query(models.Payment)
    if payment_id:
        query = query.filter(models.Payment.id == payment_id)
    if rental_id:
        query = query.filter(models.Payment.rental_id == rental_id)
    payments = query.all()
    if not payments:
        raise HTTPException(status_code=404, detail='Payments not found')
    return payments

@app.get("/api/v1/payment_details", status_code=status.HTTP_200_OK)
async def read_payment_details(
    db: db_slave_dependency,
    payment_detail_id: int = None,
    user_id: int = None,
    amount: int = None,
    method: str = None,
    payment_date: str = None
):
    query = db.query(models.PaymentDetails)
    if payment_detail_id:
        query = query.filter(models.PaymentDetails.id == payment_detail_id)
    if user_id:
        query = query.filter(models.PaymentDetails.user_id == user_id)
    if amount:
        query = query.filter(models.PaymentDetails.amount == amount)
    if method:
        query = query.filter(models.PaymentDetails.method == method)
    if payment_date:
        query = query.filter(models.PaymentDetails.payment_date == payment_date)
    payment_details = query.all()
    if not payment_details:
        raise HTTPException(status_code=404, detail='Payment details not found')
    return payment_details


#------------------------- Functions on Slave Database ------------------------------#
#...


#------------------------- API Endpoints on Master Database -------------------------#
@app.post("/api/v1/rentals", status_code=status.HTTP_201_CREATED)
async def create_rental(rental: RentalBase, db: db_master_dependency):
    new_data = models.Rental(**rental.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/passwords", status_code=status.HTTP_201_CREATED)
async def create_password(password: PasswordBase, db: db_master_dependency):
    new_data = models.Password(**password.dict())
    db.add(new_data)
    db.commit()


@app.post("/api/v1/cars", status_code=status.HTTP_201_CREATED)
async def create_car(car: CarBase, db: db_master_dependency):
    new_data = models.Car(**car.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/locations", status_code=status.HTTP_201_CREATED)
async def create_location(location: LocationBase, db: db_master_dependency):
    new_data = models.Location(**location.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_master_dependency):
    new_data = models.User(**user.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/addresses", status_code=status.HTTP_201_CREATED)
async def create_address(address: AddressBase, db: db_master_dependency):
    new_data = models.Address(**address.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/car_details", status_code=status.HTTP_201_CREATED)
async def create_car_detail(car_detail: CarDetailsBase, db: db_master_dependency):
    new_data = models.CarDetails(**car_detail.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/rental_details", status_code=status.HTTP_201_CREATED)
async def create_rental_detail(rental_detail: RentalDetailsBase, db: db_master_dependency):
    new_data = models.RentalDetails(**rental_detail.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/user_details", status_code=status.HTTP_201_CREATED)
async def create_user_detail(user_detail: UserDetailBase, db: db_master_dependency):
    new_data = models.UserDetail(**user_detail.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/payments", status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentBase, db: db_master_dependency):
    new_data = models.Payment(**payment.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/payment_details", status_code=status.HTTP_201_CREATED)
async def create_payment_detail(payment_detail: PaymentDetailsBase, db: db_master_dependency):
    new_data = models.PaymentDetails(**payment_detail.dict())
    db.add(new_data)
    db.commit()

@app.post("/api/v1/passwords", status_code=status.HTTP_201_CREATED)
async def create_password(password: PasswordBase, db: db_master_dependency):
    hashed = hashlib.sha512(password.password.encode()).hexdigest()
    password.password = hashed[:50]
    new_data = models.Password(**password.dict())
    db.add(new_data)
    db.commit()