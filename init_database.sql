-- This script should be run before the application starts
USE car_rental_db;
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    address_id INTEGER,
    name VARCHAR(50),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    brand VARCHAR(50),
    model VARCHAR(50),
    year INTEGER
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS car_details (
    id INTEGER PRIMARY KEY,
    location_id INTEGER,
    price_per_day INTEGER,
    horse_power INTEGER,
    FOREIGN KEY (id) REFERENCES cars(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS rentals (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    car_id INTEGER,
    rental_date DATE,
    return_date DATE,
    FOREIGN KEY (car_id) REFERENCES cars(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS rental_details (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    total_price INTEGER,
    FOREIGN KEY (id) REFERENCES rentals(id),
    FOREIGN KEY (customer_id) REFERENCES users(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY,
    address_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(50),
    FOREIGN KEY (id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY,
    password VARCHAR(50),
    FOREIGN KEY (id) REFERENCES users(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    rental_id INTEGER,
    FOREIGN KEY (rental_id) REFERENCES rentals(id)
) ENGINE=InnoDB ENCRYPTION='Y';

CREATE TABLE IF NOT EXISTS payment_details (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    method VARCHAR(50),
    payment_date DATE,
    FOREIGN KEY (id) REFERENCES payments(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB ENCRYPTION='Y';

-- Insert exemplary data
INSERT INTO addresses (address, city, country) VALUES ('123 Main St', 'New York', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('456 Elm St', 'Los Angeles', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('789 Oak St', 'Chicago', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('101 Pine St', 'Houston', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('202 Maple St', 'Phoenix', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('303 Cedar St', 'Philadelphia', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('404 Birch St', 'San Antonio', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('505 Walnut St', 'San Diego', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('606 Cherry St', 'Dallas', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('707 Ash St', 'San Jose', 'USA');

INSERT INTO users (username) VALUES ('john_doe');
INSERT INTO users (username) VALUES ('jane_doe');
INSERT INTO users (username) VALUES ('alice_smith');
INSERT INTO users (username) VALUES ('bob_jones');
INSERT INTO users (username) VALUES ('charlie_brown');
INSERT INTO users (username) VALUES ('david_clark');
INSERT INTO users (username) VALUES ('eve_miller');
INSERT INTO users (username) VALUES ('frank_wilson');
INSERT INTO users (username) VALUES ('grace_lee');
INSERT INTO users (username) VALUES ('henry_taylor');

INSERT INTO locations (address_id, name) VALUES (1, 'Downtown');
INSERT INTO locations (address_id, name) VALUES (2, 'Airport');
INSERT INTO locations (address_id, name) VALUES (3, 'Suburbs');
INSERT INTO locations (address_id, name) VALUES (4, 'City Center');
INSERT INTO locations (address_id, name) VALUES (5, 'Train Station');
INSERT INTO locations (address_id, name) VALUES (6, 'Bus Station');
INSERT INTO locations (address_id, name) VALUES (7, 'Mall');
INSERT INTO locations (address_id, name) VALUES (8, 'Hotel');
INSERT INTO locations (address_id, name) VALUES (9, 'University');
INSERT INTO locations (address_id, name) VALUES (10, 'Park');

INSERT INTO cars (brand, model, year) VALUES ('Toyota', 'Corolla', 2020);
INSERT INTO cars (brand, model, year) VALUES ('Honda', 'Civic', 2019);
INSERT INTO cars (brand, model, year) VALUES ('Ford', 'Focus', 2018);
INSERT INTO cars (brand, model, year) VALUES ('Chevrolet', 'Malibu', 2017);
INSERT INTO cars (brand, model, year) VALUES ('Nissan', 'Altima', 2021);
INSERT INTO cars (brand, model, year) VALUES ('BMW', '3 Series', 2020);
INSERT INTO cars (brand, model, year) VALUES ('Audi', 'A4', 2019);
INSERT INTO cars (brand, model, year) VALUES ('Mercedes', 'C-Class', 2018);
INSERT INTO cars (brand, model, year) VALUES ('Volkswagen', 'Passat', 2017);
INSERT INTO cars (brand, model, year) VALUES ('Hyundai', 'Elantra', 2021);

INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (1, 1, 50, 150);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (2, 2, 60, 160);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (3, 3, 55, 140);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (4, 4, 65, 170);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (5, 5, 70, 180);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (6, 6, 75, 190);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (7, 7, 80, 200);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (8, 8, 85, 210);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (9, 9, 90, 220);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (10, 10, 95, 230);

INSERT INTO rentals (car_id, rental_date, return_date) VALUES (1, '2023-01-01', '2023-01-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (2, '2023-02-01', '2023-02-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (3, '2023-03-01', '2023-03-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (4, '2023-04-01', '2023-04-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (5, '2023-05-01', '2023-05-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (6, '2023-06-01', '2023-06-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (7, '2023-07-01', '2023-07-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (8, '2023-08-01', '2023-08-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (9, '2023-09-01', '2023-09-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (10, '2023-10-01', '2023-10-10');

INSERT INTO rental_details (id, customer_id, total_price) VALUES (1, 1, 500);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (2, 2, 600);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (3, 3, 550);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (4, 4, 650);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (5, 5, 700);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (6, 6, 750);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (7, 7, 800);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (8, 8, 850);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (9, 9, 900);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (10, 10, 950);

INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (1, 1, TRUE, 'customer', 'john@example.com', '123456789');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (2, 2, TRUE, 'customer', 'jane@example.com', '987654321');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (3, 3, TRUE, 'customer', 'alice@example.com', '234567890');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (4, 4, TRUE, 'customer', 'bob@example.com', '345678901');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (5, 5, TRUE, 'customer', 'charlie@example.com', '456789012');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (6, 6, TRUE, 'customer', 'david@example.com', '567890123');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (7, 7, TRUE, 'customer', 'eve@example.com', '678901234');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (8, 8, TRUE, 'customer', 'frank@example.com', '789012345');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (9, 9, TRUE, 'customer', 'grace@example.com', '890123456');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (10, 10, TRUE, 'customer', 'henry@example.com', '901234567');

INSERT INTO passwords (id, password) VALUES (1, 'password123');
INSERT INTO passwords (id, password) VALUES (2, 'password456');
INSERT INTO passwords (id, password) VALUES (3, 'password789');
INSERT INTO passwords (id, password) VALUES (4, 'password012');
INSERT INTO passwords (id, password) VALUES (5, 'password345');
INSERT INTO passwords (id, password) VALUES (6, 'password678');
INSERT INTO passwords (id, password) VALUES (7, 'password901');
INSERT INTO passwords (id, password) VALUES (8, 'password234');
INSERT INTO passwords (id, password) VALUES (9, 'password567');
INSERT INTO passwords (id, password) VALUES (10, 'password890');

INSERT INTO payments (rental_id) VALUES (1);
INSERT INTO payments (rental_id) VALUES (2);
INSERT INTO payments (rental_id) VALUES (3);
INSERT INTO payments (rental_id) VALUES (4);
INSERT INTO payments (rental_id) VALUES (5);
INSERT INTO payments (rental_id) VALUES (6);
INSERT INTO payments (rental_id) VALUES (7);
INSERT INTO payments (rental_id) VALUES (8);
INSERT INTO payments (rental_id) VALUES (9);
INSERT INTO payments (rental_id) VALUES (10);

INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (1, 1, 500, 'Credit Card', '2023-01-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (2, 2, 600, 'PayPal', '2023-02-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (3, 3, 550, 'Credit Card', '2023-03-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (4, 4, 650, 'PayPal', '2023-04-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (5, 5, 700, 'Credit Card', '2023-05-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (6, 6, 750, 'PayPal', '2023-06-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (7, 7, 800, 'Credit Card', '2023-07-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (8, 8, 850, 'PayPal', '2023-08-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (9, 9, 900, 'Credit Card', '2023-09-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (10, 10, 950, 'PayPal', '2023-10-11');