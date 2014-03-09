# Django settings for artis project.
import os

DEBUG = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(PROJECT_PATH, "sqldb.lite"),                      # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'algo.pw',                      # Or path to database file if using sqlite3.
        'USER': 'algo.pw',                      # Not used with sqlite3.
        'PASSWORD': 'fAFS#fdsa#$$@#$ffak',                  # Not used with sqlite3.
        'HOST': 'algo.pw',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'read_default_file': os.path.join(PROJECT_PATH, 'mysql.cnf'),},
    }
}
