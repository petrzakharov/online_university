from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from . import models


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = models.TeacherProfile
        fields = (
            "is_phd",
            "description",
            "year_experience",
        )
        labels = {
            "is_phd": "Есть ли докторская степень?",
            "description": "Расскажите о вашем преподавательском опыте",
            "year_experience": "Количество лет опыта",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("is_phd"),
                Column("year_experience"),
            ),
            Row(
                Column("description"),
            ),
            Submit('Отправить', 'Submit', css_class='button'),
        )


class UserForm(forms.ModelForm):
    user_picture = forms.ImageField(
        widget=forms.FileInput,
    )

    class Meta:
        model = models.User
        fields = (
            "user_picture",
            "age",
            "first_name",
            "last_name",
        )
        labels = {
            "user_picture": "Ваша фотография",
            "age": "Возраст",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("age"),
                Column("first_name"),
                Column("last_name"),
            ),
            FieldWithButtons(
                "user_picture",
                StrictButton("Загрузить", type="submit", css_class="btn btn-info px-4"),
            ),
        )
