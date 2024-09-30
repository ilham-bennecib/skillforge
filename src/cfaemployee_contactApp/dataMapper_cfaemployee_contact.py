import psycopg2
from django.conf import settings

class CfaEmployeeContactMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_exchanges(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cfaemployee_contact")
                all_exchanges = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching exchanges: {e}")
            all_exchanges = []
        finally:
            self.connection.close()

        return all_exchanges

    def get_exchange_by_id(self, exchange_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cfaemployee_contact WHERE id = %s", [exchange_id])
                exchange = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching exchange: {e}")
        finally:
            self.connection.close()

        return exchange

    def create_exchange(self, cfaemployee_id, contact_id, exchange):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cfaemployee_contact ("cfaemployeeId", "contactId", "exchange")
                VALUES (%s, %s, %s)
                RETURNING id
                """, (cfaemployee_id, contact_id, exchange)
            )
            exchange_id = cursor.fetchone()[0]
        self.connection.commit()
        return exchange_id

    def update_exchange(self, exchange_id, cfaemployee_id, contact_id, exchange):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE cfaemployee_contact
                    SET "cfaemployeeId" = %s, "contactId" = %s, "exchange" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (cfaemployee_id, contact_id, exchange, exchange_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Exchange not found"}
            self.connection.commit()
            return {"success": True, "message": "Exchange updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating exchange: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_exchange(self, exchange_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM cfaemployee_contact WHERE id = %s", [exchange_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Exchange not found"}
            self.connection.commit()
            return {"success": True, "message": "Exchange deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting exchange: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
