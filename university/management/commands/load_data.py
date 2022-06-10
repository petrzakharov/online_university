from django.core.management.base import BaseCommand
from mixer.backend.django import mixer


class Command(BaseCommand):
    prices = (p for p in [15000, 20000, 30000, 40000, 50000, 60000])
    titles = (t for t in [
        'Курс по разработке на Python за 24 часа',
        'Выучи Solidity за 24 часа',
        'Стань Data Scientist за 48 часов',
        'Как двигать таски в Джире и имитрировать бурную деятельность',
        'Курс как стать QA за 1 час'
    ])

    def handle(self, *args, **options):
        # teachers = mixer.cycle(8).blend(
        #     'university.TeacherProfile', user__user_type=2, degree=mixer.FAKE, year_experience=20,
        #     user__age=50, is_phd=mixer.RANDOM
        #     # todo в идеале тут использовать изображения людей для аватарок, как?
        # )
        # students = mixer.cycle(20).blend(
        #     'university.StudentProfile', user__user_type=1,
        #     user__age=20
        # )
        courses = mixer.cycle(5).blend(
             'university.Course',
            price=Command.prices,
            #title=Command.titles #todo сделать тут уникальный выбор - функция и метод pop для списка
        )
        student_course = mixer.cycle(15).blend(
            'university.StudentCourse',
            course=mixer.SELECT,
            student__user__user_type=1
        )
        teacher_course = mixer.cycle(15).blend(
            'university.TeacherCourse',
            course=mixer.SELECT,
            teacher__user__user_type=2,
            teacher__user__age=50,
            teacher__year_experience=20,
            teacher__is_phd=mixer.RANDOM,
            count_lessons=(c for c in range(1, 20))
        )
        favorite_teachers = mixer.cycle(10).blend(
            'university.FavoriteTeachers',
            student=mixer.SELECT,
            teacher=mixer.SELECT
        )




