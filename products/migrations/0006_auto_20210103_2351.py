# Generated by Django 3.1.4 on 2021-01-03 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_color_review_size_variants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='product',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='product',
            name='min',
        ),
        migrations.RemoveField(
            model_name='review',
            name='ip',
        ),
    ]