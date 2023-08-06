# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from .NullLock import NullLock
from .MemoryLock import MemoryLock


class DefaultLockFactory(Factory):
    """
    Creates :class:`ILock` components by their descriptors.

    See :class:`Factory`, :class:`ILock`, :class:`MemoryLock`, :class:`NullLock`
    """
    descriptor = Descriptor("pip-services", "factory", "lock", "default", "1.0")
    null_lock_descriptor = Descriptor("pip-services", "lock", "null", "*", "1.0")
    memory_lock_descriptor = Descriptor("pip-services", "lock", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultLockFactory, self).__init__()
        self.register_as_type(DefaultLockFactory.null_lock_descriptor, NullLock)
        self.register_as_type(DefaultLockFactory.memory_lock_descriptor, MemoryLock)
