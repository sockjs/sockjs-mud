import os
import json

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

## Identica credentials for 'Bird' mob.
IDENTICA_USER=''
IDENTICA_PASS=''

RABBITMQ_URL='amqp://localhost'
SOCKJS_URL='http://localhost:3001/mud'
