# Generated by Django 3.0.11 on 2021-01-10 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210110_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='status',
        ),
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
    ]
