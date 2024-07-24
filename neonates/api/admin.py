from django.apps import apps
from django.contrib import admin
from .models import *


# Register your models here.
for model in apps.get_app_config('api').models.values():
    admin.site.register(model)