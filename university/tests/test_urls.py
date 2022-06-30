from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from university.models import Course, CourseCategory, TeacherProfile


class URLTests(TestCase):
    def setUp(self):
        super().setUp()
        self.authorized_client_user.force_login(URLTests.user)
        self.authorized_client_teacher.force_login(URLTests.user_teacher_type)

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
        cls.user = User.objects.create_user(username='user123', user_type=1, user_picture='media/user_pictures/1.png')
        cls.user_teacher_type = User.objects.create_user(
            username='teacher123',
            user_type=2,
            user_picture='media/user_pictures/1.png'
        )
        cls.teacher = TeacherProfile.objects.get(user=cls.user_teacher_type)
        cls.guest_client = Client()
        cls.authorized_client_user = Client()
        cls.authorized_client_teacher = Client()

        cls.teacher_urls = {
            reverse("index"): HTTPStatus.OK.value,
            reverse("all_teachers"): HTTPStatus.OK.value,
            reverse("nearest_courses"): HTTPStatus.OK.value,
            '/search/?search=test': HTTPStatus.OK.value,
            reverse("user_profile"): HTTPStatus.OK.value,
            reverse("teacher_profile"): HTTPStatus.OK.value,
            reverse(
                "teacher",
                kwargs={"pk": URLTests.teacher.id}
            ): HTTPStatus.OK.value,
            reverse(
                "add_teacher_to_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FORBIDDEN.value,
            reverse(
                "delete_teacher_from_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FORBIDDEN.value,
            reverse(
                "student",
                kwargs={
                    "pk": URLTests.user.id
                }
            ): HTTPStatus.OK.value,
            reverse(
                "join_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FORBIDDEN.value,
            reverse(
                "leave_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FORBIDDEN.value,
            }

        cls.user_urls = {
            reverse("index"): HTTPStatus.OK.value,
            reverse("all_teachers"): HTTPStatus.OK.value,
            reverse("nearest_courses"): HTTPStatus.OK.value,
            '/search/?search=test': HTTPStatus.OK.value,
            reverse("user_profile"): HTTPStatus.OK.value,
            reverse("teacher_profile"): HTTPStatus.FORBIDDEN.value,
            reverse(
                "teacher",
                kwargs={
                    "pk": URLTests.teacher.id
                }
            ): HTTPStatus.OK.value,
            reverse(
                "add_teacher_to_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "delete_teacher_from_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "student",
                kwargs={
                    "pk": URLTests.user.id
                }
            ): HTTPStatus.OK.value,
            reverse(
                "join_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "leave_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FOUND.value,
            }

        cls.anon_urls = {
            reverse("index"): HTTPStatus.OK.value,
            reverse("all_teachers"): HTTPStatus.OK.value,
            reverse("nearest_courses"): HTTPStatus.OK.value,
            '/search/?search=test': HTTPStatus.OK.value,
            reverse("user_profile"): HTTPStatus.FOUND.value,
            reverse("teacher_profile"): HTTPStatus.FOUND.value,
            reverse(
                "teacher",
                kwargs={
                    "pk": URLTests.teacher.id
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "add_teacher_to_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "delete_teacher_from_favorite",
                kwargs={
                    "pk": URLTests.teacher.id,
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "student",
                kwargs={
                    "pk": URLTests.user.id
                }
            ): HTTPStatus.OK.value,
            reverse(
                "join_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FOUND.value,
            reverse(
                "leave_the_course", kwargs={
                    "pk": URLTests.course.id
                }
            ): HTTPStatus.FOUND.value,
        }

    def test_urls_for_teacher(self):
        for url, code in URLTests.teacher_urls.items():
            with self.subTest(url):
                response = URLTests.authorized_client_teacher.get(url)
                self.assertEqual(response.status_code, code, url)

    def test_urls_for_user(self):
        for url, code in URLTests.user_urls.items():
            with self.subTest(url):
                response = URLTests.authorized_client_user.get(url)
                self.assertEqual(response.status_code, code, url)

    def test_urls_for_anon(self):
        for url, code in URLTests.anon_urls.items():
            with self.subTest(url):
                response = URLTests.guest_client.get(url)
                self.assertEqual(response.status_code, code, url)
