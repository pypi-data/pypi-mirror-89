import sys

import pytest

import meavis.instruments
import meavis.markup
import meavis.tags


self_module = sys.modules[__name__]


@meavis.tags.constructor("instrument")
class DummyConstructor:
    pass


@meavis.tags.initialiser("instrument.~")
@meavis.tags.attributes(dummy_attributes=True)
class DummyInitialiser:
    pass


@meavis.tags.initialiser("instrument.usage0")
@meavis.tags.attributes(dummy_attributes_bis=True)
class DummyInitialiserUsage0:
    pass


@meavis.tags.parameter("instrument.~.parameter0")
@meavis.tags.attributes(dummy_attributes=True)
class DummyParameter:
    pass


@meavis.tags.parameter("instrument.usage1.parameter1|parameter2")
@meavis.tags.parameter("instrument.usage1.parameter0")
@meavis.tags.attributes(dummy_attributes_bis=True)
class DummyParameterUsage1:
    pass


@meavis.tags.measurement("instrument.~.measurement0")
@meavis.tags.attributes(dummy_attributes=True)
class DummyMeasurement:
    pass


@meavis.tags.measurement("instrument.usage2.measurement1|measurement2")
@meavis.tags.measurement("instrument.usage2.measurement0")
@meavis.tags.attributes(dummy_attributes_bis=True)
class DummyMeasurementUsage2:
    pass


def test_constructor_map():
    assert "instrument" in self_module._meavis_instruments

    instrument = self_module._meavis_instruments["instrument"]

    assert "constructor" in instrument
    assert instrument["constructor"]
    assert instrument["constructor"]["class"] == DummyConstructor


def test_initialiser_map():
    assert "instrument" in self_module._meavis_instruments

    instrument = self_module._meavis_instruments["instrument"]

    assert "initialiser" in instrument
    assert "class" in instrument["initialiser"]
    assert instrument["initialiser"]["class"] == DummyInitialiser

    usages = instrument["usages"]

    assert "usage0" in usages
    assert "initialiser" in usages["usage0"]
    assert "class" in usages["usage0"]["initialiser"]
    assert usages["usage0"]["initialiser"]["class"] == DummyInitialiserUsage0


def test_parameters_map():
    assert "instrument" in self_module._meavis_instruments

    instrument = self_module._meavis_instruments["instrument"]

    assert "parameters" in instrument
    assert "parameter0" in instrument["parameters"]
    assert "class" in instrument["parameters"]["parameter0"]
    assert instrument["parameters"]["parameter0"]["class"] == DummyParameter

    usages = instrument["usages"]

    assert "usage1" in usages
    assert "parameters" in usages["usage1"]

    parameters = usages["usage1"]["parameters"]

    assert "parameter0" in parameters
    assert "class" in parameters["parameter0"]
    assert parameters["parameter0"]["class"] == DummyParameterUsage1

    assert "parameter1" in parameters
    assert "class" in parameters["parameter1"]
    assert parameters["parameter1"]["class"] == DummyParameterUsage1

    assert "parameter2" in parameters
    assert "class" in parameters["parameter2"]
    assert parameters["parameter2"]["class"] == DummyParameterUsage1


def test_measurements_map():
    assert "instrument" in self_module._meavis_instruments

    instrument = self_module._meavis_instruments["instrument"]

    assert "measurements" in instrument
    assert "measurement0" in instrument["measurements"]
    assert "class" in instrument["measurements"]["measurement0"]
    assert (
        instrument["measurements"]["measurement0"]["class"] == DummyMeasurement
    )

    usages = instrument["usages"]

    assert "usage2" in usages
    assert "measurements" in usages["usage2"]

    measurements = usages["usage2"]["measurements"]

    assert "measurement0" in measurements
    assert "class" in measurements["measurement0"]
    assert measurements["measurement0"]["class"] == DummyMeasurementUsage2

    assert "measurement1" in measurements
    assert "class" in measurements["measurement1"]
    assert measurements["measurement1"]["class"] == DummyMeasurementUsage2

    assert "measurement2" in measurements
    assert "class" in measurements["measurement2"]
    assert measurements["measurement2"]["class"] == DummyMeasurementUsage2


@pytest.fixture(scope="module")
def setup():
    meavis.instruments.inject(self_module._meavis_instruments)


def test_constructor(setup):
    assert hasattr(meavis.instruments, "instrument")
    assert hasattr(meavis.instruments.instrument, "constructor")


