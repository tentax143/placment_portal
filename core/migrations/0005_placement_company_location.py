# Generated by Django 5.0.7 on 2024-10-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_placement_stipend_alter_placement_placement_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='company_location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
