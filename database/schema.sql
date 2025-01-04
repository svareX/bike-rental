DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS bikes;
DROP TABLE IF EXISTS bike_events;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    role INTEGER NOT NULL,
    avatar VARCHAR,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    motto VARCHAR NOT NULL,
    established DATE NOT NULL
);

CREATE TABLE bikes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    brand_id INTEGER NOT NULL,
    type INTEGER NOT NULL,
    price_per_day DOUBLE NOT NULL,
    img VARCHAR NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE TABLE bike_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    bike_id INTEGER NOT NULL,
    type INTEGER NOT NULL,
    date_from DATETIME NOT NULL,
    date_to DATETIME NOT NULL,
    total_price INTEGER NOT NULL,
    payment_method INTEGER NOT NULL, -- Platba na místě: 1 | Platba kartou online: 2
    status INTEGER,
    description VARCHAR,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bike_id) REFERENCES bikes(id)
);

--Testovací účty, heslo = heslo
INSERT INTO users(first_name, last_name, email, password, role, avatar, created_at, updated_at) VALUES ('Jan', 'Zákazník', 'zakaznik@gmail.com', '87db049e442d9562038011a70fd85a9ac45875dd497f469437f25cfe30df3125', 0, 'person.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO users(first_name, last_name, email, password, role, avatar, created_at, updated_at) VALUES ('Jan', 'Zaměstnanec', 'zamestnanec@gmail.com', '87db049e442d9562038011a70fd85a9ac45875dd497f469437f25cfe30df3125', 1, 'person.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


INSERT INTO brands(name, motto, established) VALUES ('Brand#1', 'Lorem ipsum', CURRENT_DATE);
INSERT INTO brands(name, motto, established) VALUES ('Brand#2', 'Lorem ipsum', CURRENT_DATE);
INSERT INTO brands(name, motto, established) VALUES ('Brand#3', 'Lorem ipsum', CURRENT_DATE);

INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#1', 2, 1, 185, 'bike_placeholder.png');
INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#2', 3, 1, 210, 'bike_placeholder.png');
INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#3', 1, 1, 100, 'bike_placeholder.png');
INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#4', 2, 1, 290, 'bike_placeholder.png');
INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#5', 2, 1, 110, 'bike_placeholder.png');
INSERT INTO bikes(name, brand_id, type, price_per_day, img) VALUES ('Bike#6', 3, 1, 220, 'bike_placeholder.png');

INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to, total_price, payment_method, status) VALUES (1,1,1,'2024-12-08', '2024-12-11', 185*4, 1, 1);
INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to, total_price, payment_method, status) VALUES (1,2,1,'2024-12-09', '2024-12-16', 210*8, 2, 1);
INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to, total_price, payment_method, status) VALUES (1,3,2,'2024-12-01', '2024-12-03',100*3, 2, 1);
INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to, total_price, payment_method, status) VALUES (1,1,1,'2024-12-05', '2024-12-06',185*2, 2, 3);