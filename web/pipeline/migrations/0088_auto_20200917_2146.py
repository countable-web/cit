# Generated by Django 2.2.13 on 2020-09-17 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0087_auto_20200914_2209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='power_pop_2km_capacity',
            new_name='pop_2km_capacity',
        ),
        migrations.RenameField(
            model_name='community',
            old_name='power_remaining_pop_capacity',
            new_name='remaining_pop_capacity',
        ),
    ]