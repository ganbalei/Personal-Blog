from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('my_notifications/', my_notifications, name='my_notifications'),
    path('my_notification/<int:my_notification_pk>', my_notification, name='my_notification'),
    path('del_my_read_notifications/', del_my_read_notifications, name='del_my_read_notifications')
]