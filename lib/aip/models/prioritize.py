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
import time

from aip.data.access import data_path, get_attacks
from aip.models.base import BaseModel
from aip.utils.autoload import register, models
from datetime import date, datetime, timedelta
from os import path
from sklearn.ensemble import RandomForestClassifier

def _add_knowledge(last_knowledge, day):
    print(f'DEBUG: PROCESSING DATE {day}')
    st_time = time.time()
    day = datetime.strptime(day, '%Y-%m-%d').date()
    p = path.join(data_path, 'processed', 'prioritizers')
    attacks = get_attacks(dates=[day])
    df = attacks[0]
    if df.empty is True:
        return last_knowledge
    df = df.rename(columns={"count": "flows"})
    df.loc[:, 'first_seen'] = day
    df.loc[:, 'last_seen'] = day
    df.loc[:, 'days_active'] = 1
    df.loc[df['flows'] == 0, 'flows'] = 1
    last_knowledge = pd.concat([last_knowledge, df])
    dates_min = last_knowledge.groupby('orig').first_seen.min()
    dates_max = last_knowledge.groupby('orig').last_seen.max()
    knowledge = last_knowledge.groupby('orig').sum()
    knowledge.loc[:,'first_seen'] = dates_min
    knowledge.loc[:,'last_seen'] = dates_max
    knowledge.loc[:,'mean_flows'] = knowledge['flows']/knowledge['days_active']
    knowledge.loc[:,'mean_duration'] = knowledge['duration']/knowledge['flows']
    knowledge.loc[:,'mean_bytes'] = knowledge['bytes']/knowledge['flows']
    knowledge.loc[:,'mean_packets'] = knowledge['packets']/knowledge['flows']  
    knowledge.reset_index(inplace=True)
    knowledge.to_csv(path.join(p, f'knowledgebase-{day}-snapshot.gz'),
            columns=['orig', 'flows', 'duration','bytes', 'packets',
                'mean_flows', 'mean_duration', 'mean_bytes', 'mean_packets',
                'days_active', 'first_seen', 'last_seen'],
            index=False, compression='gzip')
    print(f'DEBUG: PROCESSED IN {(time.time() - st_time)/60} MINUTES.')
    return knowledge

def _build_knowledge(start, end):
    dates = pd.date_range(start=start, end=end)
    last_knowledge = pd.DataFrame()
    for day in dates:
        last_knowledge = _add_knowledge(last_knowledge, str(day.date()))
    return last_knowledge


class Knowledgebase():
    '''
    Object that represents the IP features database
    '''
    
    def _check_date_param(self, day_unchk):
        if day_unchk == 'yesterday':
            day = str(date.today() - timedelta(days=1))
        elif type(day_unchk) is str:
            # force is a date or throw and exception
            day = str(datetime.strptime(day_unchk, '%Y-%m-%d').date())
        elif type(day_unchk) is date:
            day = str(day_unchk)
        return day

    def _load_knowledge_until(self, day):
        day = self._check_date_param(day)
        self.path = path.join(data_path,
                'processed', 'prioritizers', f'knowledgebase-{day}-snapshot.gz')
        if not path.exists(self.path):
            self.build(end=datetime.strptime(day, '%Y-%m-%d').date())
        self.knowledge = pd.read_csv(self.path)
        self.knowledge.loc[:, 'last_seen'] = pd.to_datetime(self.knowledge.last_seen)
        self.knowledge.loc[:, 'first_seen'] = pd.to_datetime(self.knowledge.first_seen)
        self.timeframe = (self.knowledge.last_seen.min(), self.knowledge.last_seen.max())
    
    def __init__(self, load_until='yesterday'):
        day = self._check_date_param(load_until)
        self.path = path.join(data_path,
                'processed', 'prioritizers', f'knowledgebase-{day}-snapshot.gz')
        self._load_knowledge_until(day)
    

    def build(self, start=date(2020, 7, 4), end=date.today() - timedelta(days=1), force=False):
        if path.exists(self.path) and not force:
            print('Knowledge exists already. Use force=True to rebuild it')
            return
        # check if the snapshot for the start date exists
        # if not, all the snapshots must be created again
        p = path.join(data_path, 'processed', 'prioritizers')
        if not path.exists(path.join(p, f'knowledgebase-{str(start)}-snapshot.gz')):
            last_knowledge = _build_knowledge(start=start, end=end)
        else:
            days_ago = 1
            day = str(end - timedelta(days=days_ago))
            while not path.exists(path.join(p, f'knowledgebase-{day}-snapshot.gz')):
                days_ago += 1
                day = str(end - timedelta(days=days_ago))
            last_knowledge = pd.read_csv(path.join(p, f'knowledgebase-{day}-snapshot.gz'))
            last_knowledge.loc[:, 'first_seen'] = pd.to_datetime(last_knowledge.first_seen).dt.date
            last_knowledge.loc[:, 'last_seen'] = pd.to_datetime(last_knowledge.last_seen).dt.date
            while days_ago >= 1:
                days_ago -= 1
                day = str(end - timedelta(days=days_ago))
                last_knowledge = _add_knowledge(last_knowledge, day)

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

@register
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
            return df['ip']
        else:
            df = pd.DataFrame(columns=['ip'])
            return df
