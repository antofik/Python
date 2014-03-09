from django import forms

class PollForm(forms.Form):
    choice_id = forms.CharField()
