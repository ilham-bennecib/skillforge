from django.http import JsonResponse
from . import dataMapper_user
import json
from django.views.decorators.csrf import csrf_exempt

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
    if request.method == 'POST':
        try:
            # Extraire les données du body de la requête
            data = json.loads(request.body)

            # Récupérer les champs obligatoires (ajouter des vérifications si nécessaire)
            last_name = data.get('last_name')
            first_name = data.get('first_name')
            email = data.get('email')
            phone = data.get('phone')
            directory = data.get('directory')
            role_id = data.get('role_id')

            # Appeler la méthode de création d'utilisateur du DataMapper
            user_id = dataMapper_user.UserMapper().create_user(
                last_name, first_name, email, phone, directory, role_id
            )

            # Retourner une réponse avec l'ID de l'utilisateur créé
            return JsonResponse({'user_id': user_id, 'message': 'User created successfully'}, status=201)

        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)