# Generated by Django 4.0.6 on 2022-09-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_image'),
        ),
    ]
