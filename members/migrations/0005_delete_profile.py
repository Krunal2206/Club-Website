# Generated by Django 4.0.6 on 2022-09-15 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
