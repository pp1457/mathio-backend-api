# Generated by Django 4.2.7 on 2024-01-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontest',
            name='rated_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usercontest',
            name='unrated_score',
            field=models.IntegerField(default=0),
        ),
    ]
