# Django settings
import os
import os.path
import sys
import datetime

##### Basics

# Get the current path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Hack for vagrant
if BASE_PATH == "/project/project":
  BASE_PATH = "/server/env.example.com/project/project"

# Makes a normalized path from the base path
def make_abs_path(*rel_path):
  args = (BASE_PATH,) + rel_path
  return os.path.normpath(os.path.join(*args))

# Modify the python path
sys.path.append(make_abs_path("core/"))

# Make the tmp paths
TMP_PATHS = ["django","query"]
os.umask(0) # Set permissions on created files to 777
for p in TMP_PATHS:
  path = make_abs_path("../../tmp/",p)
  if not os.path.exists(path):
    os.makedirs(path)

# Get the date string
NOW = datetime.datetime.now()
DATE_STR = NOW.strftime("%Y-%m-%d")


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ("armon@example.com"),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = make_abs_path("../public/media/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/admin-media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '23mts!y2fo4z-25ehs1l2^4q*w1!9q-vc11&dx18_ihj!@fxi7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    make_abs_path("templates/"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'apps.main',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
      'default' : {
        'format' : '%(asctime)s %(levelname)-8s %(name)s %(message)s'
      },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'default'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'formatter': 'default',
            'filename':make_abs_path("../../tmp/django","web."+DATE_STR+".log"),
        },
        'querylog':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'backupCount':5,
            'maxBytes':1024*1024,
            'filename':make_abs_path("../../tmp/query","query."+DATE_STR+".log"),
            'delay':True,
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['querylog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    }
}

# Check which environment to load
if os.path.exists(make_abs_path("PRODUCTION")):
  from settings_prod import *
  ENVIRONMENT = "PRODUCTION"
elif os.path.exists(make_abs_path("STAGING")):
  from settings_stage import *
  ENVIRONMENT = "STAGING"
else:
  from settings_dev import *
  ENVIRONMENT = "DEV"

