from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
# Create your models here.

class Contest(models.Model):
    ctitle = models.TextField(max_length = 50)
    cdescription = models.TextField(max_length = 200)
    cpassword = models.TextField(null=True)
    cbeginingdate = models.CharField(max_length = 20, default = "05/06/2020")
    cbeginingtime = models.CharField(max_length = 20, default = "07:00 PM")
    clength = models.CharField(max_length = 20)
    problems = models.TextField(default = "", null = True)
    contestants = models.TextField(default = "", null = True)
    def __str__(self):
        return self.ctitle

class Ranklist(models.Model):

    user = models.TextField(max_length=50)

    contestid = models.IntegerField(default=0)

    spb1 = models.BooleanField(default = False, null = True)
    spb2 = models.BooleanField(default = False, null = True)
    spb3 = models.BooleanField(default = False, null = True)
    spb4 = models.BooleanField(default = False, null = True)
    spb5 = models.BooleanField(default = False, null = True)
    spb6 = models.BooleanField(default = False, null = True)
    spb7 = models.BooleanField(default = False, null = True)
    spb8 = models.BooleanField(default = False, null = True)
    spb9 = models.BooleanField(default = False, null = True)
    spb10 = models.BooleanField(default = False, null = True)

    tpb1 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb2 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb3 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb4 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb5 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb6 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb7 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb8 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb9 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)
    tpb10 = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)

    totalac = models.IntegerField(default = 0, null=True)
    totalpoint = models.DecimalField(default=0.00,max_digits=19, decimal_places=4)

    def __str__(self):
        return self.user

class Submission(models.Model):

    submissionid = models.AutoField(primary_key=True)
    user = models.CharField(default = "", null = True, max_length=50)
    contestid = models.IntegerField(null = True)
    code = models.TextField(default="", null = True)
    language = models.CharField(default="", null = True,max_length=50)
    status = models.CharField(default="",null=True,max_length=50)
    problemid = models.CharField(default="",null=True,max_length=50)
    problemtitle = models.CharField(default="",null=True,max_length=100)

    def __str__(self):
        return self.user


"""
Initialize migrations for your existing models:

./manage.py makemigrations myapp
Fake migrations for existing models:

./manage.py migrate --fake myapp
Add the new field to myapp.models:

from django.db import models

class MyModel(models.Model):
    ... #existing fields
    newfield = models.CharField(max_length=100) #new field
Run makemigrations again (this will add a new migration file in migrations folder that add the newfield to db):

./manage.py makemigrations myapp
Run migrate again:

./manage.py migrate myapp

"""
