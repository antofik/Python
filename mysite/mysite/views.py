from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render_to_response, redirect
import logging
import devconf
import authreader
from passlib.hash import apr_md5_crypt

def repository_list(request):    
    reader = devconf.DavConfReader()
    repositories = reader.GetRepositories()
   
    return render_to_response('repository_list.html', { 'repositories': repositories})
    
def repository_details(request, name):
    reader = devconf.DavConfReader()
    repository = reader.GetRepository(name)
    return render_to_response('repository_details.html', { 'this': repository})
    
def userset_details(request, userset):
    auth = authreader.AuthReader()
    users = auth.GetUsers(userset)
    allusers = auth.GetAllUsers()
    availableusers = allusers - users
    return render_to_response('user_list.html', {'name': userset, 'users':users, 'availableusers':availableusers})
    
def create_user_details(request):
    errors = []
    if request.method=='POST':
        if not request.POST.get('name', ''):
            errors.append("UserSet name is empty")
        else:
            name = request.POST['name']            
            auth = authreader.AuthReader()
            if name in auth.GetUserSets():
                errors.append('UserSet with such name already exists')                
        
        if errors:
            return render_to_response('user_create.html', {'errors':errors})
            
        auth.CreateUserSet(name)
   
        return redirect('/userset/%s' % name)        
    else:
        return render_to_response('user_create.html')
    
def adduser(request):
    if not request.POST.get('userset',''):
        redirect('/')
    else:
        userset = request.POST['userset']
        if not request.POST.get('username', ''):
            redirect('/userset/%s' % userset)
        else:
            name = request.POST['username']
            
def createuser(request):
    name = request.POST['userset']
    redirect('userset/%s' % name)
    
def create_repository(request):
    errors = []
    if request.method=='POST':
        if not request.POST.get('name',''):
            errors.append("Repository Name is empty")
        name = request.POST['name']
        reader = devconf.DavConfReader()
        repository = reader.GetRepository(request.POST['name'])
        if repository:
            errors.append("Repository with such name already exists")
            
        if errors:
            auth = authreader.AuthReader()
            sets = auth.GetUserSets()
            return render_to_response('repository_create.html', {'usersets':sets, 'errors': errors})
            
        reader.CreateRepository(name, request.POST['userset'])
        return redirect('/repository/' + name)
    else:
        auth = authreader.AuthReader()
        sets = auth.GetUserSets()
        return render_to_response('repository_create.html', {'usersets':sets, 'errors': errors})
    
def delete_repository(request, name):
    reader = devconf.DavConfReader()
    repository = reader.GetRepository(name)
    if repository:
        reader.DeleteRepository(name)
    return redirect('/')