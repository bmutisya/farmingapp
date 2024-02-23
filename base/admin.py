from django.contrib import admin
from .models import Animal,AnimalHealth,MilkRecord

# Register your models here.
admin.site.register(Animal)
admin.site.register(AnimalHealth)
admin.site.register(MilkRecord)