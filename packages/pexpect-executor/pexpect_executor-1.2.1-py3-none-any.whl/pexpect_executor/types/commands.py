#!/usr/bin/env python3

# Commands class
class Commands:

    # Members
    __arguments = None

    # Constructor
    def __init__(self, arguments):

        # Prepare arguments
        if isinstance(arguments, list):
            self.__arguments = arguments
        else: # pragma: no cover
            self.__arguments = []

    # Getter
    def get(self):

        # Variables
        command = []

        # Prepare command
        for argument in self.__arguments:

            # Quoted argument
            if ' ' in argument:
                command += ['\'%s\'' % (argument)]

            # Standard argument
            else:
                command += [argument]

        # Result
        return ' '.join(command)
