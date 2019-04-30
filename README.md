# gateway-python-sdk

### Python SDK for DevIoT service ([https://deviot.cisco.com/](https://deviot.cisco.com/))

You can use this SDK to register devices to DevIoT and sync up data and actions between the devices and DevIoT.

## Table of contents

* [Getting Started](#getting-started)
* [API](#api)

## Requirement
1. [Python 2.7](https://www.python.org/downloads/): This SDK is based on the Python 2.7.3
2. [paho-mqtt](https://eclipse.org/paho/clients/python/): This SDK uses this library to build a MQTT client

## Usage
1. You can use sample code to register GrovePi sensors and simulated sensors to DevIoT.
2. You can also use SDK to register other sensors and systems to DevIoT.

## Term

- **Gateway**: 'Gateway' is a device connected to DevIoT like a Raspberry Pi board or a mobile phone
- **Thing**: 'Thing' is a sensor or a module in a gateway like a light sensor, LED, or GPS. A thing is an icon in DevIoT. A gateway can have several things.
- **Property**: 'Property' is a variable measured by a thing. For instance, Latitude and longitude are properties of a GPS. A thing can have several properties.
- **Action**: 'Action' is a command for a module. For example, turning on and off LED are two different actions. A thing can have several actions.

## Getting Started
#### 0) Check the version of python (terminal)
In order to use this SDK, the version of python should be 2.x. You can check it with the following command.
```
python --version
```

#### 1) Set up SDK package (terminal)
Clone SDK git repository
```
git clone https://github.com/ailuropoda0/gateway-python-sdk.git
cd gateway-python-sdk
```
install sdk package on python 2 
```
python setup.py install
```

#### 2) Connect gateway (python code)
You can refer the example code in [gateway-python-starter-kit](https://wwwin-github.cisco.com/DevIoT/gateway-python-starter-kit).

Import SDK
```
from cisco_deviot.gateway import Gateway
from cisco_deviot.thing import Thing, Property, PropertyType
```
Construct a Gateway object
```
account = "your_id@cisco.com"
app = Gateway(name="gateway_name", account=account)
```

Contruct a thing instance
```
thing = Thing("thing-id", "thing-name", "thing-kind")
```

Add a property to the thing
```
property = Property("variable_name", PropertyType.INT, 0)
thing.add_property(property);
```

Add an action to the thing
```
thing.add_action("sameple_action")
def custom_function():
    print("action")

thing.sameple_action = custom_function
```

Register the sensor to the gateway
```
app.register(thing)
```

Connect the gateway to the server
```
app.start()
```

#### 3) disconnect gateway (python code)
disconnect gateway
```
app.stop()
```
&nbsp;
## API
### Gateway
#### Constructor
```
Gateway(name, deviot_server="deviot.cisco.com", connector_server="deviot.cisco.com:18883", kind="device", account="")
```
The Gateway() constructor takes the following arguments:  
**name**  
The unique name of a gateway  
**deviot_server**  
The address for the DevIoT server. The default value is 'deviot.cisco.com'. It does not need to add the protocol. The default protocol is HTTPS(secure connection).  
**connector_server**  
The address for the MQTT server. The default value is 'deviot.cisco.com:18883'. It does not need to add the protcol. The default protocol is TCP(unsecure connection) and the default port number is 1883.  
**kind**  
The kind of a gateway  
**account**  
Your DevIoT account. you also can use empty string, it will let all account get the data of your gateway.
#### register()
```
register(*things)
```
The register() function adds things to the gateway. The thing should not have been already registered.  
**thing**  
A *Thing* instance to register
#### load()
```
load(filename, class_directory=None)
```
The load() function registers things from an JSON file named [filename] and the custom Thing-sub classes inside [class_directory].
**filename**  
The JSON file having information of things. filename should include its extension. The way to write this JSON file is described in **gateway-python-starter-kit**.  
**class_directory**  
The directory which has custom Thing-sub class. If the Thing-sub class is defined in the same directory, class_directory should be omitted or be None.

#### deregister()
```
deregister(*things)
```
The deregister() function deletes things from the gateway.  
**\*things**  
A *Thing* instance to deregister
#### update_thing()
```
update_thing(thing, **new_value)
```
The update_thing() function updates the values of a thing.  
**thing**  
The thing to be updated. It can be the string id of a thing or a Thing instance.  
**\*\*new_value**  
The keyword arguments for the updated values. The key is the name of properties and the value is the new value.

#### start()
```
start()
```
Connect the things of the gateway to the DevIoT server and the MQTT server
#### stop()
```
stop()
```
Disconnect the gateway from the DevIoT server and the MQTT server.
### Thing
#### Constructor
```
Thing(id, name, kind=None)
```
The Thing() constructor takes the following arguments:  
**id**  
the unique id of a thing  
**name**  
the display name of a thing in DevIot  
**kind**  
the kind of a thing

#### add_property()
```
add_property(*thing_properties)
```
The add_property() adds properties to a Thing instance. When a string is used for arguments, new Property instance named the string is added to the Thing instance.  
**\*thing_properties**  
The list of Property instances or the string value of properties' name.
#### add_action()
```
add_action(*thing_actions)
```
The add_action() adds actions to a Thing instance. When a string is used for arguments, new Action instance named the string is added to the Thing instance.  
**\*thing_properties**  
The list of Property instances or the string value of actions' name.

### Property
#### Constructor
```
Property(name, type=0, value=None, range=None, unit=None, description=None)
```
The Property() constructor takes the following arguments:  
**name**  
The name of a property. It should be unique in a thing.  
**type**  
The variable type of a property. There are 4 types: int, bool, string, color. You can use PropertyType.INT, PropertyType.BOOL, PropertyType.STRING, PropertyType.COLOR after importing 'PropertyType' class from 'cisco_deviot.thing'.  
**value**  
The value of a property.  
**range**  
The range of a property's value.  
**unit**  
The unit of a property. It is string value.  
**description**  
The description for a property. It is shown at the page of each thing.

### Action
#### Constructor
```
Action(name, **kwargs)
```
The Action() constructor takes the following arguments:  
**name**  
The name of Action. The method with the same name should be defined in a class or an instance. So the name must not overlap with other methods of Thing class like *add_property* and *add_action, and the name cannot contain space ' '.  
**\*\*kwargs**  
The keyword arguments for properties in an action. Key is the name of a property and the value of the property. It is not mandatory.

#### add_parameter()
```
add_parameter(action_parameter)
```
The *add_parameter* adds properties to an Action instance.  
**action_parameter**  
A Property instance to be added
