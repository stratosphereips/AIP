""" 
AIP - Prioritize New/Consistent Algorithm

This module prioritize the new/consistent attackers.

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


import numpy as np
import pandas as pd

from aip.models.prioritize_consistent import Consistent
from aip.utils.autoload import register
from datetime import date


@register
class New(Consistent):
    '''
    Prioritize New algorithm
    '''

    def __init__(self):
        super().__init__()
        # Weights from Thomas' Thesis
        # nflows, conns, nbytes, npackets,
        # mean_flows, mean_conns, mean_bytes, mean_packets
        self.weights = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
        self.score_threshold = 0.00001
        self.min_ip_number = 5000

    def _get_IP_scores(self):
        days_since_last_seen = np.array([x.days for x in (pd.to_datetime(date.today()) - self.db.knowledge.last_seen)])
        features = self.db.knowledge[
                ['flows', 'duration','bytes', 'packets', 'mean_flows',
                    'mean_duration', 'mean_bytes', 'mean_packets']
                ].values
        normalized_features = np.zeros_like(features)
        for i in range(8):
            normalized_features[:,i] = (features[:,i] - features[:,i].min()) / (features[:,i].max() - features[:,i].min())
        ipscores = normalized_features * self.weights
        ipscores = ipscores.sum(axis=1)
        aging = 2 / (2 + days_since_last_seen)
        ipscores *= aging
        return ipscores
