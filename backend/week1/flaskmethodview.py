# This file was developed in Flash using methodView.

import json
from flask import Flask
from flask.views import MethodView
from flask import request
from flask import jsonify
import os

app = Flask(__name__)

class Task(MethodView):

    def get(self):
        task_list = import_file()
        print(task_list)
        if task_list is None:
            return jsonify({"error": "No tasks found or file does not exist"}), 404
        return jsonify(task_list), 200

    def post(self):

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

           
    
    def put(self):
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        
        task_id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')

        if not title:
            return jsonify({"error": "NO TITLE, ADD A TITLE"}), 400
        if not description:
            return jsonify({"error": "NO DESCRIPTION, ADD A DESCRIPTION"}), 400
        if not status:
            return jsonify({"error": "NO STATUS, ADD A STATUS"}), 400

        if status not in valid_status:
            return jsonify({"error": "INVALID STATUS, VALID STATUS [TODO, INPROGRESS, COMPLETED]"}), 400 

        try:

            task_list = import_file() or []

            for task in task_list:
                if str(task.get('id')) == str(id):
                
                    task.update({'id': id, 'title': title, 'description': description, 'status': status})
                    break
            else:
                return "Task not found", 404

        
            return jsonify(task_list)

        except Exception as error:
            return str(error), 500
        
    def delete(self):
        pass

task_list = []
valid_status=['TODO','INPROGRESS', 'COMPLETED']

def export_file (task_list):
    try:
        with open('task.json', 'w') as file_w:
            json.dump(task_list, file_w)
    except Exception as error:
        print(f"An error occurred while writing to file: {error}")

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

app.add_url_rule('/taskapp', view_func=Task.as_view('task'))

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)