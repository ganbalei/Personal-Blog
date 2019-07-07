from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from read_record.utils import get_seven_days_read, get_today_hot_data,get_yestertoday_hot_data,get_week_hot_data


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
    return render(request, 'home.html', context)

