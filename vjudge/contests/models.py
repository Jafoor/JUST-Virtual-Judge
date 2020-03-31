from __future__ import unicode_literals
from django.db import models
# Create your models here.

class Contest(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length = 50)
    description = models.TextField(max_length = 200)
    password = models.TextField(null=True)
    rule_type = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Problem(models.Model):
    Contest = models.ForeignKey(Contest,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length=2000)
    input = models.CharField(max_length = 500)
    output = models.CharField(max_length = 500)
    note = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
