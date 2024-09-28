from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form_course import CourseForm
from . import dataMapper_course
import json
import psycopg2

def get_all_courses(request):
    all_courses = dataMapper_course.CourseMapper().get_all_courses()
    if len(all_courses) != 0:
        course_list = [
            {
                'id': one_course[0],
                'name': one_course[1],
                'trainer': one_course[2],
                'createdAt': one_course[3],
                'updatedAt': one_course[4]
            } for one_course in all_courses
        ]
        return JsonResponse(course_list, safe=False)
    else:
        return JsonResponse({'error': 'No courses found'}, status=404)

def get_one_course(request, course_id):
    one_course = dataMapper_course.CourseMapper().get_course_by_id(course_id)
    if one_course:
        course_data = {
            'id': one_course[0],
            'name': one_course[1],
            'trainer': one_course[2],
            'createdAt': one_course[3],
            'updatedAt': one_course[4]
        }
        return JsonResponse(course_data, safe=False)
    else:
        return JsonResponse({'error': 'Course not found'}, status=404)

@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CourseForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                trainer = form.cleaned_data['trainer']

                course_id = dataMapper_course.CourseMapper().create_course(name, trainer)
                return JsonResponse({'course_id': course_id, 'message': 'Course created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid input', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_course(request, course_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = CourseForm(data)

            if form.is_valid():
                name = form.cleaned_data['name']
                trainer = form.cleaned_data['trainer']

                result = dataMapper_course.CourseMapper().update_course(course_id, name, trainer)
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_course(request, course_id):
    if request.method == 'DELETE':
        try:
            result = dataMapper_course.CourseMapper().delete_course(course_id)
            if result['success']:
                return JsonResponse({"message": result['message']}, status=200)
            else:
                return JsonResponse({"error": result['message']}, status=404)
        except psycopg2.Error as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
