import psycopg2
from django.conf import settings

class CfaEmployeeMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_employees(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cfaemployee")
                all_employees = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching CFA employees: {e}")
            all_employees = []
        finally:
            self.connection.close()

        return all_employees

    def get_employee_by_id(self, employee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cfaemployee WHERE id = %s", [employee_id])
                employee = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching CFA employee: {e}")
        finally:
            self.connection.close()

        return employee

    def create_employee(self, position, matricule, password, structureId, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cfaemployee ("position", "matricule", "password", "structureId", "userId")
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """, (position, matricule, password, structureId, user_id)
            )
            employee_id = cursor.fetchone()[0]
        self.connection.commit()
        return employee_id

    def update_employee(self, employee_id, position, matricule, password, structureId, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE cfaemployee
                    SET "position" = %s, "matricule" = %s, "password" = %s, "structureId" = %s, "userId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (position, matricule, password, structureId, user_id, employee_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "CFA Employee not found"}
            self.connection.commit()
            return {"success": True, "message": "CFA Employee updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating CFA employee: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_employee(self, employee_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM cfaemployee WHERE id = %s", [employee_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "CFA Employee not found"}
            self.connection.commit()
            return {"success": True, "message": "CFA Employee deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting CFA employee: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
