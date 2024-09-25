import psycopg2
from django.conf import settings

class UserMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_users(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer")
                all_users = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            all_users = []
        finally:
            self.connection.close()

        return all_users
    
    def get_user_by_id(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE id = %s", [user_id])
                user = cursor.fetchone()
                print (user)
        except psycopg2.Error as e:
            # Gestion des erreurs liées à la base de données
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")

        finally:
            # Fermer la connexion proprement
            self.connection.close()
            print("Connexion à la base de données fermée.")

        return user
        

    def create_user(self, last_name, first_name, email, phone, directory, role_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer ("lastName", "firstName", "email", "phone", "directory", "roleId")
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (last_name, first_name, email, phone, directory, role_id)
            )
            user_id = cursor.fetchone()[0]
        self.connection.commit()
        return user_id

