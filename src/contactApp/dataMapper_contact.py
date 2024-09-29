import psycopg2
from django.conf import settings

class ContactMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_contacts(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM contact")
                all_contacts = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching contacts: {e}")
            all_contacts = []
        finally:
            self.connection.close()

        return all_contacts

    def get_contact_by_id(self, contact_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM contact WHERE id = %s", [contact_id])
                contact = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching contact: {e}")
        finally:
            self.connection.close()

        return contact

    def create_contact(self, position, company_id, user_id, password):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO contact ("position", "companyId", "userId", "password")
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (position, company_id, user_id, password)
            )
            contact_id = cursor.fetchone()[0]
        self.connection.commit()
        return contact_id

    def update_contact(self, contact_id, position, company_id, user_id, password):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE contact
                    SET "position" = %s, "companyId" = %s, "userId" = %s, "password" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (position, company_id, user_id, password, contact_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Contact not found"}
            self.connection.commit()
            return {"success": True, "message": "Contact updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating contact: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_contact(self, contact_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM contact WHERE id = %s", [contact_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Contact not found"}
            self.connection.commit()
            return {"success": True, "message": "Contact deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting contact: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
