from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from .models import LikeRecord
from django.utils.html import strip_tags

@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    verb = ''
    # 博客点赞
    if instance.content_type.model == 'blog':
        blog = instance.content_object
        verb = '{0}点赞了你的《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
    #评论点赞
    elif instance.content_type.model == 'comment':
        comment = instance.content_object
        verb = '{0}点赞了你的评论"{1}"'.format(instance.user.get_nickname_or_username(), strip_tags(comment.text))

    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)
