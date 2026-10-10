# BRIDGE and TCH-Net

**A Benchmark and Gated Baseline for IoT Intrusion Detection**

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

> Under review at *Journal of Network and Systems Management* (Springer).

> ℹ️ **Version note — please read.** This repository reflects **version 2** of the paper (four audited datasets, two-branch TCH-Net), the version currently under review at JNSM. An earlier **arXiv preprint links to this same repository** but describes the **previous version** — a three-branch model over five datasets, with a different design and different numbers. If you arrived here from that preprint, note that its results do not match the ones below: this repository and the JNSM version are the current work. The arXiv preprint will not be updated while the paper is under review.
>
> **Revision update.** The results below come from the revised evaluation protocol prepared for the JNSM revision. Checkpoints are selected on a dedicated validation split, never the test set, and baselines use the same 5 seeds as TCH-Net. These numbers supersede those in the originally submitted manuscript.

**Authors:** Ammar Bhilwarawala, Likhamba Rongmei, Harsh Sharma, Arya Jena, Kaushal Singh, Jayashree Piri, Raghunath Dey
**Affiliation:** School of Computer Engineering, Kalinga Institute of Industrial Technology (KIIT), Bhubaneswar, Odisha, India

---

## Overview

IoT intrusion-detection models are almost always validated on a single dataset, where they report scores in the high 0.90s. Those numbers rarely survive a change of environment — different capture tools, different devices, different attack toolkits. The benchmark looked easy because it was a closed world.

This work makes two connected contributions.

**BRIDGE** (Benchmark Reference for IoT Domain Generalisation Evaluation) is a heterogeneous multi-dataset benchmark for IoT intrusion detection. It unifies **four independently audited datasets drawn from three structurally distinct feature-extraction toolchains** under a single 46-feature canonical vocabulary, with genuine-equivalence-only feature mapping, explicit zero-filling for absent features, and full per-dataset coverage disclosure (30%–91%). It ships with a documented **dataset-quality audit** (candidates with broken or label-leaking schemas are rejected, with reasons published), a leakage-verification suite, and a **leave-one-dataset-out (LODO)** protocol paired with a **diagnosis-and-repair methodology** applied identically to every model.

The central, deliberately honest finding: under LODO, naive zero-shot transfer collapses to a mean **F1 = 0.0724** for TCH-Net. Small-sample threshold calibration alone recovers it to **0.6366**. Unsupervised test-time BatchNorm adaptation lifts the default-threshold F1 to 0.5157, but once the threshold is calibrated it adds nothing, for TCH-Net or any other model. The repair is also **conditional**. On 6 of 12 seed–fold runs, adaptation restores the score ranking (post-adaptation AUC > 0.60), and calibration then genuinely helps: mean F1 0.6432 against a trivial 0.6037. On the other 6, the "recovered" score is just an all-attack classifier wearing a calibrated threshold (0.6003 against 0.6020). Under identical repair, **no evaluated architecture — ours included — sits more than ~0.06 above that trivial predictor.** The take-away is measurement-first: for cross-dataset transfer, thresholding matters far more than the choice of architecture.

**TCH-Net v2** is a gated two-branch neural baseline for BRIDGE — a Temporal branch and a Statistical branch, fused by Cross-Branch Gated Attention Fusion (CB-GAF) with per-expert deep supervision and held-out gate recalibration. It is offered as a **characterised reference baseline, not a leaderboard winner** (the strongest transformer baseline stays ahead in-distribution, and a standalone statistical MLP beats the fused model in-distribution under an equal budget — both reported openly).

---

## Results

### Main comparison, in-distribution (all models: same 5 seeds)

Checkpoints are selected on a held-out validation split and never on the test set. ± is the sample SD over seeds {42, 123, 456, 789, 2024}.

