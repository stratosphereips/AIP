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
import pandas as pd
import time

from aip.data.access import data_path, project_dir
from aip.models.alpha import Alpha
from lib.aip.models.prioritize_new import New
from lib.aip.models.prioritize_consistent import Consistent
from lib.aip.models.random_forest import RandomForest
from aip.models.pareto import Pareto
from datetime import date, timedelta
from joblib import Parallel, delayed
from pathlib import Path
from os import makedirs, path, scandir


#project_dir = Path(__file__).resolve().parents[1]

start = '2020-07-05'
end = str(date.today())

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #logging.basicConfig(level=logging.INFO, format=log_fmt)
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)

    # not used in this stub but often useful for finding various files
    
    # load up the .env entries as environment variables
    #load_dotenv(find_dotenv())
    
    def run_model_alpha(day):
        #Alpha Model
        output_dir = path.join(project_dir, 'data', 'output', 'alpha_model')
        if not path.exists(output_dir):
            makedirs(output_dir)
        alpha = Alpha()
        blocklist = alpha.run(for_date=day)
        blocklist = blocklist.rename(columns={'ip':'attacker'})
        pd.DataFrame(blocklist, columns=['attacker']).to_csv(path.join(output_dir, f'alpha_{str(day)}.csv.gz'), index=False, compression='gzip')
        
    def run_model_alpha7(day):
        #Alpha 7 Model
        output_dir = path.join(project_dir, 'data', 'output', 'alpha7_model')
        if not path.exists(output_dir):
            makedirs(output_dir)
        alpha = Alpha(7)
        blocklist = alpha.run(for_date=day)
        blocklist = blocklist.rename(columns={'ip':'attacker'})
        pd.DataFrame(blocklist, columns=['attacker']).to_csv(path.join(output_dir, f'alpha7_{str(day)}.csv.gz'), index=False, compression='gzip')

    def run_model_pn(day):
        # Prioritize New Model
        output_dir = path.join(data_path, 'output', 'prioritize_new')
        if not path.exists(output_dir):
            makedirs(output_dir)
        pn = New()
        blocklist = pn.run(for_date=day)
        blocklist.to_csv(path.join(output_dir, f'prioritize-new_{str(day)}.csv.gz'), index=False, compression='gzip')
    
    def run_model_pc(day):
        # Prioritize Consistent Model
        output_dir = path.join(data_path, 'output', 'prioritize_consistent')
        if not path.exists(output_dir):
            makedirs(output_dir)
        pc = Consistent()
        blocklist = pc.run(for_date=day)
        blocklist.to_csv(path.join(output_dir, f'prioritize-consistent_{str(day)}.csv.gz'), index=False, compression='gzip')
    
    def run_model_rf(day):
        # RandomForest Model
        output_dir = path.join(data_path, 'output', 'random_forest')
        if not path.exists(output_dir):
            makedirs(output_dir)
        rf = RandomForest()
        blocklist = rf.run(for_date=day)
        blocklist.to_csv(path.join(output_dir, f'rf_v1_30estimators_{str(day)}.csv.gz'), index=False, compression='gzip')
    
    def run_model_pareto(day):
        #Pareto Model
        output_dir = path.join(project_dir, 'data', 'output', 'pareto_model')
        if not path.exists(output_dir):
            makedirs(output_dir)
        pareto = Pareto()
        blocklist = pareto.run(for_date=day)
        blocklist = blocklist.rename(columns={'ip':'attacker'})
        pd.DataFrame(blocklist, columns=['attacker']).to_csv(path.join(output_dir, f'pareto_{str(day)}.csv.gz'), index=False, compression='gzip')
    
    def run_models(day):
        print(day)
        #run_model_alpha(day)
        #run_model_pn(day)
        #run_model_pc(day)
        #run_model_rf(day)
        run_model_pareto(day)

    dates = [x.date() for x in (pd.date_range(start=start, end=end))]
    st_time = time.time()
    #print(f'Creating knowledgebase from {str(dates[0])} to the present')
    #k = Knowledgebase()
    # Need to build the knowledge outside the parallel loop
    # build() is not a reentrant function
    #k.build(start=dates[0], end=dates[-1])
    #print(f'Knowledge created in {(time.time() - st_time)/60} minutes.')
#    for day in dates:
#       run_models(day)
    st_time = time.time()
    print('Running models')
    Parallel(n_jobs=16, backend='multiprocessing')(delayed(run_models)(day) for day in dates)
    print(f'Models run after {(time.time() - st_time)/60} minutes.')
