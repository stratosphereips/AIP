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

import numpy as np
import pandas as pd


public_IPs = 3706452992

def TPR(P, TP):
    # recall, sensitivity, hit rate
    return TP/P

def TNR(N, TN):
    # specificity, selectivity
    return TN/N

def PPV(TP, FP):
    # precision, 
    return TP / (TP + FP)

def NPV(TN, FN):
    return TN / (TN + FN)

def FNR(P, FN):
    # miss rate
    return FN/P

def FPR(N, FP):
    # fall-out
    return FP/N

def FDR(TP, FP):
    # false discovery rate
    return FP / (FP + TP)

def FOR(TN, FN):
    # false omission rate
    return FN / (FN + TN)

def PLR(P, N, TP, FP):
    # positive likelihood ratio
    return TPR(P, TP)/FPR(N, FP)

def NLR(P, N, TN, FN):
    # negative likelihood ratio
    return FNR(P, FN)/TNR(N, TN)

def PT(P, N, TP, FP):
    # prevalence threshold
    return np.sqrt(FPR(N, FP))/(np.sqrt(TPR(P, TP))/np.sqrt(FPR(N, FP)))

def CSI(TP, FP, FN):
    # threat score, critical success index
    return TP/(TP + FN + FP)

def prevalence(P, N):
    return P / (P + N)

def ACC(P, N, TP, TN):
    # accuracy
    return  (TP + TN) / (P + N)

def BA(P, N, TP, TN):
    # balanced accuracy
    return (TPR(P, TP) + TNR(N, TN))/2

def F05_score(P, TP, FP):
    # the F0.5 score gives less weight to recall than to precision
    return 1.25*((PPV(TP, FP) * TPR(P, TP))/(.25*PPV(TP, FP)+TPR(P, TP)))

def F1_score(TP, FP, FN):
    # the F1 score gives equal weight to recall than to precision
    # equal to 2*((PPV(TP, FP) * TPR(P, TP))/(PPV(TP, FP)+TPR(P, TP)))
    return (2*TP)/((2*TP) + FP + FN)

def F2_score(P, TP, FP):
    # the F2 score gives more weight to recall than to precision
    return 5*((PPV(TP, FP) * TPR(P, TP))/(4*PPV(TP, FP)+TPR(P, TP)))

def FM(P, TP, FP):
    # fowlkes-mallows index
    return np.sqrt(PPV(TP, FP) * TPR(P, TP))

def BM(P, N, TP, TN):
    # bookmarked informedness
    return TPR(P, TP) + TNR(N, TN) - 1

def MK(TP, TN, FP, FN):
    # markdedness or Δp
    return PPV(TP, FP) + NPV(TN, FN) - 1

def DOR(P, N, TP, TN, FP, FN):
    # diagnostics odds ratio
    try:
        return PLR(P, N, TP, FP) / NLR(P, N, TN, FN)
    except ZeroDivisionError:
        return -1

def calculate_TPTNFPFN(attacklist, blocklist):
    TP = 0.
    TN = 0.
    FP = 0.
    FN = 0.
    attacklist = {k:0 for k in attacklist.ip.values}
    blocklist = {k:0 for k in blocklist.ip.values}
    for ip in blocklist:
        if ip in attacklist:
            TP += 1
    for ip in blocklist:
        if ip not in attacklist:
            FP += 1
    for ip in attacklist:
        if ip not in blocklist:
            FN += 1
    TN = float(public_IPs - len(attacklist) - FN - FP)
    return TP, TN, FP, FN

def MCC(TP, TN, FP, FN):
    """
    Calculates the Mathew's Correlation Coeficient
    """
    if (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) == 0:
        return 0
    else:
        return ((TP*TN)-(FP*FN))/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

def calculate_nDCG(attacklist, blocklist):
    # Normalized Discounted Cumulative Gain
    attacklist = attacklist.sort_values(by='rank', ascending=False)
    df = pd.merge(attacklist, blocklist)
    df = df.sort_values(by='rank', ascending=False)
    DCGp = ((2**df['rank'])/np.log2(np.arange(1, len(df)+1)+1)).sum()
    IDCG = ((2**attacklist['rank'])/np.log2(np.arange(1, len(attacklist)+1)+1)).sum()
    try:
        return DCGp/IDCG
    except ZeroDivisionError:
        return 0

def calculate_nCG(attacklist, blocklist):
    # normalized cumulative gain
    attacklist = attacklist.sort_values(by='rank', ascending=False)
    df = pd.merge(attacklist, blocklist)
    df = df.sort_values(by='rank', ascending=False)
    CG = df['rank'].sum()
    return CG

#from sklearn.metrics import average_precision_score
#def calculate_AUCPR(attacklist, blocklist):
#    y_true = blocklist.ip.isin(attacklist.ip).values
#    y_pred = 

def calculate_BG_score(attacklist, blocklist, FP1_percent=0.0):
    FP1_impact = 10**6
    FP2_impact = 10
    TP, TN, FP, FN= calculate_TPTNFPFN(attacklist, blocklist)
    fpw = 1/(public_IPs - len(attacklist))
    CG = calculate_nCG(attacklist, blocklist)
    FP1 = int((FP*FP1_percent)/100)
    DG = ((FP - FP1) * fpw * FP2_impact) + (FP1 * fpw * FP1_impact)
    return CG - DG

