# Generated by Django 4.2.7 on 2024-01-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='score',
            field=models.IntegerField(default=5),
        ),
    ]
