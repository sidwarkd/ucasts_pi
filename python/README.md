#µCasts Raspberry Pi Library - Python

Python code for interacting with various pieces of hardware on the Raspberry Pi.

## Supported Hardware

  - [Generic LED](#led)
  - [Generic Relay](#relay)
  - [Generic Switch](#switch)
  - [Generic Button](#button)
  - [Sparkfun 7 Segment Serial Display](#sparkfun-7-segment-serial-display)
  - [TMP102 Sensor](#tmp102-sensor)
  - [ID-3LA, ID-12LA, and ID-20LA RFID Readers](#rfid-reader)

##LED
The ```ucasts``` module supports LEDs wired up as either active high or active low. The default is active low which assumes you have the cathode (negative side of the LED) connected to your I/O pin. When an ```LED``` object is deleted it will turn off the associated LED.

###Usage
```
LED(pin[,active_high[,default_on]])
```

| Argument        | Description     | Default   | Optional     |
| :-------------: | :-------------  | :--------: | :----------: |
| pin           | The physical pin number. Not the BCM pin desigation. |  | No
| active_high   | True if the LED anode (positive side) is connected to the output pin. False if the cathode is connected to the output pin.  | False  | Yes
| default_on    | True turns the LED on upon initialization  | False  | Yes

###Functions

#### on()
Turn the LED on

#### off()
Turn the LED off

#### toggle()
Toggle the state of the LED 

###Example
```python
from ucasts import LED
led = LED(12)
led = LED(12, active_high=True)
led = LED(12, active_high=True, default_on=True)
led.on()
led.off()
led.toggle()
```

##Relay
A ```Relay``` in the module works much the same as an ```LED```. The class was broken out simply for code readability. When a ```Relay``` object is deleted it will turn off the associated relay.

###Usage
```
Relay(pin[,default_on])
```

| Argument        | Description     | Default   | Optional     |
| :-------------: | :-------------  | :--------: | :----------: |
| pin           | The physical pin number. Not the BCM pin desigation. |  | No
| default_on    | True turns the relay on upon initialization  | False  | Yes

###Functions

#### on()
Turn the relay on

#### off()
Turn the relay off

#### toggle()
Toggle the state of the relay 

###Example
```python
from ucasts import Relay
relay = Relay(12)
relay = Relay(12, default_on=True)
relay.on()
relay.off()
relay.toggle()
```

##Switch
Can be hooked up to indicate the on state when the input pin senses 3.3v (active_high) or to register the on state when the input pin is low (active_low).

###Usage
```
Switch(pin[,active_high])
```

| Argument        | Description     | Default   | Optional     |
| :-------------: | :-------------  | :--------: | :----------: |
| pin           | The physical pin number. Not the BCM pin desigation. |  | No
| active_high   | If True **is_on()** will return True when **pin** senses a logic 1. If False **is_on()** will return True when **pin** senses a logic 0. | True  | Yes

###Functions

#### is_on()
Returns True if switch is on. False otherwise 

###Example
```python
from ucasts import Switch
sw = Switch(16)
sw = Switch(16, active_high=False)
if sw.is_on():
  ...
```

##Button
Works just like ```Switch``` since a button is just a momentary switch.

###Usage
```
Button(pin[,active_high])
```
See ```Switch``` for description of arguments.

###Functions

#### is_pressed()
Returns True if button is pressed. False otherwise


###Example
```python
from ucasts import Button
btn = Button(18)
btn = Button(18, active_high=False)
if btn.is_pressed():
  ...
```

##Sparkfun 7 Segment Serial Display
The [7 Segment Display](https://www.sparkfun.com/products/11442) from Sparkfun can run in SPI, I2C, or serial mode. This class assumes SPI mode. When the display object is deleted it will clear the display.

###Usage
```
SparkfunSevenSegmentDisplay()
```

###Functions

#### write(data[, clear])
**data** can be of type ```str```, ```list```, or ```int```. The optional paramater **clear**, if set to True, will cause the display to clear first before displaying **data**

#### clear()
Sends a clear command to the display

#### display_time()
Display the current time (24 hour mode) on the display

#### display_temp(temperature, unit)
Will display **temperature** (passed as a numeric type) with the given **unit** passed as 'c', 'f', 'F', or 'f'.


###Example
```python
from ucasts import SparkfunSevenSegmentDisplay
disp = SparkfunSevenSegmentDisplay()
disp.write("cool") # will display "cool" on the display
disp.write(50)     # will add "2" on the display since 50 is the ASCII value for '2'
disp.write([0x01, 0x02], clear=True)  # will display "12" on the display after clearing it
disp.display_temp(32.0, "F")
disp.display_time()
```

##TMP102 Sensor
Interface for the [TMP102 Sensor](https://www.sparkfun.com/products/11931) from Sparkfun.

###Usage
```
TMP102([bus[,address]])
```

| Argument        | Description     | Default   | Optional     |
| :-------------: | :-------------  | :--------: | :----------: |
| bus           | The I2C bus number passed to SMBus init. | 1 | Yes
| address   | Address of sensor  | 0x48  | Yes

###Functions

#### get_temp_in_f()
Return the current temperature in &deg;F

#### get_temp_in_c()
Return the current temperature in &deg;C

###Example
```python
from ucasts import TMP102
temp_sensor = TMP102()  # Uses bus 1 and address 0x48
temp_sensor = TMP102(address=0x49)
tempF = temp_sensor.get_temp_in_f()
tempC = temp_sensor.get_temp_in_c()
```

##RFID Reader
Interface for the [ID-3LA](https://www.sparkfun.com/products/11862), [ID-12LA](https://www.sparkfun.com/products/11827) and [ID-20LA](https://www.sparkfun.com/products/11828) RFID readers.

###Usage
```
ID3LA()
ID12LA()
ID20LA()
```

###Functions

#### get_last_scan()
Returns the unique id of the last scanned tag. **Note:**Until an evented version of this call is created you need to call *get_last_scan()* often enough to prevent queuing of scanned tags. If multiple tags are scanned between calls to this function, calls to the function will return the tags in first-in-first-out order.

#### wait_for_scan()
This function will block program execution until a tag is scanned at which time it returns the unique id of the scanned tag.

###Example
```python
from ucasts import ID12LA
reader = ID12LA()
tag = reader.get_last_scan()
if tag != None:
  # Do something with tag
```