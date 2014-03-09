import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Django settings for artis project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
   #  ('admin', 'admin@svnadmin'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# N.B. Should have 'write' access for the django environment
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vxl+6yp$^&amp;w9m8-naeqbi+z0t5bxr8*=^++@pv6i!#l)*zxs35'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

#CMS processors
TEMPLATE_CONTEXT_PROCESSORS = (
    #'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.request',
    #'django.core.context_processors.media',
    #'django.core.context_processors.static',
 #   'cms.context_processors.media',
 #   'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES = (
  #  'django.middleware.common.CommonMiddleware',
  #  'django.contrib.sessions.middleware.SessionMiddleware',
  #  'django.middleware.csrf.CsrfViewMiddleware',
  #  'django.contrib.auth.middleware.AuthenticationMiddleware',
  #  'django.contrib.messages.middleware.MessageMiddleware',
  #  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  #  'cms.middleware.multilingual.MultilingualURLMiddleware',
  #  'cms.middleware.page.CurrentPageMiddleware',
  #  'cms.middleware.user.CurrentUserMiddleware',
  #  'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'svnadmin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'svnadmin.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

CMS_TEMPLATES = (
    ('base.html', 'Base'),
    ('article.html', 'Article'),
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    #'django.contrib.admin',
    #'django.contrib.admindocs',
    #CMS
    #'cms',
    #'mptt',    #pre-order traversal tree
    #'menus',   
    #'south',   #intelligent schema and data migrations
    #'sekizai', #javascript and css management
    #additional CMS
    #'cms.plugins.file', 
    #'cms.plugins.flash', 
    #'cms.plugins.googlemap', 
    #'cms.plugins.link', 
    #'cms.plugins.picture', 
    #'cms.plugins.snippet',  #do you need it?
    #'cms.plugins.teaser', 
    #'cms.plugins.text', 
    #'cms.plugins.video', 
    #'cms.plugins.twitter', 
    
    #Alternative to the cms.plugins.file, picture, teaser, video
    #'filer', 
    #'cmsplugin_filer_file', 
    #'cmsplugin_filer_folder', 
    #'cmsplugin_filer_image', 
    #'cmsplugin_filer_teaser', 
    #'cmsplugin_filer_video', 
    
    #version support
    #'reversion',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
