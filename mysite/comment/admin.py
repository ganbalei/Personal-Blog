from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'object_id', 'text', 'comment_time', 'user', 'root', 'parent']
    list_display_links = ['id', 'content_object', 'object_id', 'text', 'comment_time', 'user', 'root', 'parent']
