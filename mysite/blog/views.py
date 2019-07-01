from django.shortcuts import render, get_object_or_404, render_to_response
from .models import *
from read_record.utils import read_record_read
from comment.models import Comment
from comment.forms import CommentForm
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Count
# Create your views here.

def get_blog_list_common_data(request, blogs):

    #每10篇文章进行分页
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOG_NUMBER)

    #获取页码参数
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    #显示当前页码的前后三页
    page_range = [x for x in range(int(page_num)-3, int(page_num)+3) if 0 < x < paginator.num_pages]

    # 页数不够则不实现
    if page_range:
        #加上省略号页码标记
        if page_range[0] - 1 >= 3:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 3:
            page_range.append('...')
        #加上首页和尾页
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)

    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'day', order='DESC')
    print(blog_dates)
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
        created_time__month=blog_date.month, created_time__day=blog_date.day).count()
        blog_dates_dict[blog_date] = blog_count
        print(blog_dates_dict)


    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict

    return context


def blog_list(request):

    blogs = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs)

    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):

    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_record_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    data = {}
    data['content_type'] = blog_content_type
    data['object_id'] = blog_pk
    context['comment_form'] = CommentForm(initial=data)

    response= render(request, 'blog/blog_detail.html', context)
    #设置cookie (一分钟过期)
    response.set_cookie(read_cookie_key, 'true', max_age=60*1)

    return response

def blogs_type(request, blog_type_pk):

    blogs = Blog.objects.filter(blog_type=blog_type_pk)
    context = get_blog_list_common_data(request, blogs)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type

    return render_to_response('blog/blog_type.html', context)

def blog_date(request, year, month, day):

    blog_list = Blog.objects.filter(created_time__year=year, created_time__month=month, created_time__day=day)
    context = get_blog_list_common_data(request, blog_list)
    context['blog_with_date'] = '%s-%s-%s'%(year, month, day)

    return render_to_response('blog/blog_date.html', context)
