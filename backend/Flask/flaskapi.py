# This file was developed in Flash handling request from the body.



from flask import Flask
from flask import request, jsonify
import json
import os


app = Flask(__name__)

valid_status = ['TODO', 'INPROGRESS', 'COMPLETED']

@app.route("/get", methods = ["GET"])
def get():

    task_list = import_file()
    return jsonify (task_list), 201

@app.route("/create", methods=["POST"])
def create():

    task_list = import_file()
    id_repeated = False
    task_qty = 1

    id = request.json.get("id")
    title = request.json.get("title")
    description = request.json.get("description")
    status = request.json.get("status")
    
    for i in task_list:
        id_in_task_list = i["id"]
        if id == id_in_task_list:
            id_repeated = True
            break
        else:
            id_repeated = False

    for i in task_list:
        if task_qty < i["id"]:
            for x in task_list:
                if task_qty == x["id"]:
                    pass

                else:
                  break
        else:
            task_qty += 1
        

    if id_repeated == True:
        return jsonify({"error": f"ID REPEATED, PLEASE TRY WITH {task_qty}"}), 400
    if not title:
        return jsonify({"error": "NO TITLE, ADD A TITLE"}), 400
    if not description:
        return jsonify({"error": "NO DESCRIPTION, ADD A DESCRIPTION"}), 400
    if not status:
        return jsonify({"error": "NO STATUS, ADD A STATUS"}), 400

    if status not in valid_status:
        return jsonify({"error": "INVALID STATUS, VALID STATUS [TODO, INPROGRESS, COMPLETED]"}), 400

    try:

        print(f'Actual list: {task_list}')

        new_task = {
            "id": id,
            "title": title,
            "description": description,
            "status": status,
        }

        task_list.append(new_task)
        export_file(task_list)
        return jsonify(task_list), 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/edit", methods=["GET", "POST"])
def edit():

    task_list = import_file()
    id_repeated = False
    task_qty = 1

    id = request.json.get("id")
    title = request.json.get("title")
    description = request.json.get("description")
    status = request.json.get("status")

    list_of_id = []

    for i in task_list:
        list_of_id.append(i["id"])
       
            
    if id in list_of_id:
        pass
    else:        
        return jsonify({f"error": f"NOT ID IN LIST, PLEASE TRY ANOTHER {list_of_id}"}), 400
    

    for i in task_list:
        if task_qty < i["id"]:
            for x in task_list:
                if task_qty == x["id"]:
                    pass

                else:
                  break
        else:
            task_qty += 1
        
    
    if not title:
        return jsonify({"error": "NO TITLE, ADD A TITLE"}), 400
    if not description:
        return jsonify({"error": "NO DESCRIPTION, ADD A DESCRIPTION"}), 400
    if not status:
        return jsonify({"error": "NO STATUS, ADD A STATUS"}), 400

    if status not in valid_status:
        return jsonify({"error": "INVALID STATUS, VALID STATUS [TODO, INPROGRESS, COMPLETED]"}), 400

    try:

        for task in task_list:
            if str(task.get('id')) == str(id):
                
                task.update({'id': id, 'title': title, 'description': description, 'status': status})
                break
        else:
            return "Task not found", 404

        
        return jsonify(task_list)

    except Exception as error:
        return str(error), 500

@app.route("/delete", methods = ["DELETE"])
def delete():
    id = request.json.get("id")
    print(id)
    task_list = import_file()
    list_of_id = []

    for i in task_list:
        list_of_id.append(i["id"])
       
            
    if id in list_of_id:
        pass
    else:        
        return jsonify({f"error": f"NOT ID IN LIST, PLEASE TRY ANOTHER {list_of_id}"}), 400
   
    new_task_list = [task for task in task_list if str(task.get('id')) != str(id)]
    export_file(new_task_list)
    return jsonify (new_task_list), 200

def export_file (task_list):
    with open ('task.json','w') as file_w:
        json.dump(task_list,file_w)

def import_file ():
    if not os.path.exists('task.json') or os.stat('task.json').st_size == 0:
        return []

    with open('task.json', 'r') as file_r:
        try:
            task_list = json.load(file_r)
            organized_task_list = sorted(task_list, key=lambda x: x['id'])
            return organized_task_list
        except json.JSONDecodeError:
            return []

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)