# Generated by Django 3.1.4 on 2021-01-03 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Categories',
        ),
    ]