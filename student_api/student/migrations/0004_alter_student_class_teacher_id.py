# Generated by Django 4.1 on 2022-08-24 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0003_alter_student_class_teacher_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="class_teacher_id",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]