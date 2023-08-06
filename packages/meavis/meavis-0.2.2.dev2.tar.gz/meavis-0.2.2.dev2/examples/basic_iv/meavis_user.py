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


@meavis.tags.measurement(
    "multimeter.ac_current_meter|dc_current_meter.current"
)
@meavis.tags.measurement("multimeter.ac_volt_meter|dc_volt_meter.voltage")
class DMMAverage:
    def trigger(self, handler):
        handler.initiate()

    def wait(self, handler):
        handler.opc()
        handler.calc_average()
