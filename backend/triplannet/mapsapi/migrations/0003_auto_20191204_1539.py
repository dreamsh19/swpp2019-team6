# Generated by Django 2.2.6 on 2019-12-04 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapsapi', '0002_autocomplete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autocomplete',
            old_name='structured_formatted',
            new_name='structured_formatting',
        ),
    ]
