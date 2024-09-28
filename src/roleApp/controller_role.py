from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form_role import RoleForm
from . import dataMapper_role
import json
import psycopg2

def get_all_roles(request):
    all_roles = dataMapper_role.RoleMapper().get_all_roles()
    if len(all_roles) != 0:
        role_list = [
            {
                'id': one_role[0],
                'name': one_role[1],
                'permissions': one_role[2],
                'createdAt': one_role[3],
                'updatedAt': one_role[4]
            } for one_role in all_roles
        ]
        return JsonResponse(role_list, safe=False)
    else:
        return JsonResponse({'error': 'No roles found'}, status=404)

def get_one_role(request, role_id):
    one_role = dataMapper_role.RoleMapper().get_role_by_id(role_id)
    if one_role:
        role_data = {
            'id': one_role[0],
            'name': one_role[1],
            'permissions': one_role[2],
            'createdAt': one_role[3],
            'updatedAt': one_role[4]
        }
        return JsonResponse(role_data, safe=False)
    else:
        return JsonResponse({'error': 'Role not found'}, status=404)

@csrf_exempt
def create_role(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RoleForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                permissions = form.cleaned_data['permissions']

                role_id = dataMapper_role.RoleMapper().create_role(name, permissions)
                return JsonResponse({'role_id': role_id, 'message': 'Role created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_role(request, role_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = RoleForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                permissions = form.cleaned_data['permissions']

                result = dataMapper_role.RoleMapper().update_role(role_id, name, permissions)
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_role(request, role_id):
    if request.method == 'DELETE':
        try:
            result = dataMapper_role.RoleMapper().delete_role(role_id)
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
