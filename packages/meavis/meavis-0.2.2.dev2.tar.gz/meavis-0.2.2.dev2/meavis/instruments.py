"""Main loop functions for running MeaVis measurements."""
import collections
import importlib
import logging
import sys
import threading

import meavis._detail.debug
import meavis._detail.default
import meavis._detail.inject
import meavis._detail.utils
import meavis.completer
import meavis.markup
import meavis.measurements
import meavis.parameters


self_module = sys.modules[__name__]


def clear(module_name):
    """Clear injected names by users."""
    module = importlib.import_module("meavis.{}".format(module_name))
    for injected_name in [
        key
        for key, value in module.__dict__.items()
        if hasattr(value, "_meavis_injected") and value._meavis_injected
    ]:
        delattr(module, injected_name)
        logging.getLogger("meavis").info(
            "Unregister injected class named {}.".format(injected_name)
        )


def inject(instruments):
    """Inject instruments."""
    meavis._detail.debug.parameter_isinstance(
        "instruments", collections.abc.Mapping
    )

    modules = {
        instrument_name: instrument["module"]
        for instrument_name, instrument in meavis.markup.visit_instruments(
            instruments, None, "*"
        ).items()
        if "module" in instrument
    }

    all_tags = ["parameters", "measurements"]

    for meavis_name, constructor_map in meavis.markup.visit_instruments(
        instruments, "constructor", "*.~"
    ).items():
        meavis_name_split = meavis_name.split(".")
        intrument_cls = meavis._detail.inject.inject_namespace(
            meavis_name_split[0], self_module
        )
        if not constructor_map:
            constructor_map["class"] = meavis._detail.default.Constructor
            logging.getLogger("meavis").info(
                "Add {} default constructor.".format(meavis_name_split[0])
            )
        if "module" not in constructor_map and meavis_name_split[0] in modules:
            constructor_map["module"] = modules[meavis_name_split[0]]

        constructor_cls = meavis._detail.inject.inject_cls_by_dict(
            constructor_map,
            intrument_cls,
            "constructor",
            meavis_name,
        )
        constructor_cls._meavis_map = {}

    initialisers = {
        meavis_name.split(".")[0]: initialiser_map
        for meavis_name, initialiser_map in meavis.markup.visit_instruments(
            instruments, "initialiser", "*.~"
        ).items()
    }
    for meavis_name, initialiser in initialisers.items():
        if "module" not in initialiser and meavis_name in modules:
            initialiser["module"] = modules[meavis_name]

    all_usages = {}
    for meavis_name, initialiser_map in meavis.markup.visit_instruments(
        instruments, "initialiser", "*.*"
    ).items():
        meavis_name_split = meavis_name.split(".")
        usage_cls = meavis._detail.inject.inject_namespace(
            ".".join(meavis_name_split[:2]), self_module
        )
        meavis._detail.inject.inject_cls_by_dict(
            meavis._detail.utils.merge_mapping(
                initialiser_map, initialisers[meavis_name_split[0]]
            ),
            usage_cls,
            "initialiser",
            meavis_name,
        )
        for tag_name in all_tags:
            meavis._detail.inject.inject_namespace(tag_name, usage_cls)

        if meavis_name_split[0] not in all_usages:
            all_usages[meavis_name_split[0]] = set()
        all_usages[meavis_name_split[0]].add(".".join(meavis_name_split[:2]))

    root_items = {}
    usage_items = {}
    for tag_name in all_tags:
        root_items[tag_name] = meavis.markup.visit_instruments(
            instruments, tag_name, "*.~.*"
        )
        usage_items[tag_name] = meavis.markup.visit_instruments(
            instruments, tag_name, "*.*.*"
        )
        for meavis_name, item_map in usage_items[tag_name].items():
            meavis_name_split = meavis_name.split(".")
            tag_cls = meavis._detail.inject.inject_namespace(
                ".".join(meavis_name_split[:2] + [tag_name]), self_module
            )
            root_name = ".".join(meavis_name_split[::2])
            if root_name in root_items[tag_name]:
                item_map = meavis._detail.utils.merge_mapping(
                    item_map, root_items[tag_name][root_name]
                )
            if "module" not in item_map and meavis_name_split[0] in modules:
                item_map["module"] = modules[meavis_name_split[0]]

            meavis._detail.inject.inject_cls_by_dict(
                item_map, tag_cls, meavis_name_split[2], meavis_name_split[2]
            )
    for tag_name in all_tags:
        for meavis_name, item_map in root_items[tag_name].items():
            meavis_name_split = meavis_name.split(".")
            for usage_name in all_usages[meavis_name_split[0]]:
                tag_cls = meavis._detail.inject.inject_namespace(
                    "{}.{}".format(usage_name, tag_name), self_module
                )
                if (
                    "{}.{}".format(usage_name, meavis_name_split[1])
                    in usage_items[tag_name]
                ):
                    continue
                if (
                    "module" not in item_map
                    and meavis_name_split[0] in modules
                ):
                    item_map["module"] = modules[meavis_name_split[0]]

                meavis._detail.inject.inject_cls_by_dict(
                    item_map,
                    tag_cls,
                    meavis_name_split[1],
                    meavis_name_split[1],
                )


