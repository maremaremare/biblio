from django.contrib import admin
from .models import Homepage
from solo.admin import SingletonModelAdmin

admin.site.register(Homepage, SingletonModelAdmin)
