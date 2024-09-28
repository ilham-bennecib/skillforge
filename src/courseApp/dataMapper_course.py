import psycopg2
from django.conf import settings

class CourseMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_courses(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM course")
                all_courses = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching courses: {e}")
            all_courses = []
        finally:
            self.connection.close()

        return all_courses

    def get_course_by_id(self, course_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM course WHERE id = %s", [course_id])
                course = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching course: {e}")
        finally:
            self.connection.close()

        return course

    def create_course(self, name, trainer):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO course ("name", "trainer")
                VALUES (%s, %s)
                RETURNING id
                """, (name, trainer)
            )
            course_id = cursor.fetchone()[0]
        self.connection.commit()
        return course_id

    def update_course(self, course_id, name, trainer):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE course
                    SET "name" = %s, "trainer" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, trainer, course_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Course not found"}
            self.connection.commit()
            return {"success": True, "message": "Course updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating course: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_course(self, course_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM course WHERE id = %s", [course_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Course not found"}
            self.connection.commit()
            return {"success": True, "message": "Course deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting course: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
