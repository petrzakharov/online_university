from django.core.exceptions import ValidationError
from django.db.models import Count, Exists, Prefetch, OuterRef

from university.models import TeacherProfile, Course, StudentCourse


def validate_teacher_year_experience(value):
    if 1 >= value >= 50:
        raise ValidationError("Некорректное значение опыта")


class ContextForCourse:
    def context_for_course(self, **kwargs):
        context = kwargs
        teacher_user = TeacherProfile.objects.select_related('user')
        if 'start_date' in context or 'end_date' in context:
            course_qs = Course.objects.filter(start_date__gte=context.get('start_date'), end_date__lte=context.get(
                'end_date'))
        elif 'q' in context:
            course_qs = Course.objects.filter(context.get('q'))
        else:
            course_qs = Course.objects.all()
        context['courses'] = course_qs.select_related('category').annotate(
            student_count=Count('student')
        ).prefetch_related(
            Prefetch('teacher', queryset=teacher_user)
        ).order_by('-student_count')
        if not self.request.user.is_anonymous and not len(TeacherProfile.objects.filter(user=self.request.user)):
            context['courses'] = context['courses'].annotate(
                is_join_course=Exists(
                    StudentCourse.objects.filter(
                        student=self.request.user.student_profile,
                        course_id=OuterRef('pk')
                    )
                )
            )
        return context
