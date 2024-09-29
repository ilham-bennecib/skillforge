from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_contact import ContactForm
from . import dataMapper_contact
from userApp import controller_user, dataMapper_user, form


def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def json_response_success(data, status=200):
    return JsonResponse(data, status=status)


def get_all_contacts(request):
    all_contacts = dataMapper_contact.ContactMapper().get_all_contacts()
    if len(all_contacts) != 0:
        contact_list = [
            {
                'id': one_contact[0],
                'position': one_contact[1],
                'companyId': one_contact[2],
                'userId': one_contact[3],
                'password': one_contact[4],
                'roleId': one_contact[5],
                'createdAt': one_contact[6],
                'updatedAt': one_contact[7],
            } for one_contact in all_contacts
        ]
        return JsonResponse(contact_list, safe=False)
    else:
        return JsonResponse({'error': 'Contacts not found'}, status=404)


def get_one_contact(request, contact_id):
    one_contact = dataMapper_contact.ContactMapper().get_contact_by_id(contact_id)
    if one_contact is not None:
        contact_data = {
            'id': one_contact[0],
            'position': one_contact[1],
            'companyId': one_contact[2],
            'userId': one_contact[3],
            'password': one_contact[4],
            'roleId': one_contact[5],
            'createdAt': one_contact[6],
            'updatedAt': one_contact[7],
        }
        return JsonResponse(contact_data, safe=False)
    else:
        return JsonResponse({'error': 'Contact not found'}, status=404)


@csrf_exempt
def create_contact(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return json_response_error("Invalid JSON", 400)

        # Check if user_id is provided in the request body
        if not user_id:
            return json_response_error("User ID is required to create a contact", 400)

        # Fetch user information from the user service
        try:
            user_data = controller_user.fetch_user_by_id(user_id)
            if not user_data:
                return json_response_error(f"User with ID {user_id} not found", 404)
            elif 'error' in user_data:
                return json_response_error(user_data['error'], 500)
            
        except psycopg2.Error as e:
            return json_response_error(f"Database error while fetching user: {e}", 500)

        form = ContactForm(data)
        if form.is_valid():
            position = form.cleaned_data['position']
            company_id = form.cleaned_data['companyId']
            password = form.cleaned_data['password']
            

            try:
                # Create the contact using the dataMapper
                contact_id = dataMapper_contact.ContactMapper().create_contact(
                    position=position,
                    company_id=company_id,
                    user_id=user_id,
                    password=password,
                    
                )

                if contact_id:
                    return json_response_success({"contact_id": contact_id, 'message': 'Contact created successfully'}, 201)
                else:
                    return json_response_error('Invalid input', 400)

            except psycopg2.IntegrityError as e:
                return json_response_error(f"Database Integrity Error: {e}", 500)
            except psycopg2.Error as e:
                return json_response_error(f"Database Error: {e}", 500)
        else:
            return json_response_error(form.errors, 400)
    else:
        return json_response_error("Method not allowed", 405)


@csrf_exempt
def delete_contact(request, contact_id):
    if request.method == 'DELETE':
        try:
            # Step 1: Fetch the contact to retrieve the user_id
            contact_to_delete = dataMapper_contact.ContactMapper().get_contact_by_id(contact_id)
            if not contact_to_delete:
                return JsonResponse({'error': 'Contact not found'}, status=404)

            user_id = contact_to_delete[3]
            # Step 2: Delete the contact
            delete_result = dataMapper_contact.ContactMapper().delete_contact(contact_id)
            if not delete_result:
                return JsonResponse({'error': 'Failed to delete contact'}, status=500)

            # Step 3: Delete the associated user
            try:
                dataMapper_user.UserMapper().delete_user(user_id)
            except Exception as e:
                return JsonResponse({'error': f'Failed to delete associated user: {e}'}, status=500)

            return JsonResponse({'message': 'Contact and associated user successfully deleted'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_contact(request, contact_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Fetch the contact to retrieve the associated user_id
            contact_to_update = dataMapper_contact.ContactMapper().get_contact_by_id(contact_id)
            if not contact_to_update:
                return JsonResponse({'error': 'Contact not found'}, status=404)

            # Extract the associated user_id from the existing contact
            user_id = contact_to_update[3]  # Assuming user_id is at index 3

            # Add userId into the incoming data so it's passed to the form
            data['userId'] = user_id

            # Initialize both forms
            form_contact = ContactForm(data)
            form_user = form.UserForm(data)

            # Validate both forms
            if form_contact.is_valid() and form_user.is_valid():
                # Extract contact data
                position = form_contact.cleaned_data['position']
                company_id = form_contact.cleaned_data['companyId']
                password = form_contact.cleaned_data['password']

                # Extract user data
                last_name = form_user.cleaned_data['last_name']
                first_name = form_user.cleaned_data['first_name']
                email = form_user.cleaned_data['email']
                phone = form_user.cleaned_data['phone']
                directory = form_user.cleaned_data['directory']
                role_id = form_user.cleaned_data['role_id']  # roleId included in user data

                # Step 2: Update the contact details
                result_contact = dataMapper_contact.ContactMapper().update_contact(
                    contact_id, position, company_id, user_id, password
                )
                if not result_contact.get("success"):
                    return JsonResponse(result_contact, status=400)

                # Step 3: Update the user details
                result_user = dataMapper_user.UserMapper().update_user(
                    user_id, last_name, first_name, email, phone, directory, role_id  # Include role_id in user update
                )
                if result_user.get("success"):
                    return JsonResponse({"success": True, "message": "Contact and User updated successfully"}, status=200)
                else:
                    return JsonResponse(result_user, status=400)

            else:
                # Combine form errors
                errors = {
                    'form_contact_errors': form_contact.errors,
                    'form_user_errors': form_user.errors
                }
                return JsonResponse({'error': errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)