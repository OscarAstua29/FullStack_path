task_list = [1,2,3,4,6,7]
task_qty = 1

for i in task_list:
        if task_qty < i:
            for x in task_list:
                if task_qty == x:
                    pass

                else:
                  break
        else:
            task_qty += 1

print(f'{task_qty}, {i}')        