# Generated by Django 2.2.2 on 2019-07-12 18:17

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0006_auto_20190530_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
