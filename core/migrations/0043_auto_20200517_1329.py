# Generated by Django 2.2.4 on 2020-05-17 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200515_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='apartment_address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
        migrations.AddField(
            model_name='address',
            name='alternative_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('PUR', 'PURNEA')], default='PUR', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='contact',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='landmarks',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='address',
            name='locality',
            field=models.CharField(default='purnea city', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default='sadique', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='pincode',
            field=models.IntegerField(default=854302),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('BR', 'BIHAR'), ('WB', 'WEST BENGAL')], default='BR', max_length=200),
            preserve_default=False,
        ),
    ]