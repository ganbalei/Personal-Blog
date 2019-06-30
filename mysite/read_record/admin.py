from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['content_object','read_num']
    list_display_links = ['content_object','read_num']

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['content_object','read_num','date']
    list_display_links = ['content_object','read_num','date']