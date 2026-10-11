"""Generate manuscript/rev2_numbers.tex (scalar macros + table-row macros) from the
revision-2 Kaggle results. Re-run whenever a result file changes.

Usage: python -I make_numbers.py <results_dir> <out.tex> [<c1b_results_dir>]
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

R, OUT = sys.argv[1], sys.argv[2]
C1B = sys.argv[3] if len(sys.argv) > 3 else None
A = json.load(open(f'{R}/A/tch_net_v2_results/partA_results.json'))
B = json.load(open(f'{R}/B/tch_net_v2_results/partB_results.json'))
C1 = json.load(open(f'{R}/C1/tch_net_v2_results/partC1_results.json'))
C2 = json.load(open(f'{R}/C2/tch_net_v2_results/partC2_results.json'))
LOG = open(os.path.join(os.path.dirname(__file__), 'partA_log.txt')).read()

SHORT = {'CICIDS-2017': 'CICIDS-2017', 'CIC-BCCC-NRC-TabularIoTAttacks-2024': 'BCCC-2024',
         'CICIoMT-2024': 'CICIoMT-2024', 'UNSW-NB15': 'UNSW-NB15'}
ORDER = ['CICIDS-2017', 'CIC-BCCC-NRC-TabularIoTAttacks-2024', 'CICIoMT-2024', 'UNSW-NB15']
CITE = {'BiLSTM-IDS': '~\\cite{imrana2021}', 'BiGRU-IDS': '~\\cite{cho2014}', 'Transformer-IDS': '~\\cite{akuthota2025}',
        'DeepDefense': '~\\cite{yuan2017}', 'IoT-DNN': '~\\cite{diro2017}', 'Random-Forest': '~\\cite{breiman2001}',
        'XGBoost': '~\\cite{chen2016xgboost}'}
NAME = {'Random-Forest': 'Random Forest', 'H-only': 'H-branch only', 'TCH-Net': '\\tchnet{}'}
macros = []


def mac(name, val):
    macros.append(f'\\newcommand{{\\{name}}}{{{val}}}')


def f4(x): return f'{x:.4f}'
def f3(x): return f'{x:.3f}'
def sg(x, d=4): return f'{x:+.{d}f}'.replace('+', '$+$').replace('-', '$-$')
def pm(v): v = np.asarray(v, float); return f'${v.mean():.4f} \\pm {v.std(ddof=1):.4f}$'
def comma(n): return f'{int(n):,}'
def nm(m): return NAME.get(m, m)


# ── data report ────────────────────────────────────────────────────────────
dr = A['data_report']
tags = {'CICIDS-2017': 'Cicids', 'CIC-BCCC-NRC-TabularIoTAttacks-2024': 'Bccc', 'CICIoMT-2024': 'Iomt', 'UNSW-NB15': 'Unsw'}
import re
bal = {m.group(1): int(m.group(2).replace(',', '')) for m in re.finditer(r'  ([A-Za-z0-9\-]+): ([\d,]+) rows \(ben=', LOG)}
rows = []
for d in ORDER:
    t = tags[d]; dd = dr['dedup'][d]; cov = dr['coverage'][d]
    mac(f'dup{t}', f"{dd['duplicate_frac']*100:.1f}\\%"); mac(f'rawRows{t}', comma(dd['rows_in']))
    mac(f'uniqRows{t}', comma(dd['rows_kept'])); mac(f'bal{t}', comma(bal[d]))
    for k in ('mapped', 'derived', 'non_constant', 'independent'):
        mac(f'cov{k.replace("_", "").capitalize()}{t}', len(cov[k]))
    rows.append(f"{SHORT[d]} & {comma(dd['rows_in'])} & {dd['duplicate_frac']*100:.1f}\\% & {comma(dd['conflicting_vectors_dropped'])} & {comma(dd['rows_kept'])} & {comma(bal[d]//2)} & {comma(bal[d])} \\\\")
mac('tabRecordRows', '\n'.join(rows))
mac('balTotal', comma(sum(bal.values())))
rows = [f"{SHORT[d]} & {len(dr['coverage'][d]['mapped'])} & {len(dr['derived_slots'].get(d, []))} & "
        f"{len(dr['coverage'][d]['non_constant'])} & {len(dr['coverage'][d]['independent'])} & "
        f"{len(dr['coverage'][d]['non_constant'])/46*100:.0f}\\% \\\\" for d in ORDER]
mac('tabCoverageRows', '\n'.join(rows))
mac('commonAllN', len(dr['common_features_all']))
mac('commonAllList', ', '.join(f'\\texttt{{{f.replace("_", chr(92) + "_")}}}' for f in dr['common_features_all']))
mac('commonThreeN', len(dr['common_features_all_but_one']))
wl = dr['window_labels']['test']
mac('winPurity', f"{np.mean([v['mean_purity'] for v in wl.values()]):.3f}")
mac('winBenignAtk', f"{np.mean([v['benign_windows_with_attacks_frac'] for v in wl.values()])*100:.0f}\\%")
mac('winAtkFrac', f"{np.mean([v['attack_window_frac'] for v in wl.values()])*100:.1f}\\%")
for d in ORDER: mac(f'testWin{tags[d]}', comma(wl[d]['n_windows']))
m = re.search(r'\[train\] ([\d,]+) seqs.*?atk=([\d,]+) ([\d.]+)%', LOG); mac('trainWin', m.group(1)); mac('trainWinAtk', m.group(3) + '\\%')
m = re.search(r'\[val\] ([\d,]+) seqs.*?atk=([\d,]+) ([\d.]+)%', LOG); mac('valWin', m.group(1)); mac('valWinAtk', m.group(3) + '\\%')
m = re.search(r'\[test\] ([\d,]+) seqs.*?atk=([\d,]+) ([\d.]+)%', LOG); mac('testWin', m.group(1)); mac('testWinAtk', m.group(3) + '\\%')
lk = A['A_leakage']
mac('leakTestInTrain', lk['test_in_train']); mac('leakValInTrain', lk['val_in_train']); mac('leakTestInVal', lk['test_in_val'])
mac('leakTestRows', comma(lk['test_rows'])); mac('leakTrainRows', comma(lk['train_rows'])); mac('leakValRows', comma(lk['val_rows']))
mm = re.search(r'mask → LABEL accuracy:\s+([\d.]+)%\s+\(majority-class baseline: ([\d.]+)%', LOG)
mac('maskLabelAcc', mm.group(1) + '\\%'); mac('maskLabelMaj', mm.group(2) + '\\%')
mm = re.search(r'mask → DATASET-ID accuracy:\s+([\d.]+)%\s+\(majority-class baseline: ([\d.]+)%', LOG)
mac('maskDsAcc', mm.group(1) + '\\%'); mac('maskDsMaj', mm.group(2) + '\\%')
mm = re.search(r'zero-fill maps to \|value\|>0.01 after scale\+clip: (\d+)/46', LOG); mac('zeroFillNonNeutral', mm.group(1))

# ── Part A: main comparison ────────────────────────────────────────────────
main = A['A_main']; tch = main['TCH-Net']
for k, n in [('f1', 'F'), ('roc_auc', 'AUC'), ('mcc', 'MCC'), ('pr_auc', 'PR'), ('macro_f1', 'MacroF'),
             ('fpr_at_tpr95', 'FprNineFive'), ('fpr_at_tpr99', 'FprNineNine'), ('benign_f1', 'BenF')]:
    v = np.array([r[k] for r in tch])
    h = 2.776 * v.std(ddof=1) / np.sqrt(len(v))
    mac(f'nMain{n}', f4(v.mean())); mac(f'nMain{n}sd', f4(v.std(ddof=1)))
    mac(f'nMain{n}ciL', f4(v.mean() - h)); mac(f'nMain{n}ciU', f4(v.mean() + h))
pa = {c['baseline']: c for c in A['A_paired'] if c['metric'] == 'f1'}
rows = []
order = sorted([b for b in main if b != 'TCH-Net'], key=lambda b: -np.mean([r['f1'] for r in main[b]]))
for b in order:
    c = pa[b]; v = main[b]
    p = c['p_bonf']; ps = '$<$0.0001' if p < 1e-4 else f'{p:.4f}'
    rows.append(f"{nm(b)}{CITE.get(b, '')} & {pm([r['f1'] for r in v])} & {f4(np.mean([r['macro_f1'] for r in v]))} & "
                f"{f4(np.mean([r['roc_auc'] for r in v]))} & {sg(c['d_mean'])} & "
                f"[{sg(c['ci_lo'])}, {sg(c['ci_hi'])}] & {('0.0' if abs(c['cohens_dz']) < 0.05 else sg(c['cohens_dz'], 1))} & {c['tch_ahead']}/{c['n_pairs']} & {ps} \\\\")
mac('tabMainRows', '\n'.join(rows))
mac('tabMainTchRow', f"\\textbf{{\\tchnet{{}}}} & {pm([r['f1'] for r in tch])} & {f4(np.mean([r['macro_f1'] for r in tch]))} & "
                     f"{f4(np.mean([r['roc_auc'] for r in tch]))} & -- & -- & -- & -- & -- \\\\")
tr = pa['Transformer-IDS']
mac('trDF', sg(tr['d_mean'])); mac('trCIlo', sg(tr['ci_lo'])); mac('trCIhi', sg(tr['ci_hi'])); mac('trAhead', f"{tr['tch_ahead']}/{tr['n_pairs']}")
others = [c for b, c in pa.items() if b != 'Transformer-IDS']
mac('otherMinD', sg(min(c['d_mean'] for c in others))); mac('otherMaxD', sg(max(c['d_mean'] for c in others)))
mac('otherMaxPbonf', f"{max(c['p_bonf'] for c in others):.3f}")
mac('nBaselines', len(pa))

# ── operating points ───────────────────────────────────────────────────────
rows = []
for b in ['TCH-Net'] + order:
    d = pd.DataFrame(A['A_ops'][b])
    rows.append(f"{nm(b)} & {f3(d.tpr.mean())} & {f3(d.fpr.mean())} & {f3(d['precision@0.01'].mean())} & "
                f"{f3(d['precision@0.05'].mean())} & {f3(d['precision@0.1'].mean())} & {f3(d['f1@0.05'].mean())} & {f3(d.brier.mean())} \\\\")
mac('tabOpsRows', '\n'.join(rows))
d = pd.DataFrame(A['A_ops']['TCH-Net'])
mac('opsTpr', f3(d.tpr.mean())); mac('opsFpr', f3(d.fpr.mean())); mac('opsPrecFive', f3(d['precision@0.05'].mean()))
mac('opsPrecOne', f3(d['precision@0.01'].mean())); mac('opsPrecTen', f3(d['precision@0.1'].mean())); mac('opsFFive', f3(d['f1@0.05'].mean()))
pdd = pd.DataFrame(A['A_per_dataset'])
rows = []
for dname in ORDER:
    x = pdd[pdd.dataset == dname]
    rows.append(f"{SHORT[dname]} & {comma(x.n_test_windows.iloc[0])} & {pm(x['f1_shared_0.5'])} & {pm(x['f1_own_val_thr'])} & "
                f"{f4(x.auc.mean())} & {f3(x['fpr_0.5'].mean())} \\\\")
    mac(f'pd{tags[dname]}', f4(x['f1_shared_0.5'].mean())); mac(f'pdFpr{tags[dname]}', f3(x['fpr_0.5'].mean()))
mac('tabPerDatasetRows', '\n'.join(rows))
cost = {c['model']: c for c in A['A_cost']}
f1m = {b: np.mean([r['f1'] for r in main[b]]) for b in main}
rows = []
for b in ['TCH-Net', 'H-branch only'] + [x for x in order if x in cost]:
    f = f4(f1m[b]) if b in f1m else f4(np.mean([r['f1'] for r in B['B_branch']['H']])) + '$^\\ddagger$'
    rows.append(f"{nm(b)} & {cost[b]['params_M']:.3f} & {cost[b]['latency_ms']:.3f} & {f} \\\\")
mac('tabCostRows', '\n'.join(rows))
mac('nParamsM', f"{cost['TCH-Net']['params_M']:.3f}"); mac('nLatency', f"{cost['TCH-Net']['latency_ms']:.3f}")
mac('nHParamsM', f"{cost['H-branch only']['params_M']:.3f}")

# ── Part B ─────────────────────────────────────────────────────────────────
br = B['B_branch']; base = {r['seed']: r['f1'] for r in br['T+H']}
rows = []
for k, lab in [('T+H', 'T+H (full)'), ('T', 'T only'), ('H', 'H only')]:
    v = br[k]; dd = [r['f1'] - base[r['seed']] for r in v]
    ahead = sum(x > 0 for x in dd)
    rows.append(f"{lab} & {pm([r['f1'] for r in v])} & {f4(np.mean([r['roc_auc'] for r in v]))} & {f4(np.mean([r['mcc'] for r in v]))} & "
                + ('-- & --' if k == 'T+H' else f"{sg(np.mean(dd))} & {ahead}/5") + ' \\\\')
mac('tabBranchRows', '\n'.join(rows))
dH = np.array([r['f1'] - base[r['seed']] for r in br['H']])
mac('hMinusFull', sg(dH.mean())); mac('hAheadSeeds', f'{int((dH > 0).sum())}/5')
h = 2.776 * dH.std(ddof=1) / np.sqrt(5); mac('hMinusFullCIlo', sg(dH.mean() - h)); mac('hMinusFullCIhi', sg(dH.mean() + h))
mac('nHOnlyF', f4(np.mean([r['f1'] for r in br['H']]))); mac('nFullBF', f4(np.mean([r['f1'] for r in br['T+H']])))
mac('nTOnlyF', f4(np.mean([r['f1'] for r in br['T']])))
g = B['B_gate']
mac('gateT', f"{g['gate_mean_test'][0]:.3f}"); mac('gateH', f"{g['gate_mean_test'][1]:.3f}")
mac('gateHmin', f"{g['gate_H_min']:.3f}"); mac('gateHmax', f"{g['gate_H_max']:.3f}")
rows = []
for r in g['rows']:
    a = '--' if r['alpha_H'] is None else f"{r['alpha_H']:.2f}"
    lab = {'T expert': 'T expert (inside full model)', 'H expert': 'H expert (inside full model)',
           'learned gate (logit mixture, Eq. 5-6)': 'Learned gate, logit mixture (Eq.~\\ref{eq:logitmix})',
           'fixed 0.5 probability mixture': 'Fixed equal weights, probability mixture',
           'fixed 0.5 logit mixture': 'Fixed equal weights, logit mixture',
           'recalibrated probability mixture (Alg. 2)': 'Recalibrated probability mixture (Alg.~\\ref{alg:gatecal})',
           'recalibrated logit mixture': 'Recalibrated logit mixture'}[r['predictor']]
    rows.append(f"{lab} & {a} & {f4(r['val_f1'])} & {f4(r['test_f1'])} & {f4(r['test_auc'])} \\\\")
mac('tabGateRows', '\n'.join(rows))
gr = {r['predictor']: r for r in g['rows']}
mac('gateLearnedF', f4(gr['learned gate (logit mixture, Eq. 5-6)']['test_f1']))
mac('gateProbRecalF', f4(gr['recalibrated probability mixture (Alg. 2)']['test_f1']))
mac('gateLogitRecalF', f4(gr['recalibrated logit mixture']['test_f1']))
mac('gateFixedProbF', f4(gr['fixed 0.5 probability mixture']['test_f1'])); mac('gateFixedLogitF', f4(gr['fixed 0.5 logit mixture']['test_f1']))
mac('gateTexpF', f4(gr['T expert']['test_f1'])); mac('gateHexpF', f4(gr['H expert']['test_f1']))
mac('gateAlpha', f"{gr['recalibrated probability mixture (Alg. 2)']['alpha_H']:.2f}")
gc = B['B_grad_conflict']
mac('gradCosTrained', sg(gc['trained_seed42']['mean'], 3)); mac('gradNegTrained', f"{gc['trained_seed42']['frac_negative']*100:.0f}\\%")
mac('gradCosInit', sg(gc['initialised_seed42']['mean'], 3)); mac('gradNegInit', f"{gc['initialised_seed42']['frac_negative']*100:.0f}\\%")
nv = B['B_novelty']; full = np.mean([r['f1'] for r in nv['Full']])
rows = []
for k, lab in [('Full', 'Full model'), ('w/o MSTE', 'w/o \\mste{}'), ('w/o CB-GAF', 'w/o \\cbgaf{}'), ('w/o Aux Loss', 'w/o aux.\\ loss'),
               ('w/o CORAL', 'w/o CORAL'), ('w/o All', 'w/o all three + CORAL')]:
    v = [r['f1'] for r in nv[k]]
    rows.append(f"{lab} & {pm(v)} & {f4(np.mean([r['mcc'] for r in nv[k]]))} & " + ('--' if k == 'Full' else sg(np.mean(v) - full)) + ' \\\\')
    mac('nov' + k.replace('w/o ', 'Wo').replace(' ', '').replace('-', ''), sg(np.mean(v) - full) if k != 'Full' else f4(full))
mac('tabNoveltyRows', '\n'.join(rows))
od = B['B_order']
for k, t in [('TCH-Net', 'Tch'), ('Transformer-IDS', 'Tr')]:
    p = np.mean([r['f1'] for r in od[k]['permuted']]); q = np.mean([r['f1'] for r in od[k]['reference']])
    mac(f'ord{t}Perm', f4(p)); mac(f'ord{t}Ref', f4(q)); mac(f'ord{t}D', sg(p - q))
vr = B['B_variance']
for src in ('init', 'data'):
    for k, t in [('TCH-Net', 'Tch'), ('H-only', 'H')]:
        v = np.array(vr[src][k]); mac(f'var{src.capitalize()}{t}Sd', f4(v.std(ddof=1))); mac(f'var{src.capitalize()}{t}Mean', f4(v.mean()))
hp = B['B_hp']; d0 = np.mean(hp[0]['f1'])
labs = ['LR $5{\\times}10^{-4}$, WD $10^{-4}$, DO 0.20 (default)', 'LR $10^{-3}$', 'LR $2{\\times}10^{-4}$', 'WD $10^{-3}$', 'DO 0.30', 'DO 0.10']
rows = [f"{lab} & {pm(r['f1'])} & " + ('--' if i == 0 else sg(np.mean(r['f1']) - d0)) + ' \\\\' for i, (lab, r) in enumerate(zip(labs, hp))]
mac('tabHPRows', '\n'.join(rows))
dev = [np.mean(r['f1']) - d0 for r in hp[1:]]
mac('hpMaxAbs', f4(max(abs(x) for x in dev))); mac('hpBest', sg(max(dev)))
sn = B['B_sensitivity']
mac('sensClean', f4(sn['clean_f1']))
rows = [f"{float(s):.2f} & {f4(v)} & {sg(v - sn['clean_f1'])} \\\\" for s, v in sn['gaussian'].items()]
mac('tabGaussRows', '\n'.join(rows))
rows = [f"{float(e):.2f} & {f4(v['f1_adv'])} & {sg(v['f1_adv'] - v['f1_clean_subset'])} \\\\" for e, v in sn['fgsm'].items()]
mac('tabFgsmRows', '\n'.join(rows))
_g = [(f"{float(s):.2f}", f4(v), sg(v - sn['clean_f1'])) for s, v in sn['gaussian'].items()]
_f = [(f"{float(e):.2f}", f4(v['f1_adv']), sg(v['f1_adv'] - v['f1_clean_subset'])) for e, v in sn['fgsm'].items()]
rows = []
for i in range(max(len(_g), len(_f))):
    a_ = _g[i] if i < len(_g) else ('', '', ''); b_ = _f[i] if i < len(_f) else ('', '', '')
    rows.append(' & '.join(a_ + b_) + ' \\\\')
mac('tabSensRows', '\n'.join(rows))

# ── LODO (C1, + C1b classical if available) ───────────────────────────────
runs = pd.DataFrame(C1['C1_runs'])
if C1B:
    cb = json.load(open(glob.glob(f'{C1B}/**/partC1b_results.json', recursive=True)[0]))
    runs = pd.concat([runs[~runs.model.isin(['Random-Forest', 'XGBoost'])], pd.DataFrame(cb['C1_runs'])], ignore_index=True)
cls_complete = all(runs[runs.model == m].held_out.nunique() == 4 for m in ['Random-Forest', 'XGBoost'])
triv = runs.groupby('held_out').trivial_all_attack_f1.mean()
mac('trivMean', f4(triv.mean()))
for dname in ORDER: mac(f'triv{tags[dname]}', f4(triv[dname]))
LOD = ['Transformer-IDS', '1D-CNN-IDS', 'BiGRU-IDS', 'MLP-IDS', 'CNN-LSTM', 'H-only', 'TCH-Net', 'XGBoost', 'Random-Forest']
rows = []
g = runs.groupby('model')
for mdl in LOD:
    x = g.get_group(mdl); mark = '' if (mdl not in ('Random-Forest', 'XGBoost') or cls_complete) else '$^\\ast$'
    rows.append(f"{nm(mdl)}{mark} & {int(x.bn_layers.iloc[0])} & {f4(x.f1_raw.mean())} & {f4(x.f1_ad.mean())} & {f4(x.f1_cal.mean())} & "
                f"{f4(x.f1_ad_cal.mean())} & {f4(x.f1_oracle_ad.mean())} & {f4(x.auc_ad.mean())} & {f4(x.macro_f1_ad_cal.mean())} \\\\")
mac('tabLodoRows', '\n'.join(rows))
mac('lodoClassicalNote', '' if cls_complete else
    '$^\\ast$Random Forest and XGBoost: CICIDS-2017 and BCCC-2024 folds only (the remaining two folds are being re-run).')
pf = runs.pivot_table(index='model', columns='held_out', values='f1_ad_cal', aggfunc='mean')
rows = []
for mdl in LOD:
    vals = [pf.loc[mdl, d] if d in pf.columns and not np.isnan(pf.loc[mdl, d]) else None for d in ORDER]
    rows.append(f"{nm(mdl)} & " + ' & '.join('--' if v is None else f4(v) for v in vals) + ' \\\\')
rows.append('Trivial all-attack & ' + ' & '.join(f4(triv[d]) for d in ORDER) + ' \\\\')
mac('tabLodoFoldRows', '\n'.join(rows))
pa_ = runs.pivot_table(index='model', columns='held_out', values='auc_ad', aggfunc='mean')
rows = [f"{nm(m)} & " + ' & '.join('--' if (d not in pa_.columns or np.isnan(pa_.loc[m, d])) else f3(pa_.loc[m, d]) for d in ORDER) + ' \\\\' for m in LOD]
mac('tabLodoAucRows', '\n'.join(rows))
neural = runs[~runs.model.isin(['Random-Forest', 'XGBoost'])]
mac('lodoCalMin', f4(neural.groupby('model').f1_ad_cal.mean().min())); mac('lodoCalMax', f4(neural.groupby('model').f1_ad_cal.mean().max()))
mac('lodoCalOnlyMin', f4(neural.groupby('model').f1_cal.mean().min())); mac('lodoCalOnlyMax', f4(neural.groupby('model').f1_cal.mean().max()))
mac('lodoRawTch', f4(neural[neural.model == 'TCH-Net'].f1_raw.mean())); mac('lodoAdTch', f4(neural[neural.model == 'TCH-Net'].f1_ad.mean()))
mac('lodoCalTch', f4(neural[neural.model == 'TCH-Net'].f1_ad_cal.mean()))
_neu = [m for m in LOD if m in pa_.index and m not in ('Random-Forest', 'XGBoost')]
mac('lodoIomtAucMin', f3(pa_.loc[_neu, 'CICIoMT-2024'].min()))
mac('lodoIomtAucTreeMin', f3(pa_.loc[['Random-Forest', 'XGBoost'], 'CICIoMT-2024'].min()) if 'CICIoMT-2024' in pa_.columns and not pa_.loc[['Random-Forest', 'XGBoost'], 'CICIoMT-2024'].isna().any() else '--')
mac('lodoIomtAucTreeMax', f3(pa_.loc[['Random-Forest', 'XGBoost'], 'CICIoMT-2024'].max()) if 'CICIoMT-2024' in pa_.columns and not pa_.loc[['Random-Forest', 'XGBoost'], 'CICIoMT-2024'].isna().any() else '--')
mac('lodoIomtAucMax', f3(pa_.loc[[m for m in LOD if m in pa_.index and m not in ('Random-Forest', 'XGBoost')], 'CICIoMT-2024'].max()))
mac('lodoMacroMin', f4(neural.groupby('model').macro_f1_ad_cal.mean().min())); mac('lodoMacroMax', f4(neural.groupby('model').macro_f1_ad_cal.mean().max()))
neural = neural.assign(restored=neural.auc_ad > 0.60)
mac('restoredN', int(neural.restored.sum())); mac('lodoRunsN', len(neural))
mac('restoredF', f4(neural[neural.restored].f1_ad_cal.mean())); mac('unrestoredF', f4(neural[~neural.restored].f1_ad_cal.mean()))
rs = neural.groupby('model').restored.sum()
mac('restoredTr', int(rs['Transformer-IDS'])); mac('restoredTch', int(rs['TCH-Net']))
for k, v in C1['C1_folds'].items(): mac(f'lodoWin{tags[k]}', comma(v['n_target_windows']))
mac('lodoNcalCicids', comma(runs[runs.held_out == 'CICIDS-2017'].n_cal.iloc[0]))

# orientation (post hoc, from saved probabilities)
ori = pd.read_csv(os.path.join(os.path.dirname(__file__), 'lodo_orientation.csv'))
fold_map = {'CIC-BCCC-NRC': 'CIC-BCCC-NRC-TabularIoTAttacks-2024'}
ori['held_out'] = ori.fold.map(lambda f: fold_map.get(f, f))
po = ori.pivot_table(index='model', columns='held_out', values='f1_oriented', aggfunc='mean')
pfl = ori.pivot_table(index='model', columns='held_out', values='flipped', aggfunc='mean')
rows = []
for mdl in [m for m in LOD if m in po.index]:
    rows.append(f"{nm(mdl)} & " + ' & '.join(f4(po.loc[mdl, d]) for d in ORDER) + f" & {f4(po.loc[mdl].mean())} & {f4(ori[ori.model == mdl].macro_f1_oriented.mean())} \\\\")
mac('tabOrientRows', '\n'.join(rows))
io = ori[(ori.held_out == 'CICIoMT-2024') & ~ori.model.isin(['Random-Forest', 'XGBoost'])]
_pn = po.loc[[m for m in po.index if m not in ('Random-Forest', 'XGBoost')]]
mac('oriIomtMin', f4(_pn['CICIoMT-2024'].min())); mac('oriIomtMax', f4(_pn['CICIoMT-2024'].max()))
_pt = po.loc[[m for m in po.index if m in ('Random-Forest', 'XGBoost')]]
mac('oriIomtTreeMax', f4(_pt['CICIoMT-2024'].max()) if len(_pt) else '--')
mac('oriIomtFlip', f"{io.flipped.mean()*100:.0f}\\%")
other = ori[ori.held_out != 'CICIoMT-2024']
mac('oriOtherMax', f4(ori[ori.held_out != 'CICIoMT-2024'].groupby(['model', 'held_out']).f1_oriented.mean().max()))

# budget curves
rows = []
bd = []
for b in C1['C1_budget']:
    for k, v in b['curve'].items(): bd.append({'model': b['model'], 'k': int(k), 'f1': v['mean'], 'p10': v['p10']})
bd = pd.DataFrame(bd)
pv = bd.pivot_table(index='model', columns='k', values='f1', aggfunc='mean')
p10 = bd.pivot_table(index='model', columns='k', values='p10', aggfunc='mean')
for mdl in [m for m in LOD if m in pv.index and m not in ('Random-Forest', 'XGBoost')]:
    rows.append(f"{nm(mdl)} & " + ' & '.join(f"{pv.loc[mdl, k]:.3f} ({p10.loc[mdl, k]:.3f})" for k in pv.columns) + ' \\\\')
mac('tabBudgetRows', '\n'.join(rows))
mac('budgetKs', ' & '.join(f'$k={k}$' for k in pv.columns))

# ── C2 controls ────────────────────────────────────────────────────────────
c2 = pd.DataFrame(C2['C2_runs'])
ref = runs[runs.model.isin(['TCH-Net', 'H-only'])].assign(variant='default (46 zero-filled, CORAL on)')
allc = pd.concat([ref, c2], ignore_index=True)
rows = []
for mdl in ['TCH-Net', 'H-only']:
    for var in ['default (46 zero-filled, CORAL on)', 'no CORAL', 'common features (all 4)', 'common features (>=3 of 4)', 'mask-aware (zero-fill + mask)']:
        x = allc[(allc.model == mdl) & (allc.variant == var)]
        if not len(x): continue
        nf = int(x.n_features.iloc[0]) if 'n_features' in x and not np.isnan(x.n_features.iloc[0]) else 46
        vlab = {'default (46 zero-filled, CORAL on)': 'default', 'no CORAL': 'no CORAL', 'common features (all 4)': 'common, all 4',
                'common features (>=3 of 4)': 'common, $\\geq$3 of 4', 'mask-aware (zero-fill + mask)': 'mask-aware'}[var]
        rows.append(f"{nm(mdl)} & {vlab} & {nf} & {f4(x.f1_raw.mean())} & {f4(x.f1_ad.mean())} & {f4(x.f1_ad_cal.mean())} & {f4(x.auc_ad.mean())} \\\\")
mac('tabControlRows', '\n'.join(rows))

with open(OUT, 'w') as f:
    f.write('% Generated by rev2_analysis/make_numbers.py — do not edit by hand.\n')
    f.write('\n'.join(macros) + '\n')
print(f'wrote {OUT}: {len(macros)} macros; classical LODO complete: {cls_complete}')
