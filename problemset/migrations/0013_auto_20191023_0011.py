# Generated by Django 2.2.5 on 2019-10-22 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0012_auto_20191019_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemsetTaskTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='problemsettask',
            name='tags',
            field=models.ManyToManyField(related_name='tasks', to='problemset.ProblemsetTaskTag'),
        ),
    ]