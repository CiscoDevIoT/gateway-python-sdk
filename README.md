# gateway-python-sdk

### Python SDK for DevIoT service ([https://deviot.cisco.com/](https://deviot.cisco.com/))

You can use this SDK to register devices to DevIoT, and sync up data and actions between the devices and DevIoT.

## Table of contents

* [Getting Started](#getting-started)
* [Run sample code on Raspberry Pi](#run-sample-code-on-raspberry-pi)
* [API](#api)

## Requirement
1. [Python 2.7](https://www.python.org/downloads/): This SDK base on the Python 2.7.10
2. [paho-mqtt](https://eclipse.org/paho/clients/python/): This SDK use this library to build a MQTT client

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
git clone https://wwwin-github.cisco.com/DevIoT/gateway-python-sdk.git
cd gateway-pythohn-sdk
```
install sdk package on python 2 
```
python setup.py install
```

#### 2) Connect gateway (python code)
Import SDK
```
from cisco_deviot.gateway import Gateway
from cisco_deviot.thing import Thing
from cisco_deviot.thing import Property
import constants
```
Construct a Gateway object
```
account = "your_id@cisco.com"
app = Gateway("gateway_name", "deviot.cisco.com", "deviot.cisco.com:18883", "device", account)
```

Contruct a thing instance
```
thing = Thing("thing-id", "thing-name", "thing-kind")
```

Add a property to the thing
```
property = Property("variable_name", constants.PROPERTY_TYPE_INT, 0)
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
## Run sample code on Raspberry Pi
#### Build the hardware
###### 1. Prepare your Raspberry Pi os environment in your SD card
* Download the OS for Raspberry Pi form [RASPBIAN JESSIE](https://www.raspberrypi.org/downloads/raspbian/)
* Format you SD card
* Use window install the OS image to the SD card. you can use [Win32 Disk Manager](https://sourceforge.net/projects/win32diskimager/).
    I strongly recommend you do this using Windows, I have met many issues when i installed it by mac OS
* Attach the SD card to the Raspberry Pi

You also can follow [this instructions](https://www.raspberrypi.org/documentation/installation/noobs.md)

######2. Connect the GrovePi to the Raspberry Pi.

######3. Connect Raspberry Pi with the power and network.

######4. Connect Raspberry Pi with Display using HDMI cable.

#### Build the software environment
######5. Install the Python 2.7. 
* Check the version of python that Raspberry Pi has. This sample code is based on python 2.7.3 or later. in most time, the Raspberry Pi os have installed the python 2.7.3 or later, if not, you can install the python follow [here](https://www.raspberrypi.org/documentation/linux/software/python.md)

######6. Install GrovePi SDK.

* Make sure your Raspberry Pi is connected to the Internet. 
* Type the following commands in terminal window
    
        sudo apt-get update
        sudo apt-get install rpi.gpio
    
* [Follow the tutorial for setting up the GrovePi](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/).
* Reboot your Raspberry Pi board.
    
Your SD card now has what it needs to start using the GrovePi.
[More information about installing GrovePi SDK](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/)

#### Run GrovePi sample code

######7. Download SDK and run the sample code
* Download SDK and go to the main directory of the repo

        git clone https://wwwin-github.cisco.com/DevIoT/gateway-python-sdk.git
        cd gateway-pythohn-sdk
* Run the sample python code
        
        python sample_code_for_GrovePi_sensor.py
&nbsp;
## API
### Gateway
#### Constructor
```
Gateway(name, deviot_server, connector_server, kind="device", account="")
```
The Gateway() constructor takes the following arguments:  
**name**  
The unique name of a gateway  
**deviot_server**  
The address for the DevIoT server. It does not need to add the protocol. The default protocol is HTTPS(secure connection). The public DevIoT server address is 'deviot.cisco.com'  
**connector_server**  
The address for the MQTT server. It does not need to add the protcol. The default protocol is TCP(unsecure connection) and the default port number is 1883. The public MQTT server address is 'deviot.cisco.com:18883'  
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
#### deregister()
```
deregister(*things)
```
The deregister() function deletes things from the gateway.  
**thing**  
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
The variable type of a property. There are 4 types: int, bool, string, color. You can use constants.PROPERTY_TYPE_INT, constants.PROPERTY_TYPE_BOOL, constants.PROPERTY_TYPE_STRING, constants.PROPERTY_TYPE_COLOR after importing constants.  
**value**  
The value of a property.  
**range**  
The range of a property's value.  
**unit**  
The unit of a property. It is string value.  
**description**  
The description for a property. It is shown at the page of each thing.
