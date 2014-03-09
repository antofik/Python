from django import forms 
from models import Dress, Photo
from django.http import Http404
import random
from django.core.mail import send_mail
from django.conf import settings
       
def clean_data(data):
    return data.replace('<','').replace('>','')

class DressForm(forms.Form): 
    ACCESS_KEY_LENGTH = 6
    
    textInput = forms.TextInput(attrs={'class': 'span4'})
    areaInput = forms.Textarea(attrs={'class': 'span4'})

    dress_id = forms.CharField(widget=forms.HiddenInput)
    fio = forms.CharField(max_length=128, label=u'Ваше имя', help_text=u'Укажите ваше имя, чтобы люди знали, как к вам обращаться, когда будут звонить или писать', widget=textInput)
    email = forms.EmailField(label=u'Email', help_text=u'Укажите ваш почтовый ящик, чтобы вам смогли написать', widget=textInput)
    phone = forms.CharField(max_length=128, label=u'Телефон', help_text=u'Если у вас указан телефон, то вам смогут позвонить!', widget=textInput)
    description = forms.CharField(max_length=1024, label=u'Описание платья', help_text=u'Чем подробнее описание вашего платья, тем оно будет интереснее', widget=areaInput)
    type = forms.ChoiceField(choices = Dress.DRESS_TYPES, label=u'Тип платья', help_text=u'Если у вас не латинское и не стандартное платье, укажите "Другое"')
    category = forms.ChoiceField(choices = Dress.DANCER_CATEGORY, label=u'Категория', help_text=u'В какой категории можно танцевать в этом платье?')
    color = forms.CharField(max_length=128, label=u'Цвет', help_text=u'Да, не всегда можно выразить цвет красивого платья одним словом. Попробуйте двумя?', widget=textInput)
    size = forms.CharField(max_length=128, label=u'Размер', help_text=u'Если не помните точный размер, укажите диапазон. Например: 44-48', widget=textInput)
    height = forms.CharField(max_length=128, label=u'Рост, см', help_text=u'Для платья важен не только ваш рост, но и длинна ног, поэтому всегда указывайте диапазон, от и до.', widget=textInput)
    svarovsky = forms.CharField(max_length=128, label=u'Количество камней', help_text=u'Камушки... Главное достоинство современного платья, если нет других', widget=textInput)
    country = forms.CharField(max_length=128, label=u'Кто и где сшил', help_text=u'Ваше платье из Англии? Сшито у классного модельера? Так напишите про это!', widget=textInput)
    state = forms.CharField(max_length=128, label=u'Состояние платья', help_text=u'Камни не отклеиваются? Потёртостей не наблюдается?', widget=textInput)
    cost = forms.CharField(max_length=128, label=u'Стоимость, руб.', help_text=u'Укажите желаемую стоимость, например: 11000 руб, торг уместен', widget=textInput)
    photos_to_delete = forms.CharField(widget=forms.HiddenInput, max_length=1024, required=False)
    place = forms.CharField(max_length=1024, label=u'Где и когда можно примерять', help_text=u'Вы купите платье, не померяв? Вот и другие не купят. Так что, хорошо бы сразу придумать, где можно будет померять', widget=areaInput)
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
            
    def load_data(self, dress):
        for field in ['fio', 'description', 'type', 'email', 'category', 'color', 'size', 'height', 'svarovsky', 'country', 'state', 'cost', 'phone', 'vk', 'place',]:
            try:
                self.fields[field].initial = getattr(dress, field)
            except:
                pass
        self.photos = dress.photo_set.all()
               
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
    
    
    def save(self, files, dress, send_email = False):
        if not dress:                    
            raise Http404
            
        data = self.cleaned_data
        
        main_photo = self.save_photos(dress)
        
        dress.name = 'Платье'
        dress.fio = clean_data(data['fio'])
        dress.description = clean_data(data['description'])
        dress.type = clean_data(data['type'])
        dress.email = clean_data(data['email'])
        dress.category = clean_data(data['category'])
        dress.color = clean_data(data['color'])
        dress.size = clean_data(data['size'])
        dress.height = clean_data(data['height'])
        dress.svarovsky = clean_data(data['svarovsky'])
        dress.country = clean_data(data['country'])
        dress.state = clean_data(data['state'])
        dress.cost = clean_data(data['cost'])
        dress.discount = ''
        dress.phone = clean_data(data['phone'])
        dress.vk = ''
        dress.place = clean_data(data['place'])
        if main_photo:
            dress.main_photo = main_photo.image
            dress.main_photo_description = clean_data(main_photo.description)
        
        dress.confirmed = True
        
        dress.save()
            
        #============== Email template ================    
        #TODO: move email template to separate file
        message = """
Добрый день

    Вы разместили объявление о продаже платья. 
    Вы всегда можете просмотреть и изменить ваше объявление по ссылке http://catalog.mfst.pro/dress/{dressid}
    Ваш код доступа: {access_key}

    С уважением, 
        Администрация портала"""
        #==============================================

        if send_email:
            message = message.format(dressid=dress.id, access_key=dress.access_key)    
                
            try:
                send_mail('[catalog.mfst.pro] Вы разметили объявление о продаже платья', message, 'no-reply@mfst.pro', [dress.email], fail_silently=False)
            except:
                dress.confirmed = True
                dress.save()
                pass
        
        return dress
        
class LoginForm(forms.Form):
    code = forms.CharField(max_length=128, label=u'Код доступа', required=False)
    
    def save(self, id):
        try:
            dress = Dress.objects.get(pk=id)                  
        except:
            return False
            
        if settings.DEBUG:
            return True
        return dress.access_key==self.cleaned_data['code']        
        