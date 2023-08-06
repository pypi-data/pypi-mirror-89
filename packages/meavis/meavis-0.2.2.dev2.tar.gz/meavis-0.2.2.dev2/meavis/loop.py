"""Main loop functions for running MeaVis measurements."""
import collections
import itertools
import logging
import os
import threading

import yaml

import meavis._detail.debug
import meavis.completer
import meavis.synchroniser
import meavis.tasks


class LoopMeasurement:
    """Define a measurement running a loop."""

    def __init__(self, parameters, measurements):
        """Ceate a loop measurement."""
        meavis._detail.debug.parameter_isinstance(
            "parameters", collections.abc.Sequence
        )
        meavis._detail.debug.parameter_isinstance(
            "measurements", collections.abc.Sequence
        )

        self.parameters = parameters
        self.measurements = measurements

        self._meavis_logger = logging.getLogger("meavis")
        self._meavis_handler = self

    def trigger(self, handler):
        """Nothing to trigger."""
        pass

    def wait(self, handler):
        """Run the loop."""
        for samples in itertools.product(
            *(parameter.data for parameter in self.parameters)
        ):
            parameter_tasks = []
            parameter_locks = [threading.Lock()]
            for parameter, sample in zip(self.parameters, samples):
                if sample == parameter._meavis_current:
                    continue
                parameter_locks.append(threading.Lock())
                parameter_locks[-1].acquire()
                parameter_tasks.append(
                    threading.Thread(
                        target=meavis.tasks.settle,
                        args=(
                            parameter,
                            sample,
                            parameter_locks[-2],
                            parameter_locks[-1],
                            True,
                        ),
                    )
                )
                parameter_tasks[-1].start()

            self._meavis_logger.debug("\tJoin parameter tasks.")
            for task in parameter_tasks:
                task.join()

            measurement_tasks = []
            measurement_locks = [threading.Lock()]
            measurement_barriers = []
            for measurement in self.measurements:
                measurement_locks.append(threading.Lock())
                measurement_locks[-1].acquire()

                measurement_barriers.append(threading.Lock())
                measurement_barriers[-1].acquire()

                measurement_tasks.append(
                    threading.Thread(
                        target=meavis.tasks.trigger_wait,
                        args=(
                            measurement,
                            measurement_locks[-2],
                            measurement_locks[-1],
                            measurement_barriers[-1],
                        ),
                    )
                )
                if measurement._meavis_invasive:
                    for barrier in measurement_barriers[:-1]:
                        barrier.release()
                    for task in measurement_tasks[:-1]:
                        task.join()

                    measurement_barriers = measurement_barriers[-1:]
                    measurement_tasks = measurement_tasks[-1:]

                measurement_tasks[-1].start()

            self._meavis_logger.debug("\tRelease measurement waits.")
            for barrier in measurement_barriers:
                barrier.release()

            self._meavis_logger.debug("\tJoin measurement tasks.")
            for task in measurement_tasks:
                task.join()


class LoopEngine:
    """Define how a loop has to be processed."""

    items_map = {}

    default_map = yaml.safe_load(
        open(
            os.path.expanduser(
                os.path.join("~", ".config", "meavis", "default.yaml")
            )
        )
    )

    def __init__(self, data):
        """Store a data structure as loop pattern."""
        meavis._detail.debug.parameter_isinstance(
            "data", collections.abc.Mapping
        )

        self.data = data

        self.logger = logging.getLogger("meavis")

    @classmethod
    def clear(cls):
        """Clear MeaVis item maps."""
        cls.items_map = {}

    @classmethod
    def inject_items(cls, *items):
        """Inject MeaVis items in the LoopEngine."""
        for item in items:
            logging.getLogger("meavis").debug(
                "Add MeaVis item {} to LoopEngine.".format(item._meavis_name)
            )
            cls.items_map[item._meavis_name] = item

    def inject_defaults(self):
        """Inject default attributes in LoopEngine maps."""
        for parameter_name in self.data["parameters"]:
            parameter = self.items_map[parameter_name]
            for key, value in self.default_map["parameters"].items():
                meavis_key = "_meavis_{}".format(key.lower().strip())
                if not hasattr(parameter, meavis_key):
                    setattr(parameter, meavis_key, value)
                    self.logger.debug(
                        "\tAdd attribute {} = {} to {}.".format(
                            meavis_key, value, parameter_name
                        )
                    )
        for measurement_name in self.data["measurements"]:
            if not isinstance(measurement_name, str):
                LoopEngine(measurement_name).inject_defaults()
                continue
            measurement = self.items_map[measurement_name]
            for key, value in self.default_map["measurements"].items():
                meavis_key = "_meavis_{}".format(key.lower().strip())
                if not hasattr(measurement, meavis_key):
                    setattr(measurement, meavis_key, value)
                    self.logger.debug(
                        "\tAdd attribute self.{} = {} to {}.".format(
                            meavis_key, value, measurement_name
                        )
                    )

    def complete(self):
        """Complete current data structure."""
        for parameters_completion in (
            meavis.completer.CompleterEngine(self.data).complete().values()
        ):
            if not parameters_completion:
                continue
            self.logger.info(
                "Complete parameters with [{}]".format(
                    ", ".join(parameters_completion)
                )
            )
            self.data["parameters"][:0] = parameters_completion

    def create(self, *items, completion=True):
        """Create a measurement from the pattern."""
        self.inject_items(*items)

        if completion:
            self.complete()
        self.inject_defaults()

        effective_parameters = [
            self.items_map[parameter] for parameter in self.data["parameters"]
        ]
        effective_measurements = []
        for measurement in self.data["measurements"]:
            effective_measurements.append(
                self.items_map[measurement]
                if isinstance(measurement, str)
                else LoopEngine(measurement).create(completion=False)
            )
        nested_loop = LoopMeasurement(
            effective_parameters, effective_measurements
        )

        for key, value in self.data.items():
            if key in ["parameters", "measurements"]:
                continue
            meavis_key = "_meavis_{}".format(key.lower().strip())
            setattr(nested_loop, meavis_key, value)
            self.logger.debug(
                "\tAdd attribute self.{} = {} to nested loop.".format(
                    meavis_key, value
                )
            )

        for key, value in self.default_map["measurements"].items():
            meavis_key = "_meavis_{}".format(key.lower().strip())
            setattr(nested_loop, meavis_key, value)
            self.logger.debug(
                "\tAdd attribute self.{} = {} to nested loop.".format(
                    meavis_key, value
                )
            )

        if hasattr(nested_loop, "_meavis_name"):
            self.items_map[nested_loop._meavis_name] = nested_loop

        return nested_loop

    def synchronisers(self, state_parameters, completion=True):
        """Synchronise parameters group from the pattern."""
        meavis._detail.debug.parameter_isinstance(
            "state_parameters", collections.abc.Sequence
        )
        for parameter in state_parameters:
            self.items_map[parameter._meavis_name] = parameter

        if completion:
            self.complete()
        self.inject_defaults()

        candidate_parameters = [
            parameter._meavis_name for parameter in state_parameters
        ]
        loop_parameters = [
            self.items_map[parameter]
            for parameter in self.data["parameters"]
            if parameter in candidate_parameters
        ]
        effective_synchronisers = []
        for measurement in self.data["measurements"]:
            if isinstance(measurement, str):
                continue
            effective_synchronisers.extend(
                LoopEngine(measurement).synchronisers(
                    state_parameters, completion=False
                )
            )

        return (
            [
                meavis.synchroniser.LoopSynchroniser(
                    state_parameters, loop_parameters, effective_synchronisers
                )
            ]
            if loop_parameters
            else effective_synchronisers
        )