def test_initialisers(setup):
    assert hasattr(meavis.instruments, "instrument")

    assert hasattr(meavis.instruments.instrument, "usage0")
    assert hasattr(meavis.instruments.instrument.usage0, "initialiser")
    assert hasattr(
        meavis.instruments.instrument.usage0.initialiser,
        "_meavis_dummy_attributes",
    )
    assert hasattr(
        meavis.instruments.instrument.usage0.initialiser,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage1")
    assert hasattr(meavis.instruments.instrument.usage1, "initialiser")
    assert hasattr(
        meavis.instruments.instrument.usage1.initialiser,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage1.initialiser,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage2")
    assert hasattr(meavis.instruments.instrument.usage2, "initialiser")
    assert hasattr(
        meavis.instruments.instrument.usage2.initialiser,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage2.initialiser,
        "_meavis_dummy_attributes_bis",
    )


def test_parameters(setup):
    assert hasattr(meavis.instruments, "instrument")

    assert hasattr(meavis.instruments.instrument, "usage0")
    assert hasattr(meavis.instruments.instrument.usage0, "parameters")
    assert hasattr(
        meavis.instruments.instrument.usage0.parameters, "parameter0"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.parameters, "parameter1"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.parameters, "parameter2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage0.parameters.parameter0,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.parameters.parameter0,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage1")
    assert hasattr(meavis.instruments.instrument.usage1, "parameters")
    assert hasattr(
        meavis.instruments.instrument.usage1.parameters, "parameter0"
    )
    assert hasattr(
        meavis.instruments.instrument.usage1.parameters, "parameter1"
    )
    assert hasattr(
        meavis.instruments.instrument.usage1.parameters, "parameter2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage1.parameters.parameter0,
        "_meavis_dummy_attributes",
    )
    assert hasattr(
        meavis.instruments.instrument.usage1.parameters.parameter0,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage2")
    assert hasattr(meavis.instruments.instrument.usage2, "parameters")
    assert hasattr(
        meavis.instruments.instrument.usage2.parameters, "parameter0"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage2.parameters, "parameter1"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage2.parameters, "parameter2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage2.parameters.parameter0,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage2.parameters.parameter0,
        "_meavis_dummy_attributes_bus",
    )


def test_measurements(setup):
    assert hasattr(meavis.instruments, "instrument")

    assert hasattr(meavis.instruments.instrument, "usage0")
    assert hasattr(meavis.instruments.instrument.usage0, "measurements")
    assert hasattr(
        meavis.instruments.instrument.usage0.measurements, "measurement0"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.measurements, "measurement1"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.measurements, "measurement2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage0.measurements.measurement0,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage0.measurements.measurement0,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage1")
    assert hasattr(meavis.instruments.instrument.usage1, "measurements")
    assert hasattr(
        meavis.instruments.instrument.usage1.measurements, "measurement0"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage1.measurements, "measurement1"
    )
    assert not hasattr(
        meavis.instruments.instrument.usage1.measurements, "measurement2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage1.measurements.measurement0,
        "_meavis_dummy_attributes",
    )
    assert not hasattr(
        meavis.instruments.instrument.usage1.measurements.measurement0,
        "_meavis_dummy_attributes_bis",
    )

    assert hasattr(meavis.instruments.instrument, "usage2")
    assert hasattr(meavis.instruments.instrument.usage2, "measurements")
    assert hasattr(
        meavis.instruments.instrument.usage2.measurements, "measurement0"
    )
    assert hasattr(
        meavis.instruments.instrument.usage2.measurements, "measurement1"
    )
    assert hasattr(
        meavis.instruments.instrument.usage2.measurements, "measurement2"
    )
    assert hasattr(
        meavis.instruments.instrument.usage2.measurements.measurement0,
        "_meavis_dummy_attributes",
    )
    assert hasattr(
        meavis.instruments.instrument.usage2.measurements.measurement0,
        "_meavis_dummy_attributes_bis",
    )


def test_wildcard():
    assert (
        set(["instrument"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, None, "*"
        ).keys()
    )


def test_wildcard_wildcard():
    assert (
        set(
            [
                "instrument.usage0.initialiser",
                "instrument.usage1.initialiser",
                "instrument.usage2.initialiser",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "initialiser", "*.*"
        ).keys()
    )
    assert (
        set(
            [
                "instrument.usage0.parameters",
                "instrument.usage1.parameters",
                "instrument.usage2.parameters",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.*"
        ).keys()
    )
    assert (
        set(
            [
                "instrument.usage0.measurements",
                "instrument.usage1.measurements",
                "instrument.usage2.measurements",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.*"
        ).keys()
    )


def test_wildcard_wildcard_wildcard():
    assert (
        set(
            [
                "instrument.usage1.parameter0",
                "instrument.usage1.parameter1",
                "instrument.usage1.parameter2",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.*.*"
        ).keys()
    )
    assert (
        set(
            [
                "instrument.usage2.measurement0",
                "instrument.usage2.measurement1",
                "instrument.usage2.measurement2",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.*.*"
        ).keys()
    )


def test_wildcard_home():
    assert (
        set(["instrument.constructor"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "constructor", "*.~"
        ).keys()
    )
    assert (
        set(["instrument.initialiser"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "initialiser", "*.~"
        ).keys()
    )


def test_wildcard_home_wildcard():
    assert (
        set(["instrument.parameter0"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.~.*"
        ).keys()
    )
    assert (
        set(["instrument.measurement0"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.~.*"
        ).keys()
    )


def test_wildcard_or():
    assert (
        set(["instrument.usage0.initialiser", "instrument.usage2.initialiser"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "initialiser", "*.usage0|usage2"
        ).keys()
    )
    assert (
        set(["instrument.usage0.parameters", "instrument.usage2.parameters"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.usage0|usage2"
        ).keys()
    )
    assert (
        set(
            [
                "instrument.usage0.measurements",
                "instrument.usage2.measurements",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.usage0|usage2"
        ).keys()
    )


def test_wildcard_wildcard_or():
    assert (
        set(
            [
                "instrument.usage0.parameter1",
                "instrument.usage1.parameter1",
                "instrument.usage2.parameter1",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.*.parameter1"
        ).keys()
    )
    assert (
        set(
            [
                "instrument.usage0.measurement1",
                "instrument.usage1.measurement1",
                "instrument.usage2.measurement1",
            ]
        )
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.*.measurement1"
        ).keys()
    )


def test_wildcard_home_or():
    assert (
        set(["instrument.parameter0"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "parameters", "*.~.parameter0"
        ).keys()
    )
    assert (
        set(["instrument.measurement0"])
        == meavis.markup.visit_instruments(
            self_module._meavis_instruments, "measurements", "*.~.measurement0"
        ).keys()
    )
