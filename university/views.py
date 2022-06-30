import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView, TemplateView,
                                  UpdateView, View)

from accounts.models import User

from .forms import TeacherProfileForm, UserForm
from .models import (Course, FavoriteTeachers, StudentCourse, StudentProfile,
                     TeacherProfile)
from .permissions import OnlyForStudents, OnlyForTeachers
from .utils import ContextForCourse


class Index(ContextForCourse, TemplateView):
    template_name = 'university/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_courses = self.context_for_course()
        context = dict(list(context_courses.items()) + list(context.items()))
        return context


class Teachers(ListView):
    template_name = 'university/teachers_new.html'
    model = TeacherProfile
    allow_empty = True

    def get_queryset(self):
        queryset = TeacherProfile.objects.select_related('user').annotate(
            courses_count=Count('courses'), followers_count=Count('teacher_followers')
        )
        return queryset


class NearestCourses(ContextForCourse, TemplateView):
    template_name = 'university/courses_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=30)
        context_courses = self.context_for_course(start_date=start_date, end_date=end_date)
        context = dict(list(context_courses.items()) + list(context.items()))
        return context


class OneTeacher(LoginRequiredMixin, ContextForCourse, DetailView):
    login_url = '/login/'
    model = TeacherProfile
    template_name = 'university/about_teacher.html'

    def get_queryset(self):
        queryset = TeacherProfile.objects.annotate(
            courses_count=Count('courses'), followers_count=Count('teacher_followers')
        ).select_related('user')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(TeacherProfile, pk=self.kwargs['pk'])
        context['followers'] = FavoriteTeachers.objects.filter(
            teacher=self.kwargs['pk']
        ).select_related('student__user').all()
        if self.request.user.is_anonymous or FavoriteTeachers.objects.filter(
                student__user=self.request.user,
                teacher=self.kwargs['pk']
        ).exists():
            context['is_follow'] = True
        context_courses = self.context_for_course(teacher=teacher)
        context = dict(list(context_courses.items()) + list(context.items()))
        return context


class AddTeacherToFavorite(LoginRequiredMixin, OnlyForStudents, View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.get_or_create(teacher=teacher, student=student)
        return redirect('teacher', pk=pk)


class DeleteTeacherFromFavorite(LoginRequiredMixin, OnlyForStudents, View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.filter(teacher=teacher, student=student).delete()
        return redirect('teacher', pk=pk)


class OneStudent(DetailView):
    model = StudentProfile
    template_name = 'university/about_student.html'

    def get_queryset(self):
        queryset = StudentProfile.objects.annotate(
            courses_count=Count('courses')
        ).select_related('user')
        return queryset


class JoinCourse(LoginRequiredMixin, OnlyForStudents, View):
    login_url = '/login/'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = get_object_or_404(StudentProfile, user=self.request.user)
        StudentCourse.objects.create(student=student, course=course)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LeaveCourse(LoginRequiredMixin, OnlyForStudents, View):
    login_url = '/login/'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = get_object_or_404(StudentProfile, user=self.request.user)
        StudentCourse.objects.filter(student=student, course=course).delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class SearchList(ContextForCourse, View):
    template_name = 'university/courses_new.html'

    def get(self, request):
        query = self.request.GET.get("search")
        if query:
            q = (
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__title__icontains=query)
            )
            context = self.context_for_course(q=q, search_title='Результаты поиска')
            return render(request, self.template_name, context)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    form_class = UserForm
    template_name = 'university/user_profile.html'
    success_url = reverse_lazy("user_profile")

    def get_object(self, query_set=None):
        return User.objects.get(pk=self.request.user.pk)


class UpdateTeacherProfile(LoginRequiredMixin, OnlyForTeachers, UpdateView):
    login_url = "/login/"
    form_class = TeacherProfileForm
    template_name = 'university/user_profile.html'
    success_url = reverse_lazy("teacher_profile")

    def get_object(self, query_set=None):
        return TeacherProfile.objects.get(user=self.request.user)
