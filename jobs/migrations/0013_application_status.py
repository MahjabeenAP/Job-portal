# Generated by Django 5.1.4 on 2025-03-14 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_alter_job_experience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('selected', 'Selected'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
