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
import constants


def default_value_for_type(stype):
    if stype == constants.PROPERTY_TYPE_INT:
        return 0
    if stype == constants.PROPERTY_TYPE_BOOL:
        return False
    if stype == constants.PROPERTY_TYPE_STRING:
        return ""
    if stype == constants.PROPERTY_TYPE_COLOR:
        return "FFFFFF"
    return None


class Property:
    def __init__(self, name, type=constants.PROPERTY_TYPE_INT, value=None, range=None, unit=None, description=None):
        self.name = name
        self.type = type
        if value is None:
            value = default_value_for_type(type)
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

    def __str__(self):
        return "{name}:{value}{unit}".format(name=self.name, value=self.value, unit=self.unit)


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

    def get_data(self):
        return {prop.name: prop.value for prop in self.properties}

    def add_property(self, *thing_properties):
        for prop in thing_properties:
            if isinstance(prop, str):
                self.properties.append(Property(prop))
            elif isinstance(prop, Property):
                self.properties.append(prop)
            else:
                logger.error(
                    "invalid property {property}, only string and Property are supported".format(property=prop))

        return self

    def update_property(self, **new_properties):
        for new_prop_name in new_properties:
            for prop in self.properties:
                if new_prop_name == prop.name:
                    prop.value = new_properties[new_prop_name]
                    break

    def add_action(self, *thing_actions):
        for act in thing_actions:
            if isinstance(act, str):
                self.actions.append(Action(act))
            elif isinstance(act, Action):
                self.actions.append(act)
            else:
                logger.error("invalid action {action}, only string and Action are supported".format(action=act))
        return self

    # method: action name
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
