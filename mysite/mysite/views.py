from django.shortcuts import render_to_response, render,redirect
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from read_record.utils import get_seven_days_read, get_today_hot_data,get_yestertoday_hot_data,get_week_hot_data
from django.urls import reverse
from .forms import *

def home(request):

    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read(blog_content_type)

    #获取7天热门博客的缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_week_hot_data(blog_content_type)
        cache.set('week_hot_data', week_hot_data, 60*60)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yestertoday_hot_data'] = get_yestertoday_hot_data(blog_content_type)
    context['week_hot_data'] = get_week_hot_data(blog_content_type)
    return render_to_response('home.html', context)

def login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
                #验证再forms.py里面用clean方法操作
                user = login_form.cleaned_data['user']
                auth.login(request, user)
                #设置url自带返回路径
                return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