| Model | F1 | ROC-AUC | MCC |
|-------|-----|---------|-----|
| Transformer-IDS | **0.8878 ± 0.0038** | **0.9725** | **0.8008** |
| **TCH-Net v2 (Ours)** | 0.8807 ± 0.0032 | 0.9656 | 0.7903 |
| BiGRU-IDS | 0.8495 ± 0.0022 | 0.9526 | 0.7294 |
| BiLSTM-IDS | 0.8483 ± 0.0026 | 0.9515 | 0.7273 |
| 1D-CNN-IDS | 0.8360 ± 0.0034 | 0.9409 | 0.7076 |
| CNN-LSTM | 0.8355 ± 0.0030 | 0.9412 | 0.7067 |
| DeepDefense | 0.8144 ± 0.0011 | 0.9259 | 0.6665 |
| XGBoost | 0.7891 ± 0.0026 | 0.9153 | 0.6460 |
| GraphSAGE-Approx | 0.7868 ± 0.0013 | 0.9073 | 0.6117 |
| Kitsune-AE | 0.7682 ± 0.0048 | 0.8858 | 0.5738 |
| IoT-DNN | 0.7517 ± 0.0010 | 0.8670 | 0.5471 |
| MLP-IDS | 0.7438 ± 0.0013 | 0.8605 | 0.5343 |
| Random Forest | 0.6429 ± 0.0037 | 0.8685 | 0.5141 |

TCH-Net v2 beats 11 of 12 baselines, and all 11 differences are significant. The test is a seed-matched two-sided paired t-test over 5 pairs, Bonferroni-corrected over 12 comparisons, and TCH-Net is ahead on 5/5 seeds in each. It does **not** beat the strongest transformer in-distribution. Transformer-IDS is ahead on all 5 seeds: ΔF1 = −0.0071, 95% CI [−0.0132, −0.0011], p = 0.031 uncorrected, 0.374 after Bonferroni. This is reported, not hidden — the value of the model is the characterised, honestly ablated design and its role as the BRIDGE reference baseline, not an in-distribution win.

### BRIDGE LODO generalisation (calibrated head-to-head)

Every repair stage (test-time BN adaptation + disjoint-slice threshold calibration) is applied **identically to every model**. Early stopping uses a validation slice of the *source* datasets only; the held-out domain is never used for model selection. Trivial all-attack predictor = 0.6028. F1 below is after adaptation + calibration (mean of 3 seeds per fold).

| Model | CICIDS | BCCC | CICIoMT | UNSW | Mean |
|-------|--------|------|---------|------|------|
| Transformer-IDS | **0.7685** | 0.6079 | **0.6399** | **0.6224** | **0.6597** |
| 1D-CNN-IDS | 0.6673 | **0.7211** | 0.6062 | 0.6092 | 0.6509 |
| BiGRU-IDS | 0.7492 | 0.6103 | 0.5979 | 0.6064 | 0.6409 |
| CNN-LSTM | 0.6284 | 0.7181 | 0.5983 | 0.6072 | 0.6380 |
| H-branch only (control) | 0.7102 | 0.6087 | 0.5979 | 0.6035 | 0.6301 |
| MLP-IDS | 0.6011 | 0.7011 | 0.5988 | 0.6032 | 0.6260 |
| **TCH-Net v2 (Ours)** | 0.6482 | 0.6170 | 0.6044 | 0.6175 | 0.6218 |

All six full models land inside a 0.038 band, within +0.019 to +0.057 of the trivial predictor. TCH-Net is last of the six. **No architecture dominates cross-extractor transfer.**

**Which repair stage does the work (mean over folds and seeds):**

| Model | BN layers | 0.5 thr, no adapt | 0.5 thr, adapted | Calibrated, no adapt | Calibrated, adapted |
|-------|-----------|-------------------|------------------|----------------------|---------------------|
| Transformer-IDS | 0 | 0.0376 | 0.0376 | **0.6597** | **0.6597** |
| 1D-CNN-IDS | 4 | 0.2068 | 0.5784 | 0.6487 | 0.6509 |
| BiGRU-IDS | 1 | 0.0572 | 0.5192 | 0.6419 | 0.6410 |
| CNN-LSTM | 3 | 0.3745 | 0.5583 | 0.6340 | 0.6380 |
| H-branch only | 4 | 0.1479 | 0.4650 | 0.6417 | 0.6301 |
| MLP-IDS | 3 | 0.2322 | 0.5391 | 0.6301 | 0.6260 |
| **TCH-Net v2 (Ours)** | 14 | 0.0724 | 0.5157 | 0.6366 | 0.6218 |

