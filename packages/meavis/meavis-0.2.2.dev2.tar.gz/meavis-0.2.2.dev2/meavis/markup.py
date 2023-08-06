"""Read and write MeaVis markup language."""
import itertools
import logging


def visit_instruments(meavis_instruments, tag_name, meavis_name):
    """Visit an instrument hierarchy and return corresponding items."""
    logging.getLogger("meavis").debug(
        "Markup looking for {} @ {}.".format(meavis_name, tag_name)
    )

    meavis_name_split = [
        part.lower().strip() for part in meavis_name.split(".")
    ]

    if meavis_name_split[0] == "*":
        current_items = {
            instrument_name: instrument
            for instrument_name, instrument in meavis_instruments.items()
        }
    else:
        for instrument_name in [
            part.lower().strip() for part in meavis_name_split[0].split("|")
        ]:
            if instrument_name not in meavis_instruments:
                logging.getLogger("meavis").info(
                    "Add instrument {} in the markup structure.".format(
                        instrument_name
                    )
                )
                meavis_instruments[instrument_name] = {"usages": {}}
        current_items = {
            instrument_name.lower().strip(): meavis_instruments[
                instrument_name.lower().strip()
            ]
            for instrument_name in meavis_name_split[0].split("|")
        }

    if len(meavis_name_split) == 1:
        return current_items
    tag_name_strip = tag_name.lower().strip()
    if meavis_name_split[1] == "*":
        current_items = {
            "{}.{}".format(instrument_name, usage_name): usage
            for instrument_name, instrument in current_items.items()
            for usage_name, usage in instrument["usages"].items()
        }
    elif meavis_name_split[1] == "~":
        pass
    else:
        for usage_name, instrument in itertools.product(
            [part.lower().strip() for part in meavis_name_split[1].split("|")],
            current_items.values(),
        ):
            if usage_name not in instrument["usages"]:
                logging.getLogger("meavis").info(
                    "Add usage {} in the markup structure.".format(usage_name)
                )
                instrument["usages"][usage_name] = {}
        current_items = {
            "{}.{}".format(instrument_name, usage_name): instrument["usages"][
                usage_name.lower().strip()
            ]
            for instrument_name, instrument in current_items.items()
            for usage_name in meavis_name_split[1].split("|")
        }
    for item in current_items.values():
        if tag_name_strip not in item:
            item[tag_name_strip] = {}

    if len(meavis_name_split) == 2:
        return {
            "{}.{}".format(item_name, tag_name_strip): item[tag_name_strip]
            for item_name, item in current_items.items()
        }
    if meavis_name_split[2] == "*":
        current_items = {
            "{}.{}".format(usage_name, item_name): item
            for usage_name, usage in current_items.items()
            for item_name, item in usage[tag_name_strip].items()
        }
    else:
        for item_name, usage in itertools.product(
            [part.lower().strip() for part in meavis_name_split[2].split("|")],
            current_items.values(),
        ):
            if item_name not in usage[tag_name_strip]:
                usage[tag_name_strip][item_name] = {}
        current_items = {
            "{}.{}".format(usage_name, item_name): usage[tag_name_strip][
                item_name.lower().strip()
            ]
            for usage_name, usage in current_items.items()
            for item_name in meavis_name_split[2].split("|")
        }

    return current_items
