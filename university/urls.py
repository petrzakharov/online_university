from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'), # главная все курсы
    # path('course/add', views.NearestCourses.as_view(), name='add_new_course'), # форма добавления нового курса, страница доступна админам
    path('teachers/', views.Teachers.as_view(), name='all_teachers'), # все учителя
    path(
        'nearest_courses/',
        views.NearestCourses.as_view(),
        name='nearest_courses'
    ), # ближайшие курсы, на странице должны быть фильтры и вьюха должна принимать гет запросы от них, количество дней за которые показать курсы
    path('teacher/<int:pk>/', views.OneTeacher.as_view(), name='teacher'), # страница преподавателя, какие курсы ведет,
    # биография
    path(
        'teacher/<int:pk>/add_to_favorite/',
        views.AddTeacherToFavorite.as_view(),
        name='add_teacher_to_favorite'
    ), # Вьюха принимает гет запрос и создает связь в таблице фэворитс
    path(
        'teacher/<int:pk>/delete_from_favorite/',
        views.DeleteTeacherFromFavorite.as_view(),
        name='delete_teacher_from_favorite'
    ),
    path('student/<int:pk>/', views.OneStudent.as_view(), name='student'), # Страница о студенте - фио, фотка,
    # сколько курсов 
    # прошел, какие в акивных, какие запланированы
    # на каких учителей подписался студент

    path('my_profile/', views.MyProfile.as_view, name='my_profile'),
    # обновление информации о студенте или преподавателе
    path('add_course/', views.AddCourse.as_view, name='add_new_course'),
    #форма добавления нового курса, должна быть доступна преподавателям и администратору
    path('course/<int:pk>/join/', views.JoinCourse.as_view, name='join_the_course'),
    path('course/<int:pk>/leave/', views.LeaveCourse.as_view, name='leave_the_course'),


    # Дополнительно форма которая позволяет учителям добавиться на определенный курс
    # Дополнительно роут для формы поиска, переход на новую страницу
]
