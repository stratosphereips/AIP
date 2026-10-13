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

from aip.data.access import get_attacks
from aip.models.base import BaseModel
from aip.utils.knowledge_base import Knowledgebase
from datetime import date
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier


class RandomForest(BaseModel):
    '''
    Prioritize Random Forest from Thomas O'Hara's thesis
    '''

    def __init__(self):
        super().__init__()

    def _get_training_target_set(self, for_date=date.today()):
        
        target = Knowledgebase(load_until=for_date - timedelta(days=1))
        target.attacks = get_attacks(dates=[(for_date - timedelta(days=1))])[-1]
        days_since_last_seen = np.array([x.days for x in (pd.to_datetime(for_date) - target.knowledge.last_seen)])
        total_attack_time = np.array([x.days for x in (target.knowledge.last_seen - target.knowledge.first_seen)])
        target.knowledge['last_attack_days'] = days_since_last_seen
        target.knowledge['first_attack_days'] = total_attack_time
        target.features = target.knowledge[target.knowledge['orig'].isin(target.attacks['orig'])]
        target.features = target.knowledge
        target.X = target.features.drop(columns=['orig', 'first_seen', 'last_seen']).values
        
        training = Knowledgebase(load_until=for_date - timedelta(days=2))
        training.knowledge.loc[training.knowledge['flows'] == 0, 'flows'] = 1
        training.attacks = pd.concat(get_attacks(dates=[(for_date - timedelta(days=2))]))
        days_since_last_seen = np.array([x.days for x in (pd.to_datetime(for_date) - training.knowledge.last_seen)])
        total_attack_time = np.array([x.days for x in (training.knowledge.last_seen - training.knowledge.first_seen)])
        training.knowledge['last_attack_days'] = days_since_last_seen
        training.knowledge['first_attack_days'] = total_attack_time
        training.knowledge['target'] = training.knowledge['orig'].isin(target.attacks['orig']).values.astype(int)
        training.features = training.knowledge[training.knowledge['orig'].isin(training.attacks['orig'])]
        training.features = training.knowledge
        training.X = training.features.drop(columns=['orig', 'first_seen', 'last_seen', 'target']).values
        training.Y = training.features['target'].values
        return training, target

    def run(self, for_date=date.today()):
        training, target = self._get_training_target_set(for_date=for_date)
        clf = RandomForestClassifier(n_estimators=30)
        if (target.X.shape[0] > 0) and (training.X.shape[0] > 0):
            clf = clf.fit(training.X, training.Y)
            pred = clf.predict(target.X)
            df = target.features[pred.astype(bool)]
            df = df.rename(columns={'orig': 'ip'})
            df = self.sanitize(df)
            return df[['ip']]
        else:
            df = pd.DataFrame(columns=[['ip']])
            return df
