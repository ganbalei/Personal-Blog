from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse

@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息，注册
    if kwargs['created'] == True:
        verb = '注册成功，更多精彩内容等你发现'
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, action_object=instance, url=url)
