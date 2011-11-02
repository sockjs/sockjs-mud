import os
import json

DEBUG = False

import os, sys, urlparse
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')
DATABASES = {}
try:
    if os.environ.has_key('DATABASE_URL'):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        DATABASES['default'] = {
            'NAME':     url.path[1:],
            'USER':     url.username,
            'PASSWORD': url.password,
            'HOST':     url.hostname,
            'PORT':     url.port,
        }
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg'
        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
                }
            }
except:
    print "Unexpected error:", sys.exc_info()
    raise

## Identica credentials for 'Bird' mob.
IDENTICA_USER=''
IDENTICA_PASS=''

if os.environ.has_key('RABBITMQ_URL'):
    RABBITMQ_URL = os.environ['RABBITMQ_URL']
else:
    RABBITMQ_URL='amqp://localhost'

if os.environ.has_key('RABBITMQ_URL'):
    SOCKJS_URL='http://sockjs-mud-ws.herokuapp.com/mud'
else:
    SOCKJS_URL='http://localhost:3001/mud'
