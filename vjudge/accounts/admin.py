from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)


#For migrating
#python3 manage.py migrate --run-sydbd
