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


import httplib
import threading
import time
import json

from urlparse import urlparse
from cisco_deviot import logger
from cisco_deviot.mqtt_connector import MqttConnector


MODE_HTTP_PULL = 0
MODE_HTTP_PUSH = 1
MODE_MQTT = 2


class Gateway:
    def __init__(self, name, deviot_server, connector_server, kind="device", account=""):
        name = name.replace("-", "_")
        self.name = name
        self.kind = kind
        self.owner = account
        if urlparse(deviot_server).scheme == '': # the default protocol for a DevIot server is HTTPS
            deviot_server = "https://" + deviot_server
        self.deviot_server = urlparse(deviot_server)
        self.mode = MODE_MQTT
        self.things = {}
        self.__registration_started = False
        self.__registered = 0
        if urlparse(connector_server).scheme == '': # the default protocol of MQTT is TCP
            connector_server = "tcp://" + connector_server
        self.connector = MqttConnector(self, connector_server)
        self.host = self.connector.host
        self.port = self.connector.port
        self.data = self.connector.data
        self.action = self.connector.action

    def __registration_function(self):
        while self.__registration_started:
            time.sleep(2)
            if self.__registration_started:
                self.__register()
            time.sleep(8)

    def __del_none(self, d):
        if isinstance(d, dict):
            for key, value in d.items():
                if value is None:
                    del d[key]
                else:
                    self.__del_none(value)
        elif isinstance(d, list):
            for x in d:
                self.__del_none(x)
        return d

    def __register(self):
        import collections
        model = collections.OrderedDict([("name", self.name),
                                         ("kind", self.kind),
                                         ("mode", self.mode),
                                         ("owner", self.owner),
                                         ("host", self.host),
                                         ("port", self.port),
                                         ("data", self.data),
                                         ("action", self.action),
                                         ("sensors", [thing.get_model() for thing in self.things.values()])])
        json_string = json.dumps(self.__del_none(model), sort_keys=False)
        try:
            if self.deviot_server.scheme == 'http':
                conn = httplib.HTTPConnection(self.deviot_server.netloc)
            else:
                conn = httplib.HTTPSConnection(self.deviot_server.netloc)
            conn.request("POST", "/api/v1/gateways", json_string, {'Content-Type': 'application/json'})
            response = conn.getresponse()
            code = int(response.status)
            if code < 200 or code > 300:
                if self.__registered != 1:
                    logger.error("failed to register gateway {name} to {server}: {c}-{e}".format(name=self,
                                                                                             server=self.deviot_server.netloc,
                                                                                             c=code,
                                                                                             e=response.reason))
                self.__registered = 1
            elif not self.__registered:
                if self.__registered != 2:
                    logger.info("registered gateway {name} to {server}".format(name=self,
                                                                           server=self.deviot_server.netloc))
                self.__registered = 2
        except IOError as e:
            if self.__registered != 1:
                logger.error("failed to register gateway {name} to {server}: {e}".format(name=self,
                                                                                     server=self.deviot_server.netloc,
                                                                                     e=e))
            self.__registered = 1

    def start(self):
        if self.__registration_started:
            logger.warn("gateway service {name} already started".format(name=self))
        else:
            self.__registration_started = True
            thread = threading.Thread(target=Gateway.__registration_function, args=(self,))
            thread.daemon = True
            thread.start()
            self.connector.start()
            logger.info("gateway service {name} started".format(name=self))

    def stop(self):
        if self.__registration_started:
            self.__registration_started = False
            self.connector.stop()
            logger.info("gateway service {name} stopped".format(name=self))
        else:
            logger.warn("gateway service {name} already stopped".format(name=self))

    def register(self, thing):
        if thing.id in self.things:
            logger.warn("thing {thing} is already registered".format(thing=thing))
        else:
            self.things[thing.id] = thing
            logger.info("thing {thing} registered".format(thing=thing))

    def deregister(self, thing):
        if thing.id in self.things:
            del self.things[thing.id]
            logger.info("thing {thing} deregistered".format(thing=thing))
        else:
            logger.warn("thing {thing} is not registered".format(thing=thing))

    def send_data(self, data):
        if self.connector.is_connected:
            self.connector.publish(data)
        else:
            logger.warn("{connector} not connected yet".format(connector=self.connector))

    # args: payload of the subscribed MQTT message
    def call_action(self, args):
        tid = None
        if "id" in args:
            tid = args.pop("id")

        if "name" in args:
            tid = args.pop("name")

        if tid is None:
            logger.warn("illegal message, thing id/name not available")
            return

        if "action" not in args:
            logger.warn("illegal message, thing action not available")
            return

        if tid in self.things:
            t = self.things[tid]
            action = args.pop("action")
            try:
                t.call_action(action, args)
            except Exception as error:
                logger.error("failed to call {tid}.{action}({args}): {error}".format(tid=tid,
                                                                                     action=action,
                                                                                     args=args,
                                                                                     error=error))
        else:
            logger.warn("thing {thing} not registered".format(thing=tid))

    def __str__(self):
        return "{name}({kind})".format(name=self.name, kind=self.kind)
