# from django.http import JsonResponse
# from . import dataMapper_user
# import json
# from django.views.decorators.csrf import csrf_exempt
# from .form_companie import UserForm
# import psycopg2

# def get_all_companies(request):
   
#     all_companies = dataMapper_user.UserMapper().get_all_companies()
#     print(all_companies)
#     # Créer une liste de dictionnaires avec les données des utilisateurs
#     if len(all_companies) != 0:

#         companies_list = [
#             {
#                 'id': one_company[0],
#                 'lastName': one_company[1],
#                 'firstName': one_company[2],
#                 'email': one_company[3],
#                 'phone': one_company[4],
#                 'directory': one_company[5],
#                 'roleId': one_company[6],
#                 'createdAt': one_company[7],
#                 'updatedAt': one_company[8],
#             } for one_company in all_companies
#         ]
#         return JsonResponse(companies_list, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
#     else:
#         return JsonResponse({'error': 'Users not found'}, status=404)
    
# def get_one_company(request,company_id):

#     one_user = dataMapper_user.UserMapper().get_user_by_id(company_id)
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

#         return JsonResponse(user_data,safe=False)   # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
#     else:
#         return JsonResponse({'error': 'User not found'}, status=404)

# @csrf_exempt 
# def create_company(request):
#     # Initialiser le formulaire à None pour éviter l'erreur de portée
#     form = None

#     if request.method == 'POST':
#         try:
#             # Récupérer les données du corps de la requête
#             data = json.loads(request.body)
            
#             # Créer une instance de UserForm avec les données
#             form = UserForm(data)

#             # Valider le formulaire
#             if form.is_valid():
#                 last_name = form.cleaned_data['last_name']
#                 first_name = form.cleaned_data['first_name']
#                 email = form.cleaned_data['email']
#                 phone = form.cleaned_data['phone']
#                 directory = form.cleaned_data['directory']
#                 role_id = form.cleaned_data['role_id']

#                 # Créer l'utilisateur dans la base de données
#                 company_id = dataMapper_user.UserMapper().create_user(
#                     last_name=last_name,
#                     first_name=first_name,
#                     email=email,
#                     phone=phone,
#                     directory=directory,
#                     role_id=role_id
#                 )

#                 return JsonResponse({'company_id': company_id, 'message': 'User created successfully'})
#             else:
#                 return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
#         finally:
#             print("process finished successfully")

#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt
# def delete_compagny(request, company_id):

#     if request.method == 'DELETE':
#         try:
#             result = dataMapper_user.UserMapper().delete_user(company_id)
            
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
# def update_company(request, company_id):
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
#                 result = dataMapper_user.UserMapper().update_user(company_id, last_name, first_name, email, phone, directory, role_id)
#                 return JsonResponse(result)  # Retourne le résultat au format JSON
#             else:
#                 return JsonResponse({'error': form.errors}, status=400)  # Retourner les erreurs de validation
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)  # Gestion de l'erreur pour JSON invalide
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)  # Gestion de l'erreur pour méthode non autorisée
    
# #methode créer pour ne pas passer par la requete
# def fetch_company_by_id(company_id):
#     """
#     Fetch a user by ID and return the user data as a dictionary.
#     """
    
#     try:
#         user = dataMapper_user.UserMapper().get_user_by_id(company_id)
#         if user:
#             # Create a dictionary with user details
#             user_data = {
#                 'id': user[0],
#                 'lastName': user[1],
#                 'firstName': user[2],
#                 'email': user[3],
#                 'phone': user[4],
#                 'directory': user[5],
#                 'roleId': user[6],
#                 'createdAt': user[7],
#                 'updatedAt': user[8],
#             }
#             return user_data
#         else:
#             return None
#     except psycopg2.Error as e:
#         return {'error': f'Database error: {e}'}