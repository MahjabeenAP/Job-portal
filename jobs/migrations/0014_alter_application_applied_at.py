# Generated by Django 5.1.4 on 2025-03-15 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='applied_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
