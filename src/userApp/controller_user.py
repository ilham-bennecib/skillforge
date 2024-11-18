from django.http import JsonResponse
from . import dataMapper_user
import json
from django.views.decorators.csrf import csrf_exempt
from .form import UserForm
import psycopg2

def get_all_users(request):
   
    all_users = dataMapper_user.UserMapper().get_all_users()
    print(all_users)
    # Créer une liste de dictionnaires avec les données des utilisateurs
    if len(all_users) != 0:

        users_list = [
            {
                'id': one_user[0],
                'lastName': one_user[1],
                'firstName': one_user[2],
                'email': one_user[3],
                'phone': one_user[4],
                'password': one_user[5],
                'directory': one_user[6],
                'roleId': one_user[7],
                'createdAt': one_user[8],
                'updatedAt': one_user[9],
            } for one_user in all_users
        ]
        return JsonResponse(users_list, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
    else:
        return JsonResponse({'error': 'Users not found'}, status=404)
    
def get_one_user(request,user_id):

    one_user = dataMapper_user.UserMapper().get_user_by_id(user_id)
    print (one_user)
    if one_user is not None:
        user_data={
                'id': one_user[0],
                'lastName': one_user[1],
                'firstName': one_user[2],
                'email': one_user[3],
                'phone': one_user[4],
                'password': one_user[5],
                'directory': one_user[6],
                'roleId': one_user[7],
                'createdAt': one_user[8],
                'updatedAt': one_user[9],
            }

        return JsonResponse(user_data,safe=False)   # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
    else:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
def delete_user(request, user_id):

    if request.method == 'DELETE':
        try:
            result = dataMapper_user.UserMapper().delete_user(user_id)
            
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            # Gestion des erreurs liées à la base de données
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        # Si la méthode n'est pas DELETE, on retourne une erreur
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def update_user(request, user_id):
    print("update_user method called")
    if request.method == 'PUT':
        try:
            # Charger les données JSON depuis le corps de la requête
            data = json.loads(request.body)

            # Créer une instance de UserForm avec les données
            form = UserForm(data)

            # Vérifiez si le formulaire est valide
            if form.is_valid():
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                phone = form.cleaned_data['phone']
                directory = form.cleaned_data['directory']
                role_id = form.cleaned_data['role_id']

                # Appeler la méthode update_user dans le dataMapper
                result = dataMapper_user.UserMapper().update_user(user_id, last_name, first_name, email, password, phone, directory, role_id)
                return JsonResponse(result)  # Retourne le résultat au format JSON
            else:
                return JsonResponse({'error': form.errors}, status=400)  # Retourner les erreurs de validation
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)  # Gestion de l'erreur pour JSON invalide
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)  # Gestion de l'erreur pour méthode non autorisée
    
#methode créer pour ne pas passer par la requete
def fetch_user_by_id(user_id):
    """
    Fetch a user by ID and return the user data as a dictionary.
    """
    
    try:
        user = dataMapper_user.UserMapper().get_user_by_id(user_id)
        if user:
            # Create a dictionary with user details
            user_data = {
                'id': user[0],
                'lastName': user[1],
                'firstName': user[2],
                'email': user[3],
                'password': user[4],
                'phone': user[5],
                'directory': user[6],
                'roleId': user[7],
                'createdAt': user[8],
                'updatedAt': user[9],
            }
            return user_data
        else:
            return None
    except psycopg2.Error as e:
        return {'error': f'Database error: {e}'}