# Generated by Django 2.2.6 on 2019-11-24 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_auto_20191124_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelcommit',
            name='photo',
        ),
    ]
