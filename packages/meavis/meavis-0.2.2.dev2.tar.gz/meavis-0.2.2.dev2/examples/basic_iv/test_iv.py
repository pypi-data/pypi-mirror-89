import os

import meavis_user
import numpy
import pytest
import yaml

import meavis.instruments
import meavis.loop


@pytest.fixture
def main_fixture():
    meavis.instruments.inject(meavis_user._meavis_instruments)

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "instances.yaml"
        )
    ) as file:
        meavis.instruments.register(yaml.safe_load(file))

    meavis.parameters.junction_current.aperture([10e-3])
    meavis.parameters.junction_current.average_count([100])
    meavis.parameters.junction_voltage.aperture([100e-3])
    meavis.parameters.junction_voltage.average_count([10])

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
        )
    ).create(
        meavis.parameters.junction_bias.voltage(
            numpy.linspace(-1e-3, 1e-3, 401)
        ),
        meavis.measurements.junction_current.current(),
        meavis.measurements.junction_voltage.voltage(),
    )
    measurement_loop.trigger(None)
    measurement_loop.wait(None)


def test_main(main_fixture):
    assert True
