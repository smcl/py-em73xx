# py-em73xx [![Build Status](https://travis-ci.org/smcl/py-em73xx.svg?branch=master)](https://travis-ci.org/smcl/py-em73xx) [![Coverage Status](https://coveralls.io/repos/github/smcl/py-em73xx/badge.svg?branch=master)](https://coveralls.io/github/smcl/py-em73xx?branch=master)

Python utility to interact with the telephone functionality of the Sierra Wireless EM73xx modems, present in Lenovo Thinkpads (tested on a Thinkpad X250) and possibly others.

## Install

Either retrieve from pypi using pip:

```
$ pip install em73xx
```

or clone this repo, and install using `setup.py`:
```
$ git clone https://github.com/smcl/py-em73xx
$ cd py-em73xx
$ python setup.py install
```

## Documentation

(TODO, haha!)

## Examples

Initialising the modem:
```
from em73xx import Modem

em7345 = Modem("/dev/ttyACM0", pin="1234", debug=True)
```

receiving/reading SMS messages:
```
messages = em7345.getSMS()
```

sending an SMS message:
```
em7345.sendSMS("775123456", "test message from em73xx!")
```

getting a GPS fix (`None` returned if failed):
```
gps = em7345.getGPS()
if gps:
    print(gps.latitude)
    print(gps.longitude)
```

## TODO

* write documentation - methods, types, etc
* add more functionality, sms and gps alone won't cut it. poking around with the at commands text file in /docs should help
* there's *heaps* of info returned by the `XLCSLSR` command, investigate if there's anything useful we can provide