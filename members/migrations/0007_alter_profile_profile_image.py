# Generated by Django 4.0.6 on 2022-09-16 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='profile_image/default.jpg', upload_to='profile_image'),
        ),
    ]
