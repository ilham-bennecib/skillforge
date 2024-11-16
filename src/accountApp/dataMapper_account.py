import psycopg2
from django.conf import settings

class AccountMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_user_by_email(self, email):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
                result = cursor.fetchone()
                if result:
                # Convertir le tuple en dictionnaire
                    columns = [desc[0] for desc in cursor.description]
                    user = dict(zip(columns, result))
                    print(user)
                    return user
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None

    def create_user(self, last_name, first_name, email, hashed_password, phone, directory, role_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer ("lastName", "firstName", "email", "password", "phone", "directory", "roleId")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (last_name, first_name, email, hashed_password, phone, directory, role_id)
            )
            user_id = cursor.fetchone()[0]
        self.connection.commit()
        return user_id
