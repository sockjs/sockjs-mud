import logging
log = logging.getLogger(__name__)

import datetime
import django.dispatch
from multiprocessing import Process
from . import models
from . import trigger
import os

tick_event = django.dispatch.Signal(providing_args=["curr_time"])


def cleanup_connections(sender, curr_time=None, **kwargs):
    t0 = curr_time - datetime.timedelta(seconds = 60)
    for conn in models.Connection.objects.filter(modified__lt=t0):
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


tick_event.connect(cleanup_connections)


# Load all npc modules.
def load_npc():
    for actor in models.Char.objects.filter(is_npc=True):
        trigger.action('load', actor=actor)

load_npc()



def run_process():
    from . import puk
    import time

    errors = 0
    while True:
        try:
            time.sleep(10)
            tick_event.send(sender=None, curr_time=datetime.datetime.now())
            puk.flush()
            errors = 0
        except Exception, e:
            errors += 1
            log.error("Exception in process:", exc_info=True)
            if errors > 12:
                os._exit(1)
def prepare():
    log.info("Starting timer process")
    r = Process(target=run_process)
    r.start()

