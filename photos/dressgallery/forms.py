# coding=utf-8
from django import forms
from models import  Photo
from django.http import Http404

def clean_data(data):
    return data.replace('<','').replace('>','')

class DressForm(forms.Form): 
    ACCESS_KEY_LENGTH = 6
    
    textInput = forms.TextInput(attrs={'class': 'span4'})
    areaInput = forms.Textarea(attrs={'class': 'span4'})

    tournament_id = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=1024, label=u'Название турнира', widget=textInput)
    description = forms.CharField(max_length=1024, label=u'Описание турнира', widget=areaInput)
    photos_to_delete = forms.CharField(widget=forms.HiddenInput, max_length=1024, required=False)
    main_photo_id = forms.CharField(widget=forms.HiddenInput, max_length=1024, required=False)

    def __init__(self, count = 0 , *largs, **kwargs):
        if 'data' in kwargs.keys():
            self.POST = kwargs['data']

        super(DressForm, self).__init__(*largs, **kwargs)
        self.addImageFields(count)
    
    def load_test_data(self):
        for field in self.fields:
            value = field
            if field=='email':
                value = 'test@email.email'
            if field=='vk':
                value = 'http://ya.ru'
                
            self.fields[field].initial = value
            
    def load_data(self, tournament):
        for field in ['name', 'description', ]:
            try:
                self.fields[field].initial = getattr(tournament, field)
            except:
                pass
        self.photos = tournament.photo_set.all()
               
    def addImageFields(self, count):
        for i in xrange(1, count+1):
            self.fields['description%s' % i] = forms.CharField(label=u'Описание к фотографии', widget=forms.Textarea, max_length=128,required=False, help_text=u'Каждое фото нуждается в комментарии. Это не только подчеркнёт сильные стороны платья, но и доставит удовольствие читающим')

    def clean_main_photo_id(self):
        try:
            data = self.cleaned_data['main_photo_id']
            data = int(data)
        except:
            raise forms.ValidationError("Необходимо указать основную фотографию")
        return data

    def save_photos(self, dress):        
        if self.POST['photos_to_delete']:
            for i in [i for i in self.POST['photos_to_delete'].split('|')]:
                try:
                    id = int(i)
                    Photo.objects.filter(pk=id).delete() 
                except:
                    pass
    
        if self.POST:
            for key in self.POST.keys():
                if key.startswith('description'):
                    try:
                        id = int(key.replace('description',''))
                        photo = Photo.objects.get(pk=id)
                        photo.description = clean_data(self.POST[key])
                        photo.save()
                    except:
                        pass
        
        #un-assign old main photo
        try:
            main_photo = Photo.objects.filter(dress_id=dress.id).get(is_main=True)
            main_photo.is_main = False
            main_photo.save()
        except:        
            pass
        
        #assign new main photo
        try:
            main_photo_id = int(self.POST['main_photo_id'])
            main_photo = Photo.objects.get(pk=main_photo_id)
            main_photo.is_main = True
            main_photo.save()
        except:
            main_photo = None
        return main_photo
    
    
    def save(self, files, tournament):

        print 'save'*100

        if not tournament:
            raise Http404
            
        data = self.cleaned_data
        
        main_photo = self.save_photos(tournament)
        
        tournament.name = clean_data(data['name'])
        tournament.description = clean_data(data['description'])
        if main_photo:
            tournament.main_photo = main_photo.image
            tournament.main_photo_description = clean_data(main_photo.description)
        tournament.confirmed = True
        tournament.save()

        return tournament

        