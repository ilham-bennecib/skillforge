import psycopg2
from django.conf import settings

class TaskMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_tasks(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM task")
                all_tasks = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching tasks: {e}")
            all_tasks = []
        finally:
            self.connection.close()

        return all_tasks

    def get_task_by_id(self, task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM task WHERE id = %s", [task_id])
                task = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching task: {e}")
        finally:
            self.connection.close()

        return task

    def create_task(self, title, description, date, cfaemployeeId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO task ("title", "description", "date", "cfaemployeeId")
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (title, description, date, cfaemployeeId)
            )
            task_id = cursor.fetchone()[0]
        self.connection.commit()
        return task_id

    def update_task(self, task_id, title, description, date, cfaemployeeId):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE task
                    SET "title" = %s, "description" = %s, "date" = %s, "cfaemployeeId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (title, description, date, cfaemployeeId, task_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Task not found"}
            self.connection.commit()
            return {"success": True, "message": "Task updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating task: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_task(self, task_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM task WHERE id = %s", [task_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Task not found"}
            self.connection.commit()
            return {"success": True, "message": "Task deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting task: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
