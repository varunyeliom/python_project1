# Generated by Django 4.2.1 on 2023-07-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_records_rename_course_attendance_courseandyear_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub1att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub1held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub2att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub2held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub3att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub3held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub4att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem1sub4held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub1att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub1held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub2att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub2held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub3att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub3held',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub4att',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sem2sub4held',
            field=models.IntegerField(max_length=100),
        ),
    ]
