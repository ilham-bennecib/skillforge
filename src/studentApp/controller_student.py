from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import psycopg2
import json

from .form_student import StudentForm
from . import dataMapper_student
from candidateApp import dataMapper_candidate, form_candidate
from userApp import dataMapper_user, form

def json_response_error(message, status=400):
    return JsonResponse({'error': message}, status=status)

def json_response_success(data, status=200):
    return JsonResponse(data, status=status)

def get_all_students(request):
    all_students = dataMapper_student.StudentMapper().get_all_students()
    if len(all_students) != 0:
        student_list = [
            {
                'id': one_student[0],
                'password': one_student[1],
                'companyId': one_student[2],
                'sessionId': one_student[3],
                'candidateId': one_student[4],
                'createdAt': one_student[5],
                'updatedAt': one_student[6]
            } for one_student in all_students
        ]
        return JsonResponse(student_list, safe=False)
    else:
        return JsonResponse({'error': 'Students not found'}, status=404)

def get_one_student(request, student_id):
    one_student = dataMapper_student.StudentMapper().get_student_by_id(student_id)
    if one_student is not None:
        student_data = {
            'id': one_student[0],
            'password': one_student[1],
            'companyId': one_student[2],
            'sessionId': one_student[3],
            'candidateId': one_student[4],
            'createdAt': one_student[5],
            'updatedAt': one_student[6]
        }
        return JsonResponse(student_data, safe=False)
    else:
        return JsonResponse({'error': 'Student not found'}, status=404)

@csrf_exempt
def create_student(request, candidate_id):
    if request.method == 'POST':
        try:
            # Step 1: Load JSON data from the request body
            data = json.loads(request.body)

            # Step 2: Validate the existence of the candidate
            candidate = dataMapper_candidate.CandidateMapper().get_candidate_by_id(candidate_id)
            if not candidate:
                return JsonResponse({'error': 'Candidate not found'}, status=404)

            # Step 3: Initialize the form with the data
            form = StudentForm(data)

            # Step 4: Validate the form
            if form.is_valid():
                password = form.cleaned_data['password']
                company_id = form.cleaned_data['companyId']
                session_id = form.cleaned_data['sessionId']

                # Step 5: Create the student using the dataMapper
                try:
                    student_id = dataMapper_student.StudentMapper().create_student(
                        password=password,
                        company_id=company_id,
                        session_id=session_id,
                        candidate_id=candidate_id  
                    )

                    if student_id:
                        return JsonResponse({'student_id': student_id, 'message': 'Student created successfully'}, status=201)
                    else:
                        return JsonResponse({'error': 'Failed to create student'}, status=400)

                except psycopg2.IntegrityError as e:
                    return JsonResponse({'error': f'Database Integrity Error: {e}'}, status=500)
                except psycopg2.Error as e:
                    return JsonResponse({'error': f'Database Error: {e}'}, status=500)

            else:
                return JsonResponse({'error': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


#Cette methode fonctionne différenmet des autres : elle ne supprime pas le candidat associé. Seulement l'etudiant, contrairement au delete_candidate qui supprime le candiodat mais aussi le user associé
@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        try:
            student_to_delete = dataMapper_student.StudentMapper().get_student_by_id(student_id)
            if not student_to_delete:
                return JsonResponse({'error': 'Student not found'}, status=404)

            delete_result = dataMapper_student.StudentMapper().delete_student(student_id)
            if not delete_result:
                return JsonResponse({'error': 'Failed to delete student'}, status=500)

            return JsonResponse({'message': 'Student successfully deleted'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#Cette methode va updater le candidat associé mais aussi le user associé
@csrf_exempt
def update_student(request, student_id):
    if request.method == 'PUT':
        try:
            # Step 1: Load JSON data from the request body
            data = json.loads(request.body)

            # Step 2: Fetch the student by student_id
            student = dataMapper_student.StudentMapper().get_student_by_id(student_id)
            print(f"le'student est : {student}")
            if not student:
                return JsonResponse({'error': 'Student not found'}, status=404)

            candidate_id = student[4]  # Assuming candidateId is at index 4
            candidate = dataMapper_candidate.CandidateMapper().get_candidate_by_id(candidate_id)
            print(print(f"le candidat est : {candidate}"))
            if not candidate:
                return JsonResponse({'error': 'Candidate not found'}, status=404)

            user_id = candidate[4]  
            print(f"le id user est {user_id}")
            user = dataMapper_user.UserMapper().get_user_by_id(user_id)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Step 3: Initialize the forms for student, candidate, and user
            form_student = StudentForm(data)
            formCandidate = form_candidate.CandidateForm(data)
            form_user = form.UserForm(data)  # Assuming UserForm is in the userApp

            # Step 4: Validate the forms
            if form_student.is_valid() and formCandidate.is_valid() and form_user.is_valid():
                # Extract student data
                password = form_student.cleaned_data['password']
                company_id = form_student.cleaned_data['companyId']
                session_id = form_student.cleaned_data['sessionId']

                # Extract candidate data
                last_diploma = formCandidate.cleaned_data['last_diploma']
                date_of_birth = formCandidate.cleaned_data['date_of_birth']
                address = formCandidate.cleaned_data['address']

                # Extract user data
                last_name = form_user.cleaned_data['last_name']
                first_name = form_user.cleaned_data['first_name']
                email = form_user.cleaned_data['email']
                phone = form_user.cleaned_data['phone']
                directory = form_user.cleaned_data['directory']
                role_id = form_user.cleaned_data['role_id']

                # Step 5: Update the student details
                result_student = dataMapper_student.StudentMapper().update_student(
                    student_id, password, company_id, session_id, candidate_id
                )
                if not result_student.get("success"):
                    return JsonResponse(result_student, status=400)

                # Step 6: Update the candidate details
                result_candidate = dataMapper_candidate.CandidateMapper().update_candidate(
                    candidate_id, last_diploma, date_of_birth, address
                )
                if not result_candidate.get("success"):
                    return JsonResponse(result_candidate, status=400)

                # Step 7: Update the user details with role 3 to student
                result_user = dataMapper_user.UserMapper().update_user(
                    user_id, last_name, first_name, email, phone, directory, role_id=3
                )
                if not result_user.get("success"):
                    return JsonResponse(result_user, status=400)

                # Step 8: Return success response if all updates succeed
                return JsonResponse({"success": True, "message": "Student, Candidate, and User updated successfully"}, status=200)

            else:
                # If any of the forms is invalid, return the form errors
                errors = {
                    'form_student_errors': form_student.errors,
                    'form_candidate_errors': formCandidate.errors,
                    'form_user_errors': form_user.errors
                }
                return JsonResponse({'error': errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
