# coding=utf-8
from django_cron import CronJobBase, Schedule
import datetime
from django.core.mail import send_mail
from check.models import Item

class DailyCheck(CronJobBase):
    RUN_EVERY_MINS = 60*24 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'artis.dailycheck'    # a unique code

    def do(self):
        message = 'Artis is up'
        from_email = 'no-reply@fabricartis.ru'
        send_mail(u'[UP] fabricartis.ru', message, from_email, ['contact@mfst.pro', 'antofik@gmail.com'], fail_silently=False)

class SendOneDayNotifications(CronJobBase):
    RUN_EVERY_MINS = 60*24 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'artis.sendonedaynotification'    # a unique code

    def do(self):
        now = datetime.datetime.now().date()
        for item in Item.objects.all():
            try:
                if item.date_ready.date() > now:
                    days = (item.date_ready.date() - now).days
                    if days==1:
                        self.SendNotificationOn(item)
            except Exception, e:
                print 'Error', e

    def SendNotificationOn(self, item):
        try:
            message = u'''Напоминаем, что ваш заказ %s (%s) будет готов завтра

            С уважением,
                Администрация Фабрики Артис
            ''' % (item.title, item.code)
            from_email = 'contact@fabricartis.ru'
            send_mail(u'Фабрика Артис', message, from_email, ['contact@mfst.pro', item.user.email], fail_silently=False)
        except:
            pass