Test-time BN adaptation re-estimates `BatchNorm1d` statistics only, so it does nothing for Transformer-IDS (LayerNorm only). At the default 0.5 threshold, adaptation helps every BatchNorm model a great deal. Once the threshold is calibrated, its effect is −0.015 to +0.004. Calibration alone does the repair, and its gain (+0.26 to +0.62) dwarfs the 0.030 spread between architectures.

**The repair is conditional (TCH-Net, read per seed–fold, not as a mean):**

| Regime | Runs | Post-adaptation AUC | Calibrated F1 | vs. trivial on the same folds |
|--------|------|--------------------|--------------|-------------------------------|
| Ranking restored (AUC > 0.60) | 6/12 | 0.7007 | 0.6432 | +0.0395 |
| Ranking not restored | 6/12 | 0.4607 | 0.6003 | −0.0017 (i.e. trivial) |

No run falls between a post-adaptation AUC of 0.582 and 0.646, so the two regimes are cleanly separated. Calibrated generalisation gap (in-distribution − calibrated LODO): **0.8807 − 0.6218 = +0.2589.** Cross-extractor transfer is not solved by any model or repair stage evaluated here.

---

## BRIDGE Dataset

BRIDGE maps four public IoT/network-security datasets into a shared 46-feature canonical vocabulary based on CICFlowMeter nomenclature. Features absent from a given dataset are zero-filled explicitly — nothing is fabricated, and coverage is fully disclosed and empirically verified to carry no label shortcut.

### Source datasets (three distinct extractor families)

| Dataset | Capture tool | Year | Coverage | Role |
|---------|-------------|------|----------|------|
| CICIDS-2017 | CICFlowMeter | 2017 | 91% (42/46) | Vocabulary anchor |
| CIC-BCCC-NRC-TabularIoTAttacks-2024 (BCCC-2024) | CICFlowMeter (BCCC re-extraction) | 2024 | 91% (42/46) | Primary IoT-attack data |
| CICIoMT-2024 | Custom CIC sliding-window extractor | 2024 | 35% (16/46 effective) | Distinct extractor family |
| UNSW-NB15 | Argus + Bro/Zeek | 2015 | 30% (14/46) | Non-CIC extractor anchor |

### Datasets audited and rejected (published as part of the methodology)

Direct label/schema inspection is treated as part of dataset selection. Rejected candidates and reasons:

- **Bot-IoT** (public mirror) — 100% attack rows, no benign traffic in the inspected shards; supervised benign-vs-attack evaluation impossible.
- **Edge-IIoTset** — application-layer schema (near-zero canonical flow coverage) and, more seriously, raw attack payload strings stored verbatim in a feature column (`http.request.uri.query`): a ready-made label-leakage shortcut.
- **N-BaIoT-style exports** — resolve at most 7/46 canonical slots, below the usefulness threshold for a flow-statistic fold.
- Two earlier candidates with a literal placeholder label string, and with no label column at all, respectively.

> ⚠️ These rejections are a core part of the paper. Do not add these datasets to the benchmark — they are excluded on purpose.

### Post-balancing record counts (1:1 per dataset, before windowing)

| Dataset | Benign | Attack | Total |
|---------|--------|--------|-------|
| CICIDS-2017 | 123,195 | 123,195 | 246,390 |
| BCCC-2024 | 28,907 | 28,907 | 57,814 |
| CICIoMT-2024 | 78,812 | 78,812 | 157,624 |
| UNSW-NB15 | 93,000 | 93,000 | 186,000 |
| **Combined** | **323,914** | **323,914** | **647,828** |

