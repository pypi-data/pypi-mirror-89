"""MeaVis measurements namespace for user-defined injection."""
import logging
import sys

import meavis._detail.debug
import meavis._detail.inject


self_module = sys.modules[__name__]


def inject(cls, name):
    """Wrap and inject user-defined measurement in this namespace."""
    name_split = [part.lower().strip() for part in name.split(".")]
    measurement_cls = meavis._detail.inject.inject_cls(
        cls,
        meavis._detail.inject.inject_namespace(
            ".".join(name_split[:-1]), self_module
        ),
        name_split[-1],
        ".".join(name_split),
    )
    logging.getLogger("meavis").info(
        "Register {} as measurement named {}.".format(
            cls.__name__,
            ".".join(name_split),
        )
    )
    return measurement_cls
