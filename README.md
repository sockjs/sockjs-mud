SockJS - mud
============

This is a rough and dirty Mud game. Unlike games from early 80's this
one uses web interface - you can play from your browser. It's
presenting the power of
[SockJS](https://github.com/majek/sockjs-client) and under the hood
uses also Django.

This code is derived from [flying squirrel
demos](https://github.com/rabbitmq/flying-squirrel-demos).


Local deployment
----------------

To run the stuff locally you need to have `node`, `npm` and local
`Rabbitmq` server running. Additionally you need few Python
dependencies, to install them run:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt


To run the sockjs gateway:

    cd gateway
    npm install
    node server.js


To run the main part of mud - python/django server:

    . venv/bin/activate
    cd mud
    ./manage.py syncdb --noinput
    ./manage.py createsuperuser --username=admin --email=a@b.co.uk
    ./manage.py runserver 0.0.0.0:3000

And on the second console:

    while [ 1 ]; do curl http://127.0.0.1:3000/tick; echo; sleep 10; done

If you modified the rooms, you may want to save the data:

    ./manage.py dumpdata \
        --format=json \
        --indent=4 core > /tmp/initial_data.json


