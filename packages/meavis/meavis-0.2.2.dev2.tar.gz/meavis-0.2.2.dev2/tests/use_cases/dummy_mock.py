import time

import meavis.tags


@meavis.tags.constructor("loop_instrument")
class DummyConstructor:
    def __init__(self, addr):
        self.addr = addr

    def create(self):
        return True


@meavis.tags.initialiser("loop_instrument.~")
@meavis.tags.attributes(dummy=True)
@meavis.tags.initialiser("loop_instrument.loop_use_name0")
class DummyInitialiser:
    def __init__(self):
        pass

    def initialise(self, handler, channel):
        return True


@meavis.tags.parameter("loop_instrument.loop_use_name0.parameter0")
@meavis.tags.kwargs(dummy=True)
@meavis.tags.parameter("loop_instrument.loop_use_name0.parameter1")
@meavis.tags.attributes(unit="parameter1_unit")
@meavis.tags.parameter("loop_instrument.loop_use_name1.parameter2")
class DummyParameter:
    def __init__(self, data, dummy=None):
        self.data = data
        self.dummy = dummy
        self.state = True

    def apply(self, handler, value):
        pass

    def is_settled(self, handler):
        self.state = not self.state
        return self.state


@meavis.tags.parameter("loop_instrument.~.parameter3")
@meavis.tags.attributes(unit="parameter3_unit")
class DummyParameterBis:
    def __init__(self, data):
        self.data = data

    def apply(self, handler, value):
        pass


@meavis.tags.measurement("loop_instrument.loop_use_name0.measurement0")
@meavis.tags.kwargs(dummy=True)
@meavis.tags.measurement("loop_instrument.~.measurement1")
@meavis.tags.measurement("loop_instrument.loop_use_name1.measurement2")
@meavis.tags.kwargs(wait_secs=0.1)
@meavis.tags.attributes(invasive=True)
@meavis.tags.attributes(dummy=True)
class DummyMeasurement:
    def __init__(self, wait_secs=0, trigger_secs=0, dummy=None):
        self.dummy = dummy
        self.wait_secs = wait_secs
        self.trigger_secs = trigger_secs

    def trigger(self, handler):
        time.sleep(self.trigger_secs)

    def wait(self, handler):
        time.sleep(self.wait_secs)
