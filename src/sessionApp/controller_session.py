from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_session import SessionForm
from . import dataMapper_session

def get_all_sessions(request):
    all_sessions = dataMapper_session.SessionMapper().get_all_sessions()
    if len(all_sessions) != 0:
        session_list = [
            {
                'id': one_session[0],
                'name': one_session[1],
                'referent': one_session[2],
                'tutor': one_session[3],
                'trainingId': one_session[4],
                'createdAt': one_session[5],
                'updatedAt': one_session[6],
            } for one_session in all_sessions
        ]
        return JsonResponse(session_list, safe=False)
    else:
        return JsonResponse({'error': 'Sessions not found'}, status=404)


def get_one_session(request, session_id):
    one_session = dataMapper_session.SessionMapper().get_session_by_id(session_id)
    if one_session:
        session_data = {
            'id': one_session[0],
            'name': one_session[1],
            'referent': one_session[2],
            'tutor': one_session[3],
            'trainingId': one_session[4],
            'createdAt': one_session[5],
            'updatedAt': one_session[6],
        }
        return JsonResponse(session_data, safe=False)
    else:
        return JsonResponse({'error': 'Session not found'}, status=404)


@csrf_exempt
def create_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = SessionForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                referent = form.cleaned_data['referent']
                tutor = form.cleaned_data['tutor']
                training_id = form.cleaned_data['trainingId']

                session_id = dataMapper_session.SessionMapper().create_session(
                    name=name, referent=referent, tutor=tutor, training_id=training_id
                )
                return JsonResponse({'session_id': session_id, 'message': 'Session created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_session(request, session_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = SessionForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                referent = form.cleaned_data['referent']
                tutor = form.cleaned_data['tutor']
                training_id = form.cleaned_data['trainingId']

                result = dataMapper_session.SessionMapper().update_session(
                    session_id, name, referent, tutor, training_id
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_session(request, session_id):
    if request.method == 'DELETE':
        result = dataMapper_session.SessionMapper().delete_session(session_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
