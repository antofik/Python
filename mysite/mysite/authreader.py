import os
import sys
import re
from django.conf import settings
import logging

class AuthReader():
    def __init__(self):
        pass
        
    def GetUserSets(self):
        names = [file for file in os.listdir(settings.SVN_PATH) if file.startswith('passwd')]
        files = []
        for name in names:
            files.append(re.match('passwd_?(.*)', name).group(1))
        return files
        
    def CreateUserSet(self, name):
        name = 'passwd_' + name
        path = os.path.join(settings.SVN_PATH, name)
        file = open(path, 'w+')
        file.close()
      
    def GetUsers(self, name):
        name = 'passwd_' + name
        path = os.path.join(settings.SVN_PATH, name)
        logging.info(path)
        file = open(path, 'w+')
        try:
            users = set(file.readlines())
            logging.info(users)
        finally:
            file.close()
        return users

    def GetAllUsers(self):
        result = set()
        for userset in self.GetUserSets():
            result = result | set(self.GetUsers(userset))
        return result