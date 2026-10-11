# BRIDGE

**An Audited Cross-Dataset Benchmark for IoT Intrusion Detection**

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

> Under review at *Journal of Network and Systems Management* (Springer). The paper was first submitted as "BRIDGE and TCH-Net: A Benchmark and Gated Baseline for IoT Intrusion Detection"; the revised version leads with the benchmark, and TCH-Net remains as its reference model.

> **Version note — please read.** Everything below comes from the **second revision** (folder [`revision2/`](revision2/)). The revision corrected the benchmark itself (duplicate records, unit differences, overlapping evaluation windows, model selection on the test set), so **its numbers supersede every earlier version**: the originally submitted notebook, the first-revision notebook, and the earlier arXiv preprint (a three-branch model over five datasets). Those are kept in [`archive/`](archive/) for transparency only.

**Authors:** Ammar Bhilwarawala, Likhamba Rongmei, Harsh Sharma, Arya Jena, Kaushal Singh, Jayashree Piri, Raghunath Dey
**Affiliation:** School of Computer Engineering, Kalinga Institute of Industrial Technology (KIIT), Bhubaneswar, Odisha, India

---

## Overview

IoT intrusion-detection models are almost always evaluated on one dataset at a time, and scores obtained that way say little about how a detector behaves on another network.

**BRIDGE** joins four audited public datasets from **three different feature-extraction toolchains** (CICFlowMeter, the CIC packet-window extractor, Argus/Bro) under one 46-feature canonical vocabulary:

- mappings restricted to **computationally equivalent** quantities, with **units converted explicitly** (not left to the scaler);
- coverage reported in four tiers (mapped, derived, non-constant, independent);
- **exact duplicate records removed before any split** (18–48% of each dataset were duplicates);
- a 70/10/20 split **before** windowing, non-overlapping evaluation windows, an odd window length (W = 33, so majority-vote labels cannot tie), and a full-row hash audit across partitions;
- a **leave-one-dataset-out (LODO)** protocol in which every model gets the same repair (test-time BatchNorm adaptation + threshold calibration on a record-disjoint 20% slice of the target), and every result is read against the **all-attack predictor** for its fold.

**Prediction unit.** None of the four datasets offers a usable time order, so records are shuffled before windowing: a window is a *bag* of 33 records from one dataset, labelled attack when most of its records are attacks.

### Findings

1. **In-distribution**, the gated two-branch reference model **TCH-Net** is level with Transformer-IDS and ahead of the nine other baselines, but a small **order-invariant statistical model (the H-branch alone) is the best model**, and permuting records within windows does not lower the sequence models' F1.
2. **Across datasets**, after identical repair, **no evaluated model — neural or tree-based — and no representation control transfers beyond the all-attack predictor.**
3. **One exception:** on CICIoMT-2024 every neural model's scores are *inverted* (AUC 0.10–0.29), not uninformative; choosing the score direction on the labelled slice recovers F1 0.73–0.83. The tree ensembles score that target near chance instead.

---

## Results

### In-distribution comparison (all models: the same 5 seeds)

Checkpoints are selected on a validation partition, never on the test set. ± is the sample SD over seeds {42, 123, 456, 789, 2024}. ΔF1 = TCH-Net − baseline, mean of the five seed-matched differences with a 95% t-interval.

| Model | F1 (attack) | Macro-F1 | ROC-AUC | ΔF1 (95% CI) | Seeds TCH-Net ahead |
|---|---|---|---|---|---|
| Transformer-IDS | 0.8990 ± 0.0052 | 0.8967 | 0.9684 | −0.0001 [−0.0100, +0.0099] | 2/5 |
| **TCH-Net (reference)** | 0.8989 ± 0.0059 | 0.8965 | 0.9642 | — | — |
| 1D-CNN-IDS | 0.8721 ± 0.0042 | 0.8664 | 0.9469 | +0.0268 [+0.0160, +0.0376] | 5/5 |
| CNN-LSTM | 0.8607 ± 0.0043 | 0.8556 | 0.9402 | +0.0382 [+0.0310, +0.0454] | 5/5 |
| BiGRU-IDS | 0.8586 ± 0.0068 | 0.8528 | 0.9385 | +0.0403 [+0.0259, +0.0548] | 5/5 |
| BiLSTM-IDS | 0.8538 ± 0.0045 | 0.8470 | 0.9368 | +0.0452 [+0.0336, +0.0567] | 5/5 |
| XGBoost | 0.8379 ± 0.0032 | 0.8350 | 0.9245 | +0.0610 [+0.0528, +0.0692] | 5/5 |
| DeepDefense | 0.8362 ± 0.0033 | 0.8236 | 0.9180 | +0.0627 [+0.0544, +0.0710] | 5/5 |
| Random Forest | 0.8088 ± 0.0043 | 0.8074 | 0.8964 | +0.0901 [+0.0795, +0.1007] | 5/5 |
| IoT-DNN | 0.7931 ± 0.0026 | 0.7810 | 0.8728 | +0.1058 [+0.0998, +0.1118] | 5/5 |
| MLP-IDS | 0.7858 ± 0.0019 | 0.7734 | 0.8668 | +0.1132 [+0.1044, +0.1219] | 5/5 |

