from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Contest(models.Model):
    ctitle = models.TextField(max_length = 50)
    cdescription = models.TextField(max_length = 200)
    cpassword = models.TextField(null=True)
    cbeginingdate = models.CharField(max_length = 20, default = "05/06/2020")
    cbeginingtime = models.CharField(max_length = 20, default = "07:00 PM")
    clength = models.CharField(max_length = 20)
    def __str__(self):
        return self.ctitle
