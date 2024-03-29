# Generated by Django 4.1.5 on 2023-02-09 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_employee_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Do Not Hire', 'Do Not Hire'), ('Interview', 'Interview')], default='Interview', max_length=15),
        ),
    ]
