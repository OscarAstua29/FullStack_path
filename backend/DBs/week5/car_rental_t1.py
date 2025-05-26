#INSTALL FAKER pip install faker
#AND EXTENXION FOR VEHICLES pip install faker-vehicle


from connection import PgManager
from faker import Faker
from faker_vehicle import VehicleProvider


fake = Faker()#This line, creates a faker instance
fake.add_provider(VehicleProvider)#add the Vehicles extension

db_manager = PgManager(
    db_name="postgres",
    user="postgres",
    password="postgres",
    host="localhost"
)



db_manager.execute_query(
    """
    CREATE TABLE IF NOT EXISTS  lyfter_car_rental.drivers(
	id SERIAL PRIMARY KEY,
	full_name VARCHAR(30),
	email VARCHAR(30),
    username VARCHAR(30),
	password VARCHAR(10),
    birth_date DATE,
	driver_status VARCHAR(20)
    );"""
),

db_manager.execute_query(
    """
    CREATE TABLE IF NOT EXISTS lyfter_car_rental.vehicles(
	id SERIAL PRIMARY KEY,
	brand VARCHAR(30),
	model VARCHAR(30),
    manufacture_year INTEGER,
	vehicle_status VARCHAR(15)
    );"""
)

db_manager.execute_query(
    """
    CREATE TABLE IF NOT EXISTS lyfter_car_rental.reservations(
	id SERIAL PRIMARY KEY,
	driver INT REFERENCES lyfter_car_rental.drivers(id),
	vehicle INT REFERENCES lyfter_car_rental.vehicles(id),
	reservation_date DATE,
    reservation_status VARCHAR(20)
    );"""
)

for i in range(50):

    full_name = fake.name()
    email = fake.email()
    username = fake.user_name()
    password = fake.password(length=10)
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    account_status = fake.random_element(elements=("pending payment", "paid"))

    db_manager.execute_query(

        """
        INSERT INTO lyfter_car_rental.users(full_name, email, username, password, birth_date, account_status)
	    VALUES (%s, %s, %s, %s, %s, %s)
        """,
        full_name, email, username, password, birth_date, account_status
        
    )
    
for i in range(50):
    brand=fake.vehicle_make(),
    model=fake.vehicle_model(),
    maufacture_year=fake.vehicle_year(),
    vehicle_status=fake.random_element(elements=("RENTED","AVAILABLE,DISABLED"))

    db_manager.execute_query(

        """
        INSERT INTO lyfter_car_rental.vehicles("brand","model","manufacture_year","vehicle_status")
        VALUES(%s,%s,%s,%s)
        """,
        brand,model,maufacture_year,vehicle_status
    )

qty_drivers = db_manager.execute_query("SELECT COUNT(*) FROM lyfter_car_rental.users")[0][0]
qty_vehicles = db_manager.execute_query("SELECT COUNT(*) FROM lyfter_car_rental.vehicles")[0][0]

for i in range(1, qty_drivers + 1, 1):

    vehicle_rented= fake.random_int(min=1, max=10),
    reservation_date=fake.date_this_year()

    db_manager.execute_query(

        """
        INSERT INTO lyfter_car_rental.reservations("driver","vehicle_rented","reservation_date")
        VALUES(%s,%s,%s)
        """,
        i,vehicle_rented,reservation_date
    )