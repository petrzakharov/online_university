# Generated by Django 4.0.5 on 2022-06-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacherprofile',
            old_name='degree',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='course',
            name='published_date',
            field=models.DateField(blank=True),
        ),
    ]
