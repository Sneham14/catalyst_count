# Generated by Django 3.2.11 on 2023-08-16 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst_count_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydatamodel',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
