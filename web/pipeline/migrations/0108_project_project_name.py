# Generated by Django 2.2.13 on 2020-10-26 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0107_auto_20201025_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]