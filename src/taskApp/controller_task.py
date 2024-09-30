from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_task import TaskForm
from . import dataMapper_task

def get_all_tasks(request):
    all_tasks = dataMapper_task.TaskMapper().get_all_tasks()
    if len(all_tasks) != 0:
        task_list = [
            {
                'id': one_task[0],
                'title': one_task[1],
                'description': one_task[2],
                'date': one_task[3],
                'cfaemployeeId': one_task[4],
                'createdAt': one_task[5],
                'updatedAt': one_task[6],
            } for one_task in all_tasks
        ]
        return JsonResponse(task_list, safe=False)
    else:
        return JsonResponse({'error': 'Tasks not found'}, status=404)


def get_one_task(request, task_id):
    one_task = dataMapper_task.TaskMapper().get_task_by_id(task_id)
    if one_task:
        task_data = {
            'id': one_task[0],
            'title': one_task[1],
            'description': one_task[2],
            'date': one_task[3],
            'cfaemployeeId': one_task[4],
            'createdAt': one_task[5],
            'updatedAt': one_task[6],
        }
        return JsonResponse(task_data, safe=False)
    else:
        return JsonResponse({'error': 'Task not found'}, status=404)


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = TaskForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                cfaemployeeId = form.cleaned_data['cfaemployeeId']

                task_id = dataMapper_task.TaskMapper().create_task(
                    title=title, description=description, date=date, cfaemployeeId=cfaemployeeId
                )
                return JsonResponse({'task_id': task_id, 'message': 'Task created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_task(request, task_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = TaskForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                cfaemployeeId = form.cleaned_data['cfaemployeeId']

                result = dataMapper_task.TaskMapper().update_task(
                    task_id, title, description, date, cfaemployeeId
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        result = dataMapper_task.TaskMapper().delete_task(task_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
