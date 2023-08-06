"""MeaVis parameters completion."""
import collections
import logging

import meavis._detail.debug
import meavis.synchroniser
import meavis.tasks


class CompleterEngine:
    """Define how parameters of a loop has to be completed."""

    instances_parameters = set()

    def __init__(self, data):
        """Store a data structure as loop pattern."""
        meavis._detail.debug.parameter_isinstance(
            "data", collections.abc.Mapping
        )

        self.data = data

        self.logger = logging.getLogger("meavis")

    @classmethod
    def clear(cls):
        """Clear instances set."""
        cls.instances_parameters = set()

    @classmethod
    def inject_instances(cls, instances):
        """Inject instances in CompleterEngine maps."""
        meavis._detail.debug.parameter_isinstance(
            "instances", collections.abc.Iterable
        )

        for instance_parameters, instance_measurements in instances:
            instance_group = frozenset(
                value._meavis_name
                for value in instance_parameters.__dict__.values()
                if hasattr(value, "_meavis_injected")
                and value._meavis_injected
            )
            instance_group_measurement = frozenset(
                value._meavis_name
                for value in instance_measurements.__dict__.values()
                if hasattr(value, "_meavis_injected")
                and value._meavis_injected
            )
            logging.getLogger("meavis").info(
                "Add completer group for {} : {{{}}}.".format(
                    instance_parameters._meavis_name, ", ".join(instance_group)
                )
            )
            cls.instances_parameters.add(
                (instance_group, instance_group_measurement)
            )

    def complete(self, instances=()):
        """Complete a loop pattern."""
        self.inject_instances(instances)

        outer_completion = {
            key: set(key) - set(self.data["parameters"])
            for key, measurements in self.instances_parameters
            if any(
                loop_parameter in key
                for loop_parameter in self.data["parameters"]
            )
            or any(
                measurement in measurements
                for measurement in self.data["measurements"]
                if isinstance(measurement, str)
            )
        }

        completion = {}
        for inner_completion in [
            CompleterEngine(measurement).complete()
            for measurement in self.data["measurements"]
            if not isinstance(measurement, str)
        ] + [outer_completion]:
            for key, value in inner_completion.items():
                if key not in completion:
                    completion[key] = value
                    continue
                completion[key].intersection_update(value)

        return completion
