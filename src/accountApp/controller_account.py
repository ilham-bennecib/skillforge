from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta, timezone
from django.conf import settings
import jwt
from datetime import datetime, timedelta
import bcrypt
import json
from .dataMapper_account import AccountMapper
from userApp.form import UserForm
from .token_validation import token_required

#token
def generate_tokens_for_user(user):
    # Secret pour signer les tokens
    secret = settings.SECRET_KEY
    
    
    # Temps d'expiration
    access_exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    refresh_exp = datetime.now(timezone.utc) + timedelta(days=7)

    # Payload pour les tokens
    access_payload = {
        'user_id': user['id'],
        'role_id': user['roleId'],
        'exp': access_exp,
        'type': 'access'
    }

    refresh_payload = {
        'user_id': user['id'],
        'role_id': user['roleId'],
        'exp': refresh_exp,
        'type': 'refresh'
    }

    # Générer les tokens
    access_token = jwt.encode(access_payload, secret, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, secret, algorithm='HS256')

  
    return {
        'access': access_token,
        'refresh': refresh_token
    }

@csrf_exempt

def login_user(request):
    if request.method == 'POST':
        try:
            # Récupérer les données JSON
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Vérifier que l'email et le mot de passe sont présents
            if not email or not password:
                return JsonResponse({'error': 'Email et mot de passe requis'}, status=400)

            # Récupérer l'utilisateur par email via le dataMapper
            account_mapper = AccountMapper()
            user = account_mapper.get_user_by_email(email)

            # Vérifier si l'utilisateur existe
            if not user:
                return JsonResponse({'error': 'Utilisateur introuvable'}, status=404)
            
             # Vérification de l'existence du mot de passe
            db_password = user.get('password')
            print(f"Hash récupéré depuis la base : {db_password}")
            if db_password is None :
                 return JsonResponse({'error': 'Cet utilisateur ne peut pas se connecter'}, status=403)
            if not db_password.startswith("$2b$"):
                return JsonResponse({'error': 'Mot de passe non valide ou utilisateur non autorisé'}, status=403)
            
             # Vérifier si le mot de passe est correct
            if not bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                return JsonResponse({'error': 'Mot de passe incorrect'}, status=403)

            # Générer les tokens
            tokens = generate_tokens_for_user(user)

            # Retourner les tokens
            return JsonResponse({
                'message': 'Connexion réussie',
                'tokens': tokens,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'role_id': user['roleId'],
                },
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@token_required
def logout_user(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist() #ajoute le token à la lmiste noir
            return JsonResponse({'message': 'Déconnexion réussie'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Impossible de se déconnecter'}, status=500)

@csrf_exempt
@token_required
def create_user(request):
    # Initialiser le formulaire à None pour éviter l'erreur de portée
    form = None


    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Créer une instance de UserForm avec les données
            form = UserForm(data)

            # Valider le formulaire
            if form.is_valid():
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                email = form.cleaned_data['email']
                password= form.cleaned_data['password']
                phone = form.cleaned_data['phone']
                directory = form.cleaned_data['directory']
                role_id = form.cleaned_data['role_id']

            if not email or not password or not role_id:
                return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

             # Hasher le mot de passe
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insérer l'utilisateur via le dataMapper
            user_id = AccountMapper().create_user(last_name, first_name, email, hashed_password, phone, directory, role_id)

            if user_id:
                return JsonResponse({'message': 'Utilisateur créé avec succès', 'user_id': user_id})
            return JsonResponse({'error': 'Échec de la création de l\'utilisateur'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)