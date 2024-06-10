# Generated by Django 5.0.6 on 2024-06-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_skill_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
