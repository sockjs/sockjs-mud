import logging
log = logging.getLogger(__name__)

import datetime
import django.dispatch
from . import models
from . import trigger


tick_event = django.dispatch.Signal(providing_args=["curr_time"])


# Load all npc modules.
def load_npc():
    for actor in models.Char.objects.filter(is_npc=True):
        trigger.action('load', actor=actor)

load_npc()