**Branch ablation** (same 5 seeds, every row retrained):

| Variant | F1 |
|---|---|
| T+H (full TCH-Net) | 0.8962 ± 0.0104 |
| T only (sequence branch) | 0.8972 ± 0.0082 |
| **H only (statistical branch)** | **0.9069 ± 0.0074** |

At a realistic 5% attack prevalence (class-conditional reweighting, threshold chosen on validation for TPR ≥ 0.95), TCH-Net's precision is about 0.20: no evaluated model is a high-precision detector at that prevalence.

### Leave-one-dataset-out (5 seeds per fold and model)

Each model trains on three datasets and is evaluated on the fourth. All numbers are on the same evaluation slice; "repaired" = test-time BN adaptation (where a model has BatchNorm) + threshold calibration on the first 20% of target records.

| Model | F1 @ 0.5 (mean) | Repaired F1 (mean) | CICIDS-2017 | BCCC-2024 | CICIoMT-2024 | UNSW-NB15 | CICIoMT AUC |
|---|---|---|---|---|---|---|---|
| Transformer-IDS | 0.1754 | 0.6813 | 0.6956 | 0.6867 | 0.6702 | 0.6726 | 0.099 |
| 1D-CNN-IDS | 0.1815 | 0.6744 | 0.6803 | 0.6805 | 0.6696 | 0.6674 | 0.114 |
| BiGRU-IDS | 0.2333 | 0.6738 | 0.6926 | 0.6631 | 0.6713 | 0.6683 | 0.126 |
| MLP-IDS | 0.2646 | 0.6732 | 0.6602 | 0.6929 | 0.6710 | 0.6688 | 0.098 |
| CNN-LSTM | 0.2435 | 0.6676 | 0.6623 | 0.6724 | 0.6707 | 0.6652 | 0.166 |
| H-branch only | 0.0391 | 0.6680 | 0.6641 | 0.6778 | 0.6690 | 0.6612 | 0.289 |
| TCH-Net | 0.0090 | 0.6666 | 0.6705 | 0.6639 | 0.6703 | 0.6618 | 0.221 |
| XGBoost | 0.4950 | 0.6700 | 0.6579 | 0.6852 | 0.6712 | 0.6656 | 0.469 |
| Random Forest | 0.5157 | 0.6639 | 0.6592 | 0.6580 | 0.6713 | 0.6670 | 0.497 |
| *All-attack predictor* | — | *0.6653* | *0.6604* | *0.6615* | *0.6715* | *0.6677* | — |

Every repaired F1 sits within a few hundredths of the all-attack predictor, and macro-F1 after repair is only 0.36–0.46: the repaired models label nearly every target window an attack. The same holds for the LODO controls — no CORAL, training only on the 3 features every dataset fills, the 28 features filled by at least three, and zero-fill plus an explicit missingness mask (repaired F1 0.663–0.676).

---

## Repository Structure