def register(instances):
    """Inject instances."""
    meavis._detail.debug.parameter_isinstance(
        "instances", collections.abc.Mapping
    )

    for instance_name, instance in instances.items():
        meavis._detail.debug.name_isnotinjected(
            instance_name, meavis.parameters
        )
        meavis._detail.debug.name_isnotinjected(
            instance_name, meavis.measurements
        )

        instrument_cls = meavis._detail.inject.inject_namespace(
            instance["instrument"], self_module
        )
        constructor = (
            instrument_cls.constructor(**(instance["kwargs"]))
            if "kwargs" in instance
            else instrument_cls.constructor()
        )
        constructor._meavis_hash = meavis._detail.debug.hash_setpair(
            frozenset(constructor._meavis_kwargs.items())
        )
        if constructor._meavis_hash not in constructor._meavis_map:
            constructor._meavis_map[constructor._meavis_hash] = constructor
            constructor._meavis_handler = None
            constructor._meavis_channels = set()
            constructor._meavis_lock = threading.Lock()
            logging.getLogger("meavis").info(
                "Register {} constructor [{}] {{{}}}.".format(
                    instance["instrument"],
                    constructor._meavis_hash if __debug__ else None,
                    ", ".join(
                        "{}: {}".format(key, value)
                        for key, value in constructor._meavis_kwargs.items()
                    ),
                )
            )

        usage_cls = meavis._detail.inject.inject_namespace(
            instance["usage"], instrument_cls
        )
        initialiser = usage_cls.initialiser()
        initialiser._meavis_constructor = constructor._meavis_map[
            constructor._meavis_hash
        ]
        initialiser._meavis_handler = None
        initialiser._meavis_lock = initialiser._meavis_constructor._meavis_lock
        logging.getLogger("meavis").info(
            "Register {} initialiser {{{}}} for {}.".format(
                instance["usage"],
                ", ".join(
                    "{}: {}".format(key, value)
                    for key, value in initialiser._meavis_kwargs.items()
                ),
                instance_name,
            )
        )
        for key, value in instance["attributes"].items():
            setattr(
                initialiser, "_meavis_{}".format(key.lower().strip()), value
            )

        for parameter in [
            value
            for value in usage_cls.parameters.__dict__.values()
            if hasattr(value, "_meavis_injected") and value._meavis_injected
        ]:
            injected_parameter = meavis.parameters.inject(
                parameter,
                "{}.{}".format(instance_name, parameter._meavis_name),
            )
            injected_parameter._meavis_initialiser = initialiser

        for measurement in [
            value
            for value in usage_cls.measurements.__dict__.values()
            if hasattr(value, "_meavis_injected") and value._meavis_injected
        ]:
            injected_measurement = meavis.measurements.inject(
                measurement,
                "{}.{}".format(instance_name, measurement._meavis_name),
            )
            injected_measurement._meavis_initialiser = initialiser

    meavis.completer.CompleterEngine.inject_instances(
        (
            meavis._detail.inject.inject_namespace(
                instance_name, meavis.parameters
            ),
            meavis._detail.inject.inject_namespace(
                instance_name, meavis.measurements
            ),
        )
        for instance_name in instances
    )
