# Generated by Django 4.1.5 on 2023-02-09 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('phone_number', 'date_of_birth')},
        ),
    ]
