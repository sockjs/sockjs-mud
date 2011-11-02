import os
from flask import Flask
import django.core.handlers.wsgi


app = Flask(__name__)

os.chdir('mud')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mud.settings'
app.wsgi_app = django.core.handlers.wsgi.WSGIHandler()

# preload
import mud.core

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

