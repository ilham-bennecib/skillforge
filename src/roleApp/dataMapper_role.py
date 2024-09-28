import psycopg2
from django.conf import settings

class RoleMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_roles(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM role")
                all_roles = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching roles: {e}")
            all_roles = []
        finally:
            self.connection.close()

        return all_roles

    def get_role_by_id(self, role_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM role WHERE id = %s", [role_id])
                role = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching role: {e}")
        finally:
            self.connection.close()

        return role

    def create_role(self, name, permissions):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO role (name, permissions)
                VALUES (%s, %s)
                RETURNING id
                """, (name, permissions)
            )
            role_id = cursor.fetchone()[0]
        self.connection.commit()
        return role_id

    def update_role(self, role_id, name, permissions):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE role
                    SET "name" = %s, "permissions" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, permissions, role_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Role not found"}
            self.connection.commit()
            return {"success": True, "message": "Role updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating role: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_role(self, role_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM role WHERE id = %s", [role_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Role not found"}
            self.connection.commit()
            return {"success": True, "message": "Role deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting role: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
