""" 
AIP - Pareto Model

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
from aip.utils.autoload import register, models
from aip.data.access import get_attacks
from datetime import date, timedelta


def pareto8020(df, column, threshold=80):
    df = df.sort_values(by=column, ascending=False)
    cumsum = df[column].cumsum() * 100 / df[column].sum()
    return df[cumsum < threshold]

@register
class Pareto(BaseModel):
    def __init__(self, lookback=60):
        super().__init__()
        self.lookback = lookback

    def run(self, for_date=date.today()):
        start = str(for_date - timedelta(days=self.lookback))
        end = str(for_date - timedelta(days=1))
        column = 'flows'
        attacks = get_attacks(start, end, usecols=['orig', column])
        attacks = pd.concat(attacks)
        attacks = pareto8020(attacks, column, threshold=80)
        attacks = pd.DataFrame(attacks.orig.unique(), columns=['ip'])
        self.blocklist = attacks
        self.sanitize()
        return self.blocklist

