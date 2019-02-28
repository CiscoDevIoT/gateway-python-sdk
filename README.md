# gateway-python-sdk

Python SDK for DevIoT gateway service

Version: Python 2

## How to use
#### 0) Check the version of python
In order to use this SDK, the version of python should be 2.x. You can check it with the following command.
```
python --version
```

#### 1) Set up SDK package (linux, mac)
copy SDK git repository
```
git clone https://wwwin-github.cisco.com/DevIoT/gateway-python-sdk.git
cd gateway-pythohn-sdk
```
install sdk package on python 2 
```
python setup.py install
```

#### 2) Connect gateway (python)
import sdk
```
from cisco_deviot.gateway import Gateway
from cisco_deviot.thing import Thing
```
construct a Gateway object
```
app = Gateway("gateway_name", "deviot.cisco.com", "deviot.cisco.com:18883", "device", "deviot_id@cisco.com")
```
contruct a sensor instance and register the sensor to the gateway
```
thing = Thing("sensor-id", "sensor-name", "sensor-kind")
app.register(thing)
```
connect gateway to the server
```
app.start()
```

#### 3) disconnect gateway
disconnect gateway
```
app.stop()
```