""" 
AIP - Base Model

AIP Base Model. All the AIP models are subclases of the base model.

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
import logging
from os import path

from aip.data.access import data_dir
from aip.utils.autoload import models
from aip.utils.autoload import register

# @register
class BaseModel():
    '''
    Template class for AIP models
    '''
    def __init__(self):
        # Set up the logger for the class
        self.logger = logging.getLogger(self.__class__.__name__)

        # Model initialization and configuration
        self.blocklist = pd.DataFrame()
        exclude_ips = path.join(data_dir, 'external', 'do_not_block_these_ips.csv')

        if path.exists(exclude_ips):
            self.donotblocklist = pd.read_csv(exclude_ips)
        else:
            # Warning: File 'do_not_block_these_ips.csv' does not exist. Initializing with empty DataFrame.
            self.logger.warning("File 'do_not_block_these_ips.csv' does not exist. Initializing with empty DataFrame.")
            self.donotblocklist = pd.DataFrame(columns=['ip'])

    def sanitize(self, blocklist=None):
        if blocklist is None:
            blocklist = self.blocklist
        blocklist = blocklist[blocklist.ip.isin(self.donotblocklist.ip) == False]
        self.blocklist = blocklist
        return blocklist
    
    def run(self):
        # Model execution. The result of the function should be a list of IPs to block.
        return self.blocklist
        
