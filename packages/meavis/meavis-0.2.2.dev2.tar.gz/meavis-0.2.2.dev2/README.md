## Introduction

MeaVis is a python framework intended to define how **Mea**surements have to
be run and a programming interface to **Vis**ualise resulting datasets.

See more details at [ReadTheDocs.io](https://meavis.readthedocs.io/en/latest/).

### Basic example

#### General configuration of intruments

Let's assume two basic drivers as follow:

```python
import vxi11


class AgilentB596X(vxi11.Instrument):
    def __init__(self, host):
        super().__init__(host=host)

        self.channel = None
        self.mode = None

    def conf():
        if self.channel and self.mode:
            self.write(":SOUR{}:FUNC:MODE {}".format(self.channel, self.mode))

    def output(self, value):
        self.conf()
        if self.channel:
            self.write(
                ":OUTP{} {}".format(self.channel, "ON" if value else "OFF")
            )

    def set_channel(self, channel):
        self.channel = channel
        self.write(":SOUR{}:FUNC:SHAP DC".format(self.channel))
        self.conf()

    def set_mode(self, mode):
        self.mode = mode
        self.conf()

    def set_value(self, value):
        self.write(":SOUR{}:{} {}".format(self.channel, self.mode, value))


class KeySight344XX(vxi11.Instrument):
    def __init__(self, host):
        super().__init__(host=host)

        self.write("*CLS")
        self.write("*RST")

        self.write("TRIG:SOUR IMM")

        self.write("CALC:FUNC AVER")
        self.write("CALC:STAT ON")

        self.ACorDC = None
        self.mode = None

    def calc_average(self):
        self.write("*CALC:AVER:AVER")
        return float(self.read())

    def conf(self):
        if self.ACorDC and self.mode:
            self.write("CONF:{}:{}".format(self.mode, self.ACorDC))

    def conf_ACorDC(self, ACorDC):
        self.ACorDC = ACorDC
        self.conf()

    def conf_mode(self, mode):
        self.mode = mode
        self.conf()

    def count(self, value):
        self.write("SAMP:COUN {}".format(value))

    def initiate(self):
        self.write("INIT")

    def opc(self):
        self.write("*OPC")

    def set_aperture(self, value):
        self.write("{}:APER {}".format(self.mode, value))
```

As you see, this driver is very close to a one-to-one correpondance between
the SPCI commands and the methods. Of course, methods can be more complexe,
however a simplest driver as possible allow more flexiblity.

Then classes specific to MeaVis have to be written to decribe how to use this
driver:
* *Drivers*: Front panel instrument.
* *MeaVis classes*: How an experimentalist use the front panel.

```python
import drivers

import meavis.tags


@meavis.tags.initialiser("power_source.current_source", mode="CURR")
@meavis.tags.initialiser("power_source.voltage_source", mode="VOLT")
class InitialiserB596X:
    def __init__(self, mode):
        self.mode = mode

    def initialise(self, handler, channel):
        handler_channel = drivers.AgilentB596X(**handler)

        handler_channel.set_channel(channel)
        handler_channel.set_mode(self.mode)
        handler_channel.output(True)

        return handler_channel


@meavis.tags.initialiser("multimeter.ac_current_meter")
@meavis.tags.kwargs(mode="CURR", ACorDC="AC")
@meavis.tags.initialiser("multimeter.ac_volt_meter")
@meavis.tags.kwargs(mode="VOLT", ACorDC="AC")
@meavis.tags.initialiser("multimeter.dc_current_meter")
@meavis.tags.kwargs(mode="CURR", ACorDC="DC")
@meavis.tags.initialiser("multimeter.dc_volt_meter")
@meavis.tags.kwargs(mode="VOLT", ACorDC="DC")
class Initialiser344XX:
    def __init__(self, mode, ACorDC):
        self.ACorDC = ACorDC
        self.mode = mode

    def initialise(self, handler, channel):
        handler_channel = drivers.KeySight344XX(**handler)

        handler_channel.conf_mode(self.mode)
        handler_channel.conf_ACorDC(True)

        return handler_channel


@meavis.tags.parameter("power_source.current_source.current")
@meavis.tags.attributes(unit="A", delay=0.1)
@meavis.tags.parameter("power_source.voltage_source.voltage")
@meavis.tags.attributes(unit="V", delay=0.1)
class SourceValue:
    def __init__(self, data):
        self.data = data

    def apply(self, handler, value):
        handler.set_value(value)


@meavis.tags.parameter("multimeter.~.aperture")
@meavis.tags.attributes(unit="s")
class DMMAperture:
    def __init__(self, data):
        self.data = data

    def apply(self, handler, value):
        handler.set_aperture(value)


@meavis.tags.parameter("multimeter.~.average_count")
class DMMCount:
    def __init__(self, data):
        self.data = data

    def apply(self, handler, value):
        handler.count(value)


@meavis.tags.measurement("multimeter.ac_current_meter|dc_current_meter.current")
@meavis.tags.measurement("multimeter.ac_volt_meter|dc_volt_meter.voltage")
class DMMAverage:
    def trigger(self, handler):
        handler.initiate()

    def wait(self, handler):
        handler.opc()
        handler.calc_average()
```

The elements mapped after *kwargs* will be used to initialise the
corresponding instrument when required. For exemple, if a source is used as a
voltage source, the statement 
`handler = meavis_user.InitialiserB596X(mode="VOLT").intialise(/* */)` will be
executed.

This file have to be loaded as follow:

```python
meavis.instruments.inject(meavis_user._meavis_instruments)
```

Note that it cannot be loaded multiple time, otherwise name collisions will
happen.

Up to now the configuration is independant of what we want to measure: it only
describes how to use instruments, but not how they are connect or what we want
to do.

#### Experiment-specific configuration of intruments

First we describe how instruments are wired and for which purpose with a YAML
file:

```yaml
junction_bias:
  instrument: power_source
  usage: voltage_source
  kwargs:
    addr: 192.168.0.0
  attributes:
    channel: 1
junction_current:
  instrument: multimeter
  usage: dc_current_meter
  kwargs:
    host: 192.168.0.1
  attributes:
    channel: 1
junction_voltage:
  instrument: multimeter
  usage: dc_volt_meter
  kwargs:
    host: 192.168.0.1
  attributes:
    channel: 2
```

The elements mapped after *kwargs* will be used to construct the corresponding
instrument when required. For exemple, the multimeter to measure the junction
voltage is constructed with the statement:
`handler = meavis_user.ConstructorEthernet(host="192.168.0.1").create()` when
required. Morevoer the attribute `channel: 2` is used for the initialisation 
`handler = meavis_user.InitialiserB596X(/* */).intialise(/* */, channel=2)`.

This file have to be loaded as follow:

```python
with open("instances.yaml") as file:
    meavis.instruments.register(yaml.safe_load(file))
```

Note that it cannot be loaded multiple time, otherwise name collisions will
happen. After this step, parameters and measurements can be accessed as 
follow:

```python
meavis.parameters.junction_current.aperture([10e-3])
meavis.parameters.junction_current.average_count([100])

meavis.parameters.junction_voltage.aperture([100e-3])
meavis.parameters.junction_voltage.average_count([10])
```

Avaibled parameters and measurements are displayed in the log output:

```
INFO --  Register power_source constructor [90e97748d6ea9cbb434602eb177a91c685701667] {host: 192.168.0.0}.
INFO --  Register voltage_source initialiser {mode: VOLT} for junction_bias.
INFO --  Register voltage as parameter named junction_bias.voltage.
INFO --  Register multimeter constructor [1ca226d3ca09e4167fbbfa3bd218a8323d76e12f] {host: 192.168.0.1}.
INFO --  Register dc_current_meter initialiser {mode: CURR, ACorDC: DC} for junction_current.
INFO --  Register aperture as parameter named junction_current.aperture.
INFO --  Register average_count as parameter named junction_current.average_count.
INFO --  Register current as measurement named junction_current.current.
INFO --  Register dc_volt_meter initialiser {mode: VOLT, ACorDC: DC} for junction_voltage.
INFO --  Register aperture as parameter named junction_voltage.aperture.
INFO --  Register average_count as parameter named junction_voltage.average_count.
INFO --  Register voltage as measurement named junction_voltage.voltage.
INFO --  Add completer group for junction_bias : {junction_bias.voltage}.
INFO --  Add completer group for junction_current : {junction_current.average_count, junction_current.aperture}.
INFO --  Add completer group for junction_voltage : {junction_voltage.aperture, junction_voltage.average_count}.
```

And finally the measurement can be described and processed as follow:

```python
measurement_loop = meavis.loop.LoopEngine(
    yaml.safe_load(
        """
parameters:
    - junction_bias.voltage
measurements:
    - junction_current.current
    - junction_voltage.voltage
name: iv_dc_4probes
"""
)).create(
    meavis.parameters.junction_bias.voltage(numpy.linspace(-1e-3, 1e-3, 401)),
    meavis.measurements.junction_current.current(),
    meavis.measurements.junction_voltage.voltage(),
)
measurement_loop.trigger(None)
measurement_loop.wait(None)
```

In the log output, instruments are created and intialised when required:

```
INFO --  Complete parameters with [junction_current.average_count, junction_current.aperture]
INFO --  Complete parameters with [junction_voltage.aperture, junction_voltage.average_count]
INFO --  Create handler of multimeter.constructor [1ca226d3ca09e4167fbbfa3bd218a8323d76e12f] with {host: 192.168.0.1}.
INFO --  Initialise channel 2 on handler of multimeter.dc_volt_meter.initialiser with {mode: VOLT, ACorDC: DC}.
INFO --  Set junction_voltage.aperture to 0.1 s.
INFO --  Set junction_voltage.average_count to 10.
INFO --  Initialise channel 1 on handler of multimeter.dc_current_meter.initialiser with {mode: CURR, ACorDC: DC}.
INFO --  Set junction_current.aperture to 0.01 s.
INFO --  Set junction_current.average_count to 100.
INFO --  Create handler of power_source.constructor [90e97748d6ea9cbb434602eb177a91c685701667] with {host: 192.168.0.0}.
INFO --  Initialise channel 1 on handler of power_source.voltage_source.initialiser with {mode: VOLT}.
INFO --  Set junction_bias.voltage to -0.001 V.
INFO --  Trigger junction_current.current, waiting for data.
INFO --  Trigger junction_voltage.voltage, waiting for data.
INFO --  Set junction_bias.voltage to -0.000998 V.
INFO --  Trigger junction_current.current, waiting for data.
INFO --  Trigger junction_voltage.voltage, waiting for data.
```
