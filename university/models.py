from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

# todo Как сделать авторизацию по номеру телефона, например?

User = get_user_model()


class StudentProfile(models.Model):
    user = models.OneToOneField(
        'User', related_name='student_profile', on_delete=models.CASCADE
    )
    # todo добавить photo юзера для студента и препода


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        'User', related_name='student_profile', on_delete=models.CASCADE
    )
    is_phd = models.BooleanField()
    degree = models.CharField(max_length=30)
    year_experience = models.PositiveIntegerField(
        validators=[MaxValueValidator(30)]
    )
    # todo тут необходимо сделать проверку для поля year_experience не может быть больше, чем (возраст - 21)


class CourseCategory(models.Model):
    pass


class Course(models.Model):
    pass


class FavoriteTeachers(models.Model):
    pass


class Module(models.Model): # noqa будем считать количество прошедших модулей
    pass

