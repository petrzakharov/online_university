from django.contrib import admin

from university.models import *

admin.site.register(User)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(FavoriteTeachers)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(TeacherCourse)
admin.site.register(StudentCourse)
