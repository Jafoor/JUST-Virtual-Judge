# Generated by Django 3.0.4 on 2020-05-14 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0007_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='problemid',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='problemtitle',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]