# Generated by Django 3.0.4 on 2020-05-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20200508_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='pid',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
