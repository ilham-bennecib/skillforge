import psycopg2
from django.conf import settings

class FieldMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_fields(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM field")
                all_fields = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching fields: {e}")
            all_fields = []
        finally:
            self.connection.close()

        return all_fields

    def get_field_by_id(self, field_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM field WHERE id = %s", [field_id])
                field = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching field: {e}")
        finally:
            self.connection.close()

        return field

    def create_field(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO field ("name")
                VALUES (%s)
                RETURNING id
                """, (name,)
            )
            field_id = cursor.fetchone()[0]
        self.connection.commit()
        return field_id

    def update_field(self, field_id, name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE field
                    SET "name" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, field_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Field not found"}
            self.connection.commit()
            return {"success": True, "message": "Field updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating field: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_field(self, field_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM field WHERE id = %s", [field_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Field not found"}
            self.connection.commit()
            return {"success": True, "message": "Field deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting field: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
