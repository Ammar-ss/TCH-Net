# BRIDGE and TCH-Net

**A Benchmark and Gated Baseline for IoT Intrusion Detection**

<!-- Badges: update or remove before publishing.
     NOTE: the current arXiv preprint is an EARLIER (three-branch, five-dataset)
     version and does NOT match the numbers below. Do not point readers at it as
     if it were this work. Either post the matching version or omit the arXiv badge. -->
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

> Under review at *Journal of Network and Systems Management* (Springer).

> ℹ️ **Version note — please read.** This repository reflects **version 2** of the paper (four audited datasets, two-branch TCH-Net), the version currently under review at JNSM. An earlier **arXiv preprint links to this same repository** but describes the **previous version** — a three-branch model over five datasets, with a different design and different numbers. If you arrived here from that preprint, note that its results do not match the ones below: this repository and the JNSM version are the current work. The arXiv preprint will not be updated while the paper is under review.

**Authors:** Ammar Bhilwarawala, Likhamba Rongmei, Harsh Sharma, Arya Jena, Kaushal Singh, Jayashree Piri, Raghunath Dey
**Affiliation:** School of Computer Engineering, Kalinga Institute of Industrial Technology (KIIT), Bhubaneswar, Odisha, India

---

## Overview

IoT intrusion-detection models are almost always validated on a single dataset, where they report scores in the high 0.90s. Those numbers rarely survive a change of environment — different capture tools, different devices, different attack toolkits. The benchmark looked easy because it was a closed world.

This work makes two connected contributions.

**BRIDGE** (Benchmark Reference for IoT Domain Generalisation Evaluation) is a heterogeneous multi-dataset benchmark for IoT intrusion detection. It unifies **four independently audited datasets drawn from three structurally distinct feature-extraction toolchains** under a single 46-feature canonical vocabulary, with genuine-equivalence-only feature mapping, explicit zero-filling for absent features, and full per-dataset coverage disclosure (30%–91%). It ships with a documented **dataset-quality audit** (candidates with broken or label-leaking schemas are rejected, with reasons published), a leakage-verification suite, and a **leave-one-dataset-out (LODO)** protocol paired with a **diagnosis-and-repair methodology** applied identically to every model.

The central, deliberately honest finding: under LODO, naive zero-shot transfer collapses to a mean **F1 = 0.1788**. Unsupervised test-time BatchNorm adaptation recovers it to **0.5231**, and small-sample threshold calibration to **0.6275**. But the repair is **conditional** — on 6 of 12 seed–fold runs it genuinely restores detection (mean 0.6513), while on the other 6 the "recovered" score is just an all-attack classifier wearing a calibrated threshold (0.6037 against a trivial 0.6028). Under identical repair, **no evaluated architecture — ours included — sits more than ~0.06 above that trivial predictor.** The take-away is measurement-first: for cross-dataset transfer, normalisation and thresholding matter an order of magnitude more than the choice of architecture.

**TCH-Net v2** is a gated two-branch neural baseline for BRIDGE — a Temporal branch and a Statistical branch, fused by Cross-Branch Gated Attention Fusion (CB-GAF) with per-expert deep supervision and held-out gate recalibration. It is offered as a **characterised reference baseline, not a leaderboard winner** (the strongest transformer baseline stays ahead in-distribution, and a standalone statistical MLP beats the fused model in-distribution under an equal budget — both reported openly).

---

## Results

### Main comparison, in-distribution (TCH-Net: 5 seeds; baselines: 3 seeds)

| Model | F1 | ROC-AUC | MCC |
|-------|-----|---------|-----|
| Transformer-IDS | **0.8938 ± 0.0017** | **0.9747** | **0.8121** |
| **TCH-Net v2 (Ours)** | 0.8834 ± 0.0029 | 0.9685 | 0.7953 |
| BiLSTM-IDS | 0.8536 ± 0.0034 | 0.9551 | 0.7372 |
| BiGRU-IDS | 0.8518 ± 0.0052 | 0.9528 | 0.7351 |
| CNN-LSTM | 0.8424 ± 0.0019 | 0.9441 | 0.7190 |
| 1D-CNN-IDS | 0.8401 ± 0.0013 | 0.9434 | 0.7145 |
| DeepDefense | 0.8171 ± 0.0004 | 0.9275 | 0.6698 |
| GraphSAGE-Approx | 0.7885 ± 0.0010 | 0.9094 | 0.6136 |
| XGBoost | 0.7869 ± 0.0018 | 0.9146 | 0.6420 |
| Kitsune-AE | 0.7710 ± 0.0105 | 0.8897 | 0.5780 |
| IoT-DNN | 0.7549 ± 0.0004 | 0.8699 | 0.5499 |
| MLP-IDS | 0.7473 ± 0.0004 | 0.8621 | 0.5408 |
| Random Forest | 0.6404 ± 0.0019 | 0.8686 | 0.5128 |

