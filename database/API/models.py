from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from database import Base


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True)  # We want every user to have unique name


# class Post(Base):
#     __tablename__ = 'posts'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))
#     content = Column(String(100))
#     user_id = Column(Integer)


#-------------------------------------------------


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)


class CarDetails(Base):
    __tablename__ = 'car_details' 

    id = Column(Integer, ForeignKey('cars.id'), primary_key=True,index=True)
    price_per_day = Column(Integer)
    horse_power = Column(Integer)
    location = Column(String(50))


class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    rental_date = Column(Date)
    return_date = Column(Date)


class RentalDetails(Base):
    __tablename__ = 'rental_details'

    id = Column(Integer, ForeignKey('rentals.id'),primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    is_active = Column(Boolean, default=True)


class UserDetail(Base):
    __tablename__ = 'user_details'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    role = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))


class UserAddress(Base):
    __tablename__ = 'user_address'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    address = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))


class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    password = Column(String(50))


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    address = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    amount = Column(Integer)
    method = Column(String(50))
    payment_date = Column(Date)