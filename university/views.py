import datetime

from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView

from .forms import TeacherProfileForm
from .models import Course, TeacherProfile, FavoriteTeachers, StudentProfile


class Index(TemplateView):
    template_name = 'university/index_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_user = TeacherProfile.objects.select_related('user')
        context['courses'] = Course.objects.select_related('category').annotate(student_count=Count(
            'student')).prefetch_related(Prefetch('teacher', queryset=teacher_user)).order_by('-student_count')
         # Неплохо бы добавить пагинацию, остальное ок
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
        # добавить изображения в шаблоне, остальное ок


class NearestCourses(ListView):
    template_name = 'university/courses_new.html'
    allow_empty = True

    def get_queryset(self):
        start_date, end_date = datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=30)
        teacher_user = TeacherProfile.objects.select_related('user')
        queryset = Course.objects.filter(
            start_date__gte=start_date, start_date__lte=end_date
        ).select_related('category').annotate(
            student_count=Count('student')
        ).prefetch_related(
            Prefetch('teacher', queryset=teacher_user)
        ).order_by('-start_date')
        return queryset

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
            student_count=Count('student')
        ).all()
        if FavoriteTeachers.objects.filter(student__user=self.request.user, teacher=self.kwargs['pk']).exists():
            context['is_follow'] = True
        return context


class AddTeacherToFavorite(View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.get_or_create(teacher=teacher, student=student)
        return redirect('teacher', pk=pk)


class DeleteTeacherFromFavorite(View):
    def get(self, request, pk):
        student = get_object_or_404(StudentProfile, user=self.request.user)
        teacher = get_object_or_404(TeacherProfile, pk=pk)
        FavoriteTeachers.objects.filter(teacher=teacher, student=student).delete()
        return redirect('teacher', pk=pk)

        # После регистрации пользователя User с выбором типа пользователя должен создаваться в таблице StudentProfile
        # - важно!
        # неавторизированный пользователь не может подписаться (логин реквайред)
        # запрет преподавателям подписываться на студентов
        # преподам не отображать кнопку + пермишен


class OneStudent(DetailView):
    model = StudentProfile
    template_name = 'university/about_student.html'
    # ok

    def get_queryset(self):
        queryset = StudentProfile.objects.annotate(
            courses_count=Count('courses')
        ).select_related('user')
        return queryset


class JoinCourse(View):
    def get(self, request, pk):
        pass
        # Создать связь
        # Получить курс, получить студента


class LeaveCourse(View):
    def get(self, request, pk):
        pass
        # Удалить связь
        # Получить курс, получить студента



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


class AddCourse(CreateView):
    template_name = 'university/add_course.html'
    form_class = 'asd'
