""" 
AIP - Database module for Prioritize New and Prioritize Consistent

This module implements the Database Abstraction from Thomas O'Hara thesis

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

from aip.data.access import data_path, get_attacks
from aip.models.base import BaseModel
from datetime import date, timedelta
from os import path



class Knowledgebase():
    '''
    Object that represents the IP features database
    '''
    
    def __init__(self):
        self.path = path.join(data_path, 'processed', 'prioritizers', 'prioritizer_knowledgebase')
        try:
            self.knowledge = pd.read_csv(self.path)
            self.knowledge.loc[:, 'last_seen'] = pd.to_datetime(self.knowledge.last_seen)
            self.knowledge.loc[:, 'first_seen'] = pd.to_datetime(self.knowledge.first_seen)
            self.timeframe = (self.knowledge.last_seen.min(), self.knowledge.last_seen.max())
        except FileNotFoundError:
            print('No knowledgebase found, use build() to create it')
            pass

    def build(self, start=date(2022, 1, 1), end=date.today() - timedelta(days=1), force=False):
        if path.exists(self.path) and not force:
            print('Knowledge exists already. Use force=True to rebuild it')
            return
        dates = pd.date_range(str(start), str(end))
        attacks = get_attacks(start, end)
        aggregated = pd.DataFrame()
        for day, df in zip(dates, attacks):
            df.loc[:, 'date'] = day
            df.loc[:, 'days_active'] = 1
            aggregated = pd.concat([aggregated, df])
        dates_min = aggregated.groupby('orig').date.min()
        dates_max = aggregated.groupby('orig').date.max()
        knowledge = aggregated.groupby('orig').sum()
        knowledge.loc[:,'first_seen'] = dates_min
        knowledge.loc[:,'last_seen'] = dates_max
        knowledge.loc[:,'flows'] = knowledge['count']
        knowledge.loc[knowledge['flows'] == 0, 'flows'] = 1
        knowledge.loc[:,'mean_flows'] = knowledge['flows']/knowledge['days_active']
        knowledge.loc[:,'mean_duration'] = knowledge['duration']/knowledge['flows']
        knowledge.loc[:,'mean_bytes'] = knowledge['bytes']/knowledge['flows']
        knowledge.loc[:,'mean_packets'] = knowledge['packets']/knowledge['flows']  
        knowledge.reset_index(inplace=True)
        self.knowledge = knowledge
        #knowledgebase.to_csv(self.path, index=False)
        knowledge.to_csv(self.path,
                columns=['orig', 'flows', 'duration','bytes', 'packets',
                    'mean_flows', 'mean_duration', 'mean_bytes', 'mean_packets',
                    'days_active', 'first_seen', 'last_seen'],
                index=False)
        return

    def _add_knowledge(self, date):
        attacks = get_attacks(dates=[date])[0]
        # check knowledge dates integrity
        if (date > self.knowledge.date.min()) and (date < self.knowledge.date.max()):
            print('Can\'t add information for that date. Rebuild the knowledgebase including the new date.')
            return
        attacks.loc[:, 'date'] = date
        attacks.loc[:, 'days_active'] = 1
        # THIS WILL BE SLOWER AND SLOWER OVERTIME
        # Maybe is better to go IP by IP on the attacks updating the knowledgebase.
        # Please fix
        aggregated = pd.concat([self.knowledge, attacks])
        dates_min = aggregated.groupby('orig').date.min()
        dates_max = aggregated.groupby('orig').date.max()
        knowledge = aggregated.groupby('orig').sum()
        knowledge.loc[:,'first_seen'] = dates_min
        knowledge.loc[:,'last_seen'] = dates_max
        knowledge.loc[:,'flows'] = knowledge['count']
        knowledge.loc[knowledge['flows'] == 0, 'flows'] = 1
        knowledge.loc[:,'mean_flows'] = knowledge['flows']/knowledge['days_active']
        knowledge.loc[:,'mean_duration'] = knowledge['duration']/knowledge['flows']
        knowledge.loc[:,'mean_bytes'] = knowledge['bytes']/knowledge['flows']
        knowledge.loc[:,'mean_packets'] = knowledge['packets']/knowledge['flows']
        knowledge.reset_index(inplace=True)
        self.knowledge = knowledge
        knowledge.to_csv(self.path,
                columns=['orig', 'flows', 'duration','bytes', 'packets',
                    'mean_flows', 'mean_duration', 'mean_bytes', 'mean_packets',
                    'days_active', 'last_seen'],
                index=True)
        return
    
    def update(self):
        # FIXME: Need to code the update function so models don't worry about knowledge updates
        # Knowledge should be always updated upon Knowledge instantiation?
        pass
