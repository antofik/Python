from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    user        = models.ForeignKey(User)
    title   	= models.CharField(max_length=128, verbose_name='Название заказа')
    text    	= models.CharField(max_length=1024, verbose_name='Описание заказа')
    code    	= models.CharField(max_length=32, verbose_name='Код заказа')
    added   	= models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    date_ready	= models.DateTimeField(auto_now=False, verbose_name='Дата пошивки')
    
    def __unicode__(self):
        return self.title
        
    class Meta: 
        ordering = ['added'] 
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

