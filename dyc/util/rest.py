__author__ = 'Justus Adam'

import inspect
import json


def _object_transform(o):
    items = filter(
        (lambda a: not a.startswith('_') and not a in o.__private__)
        if hasattr(o, '__private__') else
        (lambda a: not a.startswith('_'))
        , dir(o))

    def _items():
        for k in items:
            v = getattr(o, k)
            if (not inspect.isfunction(v)
                and not inspect.ismethod(v)
                and not inspect.isclass(v)):
                yield k, v

    return {
        k: v
        for k, v in _items()

    }


json_transform = lambda a: json.dumps(a, default=_object_transform)
