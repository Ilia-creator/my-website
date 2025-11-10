from django.contrib import admin
from .models import Hamster

@admin.register(Hamster)
class HamsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# Register your models here.
