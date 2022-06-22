import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Exists, OuterRef, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView

from .forms import TeacherProfileForm
from .models import Course, TeacherProfile, FavoriteTeachers, StudentProfile, StudentCourse
from .utils import ContextForCourse


class Index(ContextForCourse, TemplateView):
    template_name = 'university/index_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_courses = self.context_for_course()
        context = dict(list(context_courses.items()) + list(context.items()))
        return context
        # Неплохо бы добавить пагинацию, остальное ок


class Teachers(ListView):
    template_name = 'university/teachers_new.html'
    model = TeacherProfile
    allow_empty = True
    
    def get_queryset(self):
        queryset = TeacherProfile.objects.select_related('user').annotate(
            courses_count=Count('courses'), followers_count=Count('teacher_followers')
        )
        return queryset
        # добавить изображения в шаблоне, остальное ок


class NearestCourses(ContextForCourse, TemplateView):
    template_name = 'university/courses_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=30)
        context_courses = self.context_for_course(start_date=start_date, end_date=end_date)
        context = dict(list(context_courses.items()) + list(context.items()))
        return context
        # Было бы интересно сделать: вьюха принимает гет запрос с периодом дней за который надо вывести
        # курсы. Ссылка на эту вьюху есть на главной, "Стартует в ближайший месяц", "Стартует в ближайшие 2 месяца"


class OneTeacher(DetailView):
    model = TeacherProfile
    template_name = 'university/about_teacher.html'

    def get_queryset(self):
        queryset = TeacherProfile.objects.annotate(
            courses_count=Count('courses'), followers_count=Count('teacher_followers')
        ).select_related('user')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['followers'] = FavoriteTeachers.objects.filter(
            teacher=self.kwargs['pk']
        ).select_related('student__user').all()

        context['courses'] = Course.objects.filter(
            teacher=TeacherProfile.objects.get(id=self.kwargs['pk'])
        ).select_related('category').annotate(
            student_count=Count('student'),
            is_join_course=Exists(
                StudentCourse.objects.filter(
                    student=self.request.user.student_profile,
                    course_id=OuterRef('pk')
                )
            )
        )
        if self.request.user.is_anonymous or FavoriteTeachers.objects.filter(
                student__user=self.request.user,
                teacher=self.kwargs['pk']
        ).exists():
            context['is_follow'] = True
        return context


class AddTeacherToFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.get_or_create(teacher=teacher, student=student)
        return redirect('teacher', pk=pk)
        # разрешены только авторизованные пользователи-студенты, нужен пермишн


class DeleteTeacherFromFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.filter(teacher=teacher, student=student).delete()
        return redirect('teacher', pk=pk)
        # разрешены только авторизованные пользователи-студенты, нужен пермишн

        # После регистрации пользователя User с выбором типа пользователя должен создаваться в таблице StudentProfile
        # - важно! Сейчас этого не происходит автоматически.


class OneStudent(DetailView):
    model = StudentProfile
    template_name = 'university/about_student.html'

    def get_queryset(self):
        queryset = StudentProfile.objects.annotate(
            courses_count=Count('courses')
        ).select_related('user')
        return queryset


class JoinCourse(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = get_object_or_404(StudentProfile, user=self.request.user)
        StudentCourse.objects.create(student=student, course=course)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # разрешены только авторизованные пользователи-студенты, нужен пермишн
        # LoginRequiredMixin


class LeaveCourse(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = get_object_or_404(StudentProfile, user=self.request.user)
        StudentCourse.objects.filter(student=student, course=course).delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        # разрешены только авторизованные пользователи-студенты, нужен пермишн


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


class UpdateStudentProfile(LoginRequiredMixin, UpdateView):
    pass


# В зависимости от того имеет ли user StudentProfile или TeacherProfile в шаблоне base отображаем ссылку на нужную вьюху
# UpdateStudentProfile(UpdateView): доступно по student_profile/
    # Нужен пермишн - доступ только для студента
    # В этой вьюхе одна форма - для модели User
    # LoginRequiredMixin

class UpdateTeacherProfile(LoginRequiredMixin, View):
    pass
# UpdateTeacherProfile(UpdateView/View): доступно по teacher_profile/
    # Нужен пермишн доступ только для препода
    # Как-то в этой вьюхе совместить 2 формы - User + TeacherProfile,
    # возможно потребуется переписать на View
    # LoginRequiredMixin







class MyProfile(View):

    def user_type_for(self):
        pass
        # user_type, user_id = self.request.user.user_type, self.request.user.id
        # if user_type == 'teacher':
        #     form = TeacherProfileForm
        # else:
        #     form = StudentProfileForm

    def get(self, request):
        user_type, user_id = self.request.user.user_type, self.request.user.id
        if user_type == 'teacher':
            instance = TeacherProfile.objects.filter(user=self.request.user)
            form = TeacherProfileForm(instance=instance)
        # else:
        #     instance = StudentProfile.objects.filter(user=self.request.user)
        #     form = 'a'
        form = TeacherProfileForm()
        context = {'form': form}
        return render(request, "university/my_profile.html", context)

        # todo Тут нужно чтобы юзер мог обновить как модель Profile так и User, как это сделать

    def post(self, request):
        user_type, user_id = self.request.user.user_type, self.request.user.id
        if user_type == 'teacher':
            instance = TeacherProfile.objects.filter(user=self.request.user)
            form = TeacherProfileForm(request.POST, instance=instance)

        context = {'form': form}
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = request.user.company
            instance.save()
            context["status"] = "Вакансия обновлена"
        else:
            context["status"] = "Обновления не сохранены. Исправьте ошибки"
        return render(request, "university/my_profile.html", context)
        # Обновляем форму
        # Подставляем в нее пользователя
        # Переадресовываем на саксесс пейдж
