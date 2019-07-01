from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_object','text', 'comment_time', 'user']
    list_display_links = ['content_object','text', 'comment_time', 'user']
