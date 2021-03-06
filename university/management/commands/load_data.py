from django.core.management.base import BaseCommand
from mixer.backend.django import mixer


class Command(BaseCommand):
    prices = (p for p in [15000, 20000, 30000, 40000, 50000, 60000])

    def handle(self, *args, **options):
        mixer.cycle(5).blend(
            'university.Course',
            price=Command.prices,
        )
        mixer.cycle(15).blend(
            'university.StudentCourse',
            course=mixer.SELECT,
            student__user__user_type=1
        )
        mixer.cycle(15).blend(
            'university.TeacherCourse',
            course=mixer.SELECT,
            teacher__user__user_type=2,
            teacher__user__age=50,
            teacher__year_experience=20,
            teacher__is_phd=mixer.RANDOM,
            count_lessons=(c for c in range(1, 20))
        )
        mixer.cycle(10).blend(
            'university.FavoriteTeachers',
            student=mixer.SELECT,
            teacher=mixer.SELECT
        )
