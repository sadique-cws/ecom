# Generated by Django 2.2.8 on 2020-05-06 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200506_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='qty',
        ),
    ]
