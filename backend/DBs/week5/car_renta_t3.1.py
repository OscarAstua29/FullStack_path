from connection  import PgManager
from flask import Flask,request, jsonify
from flask.views import MethodView

app = Flask(__name__)

class drivers(MethodView):

    def __init__(self):

        self.db_connection_data = {

            "db_name": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost"
        }

        self.db_manager = connection_to_db(self.db_connection_data["db_name"],self.db_connection_data["user"], self.db_connection_data["password"], self.db_connection_data["host"])

    def post(self):

        try:

            data = request.json

            driver_key_list = valid_lists("drivers_key_list")
            driver_status_valid_options = valid_lists("drivers_status_valid_options")
            missing_fields = set(driver_key_list) - set(data.keys())

            if missing_fields:
                return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
            
            if not data["driver_status"].upper() in driver_status_valid_options:
                return jsonify({"error": "Invalid driver status", "Valid Status": driver_status_valid_options}), 400
            
            self.db_manager.execute_query(

                """
                INSERT INTO lyfter_car_rental.drivers (full_name, email, username, password, birth_date, driver_status)
                VALUES(%s,%s,%s,%s,%s,%s)
                """,
                data["full_name"].upper(),
                data["email"],
                data["username"].lower(),
                data["password"],
                data["birth_date"],
                data["driver_status"].upper()
            )

            return jsonify({"message": "Driver added successfully"}), 201
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def patch(self):

        try:

            data = request.json

            driver_status_valid_options = valid_lists("drivers_status_valid_options")

            if not data["driver_status"].upper() in driver_status_valid_options:
                return jsonify({"error": "Invalid reservation status", "Valid Status": driver_status_valid_options}), 400
                
            
            id_valid_confirmation = id_validation("drivers", data, self.db_connection_data)

            if id_valid_confirmation == False:
                return jsonify({f"error":"ID not found in drivers"}), 400


            self.db_manager.execute_query(
                
                """
                UPDATE  lyfter_car_rental.drivers SET driver_status= %s  WHERE id = %s
                """,    
                data["driver_status"].upper(),
                data["id"]
                )

            return jsonify({"message": "Driver status changed successfully"}), 201
        except Exception as e:
            return jsonify(({"error": str(e)}), 500)

    def get(self):

        try:
            
            data = request.json

            if not data:
                request_data=self.db_manager.execute_query(
                
                    f"""
                    SELECT * FROM lyfter_car_rental.drivers
                    """
                )
                print(request_data)
                
                return jsonify({"message": request_data }), 201
            
            else:  
                
                filters_for_drivers = valid_lists("drivers_key_list") 
                
                if "filter_by" not in data :
                    return jsonify({"error": "Missing filter_by key"}), 400
                
                if data["filter_by"].lower() not in filters_for_drivers:
                    
                    return jsonify({"error": "Invalid filters type ", "Valid filters types" : filters_for_drivers}), 400
                
                filter_by = data["filter_by"].lower() #
                
                request_data=self.db_manager.execute_query(
                #Ask in the next class if this quiery it is okey by a sql inyection in filter_by
                    f"""
                    SELECT * FROM lyfter_car_rental.drivers WHERE {filter_by} = %s
                    """,
                   data["filter"]
                )
                if not request_data:    
                    return jsonify({"error": "No data related with filter: " + data["filter"] }), 400

                return jsonify({"message": request_data }), 201

        except Exception as e:
            return jsonify({"error":str(e)}), 500



