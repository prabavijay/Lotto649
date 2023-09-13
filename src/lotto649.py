""" Main entry point of the program
"""
from src.task_manager import TaskManager
from src.service_manager import ServiceManager

if __name__ == '__main__':
    print("----------------------------")
    print("Hello, Welcome to Lotto 6/49!")

taskManager = TaskManager()
user_options = taskManager.user_options

serviceManager = ServiceManager()

while(True):
    print("TASK OPTIONS:")
    for user_option in user_options:
        print(user_option)
    while(True):
        request_id = input("PLEASE ENTER INTEGER FOR THE TASK:\n")
        if request_id.strip() == 'q':
            request_id = 11
            break
        elif request_id.strip().isdigit():
            break

    # get task name
    taskManager.map_request_to_task(request_id)
    print(f'Your Request: {taskManager.task_name}')

    # Exit program
    if taskManager.task_name == "QUIT":
        break

    # Handle other requests
    print("=============== START OF TASK: " + taskManager.task_name + " ===============" + "\n")

    # identify which service(s) to call to perform specific task
    service_name = serviceManager.get_service_name(taskManager.task_name)
    print("=============== END OF TASK: " + taskManager.task_name + " ===============" + "\n")
