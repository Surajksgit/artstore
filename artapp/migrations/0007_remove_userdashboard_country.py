# Generated by Django 5.1.5 on 2025-04-06 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artapp', '0006_userdashboard_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdashboard',
            name='country',
        ),
    ]
