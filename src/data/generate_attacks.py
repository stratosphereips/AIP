import click
import datetime as dt
import logging
import pandas as pd
import numpy as np

from pathlib import Path
from os import scandir, path
from joblib import Parallel, delayed
from functions import scramble

def _make_dataset(date):
    '''
    Create a dataset for the date string date in the data/interim folder
    THIS FUNCTION IS DESTRUCTIVE and will overwrite the datasets for the processed date if exists.
    '''
    logger = logging.getLogger(__name__)
    try:
        daily = pd.read_csv(path.join(project_dir,"data","interim", f'daily.conn.{date}.csv'))
        daily['ts'] = pd.to_datetime(daily['ts'])
        daily['duration'] = daily.duration.replace('-',0).astype(float)
    except FileNotFoundError:
        logger.warning(f'Skipping {path.join(project_dir,"data","interim", f"daily.conn.{date}.csv")}. File not exist.')
        return

    # Calculate the total attacks for each origin
    df = daily[['id.orig_h', 'duration', 'orig_pkts', 'orig_ip_bytes']].groupby(['id.orig_h']).sum()
    df.rename(columns={'duration':'duration', 'orig_pkts':'packets', 'orig_ip_bytes':'bytes'}, inplace=True)
    df['orig'] = df.index.values
    df['flows'] = daily.groupby(['id.orig_h']).count().ts.values
    df.reset_index(drop=True, inplace=True)
    logger.debug('Writting file: ' + path.join(project_dir,'data','processed', f'attacks.{date}.csv'))
    df.to_csv(path.join(project_dir,'data','processed', f'attacks.{date}.csv'), columns=['orig', 'flows', 'duration', 'packets', 'bytes'], index=False)

@click.command()
@click.argument('dates' , type=click.DateTime(formats=['%Y-%m-%d']), nargs=-1)
def main(dates):
    """ 
    Creates the dataset or part of it
    """
    logger = logging.getLogger(__name__)
    logger.debug(f'Making  dataset from raw data for dates {dates}')
    if dates:
        dates = [x.strftime('%Y-%m-%d') for x in dates]
    else:
        dates = []
        for x in scandir(path.join(project_dir, 'data', 'raw')):
            try:
                dt.datetime.strptime(x.name, '%Y-%m-%d')
                dates.append(x.name)
            except ValueError:
                pass
    Parallel(n_jobs=12, backend='multiprocessing')(delayed(_make_dataset)(date) for date in dates)
    ##for date in dates:
    #    _make_dataset(date)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #logging.basicConfig(level=logging.INFO, format=log_fmt)
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    #load_dotenv(find_dotenv())

    main()
