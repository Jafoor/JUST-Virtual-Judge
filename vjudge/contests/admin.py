from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Contest)
admin.site.register(Ranklist)
admin.site.register(Submission)
