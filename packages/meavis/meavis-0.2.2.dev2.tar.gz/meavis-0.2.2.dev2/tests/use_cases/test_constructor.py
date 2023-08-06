import os

import pytest
import pytest_mock
import yaml

import meavis.completer
import meavis.instruments
import meavis.loop
import meavis.tasks


@pytest.fixture(scope="module")
def constructor_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)

    meavis.loop.LoopEngine.clear()
    meavis.completer.CompleterEngine.clear()

    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "constructor_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    meavis.parameters.loop_instance1.parameter0([None])

    parameters = [
        meavis.parameters.loop_instance0.parameter0(range(10)),
    ]

    measurements = [
        meavis.measurements.loop_instance1.measurement0(),
    ]

    parameter_apply_spies = [
        mocker.spy(parameter, "apply") for parameter in parameters
    ]
    measurement_trigger_spies = [
        mocker.spy(measurement, "trigger") for measurement in measurements
    ]
    measurement_wait_spies = [
        mocker.spy(measurement, "wait") for measurement in measurements
    ]

    constructor_spy = mocker.spy(
        parameters[0]._meavis_initialiser._meavis_constructor, "create"
    )

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "constructor.yaml",
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create()
        measurement.trigger(None)
        measurement.wait(None)

    return (
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
        constructor_spy,
    )


def test_constructor_apply_count(constructor_fixture):
    (
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
        constructor_spy,
    ) = constructor_fixture

    assert parameter_apply_spies[0].call_count == 10


def test_constructor_trigger_count(constructor_fixture):
    (
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
        constructor_spy,
    ) = constructor_fixture

    assert measurement_trigger_spies[0].call_count == 10


def test_constructor_wait_count(constructor_fixture):
    (
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
        constructor_spy,
    ) = constructor_fixture

    assert measurement_wait_spies[0].call_count == 10


def test_constructor_create_count(constructor_fixture):
    (
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
        constructor_spy,
    ) = constructor_fixture

    assert constructor_spy.call_count == 1
