# Generated by Django 2.2.13 on 2020-08-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0053_auto_20200813_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='censussubdivision',
            name='low_income_status_0_to_17',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='low_income_status_18_to_64',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='low_income_status_65_and_over',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='median_total_household_income',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='median_total_household_income_one_person',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='median_total_household_income_two_or_more_person',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_100000_to_149999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_10000_to_19999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_150000_and_over',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_20000_to_29999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_30000_to_39999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_40000_to_49999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_50000_to_59999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_60000_to_69999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_70000_to_79999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_80000_to_89999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_90000_to_99999',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='censussubdivision',
            name='total_income_under_10000',
            field=models.IntegerField(null=True),
        ),
    ]