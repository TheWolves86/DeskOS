name = input("Pls Enter ur name: ")
tasks = []
print(f"Hello {name}")
def addTasks():
    ask = input("Do you want to add taks(y/n): ")
    if ask == "y":
        num_of_task = int(input("Enter the number of tasks you wanna add: "))
        for task in range(num_of_task):
            task_name = input(f"Enter the name of task {task+1}: ")
            tasks.append(task_name)
    elif ask == "n":
        print("Okay byee")
    else:
        print("Wrong input,kindly restart the program")

def printTasks():
    ask = input("Do you want to see the tasks(y/n): ")
    if ask == "y":
        for task in tasks:
            print(task)
    elif ask == "n":
        print("Okay byee")
    else:
        print("Wrong input,kindly restart the program")

def checkList():
    ask = input("Do you want to see if the list have a task or not(y/n): ")
    if ask == "y":
        if len(tasks) == 0:
            print("The list is empty")
        else:
            print(f"The list has {len(tasks)} tasks")
    elif ask == "n":
        print("Okay byee")
    else:
        print("Wrong input,kindly restart the program")

addTasks()
print(f"Hello {name}")
printTasks()
checkList()