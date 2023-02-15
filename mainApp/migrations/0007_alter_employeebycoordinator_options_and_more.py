# Generated by Django 4.1.5 on 2023-02-15 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_delete_employeeapplicationstatusundefined_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeebycoordinator',
            options={'ordering': ['-status', '-date_created'], 'verbose_name': 'My employee'},
        ),
        migrations.AlterField(
            model_name='employee',
            name='application_status',
            field=models.CharField(choices=[('FrontDesk', 'FrontDesk'), ('No Application', 'No Application'), ('Regular Application', 'Regular Application'), ('Southeast', 'Southeast'), ('Human Resources', 'Human Resources'), ('Undefined', 'Undefined')], default='Undefined', max_length=20),
        ),
    ]
