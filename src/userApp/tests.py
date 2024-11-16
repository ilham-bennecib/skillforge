import bcrypt

# Mot de passe brut
password = "securepassword"
# Hash extrait de la base de données
db_password = "$2b$12$saltedpasswordhash1"

# Validation du mot de passe
if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
    print("Mot de passe valide")
else:
    print("Mot de passe invalide")