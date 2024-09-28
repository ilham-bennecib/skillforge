import psycopg2
from django.conf import settings
from datetime import datetime

class TrainingMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_trainings(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM training")
                all_trainings = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching trainings: {e}")
            all_trainings = []
        finally:
            self.connection.close()

        return all_trainings

    def get_training_by_id(self, training_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM training WHERE id = %s", [training_id])
                training = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching training: {e}")
        finally:
            self.connection.close()

        return training

    def create_training(self, name, price, start_date, end_date, training_type, directory, field_id, structure_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO training ("name", "price", "startDate", "endDate", "type", "directory", "fieldId", "structureId")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (name, price, start_date, end_date, training_type, directory, field_id, structure_id)
            )
            training_id = cursor.fetchone()[0]
        self.connection.commit()
        return training_id

    def delete_training(self, training_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM training WHERE id = %s", [training_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Training not found"}
            self.connection.commit()
            return {"success": True, "message": "Training deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting training: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        finally:
            if self.connection:
                self.connection.close()

    def update_training(self, training_id, name, price, start_date, end_date, training_type, directory, field_id, structure_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE training
                    SET "name" = %s, "price" = %s, "startDate" = %s, "endDate" = %s, "type" = %s, "directory" = %s, "fieldId" = %s, "structureId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, price, start_date, end_date, training_type, directory, field_id, structure_id, training_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Training not found"}
            self.connection.commit()
            return {"success": True, "message": "Training updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating training: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        finally:
            if self.connection:
                self.connection.close()

