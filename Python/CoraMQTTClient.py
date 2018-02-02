# -*- coding:utf-8 -*-
""" MQTT Protocol. """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/ARMv7/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  MQTT Protocol.
# History:  2018/01/18 V1.0.0 [Heyn] Initialization & Optimization code.

# See https://linoxide.com/tools/setup-mosquitto-mqtt-server-ubuntu-16-04/

# import json
import logging
import paho.mqtt.client as mqtt

class ProtMQTT:
    
    def __init__(self, locname, subname):
        self.locname = locname
        self.subname = subname

    def connect(self, hostip, username, pwd):
        self.client = mqtt.Client(client_id='',
                                  clean_session=True,
                                  userdata=None,
                                  protocol=mqtt.MQTTv311,
                                  transport='tcp')

        # Server command: mosquitto_passwd -c /etc/mosquitto/pwfile mqtt
        self.client.username_pw_set(username, pwd)
        # Enable SSL/TLS support.
        # self.client.tls_set(ca_certs=ca_certs)

        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        # self.client.on_publish = self.__on_publish
        self.client.on_disconnect = self.__on_disconnect

        # Connect to the MQTT bridge.
        self.client.connect(hostip, 1883, 60)
        self.client.user_data_set(self.locname)

    def error_str(self, ret):
        """Convert a Paho error to a human readable string."""
        return '{}: {}'.format(ret, mqtt.error_string(ret))

    def __on_connect(self, client, userdata, flags, ret):
        """ The callback for when the client receives a CONNACK response from the server. """
        print('Connected', mqtt.connack_string(ret))
        self.client.subscribe(self.subname)

    def __on_disconnect(self, client, userdata, ret):
        """Paho callback for when a device disconnects."""
        print('on_disconnect', self.error_str(ret))

    def __on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        print(msg.topic + ' @ ' + str(msg.payload.decode('UTF-8', 'ignore')))
    
    def __on_publish(self, client, userdata, mid):
        """ Paho callback when a message is sent to the broker.
        """
        print('on_publish')

    def send(self, payload):
        """ Publish "payload" to the MQTT topic. qos=1 means at least once
        """
        self.client.publish(self.locname, payload, qos=1)

    def start(self):
        """ Start the network loop.
        """
        self.client.loop_start()

    def stop(self):
        """ Stop the network loop.
        """
        self.client.loop_stop()


if __name__ == '__main__':
    HH = ProtMQTT('Lily', 'Heyn')
    HH.connect('127.0.0.1', 'mqtt', '000000')
    HH.send('hello')
    HH.start()

    import time
    while True:
        time.sleep(1)

# LOCNAME = 'Lily'    # The local device name.
# SUBNAME = 'Heyn'    # Receive message name.

# def on_connect(client, userdata, flags, ret):
#     """ The callback for when the client receives a CONNACK response from the server. """

#     print('Connected with result code ' + str(ret))
#     client.subscribe(SUBNAME)

#     client.publish(LOCNAME, LOCNAME + ' is online.')

# def on_message(client, userdata, msg):
#     """ The callback for when a PUBLISH message is received from the server. """
#     print(msg.topic + ' @ ' + str(msg.payload.decode('UTF-8', 'ignore')))


# CLINET = mqtt.Client(client_id='',
#                      clean_session=True,
#                      userdata=None,
#                      protocol=mqtt.MQTTv311,
#                      transport='tcp')

# # Server command:
# # mosquitto_passwd -c /etc/mosquitto/pwfile mqtt

# CLINET.username_pw_set('mqtt', '000000')

# CLINET.on_connect = on_connect
# CLINET.on_message = on_message
# CLINET.connect("127.0.0.1", 1883, 60)
# # CLINET.loop_forever()

# CLINET.user_data_set(LOCNAME)
# CLINET.loop_start()

# while True:
#     MSG = input()
#     if MSG:
#         CLINET.publish(LOCNAME, MSG.encode('UTF-8', errors='strict'))
