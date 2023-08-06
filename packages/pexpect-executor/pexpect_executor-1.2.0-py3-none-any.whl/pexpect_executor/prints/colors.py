#!/usr/bin/env python3

# Modules libraries
from colored import attr, fg

# Colors class
class Colors:

    # Constants
    BOLD = attr('reset') + attr('bold')
    CYAN = fg('cyan') + attr('bold')
    GREEN = fg('green') + attr('bold')
    GREEN_THIN = attr('reset') + fg('green')
    GREY = fg('light_gray') + attr('bold')
    RED = fg('red') + attr('bold')
    RED_THIN = attr('reset') + fg('red')
    RESET = attr('reset')
    YELLOW = fg('yellow') + attr('bold')
    YELLOW_LIGHT = fg('light_yellow') + attr('bold')
    YELLOW_THIN = attr('reset') + fg('yellow')

    # Attributes
    ALL = [BOLD, CYAN, GREEN, GREY, RED, RESET, YELLOW, YELLOW_LIGHT]
