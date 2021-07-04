from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    uname = models.CharField(max_length = 50, default = "")
    pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)
    totalsub = models.IntegerField(default=0,null = True)
    totalac = models.IntegerField(default=0,null = True)
    totalwa = models.IntegerField(default=0,null = True)
    totaltle = models.IntegerField(default=0,null = True)
    totalme = models.IntegerField(default=0,null = True)
    university = models.CharField(max_length = 200, default = "")
    solverproblem = models.TextField(default="",null = True)
    participatedcon = models.TextField(default="",null = True)
    fb = models.CharField(max_length=100, default="",null = True)

    def __str__(self):
        return self.uname
