# Generated by Django 2.2.5 on 2019-11-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polygon', '0043_auto_20191030_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testgroup',
            name='index',
            field=models.IntegerField(),
        ),
    ]
