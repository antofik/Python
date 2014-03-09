from django.db import models

class Category(models.Model):
    order = models.IntegerField(verbose_name='Порядковый номер')
    name = models.CharField(max_length=128, verbose_name='Название')
    
    def __unicode__(self):
        return self.name
        
    class Meta: 
        ordering = ['order'] 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Item(models.Model):
    order = models.IntegerField(verbose_name='Порядковый номер')
    name = models.CharField(max_length=128, verbose_name='Название')
    price = models.CharField(max_length=64, verbose_name='Цена')
    category = models.ForeignKey(Category, verbose_name='Категория')
    
    def __unicode__(self):
        return self.name
        
    class Meta: 
        ordering = ['order'] 
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
    