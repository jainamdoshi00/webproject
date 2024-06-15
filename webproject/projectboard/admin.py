from django.contrib import admin
from .models import Boardmodel,TaskModel

# Register your models here.
admin.site.register(Boardmodel)
admin.site.register(TaskModel)