```
TCH-Net/
├── revision2/                                  # current version: every result in the paper and this README
│   ├── notebooks/
│   │   ├── BRIDGE_data_audit.ipynb             # units, timestamps, duplicates, window labels (no training)
│   │   ├── BRIDGE_rev2_partA.ipynb             # in-distribution comparison, operating points, cost, hash audit
│   │   ├── BRIDGE_rev2_partB.ipynb             # branch/novelty ablations, gate & mixing, record-order control,
│   │   │                                       #   variance sources, HP sensitivity, feature-space sensitivity
│   │   ├── BRIDGE_rev2_partC1.ipynb            # LODO: TCH-Net, H-only, 5 neural baselines, budget curves
│   │   ├── BRIDGE_rev2_partC1b.ipynb           # LODO: Random Forest and XGBoost (C1 hit Kaggle's 12-h limit here)
│   │   └── BRIDGE_rev2_partC2.ipynb            # LODO controls: no CORAL, common features, mask-aware
│   ├── results/                                # result files written by the notebooks
│   │   ├── audit/bridge_audit.json
│   │   └── {A,B,C1,C1b,C2}/tch_net_v2_results/ # part*_results.json (+ lodo_probs/ for C1, C1b)
│   └── analysis/
│       ├── make_numbers.py                     # generates every number and results-table row in the paper
│       ├── lodo_posthoc.py                     # orientation-aware calibration from saved LODO scores
│       ├── extract_log.py                      # rebuilds partA_log.txt from the Part A notebook
│       ├── partA_log.txt
│       └── lodo_orientation.csv
├── archive/                                    # superseded versions, kept for transparency only
│   ├── Paper_Version_of_BRIDGE_and_TCH_Net.ipynb    # as originally submitted (selected checkpoints on the test set)
│   ├── Revised_Version_of_BRIDGE_and_TCH_Net.ipynb  # first revision (before the data audit)
│   └── Temporal_Split_Rerun.ipynb                   # withdrawn: a positional split of shuffled rows is not temporal
├── Old_Arxiv_Version_of_Bridge_and_TCH_Net     # earlier arXiv preprint notebook (three-branch, five datasets)
├── LICENSE
└── README.md
```

The six notebooks share one setup (vocabulary and alias maps, unit conversions, de-duplication, loaders, preprocessing, models, training code) and differ only in the experiments they run. They are committed **with their outputs** from the Kaggle runs.

---

## Reproducing

### Run the experiments (Kaggle, NVIDIA T4)

1. Import a notebook from `revision2/notebooks/` into Kaggle and attach the four datasets:
   - [bertvankeulen/cicids-2017](https://www.kaggle.com/datasets/bertvankeulen/cicids-2017)
   - [kabeleswarpe/cic-bccc-nrc-tabulariotattacks-2024](https://www.kaggle.com/datasets/kabeleswarpe/cic-bccc-nrc-tabulariotattacks-2024)
   - [sinfdosh1990/ciciomt2024](https://www.kaggle.com/datasets/sinfdosh1990/ciciomt2024)
   - [mrwellsdavid/unsw-nb15](https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15)
2. Select GPU T4 (the audit notebook and C1b need CPU only) and use *Save Version → Save & Run All*. Results are saved incrementally to `tch_net_v2_results/part<X>_results.json`.
3. Approximate run times: audit < 1 h, A 2.6 h, B 5.9 h, C1 ≈ 12 h, C1b 5.4 h (CPU), C2 7.0 h.

Environment used: PyTorch 2.11.0 (CUDA 12.8), scikit-learn 1.6.1, XGBoost 3.4.1.

### Regenerate the paper's numbers from the result files

```bash
cd revision2/analysis
python extract_log.py ../notebooks/BRIDGE_rev2_partA.ipynb
python lodo_posthoc.py ../results/C1/tch_net_v2_results/lodo_probs ../results/C1b/tch_net_v2_results/lodo_probs
python make_numbers.py ../results rev2_numbers.tex ../results/C1b
```

`rev2_numbers.tex` holds every number and results-table row used in the manuscript as LaTeX macros (requires numpy and pandas).

---

## Limitations

- **Windows are bags of records**, labelled by majority vote; attacks that are a minority of a window are labelled benign, and record-level detection is not evaluated.
- **Four target networks** are too few to estimate uncertainty across networks; per-fold results are reported instead. Seed-based intervals hold the data fixed; data-partition variance is of similar size to initialisation variance.
- **Feature definitions:** CICIoMT-2024 features are window-averaged; byte counts may differ between extractors in header inclusion; CICIDS-2017 labels are used as distributed (no relabelling).
- **Scope:** testbed captures (two of four are enterprise, not IoT); binary detection; the feature-space sensitivity tests are unconstrained; edge-hardware cost not measured.

---

## Citation

The paper is under review, so no DOI has been issued yet.

```bibtex
@article{bhilwarawala2026bridge,
  title   = {{BRIDGE}: An Audited Cross-Dataset Benchmark for {IoT} Intrusion Detection},
  author  = {Bhilwarawala, Ammar and Rongmei, Likhamba and Sharma, Harsh
             and Jena, Arya and Singh, Kaushal and Piri, Jayashree and Dey, Raghunath},
  note    = {Under review, Journal of Network and Systems Management},
  year    = {2026}
}
```

---

## License

Released under the [Apache 2.0 License](LICENSE). The four source datasets are subject to their own licenses; consult each original source before commercial or derivative use.

## Acknowledgements

We thank the creators of the constituent datasets for making them publicly available. Experiments were conducted on Kaggle with NVIDIA Tesla T4 GPU instances.