class vehicles(MethodView):

    def __init__(self):

        self.db_connection_data = {

            "db_name": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost"
        }

        self.db_manager = connection_to_db(self.db_connection_data["db_name"],self.db_connection_data["user"], self.db_connection_data["password"], self.db_connection_data["host"])

    def post(self):

        try:

            data = request.json

            vehicles_key_list = valid_lists("vehicles_key_list")
            vehicles_status_valid_options = valid_lists("vehicles_status_valid_options")
            missing_fields = set(vehicles_key_list) - set(data.keys())

            if missing_fields:
                return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
            
            if not data["vehicle_status"].upper() in vehicles_status_valid_options:
                return jsonify({"error": "Invalid vehicles status", "Valid Status": vehicles_status_valid_options}), 400
            
            self.db_manager.execute_query(

                """
                INSERT INTO lyfter_car_rental.vehicles (brand, model, manufacture_year, vehicle_status)
                VALUES(%s,%s,%s,%s)
                """,
                data["brand"].upper(),
                data["model"].upper(),
                data["manufacture_year"],
                data["vehicle_status"].upper()
            )

            return jsonify({"message": "Vehicle added successfully"}), 201
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def patch(self):

        try:

            data = request.json

            vehicles_status_valid_options = valid_lists("vehicles_status_valid_options")

            if not data["vehicle_status"].upper() in vehicles_status_valid_options:
                return jsonify({"error": "Invalid vehicle status", "Valid Status": vehicles_status_valid_options}), 400
                
            
            id_valid_confirmation = id_validation("vehicles", data, self.db_connection_data)

            if id_valid_confirmation == False:
                return jsonify({f"error":"ID not found in vehicles"}), 400


            self.db_manager.execute_query(
                
                """
                UPDATE  lyfter_car_rental.vehicles SET vehicle_status= %s  WHERE id = %s
                """,    
                data["vehicle_status"].upper(),
                data["id"]
                )
            
            organize_tables(self.db_manager, "vehicles")
            

            return jsonify({"message": "Vehicle status changed successfully"}), 201
        except Exception as e:
            return jsonify(({"error": str(e)}), 500)

    def get(self):

        try:
            
            data = request.json

            if not data:
                request_data=self.db_manager.execute_query(
                
                    f"""
                    SELECT * FROM lyfter_car_rental.vehicles
                    """
                )
                print(request_data)
                
                return jsonify({"message": request_data }), 201

            else:
                
                filters_for_vehicles = valid_lists("vehicles_key_list") 

                if "filter_by" not in data :
                    return jsonify({"error": "Missing filter_by key"}), 400
                
                if data["filter_by"].lower() not in filters_for_vehicles:
                    
                    return jsonify({"error": "Invalid filters type ", "Valid filters types" : filters_for_vehicles}), 400
                
                filter_by = data["filter_by"].lower() 
                
                request_data=self.db_manager.execute_query(
                #Ask in the next class if this quiery it is okey by a sql inyection in filter_by
                    f"""
                    SELECT * FROM lyfter_car_rental.vehicles WHERE {filter_by} = %s
                    """,
                    data["filter"]
                )

                if not request_data:    
                    return jsonify({"error": "No data related with filter: " + data["filter"] }), 400


                return jsonify({"message": request_data }), 201

        except Exception as e:
            return jsonify({"error":str(e)}), 500



