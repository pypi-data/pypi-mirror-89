# Oriel Cornerstone 260
A library allowing easy control over an Oriel Cornerstone 260 monochromator with an RS-232C port.
> Install with `python -m pip install oriel-cornerstone-260`

> **_NOTE:_** For newer models with a USB connection, see the [USB Connection](#usb_connection) section at the bottom of this page.

## Monochromator
Represents a monochromator.

+ **Monochromator( port, timeout = 5 ):** Creates a new monochromator for the device at the specificed port, with the provided communication timeout.

### Methods

#### Low Level
Low level methods allows reading and writing to the device.

+ **connect():** Connects to the device.

+ **disconnect():** Disconnects from the device.

+ **write( msg ):** Writes a message to the device. Termination characters are added.

+ **read():** Reads a single response from the device.

+ **command( cmd, \*args ):** Sends a command to the device with the given arguments. Returns the command.

+ **query( msg ):** Queries the device. Returns a Response object.

### High Level
High level methods are convenience methods used for commonly needed functions.

+ **goto( wavelength ):** Goes to the given wavelength.

+ **abort():** Starts the given channel.

+ **set_grating( grating ):** Sets the grating to the given number.

+ **shutter( close = True ):** Open or close the shutter.

+ **set_outport( port ):** Sets the output port.

+ **slit_width( slit, width = None ):** Gets or sets the slit width.


### Properties
+ **_com:** `Serial` connection from `pyserial`.
+ **connected:** Whether the device is connected or not.
+ **port:** Device port.
+ **term_chars:** Termination characters used for reading and writing. [Default: '\r\n']
+ **info:** Device info.
+ **position:** Wavelength position.
+ **grating:** Current grating and its properties. Returns a dictionary with `number`, `lines`, and `label`.
+ **shuttered:** Whether the shutter is closed or open.
+ **outport:** The output port.

## Response
A `namedtuple` with properties `statement` which represents the command, and `response`. 

## Example

A basic example for using a Monochromator.
```python
from oriel_cornerstone_260 import Monochromator

# create device
mono = Monochromator( 'COM9' )

# print monochromator info
print( mono.info )

# go to 600 nm
mono.goto( 600 )
```

#### Note
A Monochromator is a ultimately a `Serial` object from `pyserial`, so you can call any functions on a Monochromator that you would on a Serial object.

---

### <a name="usb_connection"></a>USB Connection
The USB Newport/Oriel Cornerstone 260 works differently, and **can not utilize this package**.
It is Windows only and requires two proprietary .NET .DLLs from Newport.
The Python interface is through the package [pythonnet](https://github.com/pythonnet/pythonnet).
As of late 2020, these are 32 bit DLL's that require a 32-bit (not AMD64) version of python.

```python
import clr
clr.AddReference( 'Cornerstone' )
import CornerstoneDll

mono = CornerstoneDll.Cornerstone( True )
if not mono.connect():
  raise IOError( 'Monochromator not found' )
```
The `mono` object will control the monochromator using methods documented in the Cornerstone 260 manual.
