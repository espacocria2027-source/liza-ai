"""
====================================================
Logger Listener
====================================================
"""

from core.event_bus import event_bus
from core import events


def on_message(data):

    print()

    print("==========================")

    print("Nova mensagem")

    print(data)

    print("==========================")

    print()


def on_response(data):

    print()

    print("==========================")

    print("Resposta")

    print(data)

    print("==========================")

    print()


event_bus.subscribe(

    events.MESSAGE_RECEIVED,

    on_message

)

event_bus.subscribe(

    events.MESSAGE_RESPONSE,

    on_response

)