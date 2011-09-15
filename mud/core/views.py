import datetime
from django.conf import settings

from django.shortcuts import render_to_response
from django.http import HttpResponseNotAllowed, HttpResponse, \
    HttpResponseNotFound
from . import puk
from . import signals


def index(request):
    if request.method == 'GET':
        return index_get(request)
    elif request.method == 'POST':
        return index_post(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def index_get(request):
    my_context = {
        'sockjs_url': settings.SOCKJS_URL,
        }
    return render_to_response('index.html', my_context)


def tick(request):
    signals.tick_event.send(sender=request,
                            curr_time=datetime.datetime.now())
    puk.flush()
    return HttpResponse('ok')
