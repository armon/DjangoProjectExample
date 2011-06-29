
DEBUG = False
TEMPLATE_DEBUG = False

# Settings for Stage server, change the DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'examplestagedb',         # Or path to database file if using sqlite3.
        'USER': 'stageuser',      # Not used with sqlite3.
        'PASSWORD': 'ExampleStagePass',      # Not used with sqlite3.
        'HOST': 'db.example.com', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Use a local memcache instance
# This should be configured with the actual EC2 IPs for staging/production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': ['memcache.example.com:11211'],
        'KEY_PREFIX': 'STG',
    }
}

