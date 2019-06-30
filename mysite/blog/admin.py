from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(BlogType)
class BolgTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
    list_display_links = ['id', 'type_name']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'blog_type','get_read_num', 'author', 'created_time', 'last_updated_time']
    list_display_links = ['id','title', 'blog_type', 'get_read_num','author', 'created_time', 'last_updated_time']

