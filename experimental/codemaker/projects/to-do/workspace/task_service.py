from typing import List
from .task import Task
from .database import Database

class TaskService:
    def __init__(self, db: Database):
        self.db = db

    def create_task(self, task: Task):
        query = """
        INSERT INTO tasks (title, description, category, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        params = (task.title, task.description, task.category, task.status)
        return self.db.execute_query(query, params)

    def get_task(self, task_id: int) -> Task:
        query = "SELECT * FROM tasks WHERE id = %s"
        params = (task_id,)
        result = self.db.fetch_results(query, params)
        if result:
            return Task(*result[0])
        else:
            return None

    def update_task(self, task: Task):
        query = """
        UPDATE tasks
        SET title = %s, description = %s, category = %s, status = %s
        WHERE id = %s
        """
        params = (task.title, task.description, task.category, task.status, task.id)
        self.db.execute_query(query, params)

    def delete_task(self, task_id: int):
        query = "DELETE FROM tasks WHERE id = %s"
        params = (task_id,)
        self.db.execute_query(query, params)

    def get_all_tasks(self) -> List[Task]:
        query = "SELECT * FROM tasks"
        results = self.db.fetch_results(query)
        return [Task(*result) for result in results]
