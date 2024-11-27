CREATE DATABASE IF NOT EXISTS car_rental;

USE car_rental;

CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    make VARCHAR(50),                           
    model VARCHAR(50),                          
    year INT,                                   
    price_per_day DECIMAL(10, 2),               
    available BOOLEAN DEFAULT TRUE              
);

CREATE TABLE IF NOT EXISTS rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    car_id INT,                               
    customer_name VARCHAR(100),                
    rental_date DATE,                          
    return_date DATE,                         
    total_price DECIMAL(10, 2),                
    FOREIGN KEY (car_id) REFERENCES cars(id)   
);

INSERT INTO cars (make, model, year, price_per_day) VALUES
('Toyota', 'Corolla', 2020, 50.00),
('Ford', 'Focus', 2019, 45.00),
('Honda', 'Civic', 2021, 60.00),
('BMW', '3 Series', 2022, 100.00),
('Audi', 'A4', 2021, 90.00);