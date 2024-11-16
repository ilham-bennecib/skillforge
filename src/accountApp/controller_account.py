from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import bcrypt
import json
from .dataMapper_account import AccountMapper
from userApp.form import UserForm


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

        

            # Retourner une réponse de succès
            return JsonResponse({
                'message': 'Connexion réussie',
                'user_id': user.get('id'),  # ID de l'utilisateur
                'role_id': user.get('roleId')   # Rôle de l'utilisateur
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Déconnexion réussie'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
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