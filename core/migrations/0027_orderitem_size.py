# Generated by Django 2.2.8 on 2020-05-12 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='S', max_length=10),
            preserve_default=False,
        ),
    ]
