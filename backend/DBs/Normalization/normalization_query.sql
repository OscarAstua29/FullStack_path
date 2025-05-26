SQLite
CREATE TABLE customers (
 id INT PRIMARY KEY,
 customer_name VARCHA(25)NOT NULL,
 customer_phone VARCHA(25)NOT NULL
);

CREATE TABLE address (
 id INT PRIMARY KEY,
 address VARCHA(25)NOT NULL
);

CREATE TABLE time (
 id INT PRIMARY KEY,
 time VARCHA(10)NOT NULL
);

CREATE TABLE menu (
 id INT PRIMARY KEY,
 item VARCHA(10) NOT NULL,
 price FLOAT NOT NULL
);

CREATE TABLE orders_completed (
 id INT PRIMARY KEY,
 order_id INT NOT NULL,
 item_id INT REFERENCES menu(id),
 customer_id INT REFERENCES customers(id),
 address_id INT REFERENCES address(id),
 delivery_id INT REFERENCES time(id)
);

-- DROP table address;
-- DROP table customers;
-- DROP table menu;
-- DROP table time;
-- DROP table general;
-- DROP table make;
-- DROP table model;
-- DROP table time;
-- DROP table vin;



--------------------------------------------

CREATE TABLE vin (
 id INT PRIMARY KEY,
 vin VARCHA(25)NOT NULL
);

CREATE TABLE make (
 id INT PRIMARY KEY,
 make VARCHA(25)NOT NULL
);

CREATE TABLE model (
 id INT PRIMARY KEY,
 model VARCHA(25)NOT NULL,
 make_id INT REFERENCES make(id)
);

CREATE TABLE color (
 id INT PRIMARY KEY,
 color VARCHA(10)NOT NULL
);

CREATE TABLE car (
 id INT PRIMARY KEY,
 vin_id INT REFERENCES vin(id),
 model_id INT REFERENCES model(id),
 color_id INT REFERENCES color(id),
 year INT NOT NULL
);

CREATE TABLE owner (
 id INT PRIMARY KEY,
 owner VARCHA(15)NOT NULL,
 owner_phone VARCHA(15)NOT NULL
);

CREATE TABLE insurance_company (
 id INT PRIMARY KEY,
 insurance_company VARCHA(25)NOT NULL
);

CREATE TABLE policy (
 id INT PRIMARY KEY,
 policy VARCHA(15)NOT NULL,
 company INT NOT NULL
);

CREATE TABLE general (
 id INT PRIMARY KEY,
 owner_id INT REFERENCES owner(id)
 car_id INT REFERENCES car(id)
 insutance_id INT REFERENCES policy(id)
);