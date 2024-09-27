import psycopg2
from django.conf import settings
from datetime import datetime 

class StructureMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_structures(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM structure")
                all_structures = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching structures: {e}")
            all_structures = []
        finally:
            self.connection.close()

        return all_structures
    
    def get_structure_by_id(self, structure_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM structure WHERE id = %s", [structure_id])
                structure = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching structure: {e}")
        finally:
            self.connection.close()

        return structure
    
    def create_structure(self, name, address, siret, description, directory, fieldId):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO structure ("name", "address", "siret", "description", "directory", "fieldId")
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (name, address, siret, description, directory, fieldId)
            )
            structure_id = cursor.fetchone()[0]
        self.connection.commit()
        return structure_id

    def delete_structure(self, structure_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM structure WHERE id = %s", [structure_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Structure not found"}
            self.connection.commit()
            return {"success": True, "message": "Structure deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting structure: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        finally:
            if self.connection:
                self.connection.close()

    def update_structure(self, structure_id, name, address, siret, description, directory, fieldId):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE structure
                    SET "name" = %s, "address" = %s, "siret" = %s, "description" = %s, "directory" = %s, "fieldId" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (name, address, siret, description, directory, fieldId, structure_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Structure not found"}
            self.connection.commit()
            return {"success": True, "message": "Structure updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating structure: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        finally:
            if self.connection:
                self.connection.close()
