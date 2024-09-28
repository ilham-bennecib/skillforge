from django.urls import path
from . import controller_course

urlpatterns = [
    path('all/', controller_course.get_all_courses, name='get_all_courses'),
    path('course/<int:course_id>/', controller_course.get_one_course, name='get_one_course'),
    path('course/create/', controller_course.create_course, name='create_course'),
    path('course/update/<int:course_id>/', controller_course.update_course, name='update_course'),
    path('course/delete/<int:course_id>/', controller_course.delete_course, name='delete_course'),
]
