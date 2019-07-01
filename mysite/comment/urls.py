from django.urls import path
from .views import *


urlpatterns = [
    path('update_commnet/', update_comment, name='update_comment'),
]