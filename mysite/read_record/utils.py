import datetime
from .models import *
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType

def read_record_read(request, obj):

    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        #总计数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        #每日计数+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

#获取七天内每一天的博客阅读数
def get_seven_days_read(content_type):
    today = timezone.now().date()
    dates=[]
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

#获取今天热门博客显示前七条
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]

#获取昨天热门博客显示前七条
def get_yestertoday_hot_data(content_type):
    today = timezone.now().date()
    yestertoday = today-datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yestertoday).order_by('-read_num')
    return read_details[:7]

#获取7天热门博客显示前七条
def get_week_hot_data(content_type):
    today = timezone.now().date()
    date = today-datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gt=date)\
        .annotate(read_num_sum=Sum('read_num')).order_by('-read_num')
    return read_details[:7]