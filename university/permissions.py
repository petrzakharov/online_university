from django.contrib.auth.mixins import UserPassesTestMixin

from university.models import StudentProfile, TeacherProfile


class OnlyForStudents(UserPassesTestMixin):
    model = StudentProfile

    def test_func(self):
        return self.model.objects.filter(user=self.request.user).exists()


class OnlyForTeachers(UserPassesTestMixin):
    model = TeacherProfile

    def test_func(self):
        return self.model.objects.filter(user=self.request.user).exists()
