"""MeaVis parameters namespace for user-defined injection."""
import logging
import sys

import meavis._detail.debug
import meavis._detail.default


self_module = sys.modules[__name__]


def inject(cls, name):
    """Wrap and inject user-defined parameter in this namespace."""
    name_split = [part.lower().strip() for part in name.split(".")]
    parameter_cls = meavis._detail.inject.inject_cls(
        cls,
        meavis._detail.inject.inject_namespace(
            ".".join(name_split[:-1]), self_module
        ),
        name_split[-1],
        ".".join(name_split),
    )
    if not hasattr(parameter_cls, "is_settled"):
        parameter_cls.is_settled = meavis._detail.default.is_settled
    logging.getLogger("meavis").info(
        "Register {} as parameter named {}.".format(
            cls.__name__,
            ".".join(name_split),
        )
    )
    return parameter_cls
