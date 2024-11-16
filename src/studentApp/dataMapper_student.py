import psycopg2
from django.conf import settings

class StudentMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_students(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                               SELECT 
                    student."id",
                    customer."firstName",
                    customer."lastName"
                FROM 
                    student
                JOIN 
                    candidate ON student."candidateId" = candidate."id"
                JOIN 
                    customer ON candidate."userId" = customer."id"
                               """)
                all_students = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching students: {e}")
            all_students = []
        finally:
            self.connection.close()

        return all_students

    def get_student_by_id(self, student_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        student."id" AS student_id,
                        student."createdAt" AS student_created_at,
                        student."updatedAt" AS student_updated_at,
                        candidate."lastDiploma",
                        candidate."dateOfBirth",
                        candidate."address",
                        customer."lastName",
                        customer."firstName",
                        customer."email",
                        customer."phone",
                        customer."directory",
                        customer."roleId",
                        company."id",
                        structure."name",
                        session."name",
                        training."name"
                    FROM 
                        student
                    JOIN 
                        candidate ON student."candidateId" = candidate."id"
                    JOIN 
                        customer ON candidate."userId" = customer."id"
                    JOIN 
                        company ON company."id"=student."companyId"
                    JOIN 
                        structure ON structure."id" = company."structureId"
                    JOIN 
                        session ON session."id"=student."sessionId"
                    JOIN 
                        training ON training."id" = session."trainingId"
                    WHERE 
                        student.id = %s
                """, [student_id])
                
                student = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching student: {e}")
            student = None
        finally:
            self.connection.close()
        
        return student


    def create_student(self, company_id, session_id, candidate_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student ( "companyId", "sessionId", "candidateId")
                VALUES ( %s, %s, %s)
                RETURNING id
                """, ( company_id, session_id, candidate_id)
            )
            student_id = cursor.fetchone()[0]
        self.connection.commit()
        return student_id

    def delete_student(self, student_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM student WHERE id = %s", [student_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Student not found"}
            self.connection.commit()
            return {"success": True, "message": "Student deleted successfully"}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {str(e)}"}

    def update_student(self, student_id, company_id, session_id, candidate_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE student
                    SET  "companyId" = %s, "sessionId" = %s, "candidateId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, ( company_id, session_id, candidate_id, student_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Student not found"}
            self.connection.commit()
            return {"success": True, "message": "Student updated successfully"}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
