from django.urls import path
from . import controller_student

urlpatterns = [
    path('all/', controller_student.get_all_students, name='get_all_students'),
    path('student/<int:student_id>/', controller_student.get_one_student, name='get_one_student'),
    path('student/create/from_candidate<int:candidate_id>/', controller_student.create_student, name='create_student'),
    path('student/delete/<int:student_id>/', controller_student.delete_student, name='delete_student'),
    path('student/update/<int:student_id>/', controller_student.update_student, name='update_student'),
]
