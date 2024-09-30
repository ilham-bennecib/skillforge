import psycopg2
from django.conf import settings

class CertificateMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_certificates(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM certificate")
                all_certificates = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching certificates: {e}")
            all_certificates = []
        finally:
            self.connection.close()

        return all_certificates

    def get_certificate_by_id(self, certificate_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM certificate WHERE id = %s", [certificate_id])
                certificate = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching certificate: {e}")
        finally:
            self.connection.close()

        return certificate

    def create_certificate(self, title, description, date, status, cert_type, level, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO certificate ("title", "description", "date", "status", "type", "level", "studentId")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (title, description, date, status, cert_type, level, student_id)
            )
            certificate_id = cursor.fetchone()[0]
        self.connection.commit()
        return certificate_id

    def update_certificate(self, certificate_id, title, description, date, status, cert_type, level, student_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE certificate
                    SET "title" = %s, "description" = %s, "date" = %s, "status" = %s, "type" = %s, "level" = %s, "studentId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (title, description, date, status, cert_type, level, student_id, certificate_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Certificate not found"}
            self.connection.commit()
            return {"success": True, "message": "Certificate updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating certificate: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_certificate(self, certificate_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM certificate WHERE id = %s", [certificate_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Certificate not found"}
            self.connection.commit()
            return {"success": True, "message": "Certificate deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting certificate: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
