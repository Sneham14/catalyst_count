# Generated by Django 3.2.11 on 2023-08-16 09:11

import catalyst_count_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst_count_app', '0003_alter_companydatamodel_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydatamodel',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to=catalyst_count_app.models.upload_path),
        ),
    ]