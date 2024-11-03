"""
This module provides functionality for managing the
knowledge base used by AIP models.
"""

import logging
import time
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
from os import path
from aip.data.access import data_path
from aip.data.access import get_attacks


def _add_knowledge(last_knowledge, day, log_level=logging.ERROR):
    # Configure logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=log_level)

    logger.debug(f'_add_knowledge - Processing date {day}')
    st_time = time.time()
    day = datetime.strptime(day, '%Y-%m-%d').date()

    p = path.join(data_path, 'processed', 'prioritizers')

    attacks = get_attacks(dates=[day])

    df = attacks[0]
    if df.empty is True:
        last_knowledge.to_csv(path.join(p, f'knowledgebase-{day}-snapshot.gz'),
            columns=['orig', 'flows', 'duration','bytes', 'packets',
                'mean_flows', 'mean_duration', 'mean_bytes', 'mean_packets',
                'days_active', 'first_seen', 'last_seen'],
            index=False, compression='gzip')
        return last_knowledge
    df = df.rename(columns={"count": "flows"})
    df.loc[:, 'first_seen'] = day
    df.loc[:, 'last_seen'] = day
    df.loc[:, 'days_active'] = 1
    df.loc[df['flows'] == 0, 'flows'] = 1

    last_knowledge = pd.concat([last_knowledge, df])
    dates_min = last_knowledge.groupby('orig').first_seen.min()
    dates_max = last_knowledge.groupby('orig').last_seen.max()
    knowledge = last_knowledge.groupby('orig').sum(numeric_only=True)
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

    logger.debug(f'_add_knowledge - Processed in {(time.time() - st_time)/60} minutes')
    return knowledge


def _build_knowledge(start, end, log_level=logging.ERROR):
    # Configure logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=log_level)

    dates = pd.date_range(start=start, end=end)
    last_knowledge = pd.DataFrame()
    for day in dates:
        logger.debug(f'_build_knowledge - Building knowledge base for {day}')
        last_knowledge = _add_knowledge(last_knowledge, str(day.date()), log_level=log_level)
    return last_knowledge


def _rebuild(start_date, log_level=logging.ERROR):
    """
    Wrapper to rebuild the knowledge base from the specified start date to today.
    """
    # Configure logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=log_level)

    st_time = time.time()
    current_date = date.today()
    logger.info(f"_rebuild - Rebuilding knowledge base from {start_date} to {current_date}")

    _build_knowledge(start=start_date, end=current_date, log_level=log_level)

    logger.info(f'_rebuild - Rebuilding knowledge base finished in {(time.time() - st_time)/60} minutes')


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
        # Set up the logger for the class
        self.logger = logging.getLogger(self.__class__.__name__)

        day = self._check_date_param(load_until)

        self.path = path.join(data_path, 'processed', 'prioritizers', f'knowledgebase-{day}-snapshot.gz')
        self._load_knowledge_until(day)
    

    def build(self, start=date.today() - timedelta(days=2), end=date.today() - timedelta(days=1), force=False):
        if path.exists(self.path) and not force:
            self.logger.error('The knowledge already exists. Use force=True to force its rebuild')
            return

        # check if the snapshot for the start date exists
        # if not, all the snapshots must be created again
        p = path.join(data_path, 'processed', 'prioritizers')

        if not path.exists(path.join(p, f'knowledgebase-{str(start)}-snapshot.gz')):
            last_knowledge = _build_knowledge(start=start, end=end)
        else:
            days_ago = 1
            try:
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
            except OverflowError as err:
                raise Exception(f"There is not Knowledge Base for the model to run (Required: {end})")
