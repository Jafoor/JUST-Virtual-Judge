from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Problem(models.Model):
    pid = models.CharField(max_length = 10, default = "1")
    ptitle = models.CharField(max_length = 100)
    ptimelimit = models.IntegerField()
    pmemorylimit = models.IntegerField()
    pdescription = models.TextField()
    pinput = models.TextField()
    poutput = models.TextField()
    pexinput = models.TextField()
    pexoutput = models.TextField()
    ptags = models.TextField(null = True)
    ptype = models.CharField(max_length = 100)
    pnote = models.TextField(null = True)
    pshow = models.CharField(max_length = 10, default = "No")

    def __str__(self):
        return self.ptitle