#def calculate_BG_score(attacklist, blocklist, FP1_percent=0.0):
#    #FP1_impact = 1#0**6
#    #FP2_impact = 1#0
#    TP, TN, FP, FN = calculate_TPTNFPFN(attacklist, blocklist)
#    #fp1w = 1/whitelisted_ips
#    #fp2w = 1/(n_pub_ips - whitelisted_ips - len(attacks))
#    #fpw = 1/(n_pub_ips - len(attacks))
#    fprank = list(attacklist['rank'].values)
#    fprank.sort()
#    CG = calculate_nCG(attacklist, blocklist)
#    DG = np.sum(fprank[:int(min(len(fprank), FP))] + [fprank[-1]]*int(max(0, FP - len(fprank))))
#    return CG - DG

def calculate_coverage(attacklist, blocklist):
    df = pd.merge(attacklist, blocklist)
    flows = df.flows.sum()/max(1, attacklist.flows.sum())
    duration = df.duration.sum()/max(1, attacklist.duration.sum())
    nbytes = df.bytes.sum()/max(1, attacklist.bytes.sum())
    packets = df.packets.sum()/max(1, attacklist.packets.sum())
    flows_ip = (df.flows/max(1, attacklist.flows.sum())).sum()/max(1, len(blocklist))
    duration_ip = (df.duration/max(1, attacklist.duration.sum())).sum()/max(1, len(blocklist))
    nbytes_ip = (df.bytes/max(1, attacklist.bytes.sum())).sum()/max(1, len(blocklist))
    packets_ip = (df.packets/max(1, attacklist.packets.sum())).sum()/max(1, len(blocklist))
    return flows*100, duration*100, nbytes*100, packets*100, flows_ip*100, duration_ip*100, nbytes_ip*100, packets_ip*100

def get_rank(attacks):
    return (attacks.flows/attacks.flows.sum() + attacks.duration/attacks.duration.sum() + attacks.packets/attacks.packets.sum() + attacks['bytes']/attacks['bytes'].sum())/4

metrics_columns = ['BL_len', 'P', 'N', 'TP', 'TN', 'FP', 'FN', 
       'coverage_flows', 'coverage_duration', 'coverage_packets', 'coverage_bytes',
       'coverage_flows_ip', 'coverage_duration_ip', 'coverage_packets_ip', 'coverage_bytes_ip',
       'true_positive_rate', 'true_negative_rate', 'positive_predictive_value','negative_predictive_value',
       'false_negative_rate', 'false_positive_rate', 'false_discovery_rate', 'false_ommision_rate',
       'positive_likelihood_ratio', 'negative_likelihood_ratio', 'critical_success_index',
       'prevalence_threshold', 'prevalence', 'accuracy', 'balanced_accuracy',
       'F0.5_score', 'F1_score', 'F2_score', 'fowlkes_mallows_index',
       'bookmarked_informedness', 'markedness', 'matthews_correlation_coefficient','diagnostic_odds_ratio',
       'normalized_cumulative_gain', 'normalized_discounted_cumulative_gain', 'bg_score']

def get_metrics(attacks, blocklist):
    if len(attacks) == 0:
        return [np.nan]*len(metrics_columns)
    if len(blocklist) == 0:
        return [np.nan]*len(metrics_columns)
    attacks['rank'] = get_rank(attacks)
    bl_len = len(blocklist)
    # contingency table
    P = len(attacks)
    N = public_IPs - P
    TP, TN, FP, FN = calculate_TPTNFPFN(attacks, blocklist)
    # coverage
    c_flows, c_duration, c_packets, c_bytes, c_flows_ip, c_duration_ip, c_packets_ip, c_bytes_ip = calculate_coverage(attacks, blocklist)
    ## contingency table based metrics
    # recall or true positive rate
    tpr = TPR(P, TP)
    # specificity, selectivity or true negative rate
    tnr = TNR(N, TN)
    # precision or positive predictive value
    precision = PPV(TP, FP)
    # negative predictive value
    npv = NPV(TN, FN)
    # miss rate or false negative rate
    fnr = FNR(P, FN)
    # fall out or false positive rate
    fpr = FPR(N, FP)
    # false discovery rate
    fdr = FDR(TP, FP)
    # false omission rate
    _for = FOR(TN, FN)
    # positive likelihood ratio
    plr = PLR(P, N, TP, FP)
    # negative likelihood ratio
    nlr = NLR(P, N, TN, FN)
    #critical_success_index
    csi = CSI(TP, FP, FN)
    # prevalence threshold
    pt = PT(P, N, TP, FP)
    # Prevalence
    pv = prevalence(P, N)
    # Accuracy
    acc = ACC(P, N, TP, TN)
    # Balanced accuracy
    ba = BA(P, N, TP, TN)
    # F0.5 score
    f05 = F05_score(P, TP, FP)
    # F1 score
    f1 = F1_score(TP, FP, FN)
    # F2 score
    f2 = F2_score(P, TP, FP)
    # fowlkes-mallows index
    fm = FM(P, TP, FP)
    # bookmarked informedness
    bm = BM(P, N, TP, TN)
    # markedness or Δp
    mk = MK(TP, TN, FP, FN)
    # diagnostics odds ratio
    dor = DOR(P, N, TP, TN, FP, FN)
    # matthews correlation coefficient
    mcc = MCC(TP, TN, FP, FN)
    # normalized cumulative gain
    ncg = calculate_nCG(attacks, blocklist)
    # normalized discounted cumulative gain (best case scenario)
    ndcg = calculate_nDCG(attacks, blocklist)
    # Bogado - Garcia score
    bg_score = calculate_BG_score(attacks, blocklist)
    
    return bl_len, P, N, TP, TN, FP, FN, c_flows, c_duration, c_packets, c_bytes, c_flows_ip, c_duration_ip, c_packets_ip, c_bytes_ip, tpr, tnr, precision, npv, fnr, fpr, fdr, _for, plr, nlr, csi, pt, pv, acc, ba, f05, f1, f2, fm, bm, mk, mcc, dor, ncg, ndcg, bg_score

