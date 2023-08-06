from collections import OrderedDict
from copy import deepcopy
from functools import singledispatch
from itertools import groupby
from typing import Callable, Dict, List, Any
import pprint
from .types import KT, VT


def inspect(obj):
    pp = pprint.PrettyPrinter()
    pp.pprint(obj)


def list_flatten(t: list):
    return [item for sublist in t for item in sublist]


def list_groupby(iterable: List[Any], projection) -> List[List[Any]]:
    return [list(it) for k, it in groupby(sorted(iterable, key=projection), projection)]


def list_uniq(a: List) -> List:
    return list(dict.fromkeys(a))


def dict_merge(
    a: Dict[KT, VT], b: Dict[KT, VT], f: Callable[[VT, VT], VT]
) -> Dict[KT, VT]:
    merged = deepcopy(a)
    for k in b.keys():
        if k in merged.keys():
            merged[k] = f(a[k], b[k])
        else:
            merged[k] = b[k]
    return merged


@singledispatch
def config_merger(_, b):
    return b


@config_merger.register
def _(a: dict, b: dict):
    return dict_merge(a, b, config_merger)


@config_merger.register
def _(a: list, b: list):
    return a + b
