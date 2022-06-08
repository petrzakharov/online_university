from django.urls import path

import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"), # главная все курсы
    path("course/add", views.NearestCourses.as_view(), name="add_new_course"), # форма добавления нового курса, страница доступна админам
    path("teachers/", views.Teachers.as_view(), name="all_teachers"), # все учителя
    path(
        "nearest_courses/",
        views.NearestCourses.as_view(),
        name="nearest_courses"
    ), # ближайшие курсы, на странице должны быть фильтры и вьюха должна принимать гет запросы от них, количество дней за которые показать курсы
    path("teacher/<int:pk>", views.NearestCourses.as_view(), name="teacher"), # страница преподавателя, какие курсы ведет, биография
    path(
        "teacher/<int:pk>/add_to_favorite",
        views.NearestCourses.as_view(),
        name="add_teacher_to_favorite"
    ), # Вьюха принимает гет запрос и создает связь в таблице фэворитс
    path("student/<int:pk>", views.NearestCourses.as_view(), name="student"), # Страница о студенте - фио, фотка, сколько курсов прошел, какие в акивных, какие запланированы
    path(
        "student/<int:pk>/favorites",
        views.NearestCourses.as_view(),
        name="student_favorites"
    ), # Страница на которой показано на каких учителей подписался студент
]
