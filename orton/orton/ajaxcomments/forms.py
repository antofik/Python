# coding=utf-8
from django import forms
from django.contrib.comments.forms import CommentForm
from models import AjaxComment

class AjaxComentForm(CommentForm):
    profession = forms.CharField(max_length=100, help_text=u'Профессия')

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return AjaxComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(AjaxComentForm, self).get_comment_create_data()
        data['profession'] = self.cleaned_data['profession']
        data['url'] = u'orton.ru'
        return data