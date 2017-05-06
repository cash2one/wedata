# -*- coding: utf-8 -*-
class WedataError(Exception):
    pass


class WedataValueError(ValueError):
    pass


class WedataValueError(TypeError):
    pass


class WedataTimeoutError(TypeError):
    pass


class WedataNotExitsError(TypeError):
    pass


class WedataReturnContextManager(Exception):
    pass

__all__ = ("WedataError", "WedataValueError", "WedataValueError",
           "WedataTimeoutError", "WedataNotExitsError",
           "WedataReturnContextManager")
