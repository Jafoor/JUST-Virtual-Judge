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

    def __str__(self):
        return self.user
