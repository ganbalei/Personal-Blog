from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from read_record.utils import get_seven_days_read, get_today_hot_data,get_yestertoday_hot_data,get_week_hot_data


def home(request):

    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read(blog_content_type)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    print(context['today_hot_data'])
    context['yestertoday_hot_data'] = get_yestertoday_hot_data(blog_content_type)
    context['week_hot_data'] = get_week_hot_data(blog_content_type)
    print(context['week_hot_data'])
    return render_to_response('home.html', context)


