# Django settings for artis project.
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG=False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'photos.mfst.pro',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'read_default_file': os.path.join(PROJECT_PATH, 'mysql.cnf'),},
    }
}

