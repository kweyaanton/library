# Generated by Django 4.0.5 on 2022-08-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_status_borrowed_book_fine_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowed_book',
            name='date_returned',
        ),
        migrations.AddField(
            model_name='borrowed_book',
            name='pickup_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='borrowed_book',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]