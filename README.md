# gateway-python-sdk

Python SDK for DevIoT gateway service

You can use this SDK to register devices to DevIoT, and sync up data and actions between the devices and DevIoT.

## Requirement
1. [Python 2.7](https://www.python.org/downloads/):This SDK base on the Python 2.7.10
2. [paho-mqtt](https://eclipse.org/paho/clients/python/): this SDK use this library to build a MQTT client

## Usage
1. You can use sample code to register GrovePi sensors and simulated sensors to DevIoT.
2. You can also use SDK to register other sensors and systems to DevIoT.

## Term

- **Gateway**: 'Gateway' is a device connected to DevIoT like a raspberry pi board or a mobile phone
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
copy SDK git repository
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
```
Construct a Gateway object
```
app = Gateway("gateway_name", "deviot.cisco.com", "deviot.cisco.com:18883", "device", "deviot_id@cisco.com")
```

Contruct a thing instance
```
thing = Thing("thing-id", "thing-name", "thing-kind")
```

Add a property to the thing
```
property = Property("variable_name", PropertyTypeInt, 0)
thing.add_property(property);
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
## How to run Sample_Code_for_GrovePi_Sensor.py
#### Build the hardware
1. Prepare your RaspberryPi os environment in your SD card

* Download the OS for RaspberryPi form here[RASPBIAN JESSIE](https://www.raspberrypi.org/downloads/raspbian/)
* Format you SD card
* Use window install the OS image to the SD card. you can use [Win32 Disk Manager](https://sourceforge.net/projects/win32diskimager/) do this 
    I strongly recommend you do this use windows, i have met many issues when i installed it by mac os
* Attach the SD card to the RaspberryPi

You also can do this follow [here](https://www.raspberrypi.org/documentation/installation/noobs.md)

2. Join the GrovePi with RaspberryPi. if you correct, it should be like this

3. Connect RaspberryPi with the power and network.

4. Connect RaspberryPi with Display use the HDMI cables.

#### Build the software environment
5. Install the Python 2.7. Check the python version of RaspberryPi os. this sample code base on python2.7.3 or later. in most time, the RaspberryPi os have installed the python2.7.3 or later, if not, you can 
install the python follow [here](https://www.raspberrypi.org/documentation/linux/software/python.md)

6. Install GrovePi SDK.

* Make sure your Raspberry Pi is connected to the internet. 
* Type follow command in terminal window
    
        sudo apt-get update
        sudo apt-get install rpi.gpio
    
* [Follow this tutorial for setting up the GrovePi](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/).
* Restart the Raspberry Pi.
    
Your SD card now has what it needs to start using the GrovePi!
[Here is info more about install GrovePi SDK](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/)

#### Run Grove Pi sample
* Cd to your work space in terminal window
* Type follow command:
    
        python Sample_Code_for_GrovePi_Sensor.py
&nbsp;
