# Python asyncio library for Bosch thermostats

aionefit is a Python library to control some Bosch thermostats using the Python asycio framework. This is done with the [Slixmpp](https://slixmpp.readthedocs.io) library.

As there is no known way to talk directly to the thermostat, all communication has to be routed via cloud servers at Bosch.

## Original code
This software is based on code of the following projects:
- https://github.com/robertklep/nefit-easy-client
- https://github.com/patvdleer/nefit-client-python

## Supported hardware
[source](https://www.domoticz.com/wiki/NefitEasy)

- Nefit Easy (Netherlands)
- Junkers Control CT100 (Belgium, Germany)
- Buderus Logamatic TC100 (Belgium)
- E.L.M. Touch (France)
- Worcester Wave (UK)
- Bosch Control CT‑100 (Other)
