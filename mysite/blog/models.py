from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_record.models import ReadNumExpand

# Create your models here.

#博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


#blog的信息
class Blog(models.Model, ReadNumExpand):
    title = models.CharField(max_length=20)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField(config_name='my_config')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_user(self):
        return self.author

    def get_email(self):
        return self.author.email

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']

