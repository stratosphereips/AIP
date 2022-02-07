"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import json


class Base:
    """
    Base model
    """

    @classmethod
    def to_dict(self):
        """
        Returns the JSON representation of Base subclass
        """
        json_string = json.dumps(self, default=lambda o:o.__dict__, indent=4, sort_keys=True)
        return json.loads(json_string)