Each dataset is split by original row order into train / validation / test = 70 / 10 / 20%, **before** windowing. Windows never span two partitions or two datasets. The validation split is used only for early stopping and checkpoint selection. After sliding-window construction (W=32, S=4, majority-vote label), the balance shifts to ~57:43 benign:attack. Training sequences: 113,341 (43.1% attack). Validation sequences: 16,166 (42.9% attack). Test sequences: 32,362 (42.7% attack).

### The 46 canonical features

| Group | Category | Indices | Count |
|-------|----------|---------|-------|
| 1 | Flow rates, durations, pkt/byte counts | 0–16 | 17 |
| 2 | Packet size & IAT statistics | 17–37 | 21 |
| 3 | TCP flag indicators | 38–43 | 6 |
| 4 | Header length & window size | 44–45 | 2 |

The full alias-mapping tables are defined in the canonical-vocabulary cell of the notebook (`ALIAS_FLOWMETER`, `ALIAS_IOMT`, `ALIAS_UNSW`). They cover each dataset, and rejected mappings are documented inline with their reasons.

---

## TCH-Net v2 Architecture

Two branches process a (B, 32, 46) window in parallel, fused by CB-GAF at the logit level.

```
Input: (B, 32, 46)  — batch × 32-step window × 46 canonical features

Shared residual feature projection:
  Linear(46→92) → LayerNorm → GELU → Dropout(δ/2)
  → Linear(92→46) → LayerNorm        [X̃ = X + f_proj(X)]

T-Branch (Temporal, MSTE) — 512d:
  Path 1: ResConvSE×3 + MaxPool → BiGRU(128/dir, 2L)          → 8×256
  Path 2: StrideConv(s=2) → BiGRU(64/dir, 1L) → AvgPool(8)    → 8×128
  Path 3: Linear(46→128) + LearnablePE
          → TransformerEncoder(Pre-LN, 2L, 8H) → AvgPool(8)   → 8×128
  Merge:  concat(8×512) → LayerNorm → MHA(8H) → mean-pool      → 512d

H-Branch (Statistical) — 128d:
  mean(X̃, time) → [ MLP(46→…→64, BN+GELU+Dropout) ‖ GELU(W_r·mean) ] → 128d

CB-GAF (Cross-Branch Gated Attention Fusion, logit-level MoE):
  each branch → own expert head (2-layer MLP) → per-expert logits ℓ^b ∈ R²
  softmax gate over both branch reps mixes logits:  ℓ = a_T·ℓ^T + a_H·ℓ^H
  per-expert deep supervision trains each expert to stand alone (anti gate-collapse)
  held-out gate recalibration (α*) applied post hoc

Training-only:
  auxiliary reconstruction decoder on the gated feature mixture (λ_aux)
  CORAL source-domain alignment across dataset identities (λ_coral)
```

> **Note on the name.** The original design had three branches — Temporal (T), Contextual (C), Statistical (H). **The Contextual branch is removed in v2** for a structural reason: no trained identity embedding exists for an unseen domain, so provenance conditioning cannot transfer. Its functions are reassigned to CORAL (training) and test-time BatchNorm adaptation (evaluation). The "C" in the name now stands for CB-GAF, the central fusion mechanism, not a branch.

**~2.386M trainable parameters.** Single-sample inference latency: **8.972 ms** on NVIDIA Tesla T4.

---

## Ablations (equal budget, single architecture, 3 seeds; every row retrained)

### Branch ablation

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| T + H (Full) | 0.8801 | — |
| T only | 0.8778 | −0.0023 |
| **H only** | **0.8975** | **+0.0174** |

The strongest in-distribution model of the study is the standalone Statistical branch (an MLP over window-mean features, <0.2M params). This is reported openly and explained: windowed flow records carry little genuine temporal structure, and the shared trunk costs the internal H expert ~0.020 F1 via gradient interference. Under LODO the standalone H-branch also transfers slightly *better* than the full model (calibrated 0.6301 vs 0.6218). The temporal branch therefore does not earn its cost back cross-domain on BRIDGE.

