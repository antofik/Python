# coding=utf-8
import os
from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    main_photo = models.ImageField(upload_to='dress-photos')
    main_photo_description = models.CharField(max_length=1024, blank=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{id}. {date} {name}'.format(id=self.id, date=self.date, name=self.name)
        
    @models.permalink
    def get_absolute_url(self):
        return 'dressgallery.views.dress_view', [str(self.id)]
        
    class Meta: 
        ordering = ['-created'] 
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турнир'

def get_image_path(instance, filename):
    return os.path.join('dress-photos', str(instance.dress.id), filename)
             
class Photo(models.Model):
    description = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to='dress-photos')
    tournament = models.ForeignKey(Tournament)

    def __unicode__(self):
        return '%s: %s' % (self.tournament.name, self.description[:64])
        
    class Meta: 
        ordering = ['tournament']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'    
