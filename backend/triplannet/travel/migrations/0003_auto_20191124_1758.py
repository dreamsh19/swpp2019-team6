# Generated by Django 2.2.6 on 2019-11-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20191124_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travelblocklist',
            options={},
        ),
        migrations.AlterModelOptions(
            name='traveldaylist',
            options={},
        ),
        migrations.AlterField(
            model_name='travelcommit',
            name='photo',
            field=models.ImageField(blank=True, height_field=500, upload_to='travel_photos/', width_field=500),
        ),
    ]
