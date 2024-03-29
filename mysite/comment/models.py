from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    #发表评论的人
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    #回复的那条评论的是谁发的第一条
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    #回复哪一条评论
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    #回复谁
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def get_url(self):
        return self.content_object.get_url()

    def get_user(self):
        return self.user

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']



