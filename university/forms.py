from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from . import models


class TeacherProfileForm(forms.ModelForm):
    logo = forms.ImageField(
        widget=forms.FileInput,
    )

    class Meta:
        model = models.TeacherProfile
        fields = (
            "user",
            "is_phd",
            "description",
            "year_experience",
        )
        # labels = {
        #     "name": "Название компании",
        #     "location": "География",
        #     "logo": "Логотип",
        #     "description": "Информация о компании",
        #     "employee_count": "Количество человек в компании",
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("user"),
                Column("is_phd"),
            ),
            Row(
                Column("description"),
            ),
            FieldWithButtons(
                "year_experience",
                StrictButton("Загрузить", type="submit", css_class="btn btn-info px-4"),
            ),
        )


class CourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "category",
            "price",
        )
        # labels = {
        #     "name": "Название компании",
        #     "location": "География",
        #     "logo": "Логотип",
        #     "description": "Информация о компании",
        #     "employee_count": "Количество человек в компании",
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("title"),
                Column("description"),
                Column("start_date"),
                Column("end_date"),
                Column("category"),
                Column("price"),
            ),
        )
