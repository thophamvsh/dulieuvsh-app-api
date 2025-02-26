# Generated by Django 3.2.25 on 2025-02-20 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_title_xulysukientb_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xulysukientb',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='nhatkysukien',
            name='xulysukientbs',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.xulysukientb'),
        ),
    ]
