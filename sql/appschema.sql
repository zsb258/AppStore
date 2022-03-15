CREATE TABLE IF NOT EXISTS users(
first_name varchar(16) not null,
last_name varchar(16) not null,
email varchar(64) PRIMARY KEY,
password VARCHAR(32) NOT NULL CHECK (
		LENGTH(password) >= 8 AND LENGTH(password) <= 32 
		AND password LIKE '%[a-z]%' AND password LIKE '%[A-Z]%' AND password LIKE '%[0-9]%'),
date_of_birth date not null CHECK (CURRENT_DATE - date_of_birth >= 18),
since date not null CHECK (since > date_of_birth),
country varchar(16) not null,
credit_card_type varchar(16) not null,
credit_card_no varchar(16) UNIQUE not null
);

CREATE TABLE IF NOT EXISTS apartments(
apartment_id int PRIMARY KEY,
host VARCHAR(64) REFERENCES users(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
country varchar(16) not null,
city varchar(16)not null,
address varchar(64) not null,
num_guests int not null,
num_beds int not null,
num_bathrooms int not null,
property_type varchar(64) not null,
amenities varchar(64) not null,
house_rules varchar(64) not null,
price decimal(8,2) not null check (price > 0)
);

CREATE TABLE IF NOT EXISTS rental(
rental_id int PRIMARY KEY,
apartment_id int not null REFERENCES apartments(apartment_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
check_in date not null CHECK (check_in > CURRENT_DATE),
check_out date not null CHECK(check_out > check_in),
guest varchar(64) REFERENCES users(email),
total_price DECIMAL(8,2) not null,
rating int not null CHECK (rating >= 1 and rating <= 5)
);
