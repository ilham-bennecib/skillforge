from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_cfaEmployee import CfaEmployeeForm
from . import dataMapper_cfaEmployee
from userApp import controller_user, dataMapper_user, form


def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def json_response_success(data, status=200):
    return JsonResponse(data, status=status)


def get_all_cfaEmployees(request):
    all_employees = dataMapper_cfaEmployee.CfaEmployeeMapper().get_all_employees()
    if len(all_employees) != 0:
        employee_list = [
            {
                'id': one_employee[0],
                'position': one_employee[1],
                'matricule': one_employee[2],
                'structureId': one_employee[3],
                'userId': one_employee[4],
                'createdAt': one_employee[5],
                'updatedAt': one_employee[6],
            } for one_employee in all_employees
        ]
        return JsonResponse(employee_list, safe=False)
    else:
        return JsonResponse({'error': 'CFA Employees not found'}, status=404)


def get_one_cfaEmployee(request, employee_id):
    one_employee = dataMapper_cfaEmployee.CfaEmployeeMapper().get_employee_by_id(employee_id)
    if one_employee is not None:
        employee_data = {
            'id': one_employee[0],
            'position': one_employee[1],
            'matricule': one_employee[2],
            'structureId': one_employee[3],
            'userId': one_employee[4],
            'createdAt': one_employee[5],
            'updatedAt': one_employee[6],
        }
        return JsonResponse(employee_data, safe=False)
    else:
        return JsonResponse({'error': 'CFA Employee not found'}, status=404)


@csrf_exempt
def create_cfaEmployee(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return json_response_error("Invalid JSON", 400)

        # Check if user_id is provided in the request body
        if not user_id:
            return json_response_error("User ID is required to create a CFA Employee", 400)

        # Fetch user information from the user service
        try:
            user_data = controller_user.fetch_user_by_id(user_id)
            if not user_data:
                return json_response_error(f"User with ID {user_id} not found", 404)
            elif 'error' in user_data:
                return json_response_error(user_data['error'], 500)
        except psycopg2.Error as e:
            return json_response_error(f"Database error while fetching user: {e}", 500)

        form = CfaEmployeeForm(data)
        if form.is_valid():
            position = form.cleaned_data['position']
            matricule = form.cleaned_data['matricule']
            structureId = form.cleaned_data['structureId']

            try:
                # Create the CFA employee using the dataMapper
                employee_id = dataMapper_cfaEmployee.CfaEmployeeMapper().create_employee(
                    position=position,
                    matricule=matricule,
                    structureId=structureId,
                    user_id=user_id
                )

                if employee_id:
                    return json_response_success({"employee_id": employee_id, 'message': 'CFA Employee created successfully'}, 201)
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
def delete_cfaEmployee(request, employee_id):
    if request.method == 'DELETE':
        try:
            # Step 1: Fetch the CFA employee to retrieve the user_id
            employee_to_delete = dataMapper_cfaEmployee.CfaEmployeeMapper().get_employee_by_id(employee_id)
            if not employee_to_delete:
                return JsonResponse({'error': 'CFA Employee not found'}, status=404)

            user_id = employee_to_delete[5]
            # Step 2: Delete the CFA employee
            delete_result = dataMapper_cfaEmployee.CfaEmployeeMapper().delete_employee(employee_id)
            if not delete_result:
                return JsonResponse({'error': 'Failed to delete CFA employee'}, status=500)

            # Step 3: Delete the associated user
            try:
                dataMapper_user.UserMapper().delete_user(user_id)
            except Exception as e:
                return JsonResponse({'error': f'Failed to delete associated user: {e}'}, status=500)

            return JsonResponse({'message': 'CFA Employee and associated user successfully deleted'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_cfaEmployee(request, employee_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Fetch the CFA employee to retrieve the associated user_id
            employee_to_update = dataMapper_cfaEmployee.CfaEmployeeMapper().get_employee_by_id(employee_id)
            if not employee_to_update:
                return JsonResponse({'error': 'CFA Employee not found'}, status=404)

            # Extract the associated user_id from the existing CFA employee
            user_id = employee_to_update[5]

            # Add userId into the incoming data so it's passed to the form
            data['userId'] = user_id

            # Initialize both forms
            form_employee = CfaEmployeeForm(data)
            form_user = form.UserForm(data)

            # Validate both forms
            if form_employee.is_valid() and form_user.is_valid():
                # Extract CFA employee data
                position = form_employee.cleaned_data['position']
                matricule = form_employee.cleaned_data['matricule']
                structureId = form_employee.cleaned_data['structureId']

                # Extract user data
                last_name = form_user.cleaned_data['last_name']
                first_name = form_user.cleaned_data['first_name']
                email = form_user.cleaned_data['email']
                phone = form_user.cleaned_data['phone']
                directory = form_user.cleaned_data['directory']
                role_id = form_user.cleaned_data['role_id']  # roleId included in user data

                # Step 2: Update the CFA employee details
                result_employee = dataMapper_cfaEmployee.CfaEmployeeMapper().update_employee(
                    employee_id, position, matricule, structureId, user_id
                )
                if not result_employee.get("success"):
                    return JsonResponse(result_employee, status=400)

                # Step 3: Update the user details
                result_user = dataMapper_user.UserMapper().update_user(
                    user_id, last_name, first_name, email, phone, directory, role_id
                )
                if result_user.get("success"):
                    return JsonResponse({"success": True, "message": "CFA Employee and User updated successfully"}, status=200)
                else:
                    return JsonResponse(result_user, status=400)

            else:
                # Combine form errors
                errors = {
                    'form_employee_errors': form_employee.errors,
                    'form_user_errors': form_user.errors
                }
                return JsonResponse({'error': errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
