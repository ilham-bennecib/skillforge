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
                'directory': one_user[5],
                'roleId': one_user[6],
                'createdAt': one_user[7],
                'updatedAt': one_user[8],
            } for one_user in all_users
        ]
        return JsonResponse(users_list, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
    else:
        return JsonResponse({'error': 'Users not found'}, status=404)
    
def get_one_user(request, user_id):

    one_user = dataMapper_user.UserMapper().get_user_by_id(user_id)
    print (one_user)
    if one_user is not None:
        user_data={
                'id': one_user[0],
                'lastName': one_user[1],
                'firstName': one_user[2],
                'email': one_user[3],
                'phone': one_user[4],
                'directory': one_user[5],
                'roleId': one_user[6],
                'createdAt': one_user[7],
                'updatedAt': one_user[8],
            }

        return JsonResponse(user_data, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
    else:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt 
def create_user(request):

    # Initialiser le formulaire à None pour éviter l'erreur de portée
    form = None

    if request.method == 'POST':
        try:
            # Récupérer les données du corps de la requête
            data = json.loads(request.body)
            
            # Créer une instance de UserForm avec les données
            form = UserForm(data)

            # Valider le formulaire
            if form.is_valid():
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                directory = form.cleaned_data['directory']
                role_id = form.cleaned_data['role_id']

                # Créer l'utilisateur dans la base de données
                user_id = dataMapper_user.UserMapper().create_user(
                    last_name=last_name,
                    first_name=first_name,
                    email=email,
                    phone=phone,
                    directory=directory,
                    role_id=role_id
                )

                return JsonResponse({'user_id': user_id, 'message': 'User created successfully'})
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        finally:
            # Ici, vous pouvez fermer la connexion si nécessaire, mais assurez-vous qu'elle a été ouverte
            pass  # Remplacez ceci par votre logique de nettoyage si besoin

    return JsonResponse({'error': 'Method not allowed'}, status=405)

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