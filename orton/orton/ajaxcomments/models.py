# coding=utf-8
from django.db import models
from django.contrib.comments.models import Comment

class AjaxComment(Comment):
    profession = models.CharField(max_length=100)

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

