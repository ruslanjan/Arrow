# Generated by Django 2.2.5 on 2019-10-18 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0029_auto_20191017_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='max_memory_used',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='submission',
            name='max_time_used',
            field=models.FloatField(default=-1),
        ),
    ]
