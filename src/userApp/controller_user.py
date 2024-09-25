from django.http import JsonResponse
from . import dataMapper_user

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
