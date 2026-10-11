"""Post-hoc LODO analyses from saved target probabilities (lodo_probs of parts C1 and C1b).

Usage: python lodo_posthoc.py <probs_dir> [<probs_dir> ...]   -> writes lodo_orientation.csv next to this script

Orientation-aware calibration: the score direction (p or 1-p) and threshold are both chosen
on the calibration slice only; F1 is reported on the evaluation slice. Same split as the notebook.
"""
import glob, json, os, sys
import numpy as np, pandas as pd

def cal_eval_split(n, cal_frac=0.20, purge=1):
    n_cal = max(10, int(cal_frac * n))
    return np.arange(0, n_cal), np.arange(min(n_cal + purge, n), n)

def f1(y, yp):
    tp = ((yp == 1) & (y == 1)).sum(); fp = ((yp == 1) & (y == 0)).sum(); fn = ((yp == 0) & (y == 1)).sum()
    return 2 * tp / max(2 * tp + fp + fn, 1)

def macro_f1(y, yp):
    return 0.5 * (f1(y, yp) + f1(1 - y, 1 - yp))

def best_thr(p, y, n=200):
    cand = np.unique(np.percentile(p, np.linspace(0, 100, n))); bf, bt = 0.0, 0.5
    for t in cand:
        v = f1(y, (p >= t).astype(int))
        if v > bf: bf, bt = v, t
    return bf, bt

def auc(p, y):
    order = np.argsort(p); r = np.empty(len(p)); r[order] = np.arange(1, len(p) + 1)
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / max(n1 * n0, 1)

rows = []
for f in sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, '*.npz'))):
    model, fold, seed = os.path.basename(f)[:-4].rsplit('_', 2)
    z = np.load(f); p = z['p_ad'].astype(np.float64); y = z['y'].astype(int)
    ci, ei = cal_eval_split(len(y))
    a_cal = auc(p[ci], y[ci]); flip = a_cal < 0.5
    q = 1 - p if flip else p
    _, t = best_thr(q[ci], y[ci]); _, t0 = best_thr(p[ci], y[ci])
    rows.append({'model': model, 'fold': fold, 'seed': int(seed), 'auc_cal': a_cal, 'auc_eval': auc(p[ei], y[ei]),
                 'flipped': bool(flip), 'f1_cal_thr': f1(y[ei], (p[ei] >= t0).astype(int)),
                 'f1_oriented': f1(y[ei], (q[ei] >= t).astype(int)),
                 'macro_f1_cal_thr': macro_f1(y[ei], (p[ei] >= t0).astype(int)),
                 'macro_f1_oriented': macro_f1(y[ei], (q[ei] >= t).astype(int)),
                 'trivial_f1': 2 * y[ei].mean() / (1 + y[ei].mean())})
d = pd.DataFrame(rows)
d.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lodo_orientation.csv'), index=False)
pd.set_option('display.width', 200)
print(d.groupby('model')[['auc_eval', 'f1_cal_thr', 'f1_oriented', 'macro_f1_cal_thr', 'macro_f1_oriented', 'trivial_f1']].mean().round(4).to_string())
print(d.pivot_table(index='model', columns='fold', values='f1_oriented', aggfunc='mean').round(4).to_string())
print(d.pivot_table(index='model', columns='fold', values='flipped', aggfunc='mean').round(2).to_string())
