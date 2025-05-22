from connection import PgManager

db_manager = PgManager(
    db_name="postgres",
    user="postgres",
    password="postgres",
    host="localhost"
)

def add_user(full_name, email, username, password, birth_date, account_status):

    db_manager.execute_query(

        """
        INSERT INTO lyfter_car_rental.users(full_name, email, username, password, birth_date, account_status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        full_name, email, username, password, birth_date, account_status
        
    )

def add_vehicle (brand,model,maufacture_year,vehicle_status):
        
    db_manager.execute_query(

        """
        INSERT INTO lyfter_car_rental.vehicles("brand","model","manufacture_year","vehicle_status")
        VALUES(%s,%s,%s,%s)
        """,
        brand,model,maufacture_year,vehicle_status
    )

def change_user_status (status_to_change,user_id):
        
    db_manager.execute_query(

        """
        UPDATE lyfter_car_rental.users
        SET account_status = %s
        WHERE id = %s
        """,
        status_to_change, user_id
    )

def change_user_status (status_to_change,user_id):
        
    db_manager.execute_query(

        """
        UPDATE lyfter_car_rental.vehicles
        SET vehicles_status = %s
        WHERE id = %s
        """,
        status_to_change, user_id
    )

def add_reservation(driver, vehicle_rented, reservation_date):

    db_manager.execute_query(
        """
        INSERT INTO lyfter_car_rental.reservations(driver, vehicle_rented, reservation_date)
        VALUES(%s, %s, %s)
        """,
        driver, vehicle_rented, reservation_date
)

    db_manager.execute_query(
        """
        UPDATE lyfter_car_rental.vehicles
        SET vehicle_status = 'UNAVAILABLE'
        WHERE id = %s
        """,
        vehicle_rented
    )

def devolution (driver,vehicle_rented,reservation_date, ):

    db_manager.execute_query(

         db_manager.execute_query(
        """
        UPDATE lyfter_car_rental.vehicles
        SET vehicle_status = 'AVAILABLE'
        WHERE id = %s
        """,
        vehicle_rented
    )
        
    )

def disable_vehicle(vehicle_rented):

    db_manager.execute_query(

         db_manager.execute_query(
        """
        UPDATE lyfter_car_rental.vehicles
        SET vehicle_status = 'DISABLED'
        WHERE id = %s
        """,
        vehicle_rented
    )
        
    )

def view_rented (vehicle_rented):

    db_manager.execute_query(

         db_manager.execute_query(
        """
        SELECT * FROM lyfter_car_rental.vehicles
        WHERE vehicle_status = 'RENTED'
        """,
        vehicle_rented
    )
        
    )

def view_available (vehicle_rented):

    db_manager.execute_query(

         db_manager.execute_query(
        """
        SELECT * FROM lyfter_car_rental.vehicles
        WHERE vehicle_status = 'AVAILABLE'
        """,
        vehicle_rented
    )
        
    )