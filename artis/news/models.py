from django.db import models
import tinymce
from tinymce.models import HTMLField

class Item(models.Model):
    order	= models.IntegerField(verbose_name='Порядковый номер')
    title	= models.CharField(max_length=128, verbose_name='Название')
    excerpt	= HTMLField(verbose_name='Анонс')
    text	= HTMLField(verbose_name='Текст статьи')
    image	= models.ImageField(upload_to='cms/news', verbose_name='Картинка')
    added	= models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    
    def __unicode__(self):
        return self.title
        
    class Meta: 
        ordering = ['added'] 
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
