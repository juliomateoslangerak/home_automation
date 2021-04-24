"""This is a simple script to snc all the lights of the corridor. They are controlled using a
Sheely1 relay. They shoudl just go all on or off when any of the set is switched on of off."""

import paho.mqtt.client as mqtt
from home_config import *

curr_state = None


def on_toggle(client, userdata, message):
    global curr_state
    if message.payload != curr_state:
        for device in DEVICES_IDS:
            if message.topic != f"shellies/{device}/relay/0":
                client.publish(topic=f"shellies/{device}/relay/0/command",
                               payload=message.payload, qos=QoS)
        curr_state = message.payload


if __name__ == "__main__":

    client = mqtt.Client("corridor_controller")

    client.connect(host=HOST, port=PORT)
    client.on_message = on_toggle

    for device in DEVICES_IDS:
        client.subscribe(topic=f"shellies/{device}/relay/0", qos=QoS)

    client.loop_forever()
