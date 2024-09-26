from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_candidate import CandidateForm


from . import dataMapper_candidate
from userApp import controller_user, dataMapper_user


def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def json_response_success(data, status=200):
    return JsonResponse(data, status=status)

# def get_all_users(request):
   
#     all_users = dataMapper_user.UserMapper().get_all_users()
#     print(all_users)
#     # Créer une liste de dictionnaires avec les données des utilisateurs
#     if len(all_users) != 0:

#         users_list = [
#             {
#                 'id': one_user[0],
#                 'lastName': one_user[1],
#                 'firstName': one_user[2],
#                 'email': one_user[3],
#                 'phone': one_user[4],
#                 'directory': one_user[5],
#                 'roleId': one_user[6],
#                 'createdAt': one_user[7],
#                 'updatedAt': one_user[8],
#             } for one_user in all_users
#         ]
#         return JsonResponse(users_list, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
#     else:
#         return JsonResponse({'error': 'Users not found'}, status=404)
    
# def get_one_user(request, user_id):

#     one_user = dataMapper_user.UserMapper().get_user_by_id(user_id)
#     print (one_user)
#     if one_user is not None:
#         user_data={
#                 'id': one_user[0],
#                 'lastName': one_user[1],
#                 'firstName': one_user[2],
#                 'email': one_user[3],
#                 'phone': one_user[4],
#                 'directory': one_user[5],
#                 'roleId': one_user[6],
#                 'createdAt': one_user[7],
#                 'updatedAt': one_user[8],
#             }

#         return JsonResponse(user_data, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
#     else:
#         return JsonResponse({'error': 'User not found'}, status=404)




@csrf_exempt
def create_candidate(request,user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return json_response_error("Invalid JSON", 400)

        # Check if user_id is provided in the request body
        
        if not user_id:
            return json_response_error("User ID is required to create a candidate", 400)

        # Fetch user information from the user service
        
        try:
            user_data = controller_user.fetch_user_by_id(user_id)
            if not user_data:
                return json_response_error(f"User with ID {user_id} not found", 404)
            elif 'error' in user_data:
                return json_response_error(user_data['error'], 500)
            
        except psycopg2.Error as e:
            return json_response_error(f"Database error while fetching user: {e}", 500)

        form = CandidateForm(data)
        if form.is_valid():
            last_diploma = form.cleaned_data['last_diploma']
            date_of_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['address']
            
            try:
                # Create the candidate using the dataMapper
                candidate_id = dataMapper_candidate.CandidateMapper().create_candidate(
                    last_diploma=last_diploma, 
                    date_of_birth=date_of_birth,
                    address=address,
                    userId=user_id
                    )

                if candidate_id:
                    return json_response_success({"candidate_id": candidate_id,'message':'canddiate created sucessfully}'}, 201)
                else:
                    return json_response_error('Invalid input', 400)

            except psycopg2.IntegrityError as e:
                return json_response_error(f"Database Integrity Error: {e}", 500)
            except psycopg2.Error as e:
                return json_response_error(f"Database Error: {e}", 500)
            finally:
                # Ensure the database connection is properly closed
                pass
        else:
            return json_response_error(form.errors, 400)
    else:
        return json_response_error("Method not allowed", 405)

# @csrf_exempt
# def delete_user(request, user_id):

#     if request.method == 'DELETE':
#         try:
#             result = dataMapper_user.UserMapper().delete_user(user_id)
            
#             if result['success']:
#                 return JsonResponse({"message": result['message']}, status=200)
#             else:
#                 return JsonResponse({"error": result['message']}, status=404)
#         except psycopg2.Error as e:
#             # Gestion des erreurs liées à la base de données
#             return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
#     else:
#         # Si la méthode n'est pas DELETE, on retourne une erreur
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    
# @csrf_exempt
# def update_user(request, user_id):
#     print("update_user method called")
#     if request.method == 'PUT':
#         try:
#             # Charger les données JSON depuis le corps de la requête
#             data = json.loads(request.body)

#             # Créer une instance de UserForm avec les données
#             form = UserForm(data)

#             # Vérifiez si le formulaire est valide
#             if form.is_valid():
#                 last_name = form.cleaned_data['last_name']
#                 first_name = form.cleaned_data['first_name']
#                 email = form.cleaned_data['email']
#                 phone = form.cleaned_data['phone']
#                 directory = form.cleaned_data['directory']
#                 role_id = form.cleaned_data['role_id']

#                 # Appeler la méthode update_user dans le dataMapper
#                 result = dataMapper_user.UserMapper().update_user(user_id, last_name, first_name, email, phone, directory, role_id)
#                 return JsonResponse(result)  # Retourne le résultat au format JSON
#             else:
#                 return JsonResponse({'error': form.errors}, status=400)  # Retourner les erreurs de validation
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)  # Gestion de l'erreur pour JSON invalide
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)  # Gestion de l'erreur pour méthode non autorisée