TCH-Net v2 beats 11 of 12 baselines in raw F1 (9 significant after Bonferroni correction). It does **not** beat the strongest transformer in-distribution (−0.0105, not significant after correction). This is reported, not hidden — the value of the model is the characterised, honestly ablated design and its role as the BRIDGE reference baseline, not an in-distribution win.

### BRIDGE LODO generalisation (calibrated head-to-head)

Every repair stage (test-time BN adaptation + disjoint-slice threshold calibration) is applied **identically to every model**. Trivial all-attack predictor = 0.6028.

| Model | CICIDS | BCCC | CICIoMT | UNSW | Mean |
|-------|--------|------|---------|------|------|
| Transformer-IDS | **0.6971** | **0.7347** | 0.6016 | **0.6191** | **0.6631** |
| 1D-CNN-IDS | 0.6662 | 0.7331 | **0.6252** | 0.6100 | 0.6586 |
| CNN-LSTM | 0.6172 | 0.6968 | 0.5978 | 0.6036 | 0.6289 |
| BiGRU-IDS | 0.6060 | 0.6933 | 0.5967 | 0.6172 | 0.6283 |
| MLP-IDS | 0.6012 | 0.7036 | 0.6014 | 0.6046 | 0.6277 |
| **TCH-Net v2 (Ours)** | 0.6654 | 0.6147 | 0.6121 | 0.6179 | 0.6275 |
| H-branch only (control) | 0.6575 | 0.6138 | 0.5992 | 0.6034 | 0.6185 |

All six full models land inside a 0.036 band, within +0.016 to +0.060 of the trivial predictor. **No architecture dominates cross-extractor transfer.** The stage decomposition: +0.344 mean F1 from unsupervised BN adaptation, +0.104 from threshold calibration — both larger than the entire spread between architectures.

**The repair is conditional (read per seed–fold, not as a mean):**

| Regime | Runs | Post-adaptation AUC | Calibrated F1 | vs. trivial (0.6028) |
|--------|------|--------------------|--------------|----------------------|
| Ranking restored | 6/12 | 0.7198 | 0.6513 | +0.0485 |
| Ranking inverted | 6/12 | 0.4478 | 0.6037 | +0.0009 (i.e. trivial) |

Calibrated generalisation gap (in-distribution − calibrated LODO): **0.8834 − 0.6275 = +0.2559.** Cross-extractor transfer is repaired where adaptation restores the ranking, and remains unsolved where it does not.

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

After sliding-window construction (W=32, S=4, majority-vote label), the balance shifts to ~57:43 benign:attack. Training sequences: 129,536 (43.1% attack). Test sequences: 32,362 (42.7% attack).

### The 46 canonical features

| Group | Category | Indices | Count |
|-------|----------|---------|-------|
| 1 | Flow rates, durations, pkt/byte counts | 0–16 | 17 |
| 2 | Packet size & IAT statistics | 17–37 | 21 |
| 3 | TCP flag indicators | 38–43 | 6 |
| 4 | Header length & window size | 44–45 | 2 |

Full alias-mapping tables (per dataset, with rejected mappings and reasons) are provided in this repository.

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

**~2.386M trainable parameters.** Single-sample inference latency: **8.902 ms** on NVIDIA Tesla T4.

---

## Ablations (equal budget, single architecture, 3 seeds; every row retrained)

### Branch ablation

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| T + H (Full) | 0.8840 | — |
| T only | 0.8827 | −0.0013 |
| **H only** | **0.9017** | **+0.0177** |

The strongest in-distribution model of the study is the standalone Statistical branch (an MLP over window-mean features, <0.2M params). This is reported openly and explained: windowed flow records carry little genuine temporal structure, and the shared trunk costs the internal H expert ~0.020 F1 via gradient interference. Under LODO, however, the same standalone H-branch is the **worst** transfer performer (0.6185) — the temporal capacity that costs F1 in-distribution earns it back cross-domain.

### Novelty-component ablation (positive ΔF1 = removing it helps)

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| Full model | 0.8840 | — |
| w/o MSTE (multi-scale temporal) | 0.8681 | −0.0159 |
| w/o CB-GAF (→ plain concat) | 0.8842 | +0.0002 |
| w/o Aux loss | 0.8821 | −0.0020 |
| w/o CORAL | 0.8835 | −0.0005 |
| w/o all (≈ v1 core) | 0.8691 | −0.0150 |

