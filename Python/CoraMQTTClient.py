# -*- coding:utf-8 -*-
""" MQTT Client. """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  MQTT Client.
# History:  2018/01/18 V1.0.0 [Heyn] Initialization & Optimization code.

# See https://linoxide.com/tools/setup-mosquitto-mqtt-server-ubuntu-16-04/

# import json
import paho.mqtt.client as mqtt

LOCNAME = 'Lily'    # The local device name.
SUBNAME = 'Heyn'    # Receive message name.

def on_connect(client, userdata, flags, ret):
    """ The callback for when the client receives a CONNACK response from the server. """

    print('Connected with result code ' + str(ret))
    client.subscribe(SUBNAME)

    client.publish(LOCNAME, LOCNAME + ' is online.')

def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server. """
    print(msg.topic + ' @ ' + str(msg.payload.decode('UTF-8', 'ignore')))


CLINET = mqtt.Client(client_id='',
                     clean_session=True,
                     userdata=None,
                     protocol=mqtt.MQTTv311,
                     transport='tcp')

# Server command:
# mosquitto_passwd -c /etc/mosquitto/pwfile mqtt

CLINET.username_pw_set('mqtt', '000000')

CLINET.on_connect = on_connect
CLINET.on_message = on_message
CLINET.connect("127.0.0.1", 1883, 60)
# CLINET.loop_forever()

CLINET.user_data_set(LOCNAME)
CLINET.loop_start()

while True:
    MSG = input()
    if MSG:
        CLINET.publish(LOCNAME, MSG.encode('UTF-8',errors='strict'))
