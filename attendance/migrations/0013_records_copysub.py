# Generated by Django 4.2.1 on 2023-07-11 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_rename_copyid_records_copyname_records_copycourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='copysub',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
