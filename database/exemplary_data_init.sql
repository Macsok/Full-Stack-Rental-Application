-- Create tables if they don't exist
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
INSERT INTO cars (brand, model, year) VALUES ('Toyota', 'Corolla', 2020);
INSERT INTO cars (brand, model, year) VALUES ('Honda', 'Civic', 2019);

INSERT INTO locations (address_id, name) VALUES (1, 'Downtown');
INSERT INTO locations (address_id, name) VALUES (2, 'Airport');

INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (1, 1, 50, 150);
INSERT INTO car_details (id, location_id, price_per_day, horse_power) VALUES (2, 2, 60, 160);

INSERT INTO users (username) VALUES ('john_doe');
INSERT INTO users (username) VALUES ('jane_doe');

INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (1, 1, TRUE, 'customer', 'john@example.com', '123456789');
INSERT INTO user_details (id, address_id, is_active, role, email, phone) VALUES (2, 2, TRUE, 'customer', 'jane@example.com', '987654321');

INSERT INTO addresses (address, city, country) VALUES ('123 Main St', 'New York', 'USA');
INSERT INTO addresses (address, city, country) VALUES ('456 Elm St', 'Los Angeles', 'USA');

INSERT INTO rentals (car_id, rental_date, return_date) VALUES (1, '2023-01-01', '2023-01-10');
INSERT INTO rentals (car_id, rental_date, return_date) VALUES (2, '2023-02-01', '2023-02-10');

INSERT INTO rental_details (id, customer_id, total_price) VALUES (1, 1, 500);
INSERT INTO rental_details (id, customer_id, total_price) VALUES (2, 2, 600);

INSERT INTO passwords (id, password) VALUES (1, 'password123');
INSERT INTO passwords (id, password) VALUES (2, 'password456');

INSERT INTO payments (rental_id) VALUES (1);
INSERT INTO payments (rental_id) VALUES (2);

INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (1, 1, 500, 'Credit Card', '2023-01-11');
INSERT INTO payment_details (id, user_id, amount, method, payment_date) VALUES (2, 2, 600, 'PayPal', '2023-02-11');