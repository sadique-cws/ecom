# Generated by Django 2.2.4 on 2020-05-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20200517_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='alternative_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.TextField(max_length=200),
        ),
    ]
