#!/usr/bin/env python3

# Modules libraries
from pywintypes import error # pylint: disable=import-error
from winpexpect import EOF, TIMEOUT # pylint: disable=import-error
from winpexpect import winspawn as spawn # pylint: disable=import-error

# Components
from .base import Base

# WinPexpect class
class WinPexpect(Base):

    # Constructor
    def __init__(self, command): # pylint: disable=super-init-not-called

        # Spawn command
        self.__spawn(command)

    # Read
    def _read(self):

        # Acquire output
        try:
            return self._child.read_nonblocking(size=1024, timeout=1)
        except EOF:
            if self._child.before: # pragma: no cover
                return [self._child.before]
        except TIMEOUT:
            if self._child.before: # pragma: no cover
                return [self._child.before]

        # Empty output
        return None

    # Spawn
    def __spawn(self, command):

        # Spawn command
        Base._child = spawn(command)

    # Terminate
    def terminate(self, force=False):

        # Terminate process
        try:
            self._child.terminate()
        except error: # pragma: no cover
            pass
