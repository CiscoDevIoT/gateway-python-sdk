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

import collections

from cisco_deviot import logger

PropertyTypeInt = 0
PropertyTypeString = 1
PropertyTypeBool = 2
PropertyTypeColor = 3


def default_value_for_type(stype):
    if stype == PropertyTypeInt:
        return 0
    if stype == PropertyTypeBool:
        return False
    if stype == PropertyTypeString:
        return ""
    if stype == PropertyTypeColor:
        return "FFFFFF"
    return None


class Property:
    def __init__(self, name, type=0, value=None, range=None, unit=None, description=None):
        self.name = name
        self.type = type
        self.value = value
        self.range = range
        self.unit = unit
        self.description = description

    def get_model(self):
        return collections.OrderedDict([("name", self.name),
                                        ("type", self.type),
                                        ("range", self.range),
                                        ("value", self.value),
                                        ("unit", self.unit),
                                        ("description", self.description)])


class Action:
    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = [Property(k, kwargs[k]) for k in kwargs]
        self.need_payload = False

    def add_parameter(self, action_parameter):
        self.parameters.append(action_parameter)
        return self

    def need_payload(self, payload):
        self.need_payload = payload
        return self

    def get_model(self):
        return collections.OrderedDict([("name", self.name),
                                        ("parameters", [p.get_model() for p in self.parameters])])


class Thing:
    def __init__(self, id, name, kind=None):
        self.id = id
        self.name = name
        self.kind = kind if kind is not None else self.__class__.__name__.lower()
        self.properties = []
        self.actions = []
        self.options = {}

    def get_model(self):
        return collections.OrderedDict([("id", self.id),
                                        ("name", self.name),
                                        ("kind", self.kind),
                                        ("properties", [p.get_model() for p in self.properties]),
                                        ("actions", [a.get_model() for a in self.actions])])

    def __str__(self):
        return "{id}.{name}({kind})".format(id=self.id, name=self.name, kind=self.kind)

    def add_property(self, *thing_properties):
        for prop in thing_properties:
            if isinstance(prop, str):
                self.properties.append(Property(prop, PropertyTypeInt))
            elif isinstance(prop, Property):
                self.properties.append(prop)
            else:
                logger.error(
                    "invalid property {property}, only string and Property are supported".format(property=prop))

        return self

    def add_action(self, *thing_actions):
        for act in thing_actions:
            if isinstance(act, str):
                self.actions.append(Action(act))
            elif isinstance(act, Action):
                self.actions.append(act)
            else:
                logger.error("invalid property {property}, only string and Property are supported".format(property=act))
        return self

    def call_action(self, method, args):
        action_method = getattr(self, method)
        matches = list(a for a in self.actions if a.name == method)
        action_model = matches[0]
        valid_args = {p.name: True for p in action_model.parameters}
        if action_model.need_payload:
            valid_args["payload"] = True

        for k in args.keys():
            if k not in valid_args:
                del args[k]
        action_method.__call__(**args)
        logger.info("{name} {action}({args}) called".format(name=str(self), action=method, args=args))
