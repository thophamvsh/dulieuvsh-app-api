# Generated by Django 3.2.25 on 2025-02-20 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20250220_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nhatkysukien',
            name='xulysukientbs',
        ),
        migrations.DeleteModel(
            name='Xulysukientb',
        ),
    ]
