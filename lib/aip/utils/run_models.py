#!/usr/bin/env python
""" 
Tool to generate historical blocklists

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
__version__ = "1.0.0"

import logging
import numpy as np
import pandas as pd
import time

from aip.data.access import data_dir, project_dir
from aip import models
from datetime import date, timedelta
from joblib import Parallel, delayed
from pathlib import Path
from os import makedirs, path, scandir
from aip.utils.metrics import get_metrics, metrics_columns


#project_dir = Path(__file__).resolve().parents[1]

start = '2022-01-03'
#end = str(date.today())
end = '2022-01-31'

n_jobs = 16

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #logging.basicConfig(level=logging.INFO, format=log_fmt)
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

    def run_model(day, model):
        output_dir = path.join(data_dir, 'output', str(model.__name__))
        if not path.exists(output_dir):
            print(f'making dir {output_dir}')
            makedirs(output_dir)
        m = model()
        blocklist = m.run(for_date=day)
        try:
            blocklist = blocklist.rename(columns={'ip':'attacker'})
        except TypeError:
            print(blocklist, day, model)
            raise TypeError
        pd.DataFrame(blocklist, columns=['attacker']).to_csv(path.join(output_dir, f'{model.__name__}_{str(day)}.csv.gz'), index=False, compression='gzip')

    def run_models(day):
        print(day, end='\r')
        for model in models.models:
            if model.__name__ not in excluded_models:
                #print(str(model.__name__))
                run_model(day, model)
    
    def measure(attacks, day, modelname):
        blocklist = pd.read_csv(path.join(data_dir, 'output', f'{modelname}', f'{modelname}_{str(day)}.csv.gz')).rename(columns={'attacker':'ip'})
        results = [f'{modelname}', f'{str(day)}']
        results += get_metrics(attacks, blocklist)
        return results

    def calculate_metrics(day):
        print(day, end='\r')
        attacks = pd.read_csv(path.join(data_dir, 'processed', f'attacks.{str(day)}.csv.gz'), names=['ip', 'flows', 'duration', 'packets', 'bytes'], skiprows=1)
        results = []
        for model in models.models:
            if model.__name__ not in excluded_models:
                results.append(measure(attacks, day, model.__name__))
        #print(results)
        return results


    def make_metric_plots():
        import matplotlib.pyplot as plt
        plt.rcParams["figure.figsize"] = (11,7)
        df = pd.read_csv(path.join(metrics_output_dir, f'model_metrics_results_{start}_{end}.csv.gz'))
        df['date'] = pd.to_datetime(df.date)
        for metric in metrics_columns:
            # one plot per metric including all the models.
            plt.subplots()
            for model in models.models:
                if model.__name__ not in excluded_models:
                    selector = df.model == model.__name__
                    # WHY THE FUCK THE COLUMN TYPE OF THE DF ARE OBJECT?!?!?!
                    plt.plot(df[selector]['date'], df[selector][metric].values.astype(float), label=model.__name__)
            plt.legend()
            plt.xlabel('date')
            plt.ylabel(metric)
            plt.title(metric)
            plt.grid()
            plt.savefig(path.join(metrics_output_dir, f'models_comparison_{metric}_{start}_{end}.png'))
            plt.close()

    dates = [x.date() for x in (pd.date_range(start=start, end=end))]
    st_time = time.time()
    print('Running models')
    #excluded_models = ['New', 'Consistent', 'RandomForest', 'Alpha', 'Pareto', 'AllIPs']
    excluded_models = []
    Parallel(n_jobs=n_jobs, backend='multiprocessing')(delayed(run_models)(day) for day in dates)
    print()
    print(f'Models run after {(time.time() - st_time)/60} minutes.')

    st_time = time.time()
    print('Evaluating models')
    excluded_models = []
    results = Parallel(n_jobs=n_jobs, backend='multiprocessing')(delayed(calculate_metrics)(day) for day in dates)
    print()
    print(f'Metrics taken after {(time.time() - st_time)/60} minutes.')
    results = np.array(results).reshape(-1, 2+len(metrics_columns))
    metrics_output_dir = path.join(data_dir, 'output', 'metrics')
    if not path.exists(metrics_output_dir):
        print(f'making dir {metrics_output_dir}')
        makedirs(metrics_output_dir)
    df = pd.DataFrame(results, columns=['model', 'date'] + metrics_columns)
    df.to_csv(path.join(metrics_output_dir, f'model_metrics_results_{start}_{end}.csv.gz'), index=False, compression='gzip')

    make_plots = True
    excluded_models = []
    if make_plots:
        make_metric_plots()





