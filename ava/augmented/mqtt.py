#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: mqtt
    :platform: Unix
    :synopsis: the top-level submodule of A.V.A. that contains the classes related to A.V.A.'s communication ability with the other devices.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import json
import time

AUGMENTED_DEVICES = [{'topic': 'Augmented/T_System', 'nick_name': 'T_System', 'name': 'The Object Tracking System'},
                     {'topic': 'Augmented/W_System', 'nick_name': 'W_System', 'name': 'Weather Tracking System'}]  # the secon device for just a sample.


class MqttReceimitter():
    """Class to define a receiving and transmitting data ability of A.V.A. with mqtt protokol.

        This class provides necessary initiations and a function named :func:`ava.MqttReceimitter.move`
        for the provide move of servo motor.

    """

    def __init__(self, host, userin, port=1883, keepalive=60):
        """Initialization method of :class:`ava.MqttReceimitter` class.

        Args:
            host         :          Device's IP address.
            port         :          Communication port of the host.
            keepalive    :          Keeping a live time of the communication. (secs.)
        """
        import paho.mqtt.client as mqtt
        self.client = mqtt.Client()
        self.userin = userin

        self.host = host
        self.port = port
        self.keepalive = keepalive

        self.topic = ""

        self.client.connect(self.host, self.port, self.keepalive)

        self.incoming_message = {'message': {}, 'is_used': False}
        self.is_connected = False

    def publish(self, topic, msg):
        """The top-level method to publishing the messages.

        Args:
            topic               :   Topic of the communication.
            msg(dictionary)     :   Sending message.
        """
        formatted_msg = json.dumps(msg)
        self.client.publish(topic, formatted_msg)  # json converting cause of mqtt's data transfer limit.

    def subscribe(self, topic):
        """The top-level method to subscribing the messages.

        Args:
            topic        :          Topic of the communication.
        """
        self.topic = topic
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """The top-level method to realize processes at the moment of provided the connection.

         Args:
             client:       	        Cilent object.
             userdata:
             flags:
             rc:       	            Result code of the connection.
         """

        # for device in AUGMENTED_DEVICES:
        #     if device['topic'] == self.topic:
        #         self.userin.say("Connection with " + device['name'] + " is succesfuly!")
        if rc == 0:
            self.is_connected = True
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        """The top-level method to realize processes at the moment of caught the messages on topic's echo.
        Args:
            client  :       	    Cilent object.
            userdata:
            msg     :               message from the publisher.
        """
        msg.payload = msg.payload.decode("utf-8")

        self.incoming_message['message'] = json.loads(msg.payload)  # json converting cause of mqtt's data transfer limit.
        self.incoming_message['is_used'] = False

    def get_incoming_message(self):
        """The top-level method to controlling them during getting incoming messages.
        """
        if self.incoming_message['is_used']:
            return {}

        self.incoming_message['is_used'] = True
        return self.incoming_message['message']

    def get_is_connected(self):
        """The top-level method to checking the connection's situation.
        """
        return self.is_connected


if __name__ == '__main__':

    # FOLLOWING LINES FOR THE TESTING THE "mqtt" SUBMODULE!!
    pass
