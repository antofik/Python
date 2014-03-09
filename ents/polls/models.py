from django.db import models
from django.core.urlresolvers import reverse

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def url(self):
        return '/test/%s/' % self.id


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    added = models.DateTimeField('date added')
