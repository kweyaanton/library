# Generated by Django 4.0.5 on 2022-07-12 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]