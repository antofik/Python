# coding=utf-8
from random import randint
from django_cron import CronJobBase, Schedule
from aliexpress.aliexpress import aliexpress
from aliexpress.update_costs import updater
from webparser.models import clear_db

parser = None

class parse(CronJobBase):
    RUN_EVERY_MINS = 60*24 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'electrosha.parser' + str(randint(1,10000000))    # a unique code

    def do(self):
        print 'Parse currently blocked'
        if True: return
        global parser
        try:
            if not parser:
                print 'parsing started'
                clear_db()
                parser = aliexpress()
                parser.parse()
                print 'parsing done'
            else:
                print 'parser already launched'
        except Exception, e:
            print 'Fatal error while parsing: ' + str(e)
            import traceback
            traceback.print_exc()

class update_costs(CronJobBase):
    RUN_EVERY_MINS = 60*24 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'electrosha.updater' + str(randint(1,10000000))    # a unique code

    def do(self):
        try:
            parser = updater()
            parser.update_costs()
        except Exception, e:
            print 'Fatal error while parsing: ' + str(e)
            import traceback
            traceback.print_exc()

