"""Declares dependencies for use with :mod:`fastapi`."""
try:
    from fastapi import Depends

    __all__ = []
except ImportError:
    __all__ = []
