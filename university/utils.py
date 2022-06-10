from django.core.exceptions import ValidationError


def validate_teacher_year_experience(value):
    if 1 >= value >= 50:
        raise ValidationError("Некорректное значение опыта")
