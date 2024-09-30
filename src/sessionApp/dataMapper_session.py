import psycopg2
from django.conf import settings

class SessionMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_sessions(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM session")
                all_sessions = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching sessions: {e}")
            all_sessions = []
        finally:
            self.connection.close()

        return all_sessions

    def get_session_by_id(self, session_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM session WHERE id = %s", [session_id])
                session = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching session: {e}")
        finally:
            self.connection.close()

        return session

    def create_session(self, name, referent, tutor, training_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO session ("name", "referent", "tutor", "trainingId")
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (name, referent, tutor, training_id)
            )
            session_id = cursor.fetchone()[0]
        self.connection.commit()
        return session_id

    def update_session(self, session_id, name, referent, tutor, training_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE session
                    SET "name" = %s, "referent" = %s, "tutor" = %s, "trainingId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, referent, tutor, training_id, session_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Session not found"}
            self.connection.commit()
            return {"success": True, "message": "Session updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating session: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_session(self, session_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM session WHERE id = %s", [session_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Session not found"}
            self.connection.commit()
            return {"success": True, "message": "Session deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting session: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
