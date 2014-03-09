import os
from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import time
from adminbackup.models import Backup
from icybackup.management.commands.backup import Command as BackupCommand
from icybackup.management.commands.restore import Command as RestoreCommand
import settings


def backup(request, errors=None):
    errors = errors or []
    items = Backup.objects.all()
    print items
    return render_to_response('backup.html', RequestContext(request, {'items':items, 'errors': errors}))

def create(request):
    errors = []
    backup = Backup()
    backup.name = '{}.tgz'.format(time.strftime('%Y%m%d-%H%M%S'))
    backup.data = backup.name
    backup.save()

    th = Thread(target=create_backup, args=(backup,))
    th.start()

    return HttpResponse('ok')

def restore(request, id):
    try:
        backup = Backup.objects.get(pk=int(id))
        if not backup.data:
            raise Exception("Corrupted backup")
        command = RestoreCommand()
        file = os.path.join(settings.BACKUP_ROOT, backup.data)
        command.handle(input=file, extras=[])
        backup.status = Backup.READY
        backup.save()
        return HttpResponse('ok')
    except:
        import traceback
        traceback.print_exc()
        return HttpResponse('failed')

def delete(request, id):
    try:
        backup = Backup.objects.get(pk=int(id))
        if backup:
            backup.delete()
            if backup.data:
                file = os.path.join(settings.BACKUP_ROOT, backup.data)
                os.remove(file)
        return HttpResponse('ok')
    except:
        import traceback
        traceback.print_exc()
        return HttpResponse('failed')

def create_backup(backup):
    try:
        command = BackupCommand()
        command.handle(output=os.path.join(settings.BACKUP_ROOT, backup.name), extras=[])
        backup.status = Backup.READY
    except Exception:
        backup.status = Backup.FAILED
    backup.save()


