from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    uname = models.CharField(max_length = 50, default = "")
    pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)
    totalsub = models.IntegerField(default=0,blank=True,null = True)
    totalac = models.IntegerField(default=0,blank=True,null = True)
    totalwa = models.IntegerField(default=0,blank=True,null = True)
    totaltle = models.IntegerField(default=0,blank=True,null = True)
    totalme = models.IntegerField(default=0,blank=True,null = True)
    university = models.CharField(max_length = 200,blank=True, default = "")
    solverproblem = models.TextField(default="",blank=True, null = True)
    participatedcon = models.TextField(default="",blank=True,null = True)
    fb = models.CharField(max_length=100, default="",blank=True,null = True)

    def __str__(self):
        return self.uname
