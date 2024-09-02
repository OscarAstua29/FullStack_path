import json
from flask import Flask
from flask import request
from flask import jsonify



app = Flask(__name__)

task_list = []
valid_status=['TODO','INPROGRESS', 'COMPLETED']

@app.route("/get", methods = ["GET"])
def get():

    task_list = import_file()
    return task_list


@app.route("/create/<title>/<description>/<status>", methods=["POST"])
def create(title, description, status):

    if not title:
        return jsonify({"error": "NO TITLE, ADD A TITLE"}), 400
    if not description:
        return jsonify({"error": "NO DESCRIPTION, ADD A DESCRIPTION"}), 400
    if not status:
        return jsonify({"error": "NO STATUS, ADD A STATUS"}), 400

    if status not in valid_status:
        return jsonify({"error": "INVALID STATUS, VALID STATUS [TODO, INPROGRESS, COMPLETED]"}), 400

    try:
        task_list = import_file()

        print(f'Actual list: {task_list}')

    
        new_id = 1 if not task_list else max(task['id'] for task in task_list) + 1

        new_task = {
            "id": new_id,
            "title": title,
            "description": description,
            "status": status,
        }

        task_list.append(new_task)
        export_file(task_list)

        return jsonify(task_list), 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500




@app.route("/edit/<id>/<title>/<description>/<status>", methods=["GET", "POST"])
def edit(id, title, description, status):

    if not title:
        return jsonify({"error": "NO TITLE, ADD A TITLE"}), 400
    if not description:
        return jsonify({"error": "NO DESCRIPTION, ADD A DESCRIPTION"}), 400
    if not status:
        return jsonify({"error": "NO STATUS, ADD A STATUS"}), 400

    if status not in valid_status:
        return jsonify({"error": "INVALID STATUS, VALID STATUS [TODO, INPROGRESS, COMPLETED]"}), 400 

    try:

        task_list = import_file()

        for task in task_list:
            if str(task.get('id')) == str(id):
                
                task.update({'id': id, 'title': title, 'description': description, 'status': status})
                break
        else:
            return "Task not found", 404

        
        return jsonify(task_list)

    except Exception as error:
        return str(error), 500


@app.route("/delete/<id>", methods = ["DELETE"])
def delete(id):

    task_list = import_file()
   
    print(task_list)
    new_task_list = [task for task in task_list if str(task.get('id')) != str(id)]
    print(new_task_list)
    export_file(new_task_list)
    return jsonify (new_task_list), 200


def export_file (task_list):
    with open ('task.json','w') as file_w:
        json.dump(task_list,file_w)

def import_file ():
    with open ('task.json','r') as file_r:
        task_list = json.load(file_r)
        return task_list

 

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)