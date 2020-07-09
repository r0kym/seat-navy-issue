"""
Database signals. See `Mongoengine signals
<http://docs.mongoengine.org/guide/signals.html>`_
"""

from typing import Any

import mongoengine as me
import mongoengine.signals as signals

import sni.utils as utils


@signals.pre_save.connect
def on_pre_save(_sender: Any, document: me.Document):
    """
    If the document has a `updated_on`, sets it to the current datetime.
    """
    if 'updated_on' in document:
        document.updated_on = utils.now()
