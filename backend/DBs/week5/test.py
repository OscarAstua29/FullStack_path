#ignore this file it is just for tests

self= 2
data=[0]
jsonify=1

vehicles_table = self.db_manager.execute_query(

                        """
                        SELECT * FROM lyfter_car_rental.vehicles
                        """
                    )
        
def borrar_esto():
    if  not data["id"] in vehicles_table :
        return jsonify({"error": "Not id found in vehicles"}), 400