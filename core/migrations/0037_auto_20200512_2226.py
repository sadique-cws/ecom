# Generated by Django 2.2.8 on 2020-05-12 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20200512_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='variant',
        ),
        migrations.AddField(
            model_name='attribute',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='core.Item'),
        ),
    ]