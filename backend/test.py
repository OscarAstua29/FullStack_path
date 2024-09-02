import json

id_to_delete = 3
def import_file ():
    with open ('task.json','r') as file_r:
        task_list = json.load(file_r)
        return task_list

task_list = import_file()

new_task_list = [task for task in task_list if task.get('id') != id_to_delete]


print (new_task_list)