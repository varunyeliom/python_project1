# Generated by Django 4.2.1 on 2023-06-07 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0003_delete_student2_student_attendances_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Student",
            new_name="Attendance",
        ),
    ]
