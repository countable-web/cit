# Generated by Django 2.2.13 on 2020-09-30 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0097_mayor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mayor',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='datasource',
            name='external_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='source',
            field=models.CharField(choices=[('internal', 'Provided by Network BC team'), ('databc', 'BC Data Catalogue'), ('statscan', 'Statistics Canada')], max_length=127, null=True),
        ),
    ]