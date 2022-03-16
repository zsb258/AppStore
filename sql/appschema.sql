CREATE TABLE IF NOT EXISTS users(
first_name VARCHAR(16) NOT NULL,
last_name VARCHAR(16) NOT NULL,
email VARCHAR(64) PRIMARY KEY,
password VARCHAR(32) NOT NULL CHECK (
		LENGTH(password) >= 8 AND LENGTH(password) <= 32 
		AND password SIMILAR TO '%[a-z]%'
		AND password SIMILAR TO '%[A-Z]%'
		AND password SIMILAR TO '%[0-9]%'),
date_of_birth DATE NOT NULL CHECK (((CURRENT_DATE - date_of_birth) / 365.2425) > 18),
since DATE NOT NULL DEFAULT CURRENT_DATE,
country VARCHAR(32) NOT NULL,
credit_card_type VARCHAR(16) NOT NULL,
credit_card_no VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS apartments(
apartment_id SERIAL PRIMARY KEY,
host VARCHAR(64) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
country VARCHAR(16) NOT NULL,
city VARCHAR(32) NOT NULL,
address VARCHAR(64) NOT NULL,
num_guests INT NOT NULL,
num_beds INT NOT NULL CHECK (num_beds >= num_guests),
num_bathrooms INT NOT NULL,
property_type VARCHAR(64) NOT NULL,
amenities VARCHAR(64) NOT NULL,
house_rules VARCHAR(64) NOT NULL,
price DECIMAL(8,2) NOT NULL check (price > 0)
);

CREATE TABLE IF NOT EXISTS rentals(
rental_id SERIAL PRIMARY KEY,
apartment_id INT NOT NULL REFERENCES apartments(apartment_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
check_in DATE NOT NULL CHECK (check_in > CURRENT_DATE),
check_out DATE NOT NULL CHECK(check_out > check_in),
guest VARCHAR(64) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
total_price DECIMAL(8,2) NOT NULL,
rating INT NOT NULL CHECK (rating >= 1 and rating <= 5)
);
