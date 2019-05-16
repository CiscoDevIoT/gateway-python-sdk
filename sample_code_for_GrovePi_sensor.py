import time
import traceback
from grovepi import grovepi

from cisco_deviot.gateway import Gateway
from cisco_deviot.thing import Thing
from cisco_deviot.thing import Property
from cisco_deviot import constants

pin = {"A0":14, "A1":15, "A2":16, "D2":2, "D3":3, "D4":4, "D5":5, "D6":6, "D7":7, "D8":8}

# connect each sensor to a pin 
light_sensor_pin = pin["A2"]
led_pin = pin["D3"] 
ultrasonic_sensor_pin = pin["D4"]
temperature_sensor_pin = pin["D7"]
button_sensor_pin = pin["D8"]

grovepi.pinMode(light_sensor_pin, "INPUT")
grovepi.pinMode(led_pin, "OUTPUT")
grovepi.pinMode(ultrasonic_sensor_pin, "INPUT")
grovepi.pinMode(temperature_sensor_pin, "INPUT")
grovepi.pinMode(button_sensor_pin, "INPUT")

   
# turn on/off the led when receive action from DevIot
# action name will be 'on' or 'off'
def trigger_grove_led(action):
    print('led get action:' + action)
    if action == 'on':
        return lambda:grovepi.digitalWrite(led, 1)
    else:
        return lambda:grovepi.digitalWrite(led, 0)

account = 'your_id@cisco.com'
app = Gateway('grovepi', 'deviot.cisco.com', 'deviot.cisco.com:18883', account)

# the parameters of a Thing constructor are: id, display name, kind
light_sensor = Thing('grove_light', 'GroveLight', 'light')
light_sensor.add_property('light')
ultrasonic_sensor = Thing('grove_distance', 'GroveDistance', 'distance')
ultrasonic_sensor.add_property('distance')
temperature_sensor = Thing('grove_temp_hum', 'GroveTempHumd', 'temperature')
temperature_sensor.add_property('temperature', 'humidity')
button_sensor = Thing('grove_button', 'GroveButton', 'button')
button_sensor.add_property(Property('value', constants.PROPERTY_TYPE_BOOL))
led = Thing('grove_led', "GroveLED", led)
led.add_action('on', 'off')
led.on = trigger_grove_led('on')
led.off = trigger_grove_led('off')

app.register(light_sensor, ultrasonic_sensor, temperature_sensor, button_sensor, led)

app.start()

while True:
    try:
        light_value = grovepi.analogRead(light_sensor_pin)
        [temperature_value, humidity_value] = grovepi.dht(temperature_sensor_pin, 0)
        distance_value = grovepi.ultrasonicRead(ultrasonic_sensor_pin)
        button_value = grovepi.digitalRead(button_sensor_pin)
        
        light_sensor.update_property(light=light_value)
        app.update_thing(light_sensor, light=light_value)
        app.update_thing(temperature_sensor, temperature=temperature_value, humidity=humidity_value)
        app.update_thing(ultrasonic_sensor, distance=distance_value)
        app.update_thing(button_sensor, value=button_value)

        time.sleep(0.3)
    except:
        traceback.print_exc()
        break

app.stop()