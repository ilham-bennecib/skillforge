import psycopg2
from django.conf import settings

class EventMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_events(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM event")
                all_events = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching events: {e}")
            all_events = []
        finally:
            self.connection.close()

        return all_events

    def get_event_by_id(self, event_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM event WHERE id = %s", [event_id])
                event = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching event: {e}")
        finally:
            self.connection.close()

        return event

    def create_event(self, title, description, date, start_time, end_time, cfaemployeeId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO event ("title", "description", "date", "startTime", "endTime", "cfaemployeeId")
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (title, description, date, start_time, end_time, cfaemployeeId)
            )
            event_id = cursor.fetchone()[0]
        self.connection.commit()
        return event_id

    def update_event(self, event_id, title, description, date, start_time, end_time, cfaemployeeId):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE event
                    SET "title" = %s, "description" = %s, "date" = %s, "startTime" = %s, "endTime" = %s, "cfaemployeeId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (title, description, date, start_time, end_time, cfaemployeeId, event_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Event not found"}
            self.connection.commit()
            return {"success": True, "message": "Event updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating event: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_event(self, event_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM event WHERE id = %s", [event_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Event not found"}
            self.connection.commit()
            return {"success": True, "message": "Event deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting event: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
