import sys
from time import localtime, strftime, sleep

try:
  import RPi.GPIO as GPIO
except ImportError:
  print "You need to install the RPi.GPIO module"
  sys.exit(1)

# All I/O notation in the library uses GPIO.BOARD
# numbering for cross-revision compatibility
class IODevice(object):
  def __init__(self, pin, direction, initial_state=GPIO.LOW):

    # Only set the mode once
    if not hasattr(IODevice, 'mode'):
      IODevice.count = 0
      GPIO.setmode(GPIO.BOARD)
      IODevice.mode = GPIO.BOARD

    IODevice.count += 1
    self.pin_num = pin
    if direction == GPIO.OUT:
      GPIO.setup(pin, direction, initial=initial_state)
    else:
      GPIO.setup(pin, direction)

  def set(self, state):
    GPIO.output(self.pin_num, state)

  def read(self):
    return GPIO.input(self.pin_num)

  def __del__(self):
    IODevice.count -= 1
    if IODevice.count == 0:
      GPIO.cleanup()

# By default LEDs are active low meaning the I/O pin controls
# the ground connection so a 0 or low state turns the led on

class OnOffOutput(IODevice):

  def __init__(self, pin, **kwargs):
    
    self.active_high = kwargs.pop("active_high", False)
    self.is_on = kwargs.pop("default_on", False)

    if self.active_high:
      IODevice.__init__(self, pin, GPIO.OUT, self.is_on)
    else:
      IODevice.__init__(self, pin, GPIO.OUT, not self.is_on)

  def on(self):
    if self.active_high:
      IODevice.set(self, GPIO.HIGH)
    else:
      IODevice.set(self, GPIO.LOW)
    self.is_on = True

  def off(self):
    if self.active_high:
      IODevice.set(self, GPIO.LOW)
    else:
      IODevice.set(self, GPIO.HIGH)
    self.is_on = False

  def toggle(self):
    if self.active_high:
      IODevice.set(self, not self.is_on)
    else:
      IODevice.set(self, self.is_on)

    self.is_on = not self.is_on

  def __del__(self):
    self.off()
    IODevice.__del__(self)

class LED(OnOffOutput):
  def __init__(self, pin, **kwargs):
    OnOffOutput.__init__(self, pin, **kwargs)

class Relay(OnOffOutput):
  def __init__(self, pin, **kwargs):
    def_on = kwargs.pop("default_on", False)
    if def_on:
      OnOffOutput.__init__(self, pin, default_on=True, active_high=False)
    else:
      OnOffOutput.__init__(self, pin, active_high=False)


class Switch(IODevice):
  def __init__(self, pin, **kwargs):

    self.active_high = kwargs.pop("active_high", True)
    self.callback = kwargs.pop("callback", None)

    if self.callback != None:
      print "TODO: Implement event based I/O"
      print "Sorry, that isn't supported yet. Using polling"

    IODevice.__init__(self, pin, GPIO.IN)

  ## Polling Method
  def is_on(self):
    if self.active_high:
      return self.read() == 1
    else:
      return self.read() == 0

  ## Evented Callback

  def __del__(self):
    IODevice.__del__(self)


class Button(Switch):
  def __init__(self, pin, **kwargs):

    Switch.__init__(self, pin, **kwargs)

  ## Polling Method
  def is_pressed(self):
    return self.is_on()

  ## Evented Callback

class SerialDevice(object):
  def __init__(self, baudrate, **kwargs):
    try:
      import serial
    except ImportError:
      print "You need to install the serial module"
      sys.exit(1)

    self.baudrate = baudrate
    self.timeout = kwargs.pop("timeout", 0.1)
    self.enabled = True;

    if not hasattr(SerialDevice, 'sp'):
      SerialDevice.sp = serial.Serial("/dev/ttyAMA0", baudrate=self.baudrate, timeout=self.timeout)
    else:
      print "Another SerialDevice exists. Only one serial device may be instantiated at a time."
      self.enabled = False;

  def readline(self):
    if self.enabled:
      return SerialDevice.sp.readline()
    else:
      return ''

  def read(self, size):
    if self.enabled:
      return SerialDevice.sp.read(size)
    else:
      return ''

  def __del__(self):
    if self.enabled:
      SerialDevice.sp.close()

class I2CDevice(object):
  def __init__(self, bus_num, address, **kwargs):
    try:
      import smbus
    except ImportError:
      print "You need to install the smbus module"
      sys.exit(1)

    self.bus_num = bus_num
    self.address = address

    if not hasattr(I2CDevice, 'bus'):
      I2CDevice.bus = smbus.SMBus(bus_num)

  def read_word(self, register_address):
    return I2CDevice.bus.read_word_data(self.address, register_address)

  def read_byte(self, register_address):
    return I2CDevice.bus.read_byte_data(self.address, register_address)

