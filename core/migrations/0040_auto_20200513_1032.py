# Generated by Django 2.2.8 on 2020-05-13 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20200512_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
