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

from aip.data.access import data_path, get_attacks
from aip.models.base import BaseModel
from aip.utils.autoload import register, models
from aip.utils.knowledge_base import Knowledgebase
from datetime import date, timedelta
from os import path
from sklearn.ensemble import RandomForestClassifier


@register
class Consistent(BaseModel):
    '''
    Prioritize Consistent algorithm
    '''

    def __init__(self):
        super().__init__()
        # Weights from Thomas' Thesis
        # nflows, conns, nbytes, npackets,
        # mean_flows, mean_conns, mean_bytes, mean_packets
        self.weights = [0.05, 0.05, 0.05, 0.05, 0.2, 0.2, 0.2, 0.2]
        self.score_threshold = 0.00002
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
        days_since_last_seen = np.array([x.days for x in (pd.to_datetime(date.today()) - self.db.knowledge.last_seen)])
        total_attack_time = np.array([x.days for x in (self.db.knowledge.last_seen - self.db.knowledge.first_seen)])
        aging = 1 - (days_since_last_seen/(days_since_last_seen + total_attack_time))
        ipscores *= aging
        return ipscores

    def run(self, for_date=date.today()):
        self.db = Knowledgebase(load_until=for_date - timedelta(days=1))
        ipscores = self._get_IP_scores()
        df = pd.DataFrame()
        df['ip'] = self.db.knowledge['orig'].values
        df['score'] = ipscores
        df = df.sort_values(by='score', ascending=False)
        df = self.sanitize(df)
        if len(df[df.score > self.score_threshold]) < self.min_ip_number:
            df = df.iloc[:self.min_ip_number]
        else:
            df = df[df.score > self.score_threshold]
        return df


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
