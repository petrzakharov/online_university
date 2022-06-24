import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='student_profile', on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='teacher_profile', on_delete=models.CASCADE
    )
    is_phd = models.BooleanField(null=True, blank=True)
    description = models.CharField(max_length=30, null=True, blank=True)
    year_experience = models.PositiveIntegerField(
        null=True, blank=True
    )

    def clean(self, *args, **kwargs):
        if (self.year_experience + 18) > self.user.age:
            raise ValidationError('Your experience must be less or equal than age - 18 year!')

    def get_absolute_url(self):
        pass


class CourseCategory(models.Model):
    CATEGORY_CHOICES = (
        ('dev', 'Разработка'),
        ('design', 'Дизайн'),
        ('qa', 'Тестирование'),
        ('analytics', 'Аналитика'),
        ('management', 'Управление'),
    )
    title = models.CharField(choices=CATEGORY_CHOICES, max_length=50, unique=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    published_date = models.DateField(blank=True)
    category = models.ForeignKey('CourseCategory', related_name='course', on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    student = models.ManyToManyField('StudentProfile', through='StudentCourse', related_name='courses')
    teacher = models.ManyToManyField('TeacherProfile', through='TeacherCourse', related_name='courses')

    def clean(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValidationError('End date must be greater than start date')

    @property
    def status(self):  # todo проверить property (вывести в шаблон)
        today = datetime.date.today()
        if today < self.start_date:
            return 'planned'
        elif self.start_date <= today <= self.end_date:
            return 'active'
        return 'over'

    @property
    def days_till_course(self):
        return datetime.date.today() - self.start_date

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']


class StudentCourse(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='student_course')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)  # дата когда студент присоединился к курсу

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'], name='student_unique_courses'
            ),
        ]


class TeacherCourse(models.Model):
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    count_lessons = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'course'], name='teacher_unique_courses'
            ),
        ]


class FavoriteTeachers(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='student_favorites_teachers')
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE, related_name='teacher_followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'teacher'], name='unique_favorites_relation'
            )
        ]
