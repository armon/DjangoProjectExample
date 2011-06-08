#!/usr/bin/python
import sys
import site
import os
import os.path

# Get the base dir
base_dir = os.path.dirname(os.path.abspath(__file__))

# Fix for dev mode
if base_dir == "/project":
  base_dir = "/server/env.example.com/project/"

# Get the site dir
site_dir = os.path.join(base_dir,"../lib/python2.6/site-packages")
site.addsitedir(site_dir)

# Adjust the system path
sys.path.append(os.path.join(base_dir,"project/"))
sys.path.append(os.path.join(base_dir, "project/core/"))

# Setup the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
os.environ["CELERY_LOADER"] = "django"

# Load django
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

