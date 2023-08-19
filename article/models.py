from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ArticlePost(models.Model):
    author = models.ForeignKey(User, verbose_name='文章作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='文章标题', max_length=200)
    body = models.TextField(verbose_name='文章内容')
    created = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    updated = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.title