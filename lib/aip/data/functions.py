import datetime as dt
import gzip
import hashlib
import pandas as pd
import shutil
import subprocess, shlex
import zeeklog2pandas as z2p

from dotenv import dotenv_values
from joblib import Parallel, delayed
from os import makedirs, path, access, W_OK
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

def scramble(s):
    return hashlib.sha1(_config['salt'].encode() + s.encode()).hexdigest()

def getrawdata(date):
    dt.datetime.strptime(date, '%Y-%m-%d')
    p = path.join(_project_dir,'data','raw', date)
    if access(p, W_OK):
        makedirs(p, exist_ok=True)
        commands = [shlex.split(_config['magic'] + f'{date}/conn.{x:02}* ' + p) for x in range(0,24)]
        Parallel(n_jobs=24, backend='threading')(delayed(subprocess.run)(c) for c in commands)

def removerawdata(date, force=False):
    dt.datetime.strptime(date, '%Y-%m-%d')
    p = path.join(_project_dir,'data','raw', date)
    # Only delete raw data if explicitly allowed in the configuration file
    if (_config['remove_raw_data'].lower() == 'true') or force:
        shutil.rmtree(p)

