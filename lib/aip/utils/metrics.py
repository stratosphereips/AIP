""" 
AIP - Metrics

This module implements several metrics to measure the efficiency of the
blocklists. 

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


def _MCC(TP, TN, FP, FN):
    """
    Calculates the Mathew's Correlation Coeficient
    """
    if (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) == 0:
        return 0
    else:
        return ((TP*TN)-(FP*FN))/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

def _calculate_TPTNFPFN(attacklist, blocklist):
    TP = 0.
    TN = 0.
    FP = 0.
    FN = 0.
    attacklist = {k:0 for k in attacklist}
    blocklist = {k:0 for k in blocklist}
    for ip in blocklist:
        if ip in attacklist:
            TP += 1
        if ip not in attacklist:
            FP += 1
    for ip in attacklist:
        if ip not in blocklist:
            FN += 1
    TN = 2**32 - FP
    return TP, TN, FP, FN

def MCC(attacklist, blocklist):
    TP, TN, FP, FN = _calculate_TPTNFPFN(attacklist, blocklist)
    return _MCC(TP, TN, FP, FN)