class reservation(MethodView):

    def __init__(self):
        self.db_connection_data = {

                    "db_name": "postgres",
                    "user": "postgres",
                    "password": "postgres",
                    "host": "localhost"
                }

        self.db_manager = connection_to_db(self.db_connection_data["db_name"],self.db_connection_data["user"], self.db_connection_data["password"], self.db_connection_data["host"])

    def post(self):

        try:

            data = request.json

            reservation_key_list = valid_lists("reservation_key_list")
            reservation_status_valid_options = valid_lists("reservation_status_valid_options")
            missing_fields = set(reservation_key_list) - set(data.keys())

            if missing_fields:
                return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
            
            if not data["reservation_status"].upper() in reservation_status_valid_options:
                print("aca estoy")
                return jsonify({"error": "Invalid reservation status", "Valid Status": reservation_status_valid_options}), 400
            
            self.db_manager.execute_query(

                """
                INSERT INTO lyfter_car_rental.reservations (driver, vehicle, reservation_date, reservation_status)
                VALUES(%s,%s,%s,%s)
                """,
                data["driver"],
                data["vehicle"],
                data["reservation_date"],
                data["reservation_status"].upper()
            )

            return jsonify({"message": "Reservation added successfully"}), 201
        
        except Exception as e:
            print(e)
            return jsonify({"errorxxx": str(e)}), 500

    def patch(self):

        try:

            data = request.json

            reservation_status_valid_options = valid_lists("reservation_status_valid_options")

            if not data["reservation_status"].upper() in reservation_status_valid_options:
                return jsonify({"error": "Invalid reservation status", "Valid Status": reservation_status_valid_options}), 400
                
            
            id_valid_confirmation = id_validation("reservation", data, self.db_connection_data)

            if id_valid_confirmation == False:
                return jsonify({f"error":"ID not found in reservation"}), 400


            self.db_manager.execute_query(
                
                """
                UPDATE  lyfter_car_rental.reservations SET reservation_status= %s  WHERE id = %s
                """,    
                data["reservation_status"].upper(),
                data["id"]
                )
            

            return jsonify({"message": "Reservation status changed successfully"}), 201
        except Exception as e:
            return jsonify(({"error": str(e)}), 500)


    def get(self):

        try:
            
            data = request.json

            if not data:
                request_data=self.db_manager.execute_query(
                
                    f"""
                    SELECT * FROM lyfter_car_rental.reservations
                    """
                )
                print(request_data)
                
                return jsonify({"message": request_data }), 201

            else:
                
                filters_for_reservations = valid_lists("reservation_key_list") 

                if "filter_by" not in data :
                    return jsonify({"error": "Missing filter_by key"}), 400
                
                if data["filter_by"].lower() not in filters_for_reservations:
                    
                    return jsonify({"error": "Invalid filters type ", "Valid filters types" : filters_for_reservations}), 400
                
                filter_by = data["filter_by"].lower() 
                
                request_data=self.db_manager.execute_query(
                #Ask in the next class if this quiery it is okey by a sql inyection in filter_by
                    f"""
                    SELECT * FROM lyfter_car_rental.reservations WHERE {filter_by} = %s
                    """,
                    data["filter"]
                )

                if not request_data:    
                    return jsonify({"error": "No data related with filter: " + data["filter"] }), 400


                return jsonify({"message": request_data }), 201

        except Exception as e:
            return jsonify({"error":str(e)}), 500



def connection_to_db(param_db_name,param_user,param_password,param_host):
    db_manager = PgManager(
    db_name = param_db_name,
    user = param_user,
    password = param_password,
    host=param_host
        )
    return(db_manager)

def valid_lists(key):

    lists={

        "drivers_key_list" : ["full_name","email", "username","password", "driver_status" ,"birth_date"],
        "drivers_status_valid_options" : ["PENDING PAYMENT","PAID","DELINQUET"],
        "vehicles_key_list" : ["brand","model", "manufacture_year","vehicle_status"],
        "vehicles_status_valid_options" : ["AVAILABLE","RENTED","DISABLED"],
        "reservation_key_list" : ["driver","vehicle", "reservation_date","reservation_status"],
        "reservation_status_valid_options" : ["FINISHED","IN PROGRESS","CANCELED"],
        "tables_names_valid_options" : ["drivers","vehicles","reservations"]
    }

    return lists.get(key)

def organize_tables(db_manager,table):
        
        request_data = db_manager.execute_query(
                    f"""
                    SELECT * FROM lyfter_car_rental.{table} ORDER BY id ASC;
                    """,
                )
        
        return request_data
        
def id_validation(option, data, db_connection_data):  
    try:

        
        connection = connection_to_db (db_connection_data["db_name"],db_connection_data["user"], db_connection_data["password"], db_connection_data["host"])

        option_data = connection.execute_query(

            f"""
            SELECT id FROM lyfter_car_rental.{option}
            """
        )

        id_list = []

        for i in option_data:
            id_list.append(i[0])

        if  data["id"] not in id_list :
            return False       
        return True
            
    except Exception as e:
        return jsonify({"error":str(e)}), 500 

drivers_view = drivers.as_view('drivers_view')
app.add_url_rule('/drivers', view_func=drivers_view, methods=['POST','GET'])
app.add_url_rule('/drivers', view_func=drivers_view, methods=['PATCH'])

vehicles_view = vehicles.as_view('vehicles_view')
app.add_url_rule('/vehicles', view_func=vehicles_view , methods=['POST','GET'])
app.add_url_rule('/vehicles', view_func=vehicles_view , methods=['PATCH'])

reservations_view = reservation.as_view('reservations_view')
app.add_url_rule('/reservations', view_func=reservations_view , methods=['POST','GET'])
app.add_url_rule('/reservations', view_func=reservations_view , methods=['PATCH'])

if __name__ == "__main__":
    app.run(host="localhost", debug=True)