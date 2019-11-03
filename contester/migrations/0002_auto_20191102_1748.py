# Generated by Django 2.2.5 on 2019-11-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contester', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestusertaskprofile',
            name='points_after_contest',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='contestusertaskprofile',
            name='solved_after_contest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contestusertaskprofile',
            name='tries_after_contest',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contestusertaskprofile',
            name='penalty',
            field=models.FloatField(default=0),
        ),
    ]
