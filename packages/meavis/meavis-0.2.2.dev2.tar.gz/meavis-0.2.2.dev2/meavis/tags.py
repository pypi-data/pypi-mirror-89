"""Class decorators to tag MeaVis classes."""
import logging
import sys

import meavis._detail.debug
import meavis.markup


def add_metadata(metadata_name, **kwargs):
    """Add metadata to a tagged MeaVis class."""

    def wrapper(cls):
        if not hasattr(cls, "_meavis_metadata"):
            cls._meavis_metadata = {}
        if metadata_name not in cls._meavis_metadata:
            cls._meavis_metadata[metadata_name] = {}
        for key, value in kwargs.items():
            cls._meavis_metadata[metadata_name][key] = value
        return cls

    return wrapper


def add_item(tag_name, meavis_name, **kwargs):
    """Tag a MeaVis class."""
    logging.getLogger("meavis").info(
        "Add MeaVis item {} @ {}.".format(meavis_name, tag_name)
    )

    def wrapper(cls):
        module = sys.modules[cls.__module__]
        if not hasattr(module, "_meavis_instruments"):
            module._meavis_instruments = {}

        for item in meavis.markup.visit_instruments(
            module._meavis_instruments, tag_name, meavis_name
        ).values():
            item["class"] = cls
            item["kwargs"] = kwargs
            if hasattr(cls, "_meavis_metadata"):
                for (
                    metadata_name,
                    metadata_dict,
                ) in cls._meavis_metadata.items():
                    if metadata_name not in item:
                        item[metadata_name] = {}
                    for key, value in metadata_dict.items():
                        item[metadata_name][key] = value

        if hasattr(cls, "_meavis_metadata"):
            delattr(cls, "_meavis_metadata")

        return cls

    return wrapper


def attributes(**kwargs):
    """Add attributes to a tagged MeaVis class."""
    return add_metadata("attributes", **kwargs)


def kwargs(**kwargs):
    """Add kwargs to a tagged MeaVis class."""
    return add_metadata("kwargs", **kwargs)


def constructor(meavis_name, **kwargs):
    """Tag a class as a MeaVis initialiser."""
    meavis._detail.debug.substring_notin(".", meavis_name)
    return add_item("constructor", "{}.~".format(meavis_name), **kwargs)


def initialiser(meavis_name, **kwargs):
    """Tag a class as a MeaVis initialiser."""
    return add_item("initialiser", meavis_name, **kwargs)


def measurement(meavis_name, **kwargs):
    """Tag a class as a MeaVis measurement."""
    return add_item("measurements", meavis_name, **kwargs)


def parameter(meavis_name, **kwargs):
    """Tag a class as a MeaVis parameter."""
    return add_item("parameters", meavis_name, **kwargs)
