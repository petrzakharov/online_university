from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from .models import StudentProfile, TeacherProfile


@receiver(post_save, sender=User)  # sender - модель отправитель, # post_save - сигнал (при сохранении)
def create_student_or_teacher_profile(sender, instance, created, **kwargs):  # функция получатель сигнала
    if created:
        if instance.user_type == 1:
            StudentProfile.objects.create(user=instance)
        elif instance.user_type == 2:
            TeacherProfile.objects.create(user=instance)
