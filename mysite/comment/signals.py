from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from .models import Comment
from django.utils.html import strip_tags

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.reply_to is None:
        # 评论
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':
            blog = instance.content_object
            verb = '{0}评论了你的《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
        else:
            raise Exception('unkown comment object type')
    else:
        # 回复
        recipient = instance.reply_to
        verb = '{0}回复了你的评论"{1}"'.format(instance.user.get_nickname_or_username(), strip_tags(instance.parent.text))

    url = instance.content_object.get_url() + '#comment_' + str(instance.pk)
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)
