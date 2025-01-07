from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from database_connection import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    name = Column(String(50))

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)

class CarDetails(Base):
    __tablename__ = 'car_details'

    id = Column(Integer, ForeignKey('cars.id'), primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    price_per_day = Column(Integer)
    horse_power = Column(Integer)

class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    rental_date = Column(Date)
    return_date = Column(Date)

class RentalDetails(Base):
    __tablename__ = 'rental_details'

    id = Column(Integer, ForeignKey('rentals.id'), primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Integer)

class UserDetail(Base):
    __tablename__ = 'user_details'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    is_active = Column(Boolean, default=True)
    role = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    password = Column(String(50))

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))

class PaymentDetails(Base):
    __tablename__ = 'payment_details'

    id = Column(Integer, ForeignKey('payments.id'), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    method = Column(String(50))
    payment_date = Column(Date)