# Generated by Django 5.0.7 on 2024-10-17 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_trainingcompanydetails_trainingcompanydept_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='company_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='placement',
            name='job_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
