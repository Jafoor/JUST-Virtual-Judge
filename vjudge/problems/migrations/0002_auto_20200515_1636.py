# Generated by Django 3.0.4 on 2020-05-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='psinput',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='psoutput',
            field=models.TextField(blank=True, null=True),
        ),
    ]
