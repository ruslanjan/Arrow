# Generated by Django 2.2.5 on 2019-10-18 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0009_auto_20191019_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemsetsubmission',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problemset.ProblemsetUserProfile'),
        ),
        migrations.AlterField(
            model_name='problemsetusertaskprofile',
            name='user_profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='problemset.ProblemsetUserProfile'),
        ),
    ]
