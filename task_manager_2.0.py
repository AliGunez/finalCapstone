import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Task list to store the task inputs

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

# Start the program by asking the user for inputs (only admin login will work at first)

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Defining a function to register a new user

def reg_user():
    new_username = input("New Username: ")

    if new_username in username_password:
        print("Username already exists, please try a different username.")
        return
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    else:
        print("Passwords do not match")

# Defining the function to add a new task for a user

def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    with open("tasks.txt", "w") as task_file:
        task_data = []
        for task in task_list:
            task_data.append(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}")
        task_file.write("\n".join(task_data))

    print("Task added successfully!")

# Defining the function to list the tasks when needed

def list_tasks(username=None):
    filtered_tasks = task_list if username is None else [task for task in task_list if task['username'] == username]

    if not filtered_tasks:
        print("No tasks found.")
    else:
        for idx, task in enumerate(filtered_tasks):
            print(f"{idx}: {task['title']} - {task['description']} - Due: {task['due_date'].strftime(DATETIME_STRING_FORMAT)} - Completed: {'Yes' if task['completed'] else 'No'}")

    return filtered_tasks

# Defining a function that lists the task as completed

def mark_complete(task_title):
    found = False
    for task in task_list:
        if task["title"] == task_title:
            task["completed"] = True
            found = True
            break

    if not found:
        print("No task found with that title")
        return

    with open("tasks.txt", "w") as task_file:
        task_data = []
        for task in task_list:
            task_data.append(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}")
        task_file.write("\n".join(task_data))

    print("Task marked as complete")

# Defining a function to generate the reports

def generate_reports():
    today = date.today()

    # Calculate task statistics
    total_tasks = len(task_list)
    completed_tasks = len([t for t in task_list if t["completed"]])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = len([t for t in task_list if not t["completed"] and t["due_date"].date() < today])
    perc_incomplete = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    perc_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Write task_overview.txt
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(f"Total tasks: {total_tasks}\n")
        task_overview.write(f"Completed tasks: {completed_tasks}\n")
        task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview.write(f"Percentage of tasks incomplete: {perc_incomplete:.2f}%\n")
        task_overview.write(f"Percentage of tasks overdue: {perc_overdue:.2f}%\n")

    # Calculate user statistics
    total_users = len(username_password)
    user_stats = {}
    for task in task_list:
        user = task["username"]
        if user not in user_stats:
            user_stats[user] = {"total": 0, "completed": 0, "overdue": 0}
        user_stats[user]["total"] += 1
        if task["completed"]:
            user_stats[user]["completed"] += 1
        elif task["due_date"].date() < today:
            user_stats[user]["overdue"] += 1

    # Write user_overview.txt
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(f"Total users: {total_users}\n")
        user_overview.write(f"Total tasks: {total_tasks}\n\n")
        for user, stats in user_stats.items():
            user_overview.write(f"{user}:\n")
            user_perc_total = (stats["total"] / total_tasks) * 100 if total_tasks > 0 else 0
            user_perc_completed = (stats["completed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            user_perc_incomplete = 100 - user_perc_completed
            user_perc_overdue = (stats["overdue"] / stats["total"]) * 100 if stats["total"] > 0 else 0

            user_overview.write(f"Total tasks assigned: {stats['total']}\n")
            user_overview.write(f"Percentage of all tasks: {user_perc_total:.2f}%\n")
            user_overview.write(f"Percentage of tasks completed: {user_perc_completed:.2f}%\n")
            user_overview.write(f"Percentage of tasks incomplete: {user_perc_incomplete:.2f}%\n")
            user_overview.write(f"Percentage of tasks overdue: {user_perc_overdue:.2f}%\n\n")

# Defining a function to display the statistics of the tasks and users

def display_statistics():
    
    with open("task_overview.txt", "r") as task_file:
        task_content = task_file.read()
    with open("user_overview.txt", "r") as user_file:
        user_content = user_file.read()

    # Print the contents of both files
    print("Task Overview:\n", task_content)
    print("User Overview:\n", user_content)


# Continuation of the program

while True:
    print("MENU")
    print("r: Register user")
    print("a: Add task")
    print("va: View all tasks")
    print("vm: View my tasks")
    print("gr: Generate reports")
    print("ds: Display statistics")
    print("e: Exit")

    choice = input("Enter your choice: ")

    if choice == "r":
        if curr_user == "admin":
         reg_user()
        else:
            print("Sorry only an admin can register a new user")
    elif choice == "a":
        add_task()
    elif choice == "va":
        list_tasks()
    elif choice == "vm":
        filtered_tasks = list_tasks(username=curr_user)
        task_choice = int(input("Enter the task number to select a task or -1 to return to the main menu: "))
        if task_choice != -1:
            selected_task = filtered_tasks[task_choice]
            task_title = selected_task['title']
            action_choice = input("Enter 'c' to mark the task as complete, 'e' to edit the task, or 'm' to return to the main menu: ")
            if action_choice == 'c':
                mark_complete(task_title)
            elif action_choice == 'e':
                edit_task(task_title)
            elif action_choice == 'm':
                continue
            else:
                print("Invalid choice, please try again")
    elif choice == "gr":
        if curr_user == "admin":
         generate_reports()
        else:
            print("Sorry only an admin can generate reports")
    elif choice == "ds":
        if curr_user == "admin":
         display_statistics()
        else:
            print("Sorry only an admin can display statistics")
    elif choice == "e":
        print("Exiting...")
        break
    else:
        print("Invalid choice, please try again")