### Novelty-component ablation (positive ΔF1 = removing it helps)

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| Full model | 0.8801 | — |
| w/o MSTE (multi-scale temporal) | 0.8655 | −0.0146 |
| w/o CB-GAF (→ plain concat) | 0.8791 | −0.0010 |
| w/o Aux loss | 0.8794 | −0.0007 |
| w/o CORAL | 0.8784 | −0.0017 |
| w/o all (≈ v1 core) | 0.8640 | −0.0161 |

The one unambiguously positive component is **MSTE**. CB-GAF is in-distribution-neutral by F1; its justification is the verified fusion properties below, not raw score.

### Gate recalibration (seed-42 model; α* and thresholds chosen on the validation split, F1 on the full test set)

| Predictor | Test F1 |
|-----------|---------|
| T expert (inside full model) | 0.8827 |
| H expert (inside full model) | 0.8775 |
| Full model, learned gate | 0.8833 |
| Full model, recalibrated (α*=0.80) | **0.8887** |

Gated late fusion with deep supervision matches the best internal expert; held-out recalibration lifts the fused model above both, repairing the mixture-collapse pathology.

---

## Training Configuration

| Hyperparameter | Value |
|---------------|-------|
| Optimizer | AdamW |
| Learning rate | 5×10⁻⁴ |
| Weight decay | 1×10⁻⁴ |
| Scheduler | Cosine annealing, 3-epoch warmup |
| Loss | Focal (γ=2.5, α-weighted, ε=0.01) + deep-sup (λ_ds=0.3) + aux (λ_aux=0.05) + CORAL (λ_coral=0.5) |
| Batch size | 512 |
| Max epochs / patience | 30 / 7 (LODO: 30 / 5) |
| Early stopping / checkpoint selection | Validation F1 (10% chronological split; LODO: last 10% of each source dataset) |
| Window size / stride | 32 / 4 |
| Dropout | 0.20 |
| Augmentation | Gaussian noise (σ=0.01, p=0.30, train only) |
| Hardware | NVIDIA Tesla T4 (Kaggle) |

Seeds: TCH-Net and all 12 baselines 5 seeds {42, 123, 456, 789, 2024}, paired by seed for significance tests; ablations 3 seeds {42, 123, 456}; LODO 3 seeds per fold with bootstrap CIs.

---

## Computational Efficiency (NVIDIA Tesla T4)

| Model | Params (M) | Latency (ms) | F1 |
|-------|-----------|-------------|-----|
| **TCH-Net v2 (Ours)** | 2.386 | 8.972 | 0.8807 |
| Transformer-IDS | 0.618 | 1.820 | 0.8878 |
| BiLSTM-IDS | 0.609 | 2.000 | 0.8483 |
| BiGRU-IDS | 0.465 | 1.281 | 0.8495 |
| CNN-LSTM | 0.142 | 1.149 | 0.8355 |
| 1D-CNN-IDS | 0.068 | 0.949 | 0.8360 |
| MLP-IDS | 0.920 | 0.613 | 0.7438 |

---

## Repository Structure

```
TCH-Net/
├── Revised_Version_of_BRIDGE_and_TCH_Net.ipynb   # current version: every result in this README
├── Temporal_Split_Rerun.ipynb                    # temporal re-split only (3 seeds), see note below
├── Paper_Version_of_BRIDGE_and_TCH_Net.ipynb     # code as originally submitted to JNSM (superseded)
├── Old_Arxiv_Version_of_Bridge_and_TCH_Net       # earlier arXiv preprint (three-branch, five-dataset) notebook
├── LICENSE
└── README.md
```

The revised notebook is self-contained. It includes the 46-feature canonical vocabulary and alias-mapping tables, dataset loaders and audit checks, preprocessing and windowing, all models, the statistical tests, the LODO protocol, and the calibration methodology. It is committed **with its outputs** from the Kaggle run, so every number above can be traced to a cell. Its first cell lists what changed from the submitted version.

The full run reached Kaggle's 12-hour session limit during the last experiment, the temporal re-split (paper Table 16), after 2 of its 3 seeds. `Temporal_Split_Rerun.ipynb` re-runs only that experiment, for all 3 seeds. It uses the same setup cells, unchanged, and is committed with its outputs. Re-split F1 is 0.8831 ± 0.0022 against 0.8807 for the default split.

