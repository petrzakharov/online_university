from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from university.models import Course, CourseCategory, TeacherProfile


class URLTests(TestCase):
    def setUp(self):
        super().setUp()
        self.authorized_client_user.force_login(URLTests.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        course_category = CourseCategory.objects.create(title='dev')
        cls.course = Course.objects.create(
            title='Тестовый курс',
            description='Тестовый текст',
            start_date='2022-01-01',
            end_date='2022-01-02',
            published_date='2022-01-02',
            category=course_category,
            price=20000,
        )
        cls.user = User.objects.create_user(username='user123', user_picture='media/user_pictures/1.png', user_type=1)
        cls.user_teacher_type = User.objects.create_user(
            username='teacher123',
            user_type=2,
            user_picture='media/user_pictures/1.png'
        )
        cls.teacher = TeacherProfile.objects.get(user=cls.user_teacher_type)
        cls.guest_client = Client()
        cls.authorized_client_user = Client()
        cls.user_urls = {
            reverse("index"): 'university/index.html',
            reverse("all_teachers"): 'university/teachers_new.html',
            reverse("nearest_courses"): 'university/courses_new.html',
            '/search/?search=test': 'university/courses_new.html',
            reverse("user_profile"): 'university/user_profile.html',
            reverse("teacher_profile"): 'university/user_profile.html',
            reverse(
                "teacher",
                kwargs={"pk": URLTests.teacher.id}
            ): 'university/about_teacher.html',
            reverse(
                "student",
                kwargs={
                    "pk": URLTests.user.id
                }
            ): 'university/about_student.html',
        }

    def test_templates(self):
        for reverse_name, template in URLTests.user_urls.items():
            with self.subTest(reverse_name):
                response = URLTests.authorized_client_user.get(reverse_name)
                self.assertTemplateUsed(response, template)
