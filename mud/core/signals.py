import logging
log = logging.getLogger(__name__)

import datetime
import django.dispatch
from multiprocessing import Process
from . import models
from . import trigger


tick_event = django.dispatch.Signal(providing_args=["curr_time"])


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
            signals.tick_event.send(sender=request,
                                    curr_time=datetime.datetime.now())
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

