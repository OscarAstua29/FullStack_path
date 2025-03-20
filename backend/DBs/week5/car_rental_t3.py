from flask import Flask,request, jsonify
from flask.views import MethodView
from connection import PgManager

app = Flask(__name__)


class Car_Rental_API(MethodView):

    
    def __init__(self):
        self.db_manager = PgManager(
            db_name="postgres",
            user="postgres",
            password="postgres",
            host="localhost"
        )
    

    def post(self, option):

        try:
            data = request.json

            if option == "drivers":

                driver_key_list = self.valid_lists("driver_key_list")
                driver_status_valid_options = self.valid_lists("driver_status_valid_options")
            

                missing_fields = driver_key_list - data.keys()
    
                if  not driver_key_list.issubset(data.keys()):
                    return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
                

                if not data["driver_status"].upper() in driver_status_valid_options:
                    return jsonify({"error": "Invalid driver status", "Valid Status": driver_status_valid_options}), 400
                        

                self.db_manager.execute_query(
                    """
                    INSERT INTO lyfter_car_rental.drivers (full_name, email, username, password, birth_date, driver_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    data["full_name"].upper(), 
                    data["email"].lower(),
                    data["username"], 
                    data["password"], 
                    data["birth_date"],
                    data["driver_status"].upper()
                )

                return jsonify({"message": "Driver added successfully"}), 201
#-------------------------------------------------------------------------------------------------------------------         
   
            if  option == "vehicles":

                vehicles__key_list = self.valid_lists("vehicles__key_list")
                vehicles_status_valid_options = self.valid_lists("vehicles_status_valid_options")
            

                missing_fields = vehicles__key_list - data.keys()
    
                if  not vehicles__key_list.issubset(data.keys()):
                    return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
                

                if not data["vehicle_status"].upper() in vehicles_status_valid_options:
                    return jsonify({"error": "Invalid vehicle status", "Valid Status": vehicles_status_valid_options}), 400
                        

                self.db_manager.execute_query(
                    """
                    INSERT INTO lyfter_car_rental.vehicles ("brand","model", "manufacture_year","vehicle_status")
                    VALUES (%s, %s, %s, %s)
                    """,
                    data["brand"].upper(), 
                    data["model"].upper(),
                    data["manufacture_year"], 
                    data["vehicle_status"].upper()
                )

                return jsonify({"message": "Vehicle added successfully"}), 201
            
 #----------------------------------------------------------------------------------------------------------------------------------


            if  option == "reservations":

                reservation__key_list = self.valid_lists("reservation__key_list")
                reservation_status_valid_options = self.valid_lists("reservation_status_valid_options")

                missing_fields = reservation__key_list - data.keys()
    
                if  not reservation__key_list.issubset(data.keys()):
                    return jsonify({"error": "Missing required fields", "missing": list(missing_fields)}), 400
                

                if not data["reservation_status"].upper() in reservation_status_valid_options:
                    return jsonify({"error": "Invalid reservation status", "Valid Status": reservation_status_valid_options}), 400

                vehicle_status_for_reservation = self.db_manager.execute_query(
                        """
                        SELECT vehicle_status FROM lyfter_car_rental.vehicles WHERE id = %s
                        """,
                        data["vehicle"], 
                        )
                
                if vehicle_status_for_reservation is not None and vehicle_status_for_reservation[0][0] == "DISABLED":
                    return jsonify({"error": "The requested vehicle is DISABLED",}), 400
                

                driver_status_for_reservation = self.db_manager.execute_query(
                        """
                        SELECT driver_status FROM lyfter_car_rental.drivers WHERE id = %s
                        """,
                        data["driver"], 
                        )
                
                if driver_status_for_reservation is not None and driver_status_for_reservation[0][0] == "DELINQUET":
                    return jsonify({"error": "The requested driver is DELINQUET",}), 400        

                self.db_manager.execute_query(
                    """
                    INSERT INTO lyfter_car_rental.reservations ("driver","vehicle", "reservation_date","reservation_status")
                    VALUES (%s, %s, %s, %s)
                    """,
                    data["driver"], 
                    data["vehicle"],
                    data["reservation_date"], 
                    data["reservation_status"].upper()
                )

                return jsonify({"message": "Reservation added successfully"}), 201           
            

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
 #----------------------------------------------------------------------------------------------------------------------------------

    def put(self, option):

        data = request.json

        try:

            if option == "drivers":

                driver_status_valid_options = self.valid_lists("driver_status_valid_options")

                if not data["driver_status"].upper() in driver_status_valid_options:
                    return jsonify({"error": "Invalid reservation status", "Valid Status": driver_status_valid_options}), 400
                
                self.id_validation(option, data)

                self.db_manager.execute_query(
                
                    """
                    UPDATE  lyfter_car_rental.drivers SET driver_status= %s  WHERE id = %s
                    """,
                    
                    data["driver_status"].upper(),
                    data["id"]
                )

                return jsonify({"message": "Driver status changed successfully"}), 201
            
#----------------------------------------------------------------------------------------------------------------------------------


            if option == "vehicles":

                vehicles_status_valid_options = self.valid_lists("vehicles_status_valid_options")

                if not data["vehicle_status"].upper() in vehicles_status_valid_options:
                    return jsonify({"error": "Invalid reservation status", "Valid Status": vehicles_status_valid_options}), 400
                
                self.id_validation(option, data)

                self.db_manager.execute_query(
                
                    """
                    UPDATE  lyfter_car_rental.vehicles SET vehicle_status= %s  WHERE id = %s
                    """,
                    
                    data["vehicle_status"].upper(),
                    data["id"]
                )

                return jsonify({"message": "Vehicle status changed successfully"}), 201
            
 #----------------------------------------------------------------------------------------------------------------------------------

            if option == "reservations":

                reservation_status_valid_options = self.valid_lists("reservation_status_valid_options")

                if  not data["reservation_status"].upper() in reservation_status_valid_options:
                    return jsonify({"error": "Invalid reservation status", "Valid Status": reservation_status_valid_options}), 400

                self.id_validation(option, data)

                self.db_manager.execute_query(
                
                    """
                    UPDATE  lyfter_car_rental.reservations SET reservation_status= %s  WHERE id = %s
                    """,
                    
                    data["reservation_status"].upper(),
                    data["id"]
                )

                return jsonify({"message": "Reservation status changed successfully"}), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

 #----------------------------------------------------------------------------------------------------------------------------------


    def get(self, action):

        try:
            
            data = request.json
            table_name = data["table_name"]
            parametro= f"{table_name}_key_list"

            tables_names_valid_options= self.valid_lists("tables_names_valid_options")
            table_key_list = self.valid_lists(parametro)
            print(f"{table_name}_key_list")
            print(table_key_list)

            if action == "all":

                print()

                if not data["table_name"].lower() in tables_names_valid_options:
                    return jsonify({"error": "Invalid table name ", "Valid table name": tables_names_valid_options}), 400
    
                request_data=self.db_manager.execute_query(
                
                    f"""
                    SELECT * FROM lyfter_car_rental.{table_name}
                    """
                )
                
                return jsonify({"message": request_data }), 201

            if action == "filter":
                
#need to add here a conditional to verify the 3 keys.

                filter_by = data["filter_by"]

                if not data["table_name"].lower() in tables_names_valid_options:
                    return jsonify({"error": "Invalid table name ", "Valid table name": tables_names_valid_options}), 400
                
                if not data["filter_by"].lower() in table_key_list:
                    return jsonify({"error": "Invalid filters type ", "Valid filters types" : table_key_list}), 400

                request_data=self.db_manager.execute_query(
                
                    """
                    SELECT * FROM lyfter_car_rental.{0} WHERE {1} = %s
                    """.
                    format(table_name, filter_by), data["filter"]
                )

                
                return jsonify({"message": request_data }), 201

        except Exception as e:
            return jsonify({"error":str(e)}), 500


    def id_validation(self, option, data):  
        try:
            option_data = self.db_manager.execute_query(

                f"""
                SELECT id FROM lyfter_car_rental.{option}
                """
                )
                    

            if  not data["id"] in option_data[0] :
                print("estoy acá")
                return jsonify({f"error": f"Not id found in {option}"}), 400    # this line is no running  
            
        except Exception as e:
            return jsonify({"error":str(e)}), 500  
                

    def valid_lists(self, key):

        valid_lists={

            "drivers_key_list" : ["full_name","email", "username","password", "driver_status" ,"birth_date"],
            "drivers_status_valid_options" : ["PENDING PAYMENT","PAID","DELINQUET"],
            "vehicles_key_list" : ["brand","model", "manufacture_year","vehicle_status"],
            "vehicles_status_valid_options" : ["AVAILABLE","RENTED","DISABLED"],
            "reservation_key_list" : ["driver","vehicle", "reservation_date","reservation_status"],
            "reservation_status_valid_options" : ["FINISHED","IN PROGRESS","CANCELED"],
            "tables_names_valid_options" : ["drivers","vehicles","reservations"]
        }

        return valid_lists.get(key, set()) 
                            

task_view = Car_Rental_API.as_view('task')
app.add_url_rule('/add/<string:option>', view_func=task_view, methods=['POST'])
app.add_url_rule('/modify/<string:option>', view_func=task_view, methods=['PUT'])
app.add_url_rule('/get/<string:action>', view_func=task_view, methods=['GET'])


if __name__ == "__main__":
    app.run(host="localhost", debug=True)