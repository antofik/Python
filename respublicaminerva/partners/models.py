from django.db import models

class Item(models.Model):
    order	= models.IntegerField(verbose_name='Порядковый номер')
    title	= models.CharField(max_length=128, verbose_name='Название')
    url     = models.CharField(max_length=256, verbose_name='Ссылка')
    excerpt	= models.CharField(max_length=256, verbose_name='Анонс')
    text	= models.CharField(max_length=1024, verbose_name='Текст статьи')
    image	= models.ImageField(upload_to='cms/partners', verbose_name='Картинка')
    added	= models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    
    def __unicode__(self):
        return self.title
        
    class Meta: 
        ordering = ['added'] 
        verbose_name = 'Партнеры'
        verbose_name_plural = 'Партнеры'
    