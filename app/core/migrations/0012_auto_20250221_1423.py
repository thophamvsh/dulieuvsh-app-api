# Generated by Django 3.2.25 on 2025-02-21 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20250220_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nhatkysukien',
            name='xulysukientbs',
        ),
        migrations.AddField(
            model_name='nhatkysukien',
            name='xulysukientbs',
            field=models.ManyToManyField(to='core.Xulysukientb'),
        ),
    ]
