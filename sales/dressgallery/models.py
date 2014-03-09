# coding=utf-8
import os
from django.db import models
from djangoratings.fields import AnonymousRatingField

class Dress(models.Model):
    DRESS_TYPES = (
        (u"Стандартное", u"Стандартное"),
        (u"Латинское", u"Латинское"),
        (u"Другое", u"Другое"),
    )
    
    DANCER_CATEGORY = (
        (u"Ювеналы", u"Ювеналы"),
        (u"Юниоры", u"Юниоры"),
        (u"Молодёжь", u"Молодёжь"),
        (u"Взрослые", u"Взрослые"),
    )

    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=128, choices = DRESS_TYPES)
    fio = models.CharField(max_length=128)
    email = models.EmailField()
    category = models.CharField(max_length=128, choices = DANCER_CATEGORY)
    color = models.CharField(max_length=128)
    size = models.CharField(max_length=128)
    height = models.CharField(max_length=128)
    svarovsky = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    cost = models.CharField(max_length=128)
    discount = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=128)
    vk = models.URLField(blank=True)
    place = models.CharField(max_length=1024)
    main_photo = models.ImageField(upload_to='dress-photos')
    main_photo_description = models.CharField(max_length=1024, blank=True)
    
    complains = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=True)
    access_key = models.CharField(max_length=16)
    
    views = models.IntegerField(default=0)
    buy_tries = models.IntegerField(default=0)
    rating = AnonymousRatingField(range=5, allow_anonymous=True, use_cookies=True) 
    
    def __unicode__(self):
        return u'{id}. {fio} {description}'.format(id=self.id, fio=self.fio, description=self.description)
        
    @models.permalink
    def get_absolute_url(self):
        return ('dressgallery.views.dress_view', [str(self.id)])
        
    class Meta: 
        ordering = ['-created'] 
        verbose_name = 'Платье'
        verbose_name_plural = 'Платья'                   

def get_image_path(instance, filename):
    return os.path.join('dress-photos', str(instance.dress.id), filename)
             
class Photo(models.Model):
    GALLERY_CHOICES = (
        (u"DressOnly", u"Только платье"),
        (u"OnGirl", u"Платье на хозяйке"),
        (u"InDance", u"Платье в танце"),
        (u"Other", u"Другое"),
    )

    description = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='dress-photos')
    gallery = models.CharField(max_length=128, choices = GALLERY_CHOICES)
    dress = models.ForeignKey(Dress)
    is_main = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s: %s' % (self.dress.name, self.description)
        
    class Meta: 
        ordering = ['dress'] 
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'    
    
class Reply(models.Model):
    dress = models.ForeignKey(Dress)
    date = models.DateTimeField()
    ip = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    email = models.EmailField()
    fio = models.CharField(max_length=128)
    message = models.TextField(blank=True)
    email_delivered = models.BooleanField(default=False)
    sms_delivered = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s %s %s' % (self.dress.name, self.fio, self.email, self.email_delivered)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'




