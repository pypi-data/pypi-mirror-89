import collections
import itertools


def merge_mapping(*args):
    result = {}

    for key, value in itertools.chain(*(arg.items() for arg in args)):
        if key not in result:
            result[key] = value
        elif isinstance(value, collections.abc.Mapping):
            result[key] = merge_mapping(result[key], value)

    return result
