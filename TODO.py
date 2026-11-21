class Task:
    def __init__(self, task_id, title):
        self.task_id = task_id
        self.title = title
        self.completed = False


class TodoApp:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    # Add a new task
    def add_task(self):
        title = input("Enter task name: ")

        if title.strip() == "":
            print("Task cannot be empty!")
            return

        task = Task(self.next_id, title)
        self.tasks.append(task)
        self.next_id += 1

        print("Task added successfully!")

    # Remove a task
    def remove_task(self):
        self.display_tasks()

        try:
            task_id = int(input("Enter task ID to remove: "))

            for task in self.tasks:
                if task.task_id == task_id:
                    self.tasks.remove(task)
                    print("Task removed successfully!")
                    return

            print("Task ID not found!")

        except ValueError:
            print("Please enter a valid number!")

    # Mark task as completed
    def mark_completed(self):
        self.display_tasks()

        try:
            task_id = int(input("Enter task ID: "))

            for task in self.tasks:
                if task.task_id == task_id:
                    task.completed = True
                    print("Task marked as completed!")
                    return

            print("Task ID not found!")

        except ValueError:
            print("Please enter a valid number!")

    # Display all tasks
    def display_tasks(self):
        if not self.tasks:
            print("\nNo tasks available!")
            return

        print("\n-------- ALL TASKS --------")

        for task in self.tasks:
            status = "Completed" if task.completed else "Not Completed"

            print("ID:", task.task_id)
            print("Task:", task.title)
            print("Status:", status)
            print("--------------------------")

    # Display pending tasks
    def pending_tasks(self):
        print("\n-------- PENDING TASKS --------")

        found = False

        for task in self.tasks:
            if not task.completed:
                print(task.task_id, "-", task.title)
                found = True

        if not found:
            print("No pending tasks!")

    # Display completed tasks
    def completed_tasks(self):
        print("\n-------- COMPLETED TASKS --------")

        found = False

        for task in self.tasks:
            if task.completed:
                print(task.task_id, "-", task.title)
                found = True

        if not found:
            print("No completed tasks!")


# Main application
app = TodoApp()

while True:
    print("\n===== TO-DO LIST APPLICATION =====")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Completed")
    print("4. Display All Tasks")
    print("5. Display Pending Tasks")
    print("6. Display Completed Tasks")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        app.add_task()

    elif choice == "2":
        app.remove_task()

    elif choice == "3":
        app.mark_completed()

    elif choice == "4":
        app.display_tasks()

    elif choice == "5":
        app.pending_tasks()

    elif choice == "6":
        app.completed_tasks()

    elif choice == "7":
        print("Thank you for using To-Do List Application!")
        break

    else:
        print("Invalid choice! Please try again.")