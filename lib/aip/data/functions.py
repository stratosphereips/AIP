import datetime as dt
import gzip
import hashlib
import pandas as pd
import shutil
import shlex
import subprocess
import zeeklog2pandas as z2p

from dotenv import dotenv_values
from joblib import Parallel
from joblib import delayed
from os import makedirs
from os import path
from os import access
from os import W_OK
from pathlib import Path

_project_dir = Path(__file__).resolve().parents[3]
_config = {
    **dotenv_values(path.join(_project_dir, ".env")),  # load sensitive variables
}


def read_zeek(path, **kwargs):
    """
    Reads a Zeek file to a DataFrame
    """
    try:
        # Load Zeek path to DataFrame
        df = z2p.read_zeek(path, **kwargs)

        # Convert to readable time format
        if 'ts' in df.keys():
            df['ts'] = pd.to_datetime(df.ts, unit='s')

        # Returns data frame
        return df
    except:
        raise z2p.NotAZeekFile(path)


# Currently deprecated, AIP is using now strictly Zeek logs
def read_argus(path, **kwargs):
    from os import path as ospath
    if ospath.exists(path.path + '.csv'):
        df = pd.read_csv(path.path + '.csv')
    else:
        raconf = ospath.join(_project_dir, 'etc', 'ra.conf')
        result = subprocess.run(shlex.split(f'ra -F {raconf} -n -Z b -r {path.path}'), capture_output=True, text=True)
        open(path.path + '.csv', 'w').write(result.stdout)
        df = pd.read_csv(path.path + '.csv')
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df['Dur'] += 0.000000000001
    #subprocess.run(shlex.split(f'rm {path.name}.csv'))
    df.rename(columns={'StartTime':'ts', 'SrcAddr':'id.orig_h', 'DstAddr':'id.resp_h', 'Dur': 'duration', 'SrcBytes': 'orig_ip_bytes', 'SrcPkts': 'orig_pkts'}, inplace=True)
    return df


# This function is unused right now
def scramble(s):
    return hashlib.sha1(_config['salt'].encode() + s.encode()).hexdigest()


def getrawdata(date):
    """
    Retrieves Zeek data from a remote? location and stores it
    on a directory for AIP to process it. The copy is done in
    parallel.
    """

    # Validate date is well formatted
    dt.datetime.strptime(date, '%Y-%m-%d')

    raw_data_dir = path.join(_project_dir,'data','raw', date)

    # Ensure directory exists and is writable
    if access(raw_data_dir, W_OK):
        # Create directory, ignore if it exists
        makedirs(raw_data_dir, exist_ok=True)

        # The next part seems to be prepared to retrieve data from a location
        # and store it in the data/raw/YYYY-MM-DD directory for processing.
        commands = [
            shlex.split(_config['magic'] + f'{date}/conn.{x:02}* ' + raw_data_dir) 
            for x in range(0,24)
        ]

        # Attempting to run the previous commands in parallel
        Parallel(n_jobs=24, backend='threading')(delayed(subprocess.run)(cmd) for cmd in commands)


def removerawdata(date, force=False):
    dt.datetime.strptime(date, '%Y-%m-%d')
    p = path.join(_project_dir,'data','raw', date)
    # Only delete raw data if explicitly allowed in the configuration file
    if (_config['remove_raw_data'].lower() == 'true') or force:
        shutil.rmtree(p)
