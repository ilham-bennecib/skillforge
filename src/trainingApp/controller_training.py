from django.http import JsonResponse
from . import dataMapper_training
import json
from django.views.decorators.csrf import csrf_exempt
from .form_training import TrainingForm
import psycopg2

def get_all_trainings(request):
    all_trainings = dataMapper_training.TrainingMapper().get_all_trainings()
    if len(all_trainings) != 0:
        training_list = [
            {
                'id': one_training[0],
                'name': one_training[1],
                'price': float(one_training[2]),
                'startDate': one_training[3],
                'endDate': one_training[4],
                'type': one_training[5],
                'directory': one_training[6],
                'fieldId': one_training[7],
                'structureId': one_training[8],
                'createdAt': one_training[9],
                'updatedAt': one_training[10],
            } for one_training in all_trainings
        ]
        return JsonResponse(training_list, safe=False)
    else:
        return JsonResponse({'error': 'Trainings not found'}, status=404)

def get_one_training(request, training_id):
    one_training = dataMapper_training.TrainingMapper().get_training_by_id(training_id)
    if one_training is not None:
        training_data = {
            'id': one_training[0],
            'name': one_training[1],
            'price': float(one_training[2]),
            'startDate': one_training[3],
            'endDate': one_training[4],
            'type': one_training[5],
            'directory': one_training[6],
            'fieldId': one_training[7],
            'structureId': one_training[8],
            'createdAt': one_training[9],
            'updatedAt': one_training[10],
        }
        return JsonResponse(training_data, safe=False)
    else:
        return JsonResponse({'error': 'Training not found'}, status=404)

@csrf_exempt
def create_training(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = TrainingForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                start_date = form.cleaned_data['startDate']
                end_date = form.cleaned_data['endDate']
                training_type = form.cleaned_data['type']
                directory = form.cleaned_data['directory']
                field_id = form.cleaned_data['fieldId']
                structure_id = form.cleaned_data['structureId']

                training_id = dataMapper_training.TrainingMapper().create_training(
                    name=name,
                    price=price,
                    start_date=start_date,
                    end_date=end_date,
                    training_type=training_type,
                    directory=directory,
                    field_id=field_id,
                    structure_id=structure_id
                )
                return JsonResponse({'training_id': training_id, 'message': 'Training created successfully'})
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_training(request, training_id):
    if request.method == 'DELETE':
        try:
            result = dataMapper_training.TrainingMapper().delete_training(training_id)
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_training(request, training_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = TrainingForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                start_date = form.cleaned_data['startDate']
                end_date = form.cleaned_data['endDate']
                training_type = form.cleaned_data['type']
                directory = form.cleaned_data['directory']
                field_id = form.cleaned_data['fieldId']
                structure_id = form.cleaned_data['structureId']

                result = dataMapper_training.TrainingMapper().update_training(
                    training_id, name, price, start_date, end_date, training_type, directory, field_id, structure_id
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

