# Generated by Django 5.1.4 on 2025-03-17 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_interview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interview_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
