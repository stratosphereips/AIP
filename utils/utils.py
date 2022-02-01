"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from datetime import datetime


class Utils:
    """
    Helpers methods
    """

    @staticmethod
    def now():
        """
        Construct a UTC datetime object
        """
        return datetime.utcnow()
