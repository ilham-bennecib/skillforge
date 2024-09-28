from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_company import CompanyForm  # Adjust to your form
from . import dataMapper_company
from structureApp import controller_structure, dataMapper_structure, form_structure

def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)

def json_response_success(data, status=200):
    return JsonResponse(data, status=status)

def get_all_companies(request):
    all_companies = dataMapper_company.CompanyMapper().get_all_companies()
    if len(all_companies) != 0:
        company_list = [
            {
                'id': one_company[0],
                'status': one_company[1],
                'structureId': one_company[2],
                'createdAt': one_company[3],
                'updatedAt': one_company[4]
            } for one_company in all_companies
        ]
        return JsonResponse(company_list, safe=False)
    else:
        return JsonResponse({'error': 'Companies not found'}, status=404)

def get_one_company(request, company_id):
    one_company = dataMapper_company.CompanyMapper().get_company_by_id(company_id)
    if one_company is not None:
        company_data = {
            'id': one_company[0],
            'status': one_company[1],
            'structureId': one_company[2],
            'createdAt': one_company[3],
            'updatedAt': one_company[4]
        }
        return JsonResponse(company_data, safe=False)
    else:
        return JsonResponse({'error': 'Company not found'}, status=404)

@csrf_exempt
def create_company(request, structure_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return json_response_error("Invalid JSON", 400)

        # Check if structure_id is provided
        if not structure_id:
            return json_response_error("Structure ID is required to create a company", 400)

        # Fetch structure information
        try:
            structure_data = controller_structure.fetch_structure_by_id(structure_id)
            if not structure_data:
                return json_response_error(f"Structure with ID {structure_id} not found", 404)
            elif 'error' in structure_data:
                return json_response_error(structure_data['error'], 500)
        except psycopg2.Error as e:
            return json_response_error(f"Database error while fetching structure: {e}", 500)

        form = CompanyForm(data)
        if form.is_valid():
            status = form.cleaned_data['status']

            try:
                # Create the company using the dataMapper
                company_id = dataMapper_company.CompanyMapper().create_company(
                    status=status,
                    structure_id=structure_id
                )

                if company_id:
                    return json_response_success({"company_id": company_id, 'message': 'Company created successfully'}, 201)
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
def delete_company(request, company_id):
    if request.method == 'DELETE':
        try:
            # Step 1: Retrieve the company to get the associated structure ID
            company_to_delete = dataMapper_company.CompanyMapper().get_company_by_id(company_id)
            if not company_to_delete:
                return JsonResponse({'error': 'Company not found'}, status=404)

            structure_id = company_to_delete[2]  # Assuming structureId is at index 2 in the company tuple
            
            # Step 2: Delete the company
            delete_result = dataMapper_company.CompanyMapper().delete_company(company_id)
            if not delete_result.get('success'):
                return JsonResponse({'error': 'Failed to delete company'}, status=500)
            
            # Step 3: Delete the associated structure
            try:
                structure_delete_result = dataMapper_structure.StructureMapper().delete_structure(structure_id)
                if not structure_delete_result.get('success'):
                    return JsonResponse({'error': 'Failed to delete associated structure'}, status=500)

            except Exception as e:
                return JsonResponse({'error': f'Failed to delete associated structure: {e}'}, status=500)

            # Step 4: Success message
            return JsonResponse({'message': 'Company and associated structure successfully deleted'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_company(request, company_id):
    if request.method == 'PUT':
        try:
            # Step 1: Load JSON data from the request body
            data = json.loads(request.body)

            # Step 2: Initialize the forms for both company and structure
            form_company = CompanyForm(data)
            formStructure = form_structure.StructureForm(data)

            # Step 3: Validate both forms
            if form_company.is_valid() and formStructure.is_valid():
                # Extract company data
                status = form_company.cleaned_data['status']

                # Extract structure data
                name = formStructure.cleaned_data['name']
                address = formStructure.cleaned_data['address']
                siret = formStructure.cleaned_data['siret']
                description = formStructure.cleaned_data['description']
                directory = formStructure.cleaned_data['directory']
                field_id = formStructure.cleaned_data['fieldId']
                status = form_company.cleaned_data['status']  
                structureId = form_company.cleaned_data['structureId'] 

                # Step 4: Fetch the company details to update
                company_to_update = dataMapper_company.CompanyMapper().get_company_by_id(company_id)
                if not company_to_update:
                    return JsonResponse({'error': 'Company not found'}, status=404)

                structure_id = company_to_update[2]  # Assuming structureId is at index 2 in the company tuple

                # Step 5: Update the company details
                result_company = dataMapper_company.CompanyMapper().update_company(company_id, status, structure_id)
                if not result_company.get("success"):
                    return JsonResponse(result_company, status=400)

                # Step 6: Update the associated structure details
                result_structure = dataMapper_structure.StructureMapper().update_structure(
                    structure_id, name, address, siret, description, directory, field_id
                )
                if not result_structure.get("success"):
                    return JsonResponse(result_structure, status=400)

                # Step 7: Return success response if both updates succeed
                return JsonResponse({"success": True, "message": "Company and Structure updated successfully"}, status=200)

            else:
                # If either form is invalid, return the form errors
                errors = {
                    'form_company_errors': form_company.errors,
                    'form_structure_errors': formStructure.errors
                }
                return JsonResponse({'error': errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

