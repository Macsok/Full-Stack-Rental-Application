from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models as models
from bases import *
from database_connection import engine_master, engine_slave, SessionLocal_Master, SessionLocal_Slave
from sqlalchemy.orm import Session
from sqlalchemy import text

# To test API visit http://localhost:8000/docs#

app = FastAPI()
models.Base.metadata.create_all(bind=engine_master)

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

@app.post("/api/v1/cars", status_code=status.HTTP_201_CREATED)
async def create_car(car: CarBase, db: db_master_dependency):
    new_data = models.Car(**car.dict())
    db.add(new_data)
    db.commit()

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

@app.post("/api/v1/rentals", status_code=status.HTTP_201_CREATED)
async def create_rental(car: RentalBase, db: db_master_dependency):
    new_data = models.Rental(**car.dict())
    db.add(new_data)
    db.commit()