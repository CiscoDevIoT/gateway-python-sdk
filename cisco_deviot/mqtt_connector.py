# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import json
from urlparse import urlparse

import time
from paho.mqtt.client import Client

from cisco_deviot import logger


class MqttConnector:
    def __init__(self, gateway, mqtt_server):
        self.gateway = gateway
        self.client = Client()
        self.client.on_connect = self.__on_connect__
        self.client.on_disconnect = self.__on_disconnect__
        self.client.on_message = self.__on_message__
        self.__connected = False
        ns = gateway.owner.replace("@", "_").replace(".", "_").replace("/", "_")
        if ns == "":
            ns = "_"
        name = gateway.name.replace("/", "_")

        surl = urlparse(mqtt_server)
        self.host = surl.hostname
        self.port = surl.port
        self.data = "/deviot/{ns}/{name}/data".format(name=name, ns=ns)
        self.action = "/deviot/{ns}/{name}/action".format(name=name, ns=ns)

    def start(self):
        self.client.connect_async(self.host, self.port, 60)
        self.client.loop_start()
        logger.info("connecting to {server} ...".format(server=self))

    def stop(self):
        self.client.disconnect()

    def __on_connect__(self, client, userdata, flags, rc):
        self.client.subscribe(self.action)
        self.__connected = True
        logger.info("{server}{topic} connected".format(server=self, topic=self.action))

    def __on_disconnect__(self, client, userdata, rc):
        logger.warn("{server} disconnected".format(server=self))
        self.__connected = False
        backoff = 2
        while not self.__connected:
            logger.info("reconnecting to {server} in {sec} seconds ...".format(server=self, sec=backoff))
            time.sleep(backoff)
            backoff = min(128, backoff * 2)
            try:
                self.client.reconnect()
                self.__connected = True
            except:
                pass

    def is_connected(self):
        return self.__connected

    def __on_message__(self, client, userdata, msg):
        message = str(msg.payload)
        try:
            args = json.loads(message)
            self.gateway.call_action(args)
        except Exception, error:
            logger.error("failed to process message {message}: {error}".format(message=message, error=error))

    def publish(self, data):
        json_string = json.dumps(data, sort_keys=False)
        self.client.publish(self.data, json_string)

    def __str__(self):
        return "mqtt connector {server}:{port}".format(server=self.host,
                                                    port=self.port)
