import puka
from multiprocessing import Process
import os
import json
import logging
from django.conf import settings
log = logging.getLogger(__name__)

from . import models
from . import mud


def run_process():
    client = puka.Client(settings.RABBITMQ_URL)
    promise = client.connect()
    client.wait(promise)
    promise = client.queue_declare(queue='mud', durable=True)
    client.wait(promise)

    consume_promise = client.basic_consume(queue='mud', prefetch_count=1)
    try:
        while True:
            result = client.wait(consume_promise)
            got = json.loads(result['body'])
            reply_to = got['id'] + ' ' + got['reply-to']
            inbound_message(reply_to, got['data'], got.get('closed', False))

            client.basic_ack(result)
    except Exception, e:
        log.error("Exception in process:", exc_info=True)
        promise = client.close()
        client.wait(promise)
        os._exit(1)

def prepare():
    log.info("Starting puka process")
    r = Process(target=run_process)
    r.start()

client = None
def flush():
    global client
    if not client:
        log.info("Starting RMQ connection")
        client = puka.Client(settings.RABBITMQ_URL)
        promise = client.connect()
        client.wait(promise)

    promise = None
    for reply_to, messages in models.OUTBOUND.iteritems():
        id, rt = reply_to.encode('utf-8').split(' ', 2)

        aaa = '\n\r'.join(messages).encode('utf-8')
        promise = client.basic_publish(exchange='', routing_key=rt,
                                       body=json.dumps({'data':aaa, 'id':id}))
    if promise:
        # waiting for last one should be enough
        client.wait(promise)
    models.OUTBOUND.clear()

def inbound_message(reply_to, msg, closed):
    if not closed:
        try:
            conn = models.Connection.objects.get(reply_to__exact=reply_to)
        except models.Connection.DoesNotExist:
            conn = models.Connection(reply_to=reply_to)
        conn.save()
        if msg != "\x00":
            mud.inbound(conn, msg)
        else:
            conn.send("\x00")
        flush()
    else:
        try:
            conn = models.Connection.objects.get(reply_to__exact=reply_to)
        except models.Connection.DoesNotExist:
            return
        actor = conn.char
        log.info(" [*] %s (%s) disconnected", actor, conn.reply_to)
        conn.send("Come back to us later.")
        conn.send("Disconnected...")
        conn.delete()
        if actor and not actor.is_npc and actor.connection_set.count() == 0:
            # Last connection lost, moving to limbo
            actor.render_to_others('to_limbo.txt')
            actor.room_id = 1
            actor.save()
