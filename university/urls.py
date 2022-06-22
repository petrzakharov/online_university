from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('teachers/', views.Teachers.as_view(), name='all_teachers'),
    path(
        'nearest_courses/',
        views.NearestCourses.as_view(),
        name='nearest_courses'
    ),
    path('teacher/<int:pk>/', views.OneTeacher.as_view(), name='teacher'),
    path(
        'teacher/<int:pk>/add_to_favorite/',
        views.AddTeacherToFavorite.as_view(),
        name='add_teacher_to_favorite'
    ),
    path(
        'teacher/<int:pk>/delete_from_favorite/',
        views.DeleteTeacherFromFavorite.as_view(),
        name='delete_teacher_from_favorite'
    ),
    path('student/<int:pk>/', views.OneStudent.as_view(), name='student'), #
    path('my_profile/', views.MyProfile.as_view(), name='my_profile'),
    path('course/<int:pk>/join/', views.JoinCourse.as_view(), name='join_the_course'),
    path('course/<int:pk>/leave/', views.LeaveCourse.as_view(), name='leave_the_course'),
    path('search/', views.SearchList.as_view(), name='search'),
    path('student_profile/', views.UpdateStudentProfile.as_view(), name='student_profile'),
    path('teacher_profile', views.UpdateTeacherProfile.as_view(), name='teacher_profile')
]