The one unambiguously positive component is **MSTE**. CB-GAF is in-distribution-neutral by F1; its justification is the verified fusion properties below, not raw score.

### Gate recalibration (seed-42 model; all rows calibrated on the same 20% slice, F1 on disjoint 80%)

| Predictor | Eval F1 |
|-----------|---------|
| T expert (inside full model) | 0.8872 |
| H expert (inside full model) | 0.8819 |
| Full model, learned gate | 0.8874 |
| Full model, recalibrated (α*=0.70) | **0.8927** |

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
| Max epochs / patience | 30 / 7 |
| Window size / stride | 32 / 4 |
| Dropout | 0.20 |
| Augmentation | Gaussian noise (σ=0.01, p=0.30, train only) |
| Hardware | NVIDIA Tesla T4 (Kaggle) |

Seeds: TCH-Net 5 seeds {42, 123, 456, 789, 2024}; baselines and ablations 3 seeds {42, 123, 456}; LODO 3 seeds per fold with bootstrap CIs.

---

## Computational Efficiency (NVIDIA Tesla T4)

| Model | Params (M) | Latency (ms) | F1 |
|-------|-----------|-------------|-----|
| **TCH-Net v2 (Ours)** | 2.386 | 8.902 | 0.8834 |
| Transformer-IDS | 0.618 | 1.786 | 0.8938 |
| BiLSTM-IDS | 0.609 | 1.995 | 0.8536 |
| BiGRU-IDS | 0.465 | 1.175 | 0.8518 |
| CNN-LSTM | 0.142 | 1.199 | 0.8424 |
| 1D-CNN-IDS | 0.068 | 0.943 | 0.8401 |
| MLP-IDS | 0.920 | 0.640 | 0.7473 |

---

## Repository Structure

<!-- PLACEHOLDER: replace with your actual v2 files. Only you know the real
     notebook/checkpoint/data filenames. Do NOT ship the old five-dataset
     BRIDGE.csv or the three-branch checkpoints — they contradict this paper. -->

```
TCH-Net/
├── data/                     # BRIDGE unified benchmark (4 datasets) + alias tables
├── audit/                    # dataset-quality audit docs + rejection reasons
├── vocabulary/               # 46-feature canonical vocabulary spec + per-dataset maps
├── notebooks/                # experimental notebook(s): baselines, ablations,
│                             #   LODO + diagnosis-and-repair (TTBN + calibration)
├── checkpoints/              # TCH-Net v2 weights (5 seeds) + RobustScaler + manifest
└── README.md
```

> The submitted manuscript's Data Availability statement promises: the canonical
> vocabulary spec, alias-mapping tables, dataset-audit documentation, preprocessing
> pipeline, **calibration methodology**, and complete experimental code. Make sure
> each of these is actually present and current before a reviewer looks.

---

## Quickstart

```bash
pip install torch numpy pandas scikit-learn tqdm
```

Open the experimental notebook (GPU recommended), point the dataset paths at the four
BRIDGE sources (all publicly available on Kaggle), and run all cells. Checkpoints and
the fitted `RobustScaler` save automatically. Inference requires the saved scaler:
raw features are scaled and clipped to [−10, 10] before windowing.

<!-- If you keep pretrained checkpoints on Hugging Face, add the load snippet here.
     Ensure any HF model/dataset mirror hosts the v2 (four-dataset, two-branch)
     artifacts — not the old ones. -->

---

## Limitations

- **Residual cross-dataset gap.** Even after both repair stages, a genuine +0.2559 F1 gap remains, and on half the seed–fold runs the repaired model does not measurably beat the all-attack predictor. Normalisation and threshold placement are recovered; transferable signal that was never learned is not manufactured.
- **In-distribution position.** Transformer-IDS stays ahead of TCH-Net in-distribution (+0.0105, not significant after correction) and leads the calibrated LODO head-to-head. TCH-Net is a characterised baseline, not the leaderboard winner.
- **Testbed data.** All four datasets are controlled-testbed or aggregated research captures; two (CICIDS-2017, UNSW-NB15) are enterprise rather than IoT-specific, retained as vocabulary/extractor-family anchors.
- **Binary scope.** Evaluated as a binary detector; multi-class attack typing is future work.
- **Edge deployment.** Memory/throughput on edge hardware were not measured; distillation, pruning, and INT8 quantisation are the obvious compression routes.

---

## Citation

<!-- Update once a DOI is issued. The current arXiv preprint is an EARLIER version
     with different results; cite it only if you post a matching version. -->

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
