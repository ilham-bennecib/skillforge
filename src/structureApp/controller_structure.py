from django.http import JsonResponse
from . import dataMapper_structure
import json
from django.views.decorators.csrf import csrf_exempt
from .form_structure import StructureForm
import psycopg2

def get_all_structures(request):
    all_structures = dataMapper_structure.StructureMapper().get_all_structures()
    if len(all_structures) != 0:
        structures_list = [
            {
                'id': one_structure[0],
                'name': one_structure[1],
                'address': one_structure[2],
                'siret': one_structure[3],
                'description': one_structure[4],
                'directory': one_structure[5],
                'fieldId': one_structure[6],
                'createdAt': one_structure[7],
                'updatedAt': one_structure[8],
            } for one_structure in all_structures
        ]
        return JsonResponse(structures_list, safe=False)
    else:
        return JsonResponse({'error': 'Structures not found'}, status=404)

def get_one_structure(request, structure_id):
    one_structure = dataMapper_structure.StructureMapper().get_structure_by_id(structure_id)
    if one_structure is not None:
        structure_data = {
            'id': one_structure[0],
            'name': one_structure[1],
            'address': one_structure[2],
            'siret': one_structure[3],
            'description': one_structure[4],
            'directory': one_structure[5],
            'fieldId': one_structure[6],
            'createdAt': one_structure[7],
            'updatedAt': one_structure[8],
        }
        return JsonResponse(structure_data, safe=False)
    else:
        return JsonResponse({'error': 'Structure not found'}, status=404)

@csrf_exempt
def create_structure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = StructureForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                address = form.cleaned_data['address']
                siret = form.cleaned_data['siret']
                description = form.cleaned_data['description']
                directory = form.cleaned_data['directory']
                fieldId = form.cleaned_data['fieldId']

                structure_id = dataMapper_structure.StructureMapper().create_structure(
                    name=name,
                    address=address,
                    siret=siret,
                    description=description,
                    directory=directory,
                    fieldId=fieldId
                )
                return JsonResponse({'structure_id': structure_id, 'message': 'Structure created successfully'})
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_structure(request, structure_id):
    if request.method == 'DELETE':
        try:
            result = dataMapper_structure.StructureMapper().delete_structure(structure_id)
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_structure(request, structure_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = StructureForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                address = form.cleaned_data['address']
                siret = form.cleaned_data['siret']
                description = form.cleaned_data['description']
                directory = form.cleaned_data['directory']
                fieldId = form.cleaned_data['fieldId']

                result = dataMapper_structure.StructureMapper().update_structure(
                    structure_id, name, address, siret, description, directory, fieldId
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
