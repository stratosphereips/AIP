""" 
AIP - AlphaX Model

This model filter the attackers of the previous X days. 

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Joaquin Bogado <joaquinbogado@duck.com>"]
__contact__ = "stratosphere@aic.fel.cvut.cz"
__copyright__ = "Copyright 2022, Stratosphere Laboratory."
__credits__ = ["Joaquín Bogado"]
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "Joaquin Bogado"
__version__ = "0.0.1"

import pandas as pd

from aip.models.base import BaseModel
from aip.data.access import get_attacks
from datetime import date, timedelta


class Alpha(BaseModel):
    def __init__(self, lookback=1):
        # should be possible to set an arbitrary start and lookback or start and end to the model?
        super().__init__()
        self.start = str(date.today() - timedelta(days=lookback))
        self.end = str(date.today() - timedelta(days=1))

    def run(self):
        # get all the attackers IPs
        attacks = get_attacks(self.start, self.end, usecols=['orig'])
        attacks = pd.concat(attacks)
        blocklist = list(set(attacks['orig'].values))
        return blocklist

