from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_event import EventForm
from . import dataMapper_event

def get_all_events(request):
    all_events = dataMapper_event.EventMapper().get_all_events()
    if len(all_events) != 0:
        event_list = [
            {
                'id': one_event[0],
                'title': one_event[1],
                'description': one_event[2],
                'date': one_event[3],
                'startTime': one_event[4],
                'endTime': one_event[5],
                'cfaemployeeId': one_event[6],
                'createdAt': one_event[7],
                'updatedAt': one_event[8],
            } for one_event in all_events
        ]
        return JsonResponse(event_list, safe=False)
    else:
        return JsonResponse({'error': 'Events not found'}, status=404)


def get_one_event(request, event_id):
    one_event = dataMapper_event.EventMapper().get_event_by_id(event_id)
    if one_event:
        event_data = {
            'id': one_event[0],
            'title': one_event[1],
            'description': one_event[2],
            'date': one_event[3],
            'startTime': one_event[4],
            'endTime': one_event[5],
            'cfaemployeeId': one_event[6],
            'createdAt': one_event[7],
            'updatedAt': one_event[8],
        }
        return JsonResponse(event_data, safe=False)
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)


@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = EventForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                start_time = form.cleaned_data['startTime']
                end_time = form.cleaned_data['endTime']
                cfaemployeeId = form.cleaned_data['cfaemployeeId']

                event_id = dataMapper_event.EventMapper().create_event(
                    title=title, description=description, date=date, start_time=start_time, end_time=end_time, cfaemployeeId=cfaemployeeId
                )
                return JsonResponse({'event_id': event_id, 'message': 'Event created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_event(request, event_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = EventForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                start_time = form.cleaned_data['startTime']
                end_time = form.cleaned_data['endTime']
                cfaemployeeId = form.cleaned_data['cfaemployeeId']

                result = dataMapper_event.EventMapper().update_event(
                    event_id, title, description, date, start_time, end_time, cfaemployeeId
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'DELETE':
        result = dataMapper_event.EventMapper().delete_event(event_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
