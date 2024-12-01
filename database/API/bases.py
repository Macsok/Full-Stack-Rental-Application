from pydantic import BaseModel


class CarBase(BaseModel):
    brand: str
    model: str
    year: int


class UserBase(BaseModel):
    username: str


class RentalBase(BaseModel):
    car_id: int
    rental_date: str
    return_date: str


class CarDetailsBase(BaseModel):
    location_id: int
    price_per_day: int
    horse_power: int


class RentalDetailsBase(BaseModel):
    customer_id: int
    total_price: int


class UserDetailBase(BaseModel):
    address_id: int
    is_active: bool
    role: str
    email: str
    phone: str


class PasswordBase(BaseModel):
    password: str


class LocationBase(BaseModel):
    address_id: int
    name: str


class AddressBase(BaseModel):
    address: str
    city: str
    country: str


class PaymentBase(BaseModel):
    rental_id: int


class PaymentDetailsBase(BaseModel):
    user_id: int
    amount: int
    method: str
    payment_date: str