The submitted-version notebook is kept for transparency only. It selected checkpoints on the test set, which the revised version corrects, so its numbers should not be used.

---

## Quickstart

The notebook is written for Kaggle (NVIDIA T4 GPU).

1. Import `Revised_Version_of_BRIDGE_and_TCH_Net.ipynb` into a new Kaggle notebook.
2. Attach the four source datasets:
   - [bertvankeulen/cicids-2017](https://www.kaggle.com/datasets/bertvankeulen/cicids-2017)
   - [kabeleswarpe/cic-bccc-nrc-tabulariotattacks-2024](https://www.kaggle.com/datasets/kabeleswarpe/cic-bccc-nrc-tabulariotattacks-2024)
   - [sinfdosh1990/ciciomt2024](https://www.kaggle.com/datasets/sinfdosh1990/ciciomt2024)
   - [mrwellsdavid/unsw-nb15](https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15)

   The paths are set in `Config` at the top of the notebook.
3. Select the GPU T4 accelerator and run all cells. A full run trains 13 models × 5 seeds plus ablations and LODO, so use *Save & Run All* to run it in the background.

Result tables are written as CSV files to `tch_net_v2_results/` (for example `stat_tests.csv`, `lodo_calibrated_head_to_head.csv`, `lodo_repair_decomposition_mean.csv` and `bn_coverage.csv`). Model weights are not saved. Raw features are scaled with a RobustScaler fitted on training rows only, then clipped to [−10, 10] before windowing.

To run outside Kaggle, point the paths in `Config` at local copies of the four datasets and install the dependencies:

```bash
pip install torch numpy pandas scikit-learn scipy xgboost seaborn tqdm
```

---

## Limitations

- **Residual cross-dataset gap.** Even after both repair stages, a genuine +0.2589 F1 gap remains. On half the seed–fold runs, the repaired model does not beat the all-attack predictor by more than 0.005. Threshold placement is recovered; transferable signal that was never learned is not manufactured.
- **Test-time BN adaptation is not a repair on its own.** It helps only at the default 0.5 threshold, and adds nothing once the threshold is calibrated. It also cannot act on BatchNorm-free models such as Transformer-IDS.
- **In-distribution position.** Transformer-IDS stays ahead of TCH-Net in-distribution: +0.0071, consistent across all 5 seeds, but not significant after Bonferroni correction. It also leads the calibrated LODO head-to-head, where TCH-Net is last of the six full models. TCH-Net is a characterised baseline, not the leaderboard winner.
- **Testbed data.** All four datasets are controlled-testbed or aggregated research captures; two (CICIDS-2017, UNSW-NB15) are enterprise rather than IoT-specific, retained as vocabulary/extractor-family anchors.
- **Binary scope.** Evaluated as a binary detector; multi-class attack typing is future work.
- **Edge deployment.** Memory/throughput on edge hardware were not measured; distillation, pruning, and INT8 quantisation are the obvious compression routes.

---

## Citation

The paper is under review, so no DOI has been issued yet. Please cite as follows. The earlier arXiv preprint describes a previous version with different results.

```bibtex
@article{bhilwarawala2026bridge,
  title   = {{BRIDGE} and {TCH-Net}: A Benchmark and Gated Baseline for
             {IoT} Intrusion Detection},
  author  = {Bhilwarawala, Ammar and Rongmei, Likhamba and Sharma, Harsh
             and Jena, Arya and Singh, Kaushal and Piri, Jayashree and Dey, Raghunath},
  note    = {Under review, Journal of Network and Systems Management},
  year    = {2026}
}
```

---

## License

Released under the [Apache 2.0 License](LICENSE). The four source datasets are subject to their own respective licenses; consult each original source before commercial or derivative use.

## Acknowledgements

We thank the creators of the constituent datasets for making them publicly available. Experiments were conducted on Kaggle with NVIDIA Tesla T4 GPU instances.