class SPIDevice(object):

  def __init__(self, spi_num, ce_num, **kwargs):
    try:
      import spidev
    except ImportError:
      print "You need to install the spidev module"
      sys.exit(1)

    self.spi_num = spi_num
    self.ce_num = ce_num

    if "max_speed" in kwargs:
      self.max_speed = kwargs["max_speed"]

    if not hasattr(SPIDevice, 'spi'):
      SPIDevice.spi = spidev.SpiDev()
      SPIDevice.current_spi = spi_num
      SPIDevice.current_ce = ce_num
      SPIDevice.spi.open(self.spi_num, self.ce_num)

  def set_bus(self):
    if(SPIDevice.current_spi != self.spi_num and SPIDevice.current_ce != self.ce_num):
      SPIDevice.spi.close()
      SPIDevice.current_spi = self.spi_num
      SPIDevice.current_ce = self.ce_num
      SPIDevice.spi.open(self.spi_num, self.ce_num)

  def send_data(self, data):
    self.set_bus()

    xfer_list = []
    if type(data) == str:
      for c in data:
        xfer_list.append(ord(c))
    elif type(data) == list:
      xfer_list += data
    elif type(data) == int:
      xfer_list.append(data)
    else:
      print "Unsupported type passed to write. Must be str, int, or list"

    if hasattr(self, 'max_speed'):
      SPIDevice.spi.xfer2(xfer_list, self.max_speed)
    else:
      SPIDevice.spi.xfer2(xfer_list)


  def __del__(self):
    SPIDevice.spi.close()

class SparkfunSevenSegmentDisplay(SPIDevice):
  def __init__(self, **kwargs):
    if "spi" in kwargs:
      print "TODO: Implement spi and ce keyword args"
      print "Not supported yet. Using default of 0,0"

    SPIDevice.__init__(self, 0, 0, max_speed=250000)

  def __del__(self):
    self.clear()
    SPIDevice.__del__(self)

  def write(self, data, **kwargs):
    if "clear" in kwargs and kwargs["clear"] == True:
      self.clear()
    
    # TODO: Handle decimal points and colon

    self.send_data(data)

  def clear(self):
    self.send_data([0x76])

  # ======= UTILITY FUNCTIONS =======

  def display_time(self):
    t = strftime("%H%M", localtime())
    self.clear()
    self.send_data(t)
    self.send_data([0x77, 0x10])

  def display_temp(self, temp, unit):
    # Display temp with one decimal of precision
    temp_format = "{:4.1f}" + unit
    temp_str = temp_format.format(round(temp,1))
    display_val = temp_str.replace('.','')
    self.clear()
    self.send_data(display_val)
    # Turn on the decimal and the apostrophe
    self.send_data([0x77, 0x22])

class TMP102(I2CDevice):
  def __init__(self, **kwargs):

    bus = kwargs.pop("bus", 1)
    address = kwargs.pop("address", 0x48)

    I2CDevice.__init__(self, bus, address)

  def get_temp_in_f(self, **kwargs):
    temp = self.read_word(0)
    byte1_mask = 0b0000000011111111
    byte2_mask = 0b1111111100000000
    byte1 = (temp & byte1_mask) << 4
    byte2 = (temp & byte2_mask) >> 12
    temp_c = byte2 | byte1
    temp_c *= .0625
    temp_f = temp_c*1.80 + 32.00
    if "digits" in kwargs: 
      return round(temp_f,int(kwargs["digits"]))
    else:
      return temp_f

  def get_temp_in_c(self, **kwargs):
    temp = self.read_word(0)
    byte1_mask = 0b0000000011111111
    byte2_mask = 0b1111111100000000
    byte1 = (temp & byte1_mask) << 4
    byte2 = (temp & byte2_mask) >> 12
    temp_c = byte2 | byte1
    temp_c *= .0625
    if "digits" in kwargs: 
      return round(temp_c,int(kwargs["digits"]))
    else:
      return temp_c

class InnovationsRFIDReader(SerialDevice):
  def __init__(self):
    SerialDevice.__init__(self, 9600)

  def get_last_scan(self):
    data = self.readline()
    if len(data) > 0:
      # Read and discard the ETX byte
      self.read(1)
      # The actual id consists of the 10 characters after the STX byte
      return data[1:11]
    else:
      return None

  def wait_for_scan(self):
    rfid = None
    while rfid == None:
      sleep(.1)
      rfid = self.get_last_scan()

    return rfid

class ID12LA(InnovationsRFIDReader):
  pass

class ID20LA(InnovationsRFIDReader):
  pass

class ID3LA(InnovationsRFIDReader):
  pass