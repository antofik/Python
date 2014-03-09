from django import forms 
from models import *

class MeasuresForm(forms.Form):
    def __init__(self,question, *args, **kwargs):
        super(MeasuresForm, self).__init__(*args, **kwargs)

        measureTypes = MeasureType.objects.all()      
        i = 1
        for measure in measureTypes:
            self.fields['measure_%s' % i] = forms.IntegerField();
            self.fields['measure_id_%s' % i] = forms.IntegerField(widget=forms.HiddenInput, initial=measure.id)
            i++