# Generated by Django 5.0.6 on 2024-06-07 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='issue_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
