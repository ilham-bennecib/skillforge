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


    def delete_user(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                # Exécuter la requête de suppression
                cursor.execute("DELETE FROM customer WHERE id = %s", [user_id])
                
                # Vérifier si la suppression a affecté une ligne
                if cursor.rowcount == 0:
                    return {"success": False, "message": "User not found"}

            # Valider la transaction
            self.connection.commit()
            return {"success": True, "message": "User deleted successfully"}
        
        except psycopg2.Error as e:
            # Gestion des erreurs liées à la base de données
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        
        finally:
            # Fermer la connexion proprement si elle n'a pas déjà été fermée
            if self.connection:
                self.connection.close()
                print("Connexion à la base de données fermée.")


    def update_user(self, user_id, last_name, first_name, email, phone, directory, role_id):
        try:
            with self.connection.cursor() as cursor:
                #verifiactaion de l'existance du user
                cursor.execute("SELECT * FROM customer WHERE id = %s", [user_id])
                user = cursor.fetchone()
                if user is None:
                    return {"success": False, "message": "User not found"}
                
                #sinon , mise à jour des informations utilisateurs
                cursor.execute(
                    """
                    UPDATE customer
                    SET "lastName" = %s, "firstName" = %s, "email" = %s, "phone" = %s, "directory" = %s, "roleId" = %s
                    WHERE id = %s
                    """,
                    (last_name, first_name, email, phone, directory, role_id, user_id)
                )
                if cursor.rowcount == 0:  # Vérifie si l'utilisateur a été trouvé et mis à jour
                    return {"error": "User not found"}  # Retourne une erreur si aucun utilisateur n'est trouvé

            #valide la transaction
            self.connection.commit()  # Commiter les changements
            return {"success": True, "message": "User updated successfully"}
        
        except psycopg2.Error as e:
            # Gestion des erreurs liées à la base de données
            print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
        
        finally:
            #fermer la connexion 
            if self.connection:
                self.connection.close()
                print("Connexion à la base de données fermée.")
