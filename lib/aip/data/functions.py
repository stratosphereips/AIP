import datetime as dt
import gzip
import hashlib
import pandas as pd
import shutil
import subprocess, shlex
import zeeklog2pandas as z2p

from dotenv import dotenv_values
from joblib import Parallel, delayed
from os import makedirs, path
from pathlib import Path

_project_dir = Path(__file__).resolve().parents[3]
_config = {
    **dotenv_values(path.join(_project_dir, ".env")),  # load sensitive variables
}

def read_zeek(path, **kwargs):
    try:
        df = z2p.read_zeek(path, **kwargs)
        if 'ts' in df.keys():
            df['ts'] = pd.to_datetime(df.ts, unit='s')
        return df
    except:
        raise z2p.NotAZeekFile(path)

def scramble(s):
    return hashlib.sha1(_config['salt'].encode() + s.encode()).hexdigest()

def getrawdata(date):
    dt.datetime.strptime(date, '%Y-%m-%d')
    p = path.join(_project_dir,'data','raw', date)
    makedirs(p, exist_ok=True)
    commands = [shlex.split(_config['magic'] + f'{date}/conn.{x:02}* ' + p) for x in range(0,24)]
    Parallel(n_jobs=24, backend='threading')(delayed(subprocess.run)(c) for c in commands)

def removerawdata(date, force=False):
    dt.datetime.strptime(date, '%Y-%m-%d')
    p = path.join(_project_dir,'data','raw', date)
    # Only delete raw data if explicitly allowed in the configuration file
    if (_config['remove_raw_data'].lower() == 'true') or force:
        shutil.rmtree(p)

