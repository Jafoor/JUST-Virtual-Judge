from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Problem(models.Model):

    ptitle = models.CharField(max_length = 200, unique=True, default="")
    ptimelimit = models.IntegerField(null=True,blank=True)
    pmemorylimit = models.IntegerField(null=True,blank=True)
    pdescription = models.TextField(null=True,blank=True)
    pinput = models.TextField(null=True,blank=True)
    poutput = models.TextField(null=True,blank=True)
    #new add
    psinput = models.TextField(null=True,blank=True)
    psoutput = models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    pexinput = models.TextField(null=True,blank=True)
    pexoutput = models.TextField(null=True,blank=True)
    ptags = models.TextField(null=True,blank=True)
    ptype = models.CharField(max_length = 100)
    pnote = models.TextField(null = True)
    pshow = models.CharField(max_length = 10, default = "No")

    def __str__(self):
        return self.ptitle
class Submitted(models.Model):
    pid = models.CharField(max_length = 10, default = "")
    psubmit = models.IntegerField(default=0)
    pac = models.IntegerField(default=0)
    pwa = models.IntegerField(default=0)

    def __str__(self):
        return self.pid
