#µCasts Raspberry Pi Library

Python and NodeJS code meant to make interacting with specific hardware on the Raspberry Pi easy. There are lots of sensors and other modules available that can be connected to the Raspberry Pi but most of the time custom code needs to be written to interact with those modules. The code in this project makes using the supported hardware painless and in many cases adds helpful functionality.

Spend more time creating your projects instead of buried in the datasheet trying to figure out if your sensor returns data MSB or LSB first.

## Supported Hardware - Python

  - [Generic LED](python/README.md#led)
  - [Generic Relay](python/README.md#relay)
  - [Generic Switch](python/README.md#switch)
  - [Generic Button](python/README.md#button)
  - [Sparkfun 7 Segment Serial Display](python/README.md#sparkfun-7-segment-serial-display)
  - [TMP102 Sensor](python/README.md#tmp102-sensor)

## Supported Hardware - NodeJS

*Coming Soon*

## Want to Help?
If you're interested in contributing to the project I've included a wish list below.

 - Code review my Python. It's not my strongest language and while the library works there are probably things that could be done in a cleaner/better way
 - Add classes for sensors or other hardware
 - Add more helper functions. Specifically the 7 Segment Display could use some helpers around the decimals, apostrophe, and colon
 - Improve the documentation if you see something wrong.
 - Have RPi.GPIO only be imported if using an I/O class. Currently it's always imported.