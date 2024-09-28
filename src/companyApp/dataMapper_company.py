import psycopg2
from django.conf import settings

class CompanyMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_companies(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM company")
                all_companies = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching companies: {e}")
            all_companies = []
        finally:
            self.connection.close()

        return all_companies

    def get_company_by_id(self, company_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM company WHERE id = %s", [company_id])
                company = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching company: {e}")
        finally:
            self.connection.close()
        return company

    def create_company(self, status, structure_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO company ("status", "structureId")
                VALUES (%s, %s)
                RETURNING id
                """, (status, structure_id)
            )
            company_id = cursor.fetchone()[0]
        self.connection.commit()
        return company_id

    def delete_company(self, company_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM company WHERE id = %s", [company_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Company not found"}
            self.connection.commit()
            return {"success": True, "message": "Company deleted successfully"}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {str(e)}"}

    def update_company(self, company_id, status, structure_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE company
                    SET "status" = %s, "structureId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (status, structure_id, company_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Company not found"}
            self.connection.commit()
            return {"success": True, "message": "Company updated successfully"}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
