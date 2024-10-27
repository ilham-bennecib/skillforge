from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_candidate import CandidateForm


from . import dataMapper_candidate
from userApp import controller_user, dataMapper_user, form


def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def json_response_success(data, status=200):
    return JsonResponse(data, status=status)

def get_all_candidates(request):
    all_candidates = dataMapper_candidate.CandidateMapper().get_all_candidates()
    if len(all_candidates) != 0:
        # Créer une liste de dictionnaires avec les données des candidats
        candidate_list = [
            {
                'id': one_candidate[0],  # ID du candidat
                'firstName': one_candidate[1],  # Prénom
                'lastName': one_candidate[2]  # Nom
            } for one_candidate in all_candidates
        ]
        return JsonResponse(candidate_list, safe=False)  # safe=False permet d'envoyer une liste au lieu d'un dictionnaire
    else:
        return JsonResponse({'error': 'Candidats non trouvés'}, status=404)
    
def get_one_candidate(request, candidate_id):
    one_candidate = dataMapper_candidate.CandidateMapper().get_candidate_by_id(candidate_id)
    
    if one_candidate is not None:
        candidate_data = {
            'id': one_candidate[0],
            'lastDiploma': one_candidate[1],
            'dateOfBirth': one_candidate[2],
            'address': one_candidate[3],
            'userId': one_candidate[4],
            'createdAt': one_candidate[5],
            'updatedAt': one_candidate[6],
            'firstName': one_candidate[7],
            'lastName': one_candidate[8],
            'email': one_candidate[9],
            'phone': one_candidate[10],
            'directory': one_candidate[11],
            'roleId': one_candidate[12],
            'customerCreatedAt': one_candidate[13],
            'customerUpdatedAt': one_candidate[14]
        }
        return JsonResponse(candidate_data, safe=False)
    else:
        return JsonResponse({'error': 'Candidate not found'}, status=404)

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

@csrf_exempt
def delete_candidate(request, candidate_id):

    if request.method == 'DELETE':
        try:
            #Etape 1 : recupération de candidat pour son avoir l'id user
            candidate_to_delete = dataMapper_candidate.CandidateMapper().get_candidate_by_id(candidate_id)
            if not candidate_to_delete:
                return JsonResponse({'error': 'Candidate not found'}, status=404)

            user_id = candidate_to_delete[4]
            #Etape 2 :  On supprime candidat
            delete_result = dataMapper_candidate.CandidateMapper().delete_candidate(candidate_id)
            if not delete_result:
                return JsonResponse({'error': 'Failed to delete candidate'}, status=500)
            
            #Etape 3 : on supprime le user associé : 
            try:
                dataMapper_user.UserMapper().delete_user(user_id)
            except Exception as e:
                return JsonResponse({'error': f'Failed to delete associated user: {e}'}, status=500)

            return JsonResponse({'message': 'Candidate and associated user successfully deleted'}, status=200)
        except Exception as e:
                return JsonResponse({'error': f'Error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def update_candidate(request, candidate_id):
    print("update_user method called")
    if request.method == 'PUT':
        try:
            # Charger les données JSON depuis le corps de la requête
            data = json.loads(request.body)

            # Créer une instance de UserForm avec les données
            form_candidate = CandidateForm(data)
            form_user = form.UserForm(data)

            # Vérifiez si le formulaire est valide
            if form_candidate.is_valid() and form_user.is_valid() :
                last_name = form_user.cleaned_data['last_name']
                first_name = form_user.cleaned_data['first_name']
                email = form_user.cleaned_data['email']
                phone = form_user.cleaned_data['phone']
                directory = form_user.cleaned_data['directory']
                role_id = form_user.cleaned_data['role_id']
                last_diploma = form_candidate.cleaned_data['last_diploma']
                date_of_birth = form_candidate.cleaned_data['date_of_birth']
                address = form_candidate.cleaned_data['address']

                #recupérer le user associé
                candidate_to_update = dataMapper_candidate.CandidateMapper().get_candidate_by_id(candidate_id)
                if not candidate_to_update:
                    return JsonResponse({'error': 'Candidate not found'}, status=404)

                user_id = candidate_to_update[4]

                # Appeler la méthode update_user dans le dataMapper
                
                result_candidate = dataMapper_candidate.CandidateMapper().update_candidate(candidate_id, last_diploma, date_of_birth, address)
                if not result_candidate.get("success"):
                    return JsonResponse(result_candidate, status=400)
                
                # Appeler la méthode update_user dans le dataMapper
                result_user = dataMapper_user.UserMapper().update_user(user_id, last_name, first_name, email, phone, directory, role_id)
                if result_user.get("success"):
                    return JsonResponse({"success": True, "message": "Candidate and User updated successfully"}, status=200)
                else:
                    return JsonResponse(result_user, status=400)

            else:
                # Combine errors from both forms
                errors = {}
                errors['form_user_errors'] = form_user.errors
                errors['form_candidate_errors'] = form_candidate.errors
                return JsonResponse({'error': errors}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)  # Gestion de l'erreur pour JSON invalide
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)  # Gestion de l'erreur pour méthode non autorisée
    

