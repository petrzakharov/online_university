from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(17), MaxValueValidator(90)],
        blank=True,
        null=True
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    user_picture = models.ImageField(
        'Фотография',
        upload_to='user_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
