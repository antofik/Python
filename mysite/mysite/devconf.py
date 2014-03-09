import os
import sys
import re
from django.conf import settings
import logging

class DavConfReader():
    def __init__(self):
        apache_path = os.path.join(settings.APACHE_PATH, "conf/extra/httpd-dav.conf")       
        
        conf = open(apache_path)
        try:
            self.lines = conf.readlines()
        finally:
            conf.close()
            
    def GetRepositories(self):
        result = []
        
        start_location_re = re.compile('\s*<Location /svn/([^>]*)>\s*')
        end_location_re = re.compile('\s*</Location>\s*')
        auth_re = re.compile('(.*)passwd_?(.*)"')
        current = None
        for line in self.lines:
            if current==None:
                match = start_location_re.match(line)
                if match:   
                    current = DavConf()
                    current.name = match.group(1)
            else:
                match = end_location_re.match(line)
                if match:   
                    result.append(current)
                    current = None                    
                else:
                    match = auth_re.match(line)
                    if match:   
                        current.userset = match.group(2)
        return result
        
    def GetRepository(self, name):
        items = [r for r in self.GetRepositories() if r.name==name]
        if items:
            return items[0]
        else:
            return None

    def CreateRepository(self, name, userset):
        apache_path = os.path.join(settings.APACHE_PATH, "conf/extra/httpd-dav.conf")       
         
        pattern = ['\n<Location /svn/{{name}}>\n',
                   "     Dav svn\n",
                   '     Order Deny,Allow\n',
                   '     SVNPath "c:/inetpub/svn/{{name}}/"\n',
                   '     AuthType Basic\n',
                   '     AuthName "Subversion repository"\n',
                   '     Require valid-user\n',
                   '     AuthUserFile "C:\inetpub\svn\passwd{{userset}}"\n',
                   ' </Location>\n']                                      
        if userset:
            userset = '_' + userset
                   
        pattern = [line.replace('{{name}}', name).replace('{{userset}}', userset) for line in pattern]           
                   
        
        conf = open(apache_path, 'a')
        try:
            conf.writelines(pattern)
                
        finally:
            conf.close()
       
    def DeleteRepository(self, name):
        apache_path = os.path.join(settings.APACHE_PATH, "conf/extra/httpd-dav.conf")       
        
        conf = open(apache_path)
        try:
            self.lines = conf.readlines()
        finally:
            conf.close()
            
       
        start_location_re = re.compile('\s*<Location /svn/%s>\s*' % name)
        end_location_re = re.compile('\s*</Location>\s*')

        result = []        
        Found = False
        for line in self.lines:
            if not Found:
                match = start_location_re.match(line)
                if match:   
                    Found = True
                else:
                    result.append(line)
            else:
                match = end_location_re.match(line)
                if match:                       
                    Found = False

        
        conf = open(apache_path, 'w')
        try:
            conf.writelines(result)
        finally:
            conf.close()        

class DavConf():
    name = ''
    userset = ''

