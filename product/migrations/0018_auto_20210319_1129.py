# Generated by Django 3.1.7 on 2021-03-19 04:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20210319_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfromshopee',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='productfromshopee',
            name='variants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None),
        ),
    ]
