# Generated by Django 3.0.11 on 2021-01-10 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
