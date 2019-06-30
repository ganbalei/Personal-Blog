from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<int:blog_pk>', blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', blogs_type, name='blog_type'),
    path('date/<int:year>/<int:month>/<int:day>', blog_date, name='blog_date'),
]