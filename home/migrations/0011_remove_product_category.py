# Generated by Django 3.0.11 on 2021-01-10 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
