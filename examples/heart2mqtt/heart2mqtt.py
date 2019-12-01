#!/usr/bin/env python2.7
import sys
import logging
from urlparse import urlparse

import BLEHeartRateLogger

import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)

HRM_MAC = 'fc:4b:88:a0:93:9d'
CLIENT_NAME = 'BLE-HRM-' + HRM_MAC.replace(':', '')


class HrmMqttPublisher(BLEHeartRateLogger.HrmEventListener):
    def __init__(self, mqtt_client, topic_base):
        self.client = mqtt_client
        self.topic_base = topic_base.strip("/")

    def on_battery_level(self, level):
        self.client.publish(self.topic_base + '/battery_level', level)

    def on_heart_rate(self, rate):
        self.client.publish(self.topic_base + '/heart_rate', rate)

    def on_connection_established(self):
        self.client.publish(self.topic_base + '/connected', True)

    def on_disconnection(self):
        self.client.publish(self.topic_base + '/connected', False)


def main():
    assert 2 <= len(sys.argv) <= 3
    client_mac = None
    client_name = 'BLE-HRM'
    if len(sys.argv) >= 3:
        client_mac = sys.argv[2]
        client_name += ('-' + client_mac.replace(':', ''))
    
    mqtt_url = urlparse(sys.argv[1])
    mqtt_host  = mqtt_url.netloc
    mqtt_topic = mqtt_url.path.strip()

    client = mqtt.Client(client_name)
    client.connect(mqtt_host)
    publisher = HrmMqttPublisher(client, mqtt_topic)
    publisher.on_disconnection()
    BLEHeartRateLogger.main(client_mac, check_battery=True, user_event_listener=publisher)

main()
