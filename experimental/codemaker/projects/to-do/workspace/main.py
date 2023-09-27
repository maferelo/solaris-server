from .database import Database
from .task_service import TaskService
from .task import Task

def main():
    db = Database('todo_db', 'user', 'password')
    db.connect()

    task_service = TaskService(db)

    # Create a task
    task = Task(None, 'Buy groceries', 'Buy milk and eggs', 'Shopping', 'Pending')
    task_id = task_service.create_task(task)
    print(f'Task created with ID: {task_id}')

    # Get a task
    task = task_service.get_task(task_id)
    print(f'Got task: {task}')

    # Update a task
    task.status = 'Done'
    task_service.update_task(task)
    print(f'Task updated: {task}')

    # Delete a task
    task_service.delete_task(task_id)
    print(f'Task deleted with ID: {task_id}')

    # Get all tasks
    tasks = task_service.get_all_tasks()
    print(f'All tasks: {tasks}')

    db.disconnect()

if __name__ == '__main__':
    main()
