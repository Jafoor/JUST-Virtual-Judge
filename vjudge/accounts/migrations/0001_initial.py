# Generated by Django 3.0.4 on 2020-05-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(default='', max_length=50)),
                ('picname', models.TextField(null=True)),
                ('picurl', models.TextField(default='-', null=True)),
                ('totalsub', models.IntegerField(default=0, null=True)),
                ('totalac', models.IntegerField(default=0, null=True)),
                ('totalwa', models.IntegerField(default=0, null=True)),
                ('totaltle', models.IntegerField(default=0, null=True)),
                ('totalme', models.IntegerField(default=0, null=True)),
                ('university', models.CharField(default='', max_length=200)),
                ('solverproblem', models.TextField(default='', null=True)),
                ('participatedcon', models.TextField(default='', null=True)),
                ('fb', models.CharField(default='', max_length=100, null=True)),
            ],
        ),
    ]