USERS_FAKE = [{
    'age': 20, 'first_name': 'John', 'last_name': 'Doe',
    'email': 'johndoe@gmail.com', 'user_type': 1
},
    {
        'age': 50, 'first_name': 'Ivan', 'last_name': 'Ivanov',
        'email': 'ivan@gmail.com', 'user_type': 2
    },
]

STUDENT_PROFILE_FAKE = [
    {
        'user': USERS_FAKE[0],
    },
]

TEACHER_PROFILE_FAKE = [
    {
        'user': USERS_FAKE[1], 'is_phd': True, 'degree': 'Какие-то регалии',
        'year_experience': 22
    },
]


COURSE_FAKE = [
    {
        'title': 'Разработка WEB приложений на Python',
        'description': 'Научим за 1 день.',
        'start_date': '2022-11-11',
        'end_date': '2022-11-12',
        'category': 'dev',
        'price': 99999,
        'student': USERS_FAKE[0],
        'teacher': USERS_FAKE[1],

    },
]
