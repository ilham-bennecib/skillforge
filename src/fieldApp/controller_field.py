from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form_field import FieldForm
from . import dataMapper_field
import json
import psycopg2

def get_all_fields(request):
    all_fields = dataMapper_field.FieldMapper().get_all_fields()
    if len(all_fields) != 0:
        field_list = [
            {
                'id': one_field[0],
                'name': one_field[1],
                'createdAt': one_field[2],
                'updatedAt': one_field[3]
            } for one_field in all_fields
        ]
        return JsonResponse(field_list, safe=False)
    else:
        return JsonResponse({'error': 'No fields found'}, status=404)

def get_one_field(request, field_id):
    one_field = dataMapper_field.FieldMapper().get_field_by_id(field_id)
    if one_field:
        field_data = {
            'id': one_field[0],
            'name': one_field[1],
            'createdAt': one_field[2],
            'updatedAt': one_field[3]
        }
        return JsonResponse(field_data, safe=False)
    else:
        return JsonResponse({'error': 'Field not found'}, status=404)

@csrf_exempt
def create_field(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = FieldForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']

                field_id = dataMapper_field.FieldMapper().create_field(name)
                return JsonResponse({'field_id': field_id, 'message': 'Field created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_field(request, field_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = FieldForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']

                result = dataMapper_field.FieldMapper().update_field(field_id, name)
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_field(request, field_id):
    if request.method == 'DELETE':
        try:
            result = dataMapper_field.FieldMapper().delete_field(field_id)
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
