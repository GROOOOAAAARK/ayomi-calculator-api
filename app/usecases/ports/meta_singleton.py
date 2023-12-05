from abc import ABCMeta
from weakref import WeakValueDictionary

from typing import Any

class MetaSingleton(ABCMeta):
    _instances: WeakValueDictionary = WeakValueDictionary()

    def __call__(cls, *args: Any, **kwds: Any):
        if cls not in cls._instances:
            instance = super(MetaSingleton, cls).__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]
