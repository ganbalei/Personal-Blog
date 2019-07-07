from .models import *
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.

#更新评论区
def update_comment(request):

    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        #检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        #判断是否是回复他人的消息
        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['reply_to'] = comment.reply_to.get_nickname_or_username() if parent else ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root else ''

    else:
        #return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
