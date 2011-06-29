
DEBUG = False
TEMPLATE_DEBUG = False

# Settings for production server

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'exampleproddb',         # Or path to database file if using sqlite3.
        'USER': 'produser',      # Not used with sqlite3.
        'PASSWORD': 'ExampleProdPass',      # Not used with sqlite3.
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
        'KEY_PREFIX': 'PROD',
    }
}


