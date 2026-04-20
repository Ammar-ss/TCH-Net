# BRIDGE and TCH-Net

**Heterogeneous Benchmark and Multi-Branch Baseline for Cross-Domain IoT Botnet Detection**

[![arXiv](https://img.shields.io/badge/arXiv-2604.11324-b31b1b.svg)](https://arxiv.org/abs/2604.11324)
[![HF Model](https://img.shields.io/badge/🤗%20Model-Ammar--ss/BRIDGE__and__TCH--Net-yellow)](https://huggingface.co/Ammar-ss/BRIDGE_and_TCH-Net)
[![HF Dataset](https://img.shields.io/badge/🤗%20Dataset-Ammar--ss/BRIDGE-blue)](https://huggingface.co/datasets/Ammar-ss/BRIDGE)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

> Submitted to *Journal of Network and Computer Applications*

**Authors:** Ammar Bhilwarawala, Likhamba Rongmei, Harsh Sharma, Arya Jena, Kaushal Singh, Jayashree Piri, Raghunath Dey  
**Affiliation:** School of Computer Engineering, KIIT University, Bhubaneswar, India

---

## Overview

The IoT botnet detection field has a quiet problem that's been building for years. Almost every published system trains on one dataset, reports numbers in the high 90s, and treats that as evidence of a solved problem. But models trained in one environment fall apart when you point them at a different one — different capture tools, different devices, different attack toolkits. The benchmark looked easy because it was a closed world.

This paper makes two contributions toward fixing that.

**BRIDGE** (Benchmark Reference for IoT Domain Generalisation Evaluation) is the first formally specified heterogeneous multi-dataset benchmark for IoT intrusion detection. It unifies five structurally distinct public datasets through a 46-feature semantic canonical vocabulary, with genuine-equivalence-only feature mapping, explicit zero-filling for absent features, and full coverage disclosure for every dataset. The leave-one-dataset-out (LODO) evaluation protocol establishes, for the first time with a formally reproducible methodology, just how large the cross-dataset generalisation gap is: all five evaluated deep learning architectures achieve LODO F1 between 0.39–0.47, and TCH-Net achieves the highest at 0.5577 — the first formally quantified community generalisation baseline in heterogeneous IoT intrusion detection.

**TCH-Net** is a multi-branch neural architecture proposed as a strong and well-characterised baseline for BRIDGE. It integrates three parallel branches — a three-path Temporal branch with residual convolutional-BiGRU, stride-downsampled BiGRU, and full-resolution pre-LayerNorm Transformer; a provenance-conditioned Contextual branch; and an aggregate Statistical branch — fused via Cross-Branch Gated Attention Fusion (CB-GAF) with learnable per-branch sigmoid vector gates. Evaluated across five independent seeds on BRIDGE, TCH-Net achieves **F1 = 0.8296 ± 0.0028**, **AUC = 0.9380 ± 0.0025**, and **MCC = 0.6972 ± 0.0056**, outperforming all 12 baseline models with statistical significance (p < 0.05).

---

## Results

### Main Comparison (5 seeds: 42, 123, 456, 789, 2024)

| Model | F1 | ROC-AUC | MCC | PR-AUC |
|-------|-----|---------|-----|--------|
| **TCH-Net (Ours)** | **0.8296 ± 0.0028** | **0.9380** | **0.6972** | **0.8912** |
| Transformer-IDS | 0.7958 ± 0.0030 | 0.9147 | 0.6255 | 0.8699 |
| 1D-CNN-IDS | 0.7932 ± 0.0076 | 0.9076 | 0.6213 | 0.8601 |
| CNN-LSTM | 0.7919 ± 0.0137 | 0.9056 | 0.6208 | 0.8578 |
| BiLSTM-IDS | 0.7805 ± 0.0010 | 0.8975 | 0.5972 | 0.8441 |
| BiGRU-IDS | 0.7805 ± 0.0011 | 0.8962 | 0.5987 | 0.8438 |
| DeepDefense | 0.7627 ± 0.0011 | 0.8776 | 0.5638 | 0.8192 |
| XGBoost | 0.7265 ± 0.0014 | 0.8704 | 0.5542 | 0.7989 |
| GraphSAGE-Approx | 0.7097 ± 0.0004 | 0.8259 | 0.4465 | 0.7403 |
| Kitsune-AE | 0.7045 ± 0.0007 | 0.8200 | 0.4362 | 0.7348 |
| MLP-IDS | 0.7039 ± 0.0008 | 0.8152 | 0.4348 | 0.7311 |
| IoT-DNN | 0.7009 ± 0.0002 | 0.8146 | 0.4278 | 0.7286 |
| Random Forest | 0.4323 ± 0.0082 | 0.8005 | 0.3557 | 0.6214 |

### BRIDGE LODO Generalisation Benchmark

| Held-Out Dataset | TCH-Net LODO F1 | Best Baseline LODO F1 |
|-----------------|----------------|----------------------|
| CICIDS-2017 | 0.3128 | 0.19 (BiGRU-IDS) |
| CIC-IoT-2023 | 0.6013 | 0.47 (CNN-LSTM) |
| Bot-IoT | 0.5934 | 0.50 (CNN-LSTM) |
| Edge-IIoTset | 0.6791 | 0.56 (CNN-LSTM) |
| N-BaIoT | 0.6021 | 0.47 (BiGRU-IDS) |
| **Mean** | **0.5577** | **0.4297** |

Generalisation gap (in-distribution vs LODO): **+0.2719**. This is not a TCH-Net failure — all architectures show the same structural gap. The 0.5577 LODO mean is the first formally specified community baseline for cross-dataset IoT intrusion detection.

---

## Repository Structure

```
TCH-Net/
│
├── BRIDGE.csv                              # Unified 549 MB benchmark dataset
│
├── BRIDGE and TCH-Net (FULL PAPER).ipynb  # Complete experimental notebook
│                                           # All 12 baselines, branch ablation,
│                                           # novelty ablation, LODO, temporal split,
│                                           # adversarial robustness, HP sensitivity
│
├── bridge-and-tch-net.ipynb               # Clean training-only notebook
│                                           # TCH-Net, 5 seeds, saves checkpoints
│
├── checkpoints/
│   ├── tch_net_best.pth                   # Best checkpoint (highest F1)
│   ├── tch_net_seed_42.pth
│   ├── tch_net_seed_123.pth
│   ├── tch_net_seed_456.pth
│   ├── tch_net_seed_789.pth
│   ├── tch_net_seed_2024.pth
│   ├── scaler.pkl                         # RobustScaler — required for inference
│   └── manifest.json                      # Config, metrics, feature names
│
└── README.md
```

---

## BRIDGE Dataset

### What it is

BRIDGE maps five publicly available IoT network security datasets into a single shared 46-feature canonical vocabulary based on CICFlowMeter nomenclature. Features that don't exist in a given dataset are zero-filled explicitly — nothing is fabricated, and coverage is fully disclosed.

### Source Datasets

| Dataset | Capture Tool | Year | Coverage | Role | Official | Kaggle |
|---------|-------------|------|----------|------|----------|--------|
| CICIDS-2017 | CICFlowMeter | 2017 | 93% (43/46) | Primary | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) | [Kaggle](https://www.kaggle.com/datasets/dhoogla/cicids2017) |
| CIC-IoT-2023 | CICFlowMeter | 2023 | 87% (40/46) | Primary | [UNB CIC](https://www.unb.ca/cic/datasets/iotdataset-2023.html) | [Kaggle](https://www.kaggle.com/datasets/raqeeb24/ciciot-2023-stratified-dataset) |
| Bot-IoT | Argus | 2019 | 39% (18/46) | Primary | [UNSW](https://research.unsw.edu.au/projects/bot-iot-dataset) | [Kaggle](https://www.kaggle.com/datasets/vigneshvenkateswaran/bot-iot-5-data) |
| Edge-IIoTset | Wireshark | 2022 | 22% (10/46) | Supplementary | [IEEE DataPort](https://ieee-dataport.org/documents/edge-iiotset-new-comprehensive-realistic-cyber-security-dataset-iot-and-iiot-applications) | [Kaggle](https://www.kaggle.com/datasets/mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot) |
| N-BaIoT | Kitsune | 2018 | 15% (7/46) | Supplementary | [UCI](https://archive.ics.uci.edu/ml/datasets/detection_of_IoT_botnet_attacks_N_BaIoT) | [Kaggle](https://www.kaggle.com/datasets/mkashifn/nbaiot-dataset) |

### Post-Balancing Record Counts

| Dataset | Benign | Attack | Total | Atk% |
|---------|--------|--------|-------|------|
| CICIDS-2017 | 19,321 | 14,350 | 33,671 | 42.6% |
| CIC-IoT-2023 | 3,964 | 3,001 | 6,965 | 43.1% |
| Bot-IoT | 22 | 16 | 38 | 42.1% |
| Edge-IIoTset | 30,951 | 23,435 | 54,386 | 43.1% |
| N-BaIoT | 13,557 | 10,055 | 23,612 | 42.6% |
| **Combined** | **67,815** | **50,857** | **118,672** | **42.9%** |

### The 46 Canonical Features

| Group | Category | Indices | Count |
|-------|----------|---------|-------|
| 1 | Flow rates, durations, pkt/byte counts | 0–16 | 17 |
| 2 | Packet size & IAT statistics | 17–37 | 21 |
| 3 | TCP flag indicators | 38–43 | 6 |
| 4 | Header length & window size | 44–45 | 2 |

Full feature list: `flow_duration`, `pkt_count_fwd`, `pkt_count_bwd`, `byte_count_fwd`, `byte_count_bwd`, `pkt_rate`, `byte_rate`, `fwd_pkt_rate`, `bwd_pkt_rate`, `fwd_byte_rate`, `bwd_byte_rate`, `pkt_count_total`, `byte_count_total`, `fwd_pkt_len_total`, `bwd_pkt_len_total`, `subflow_fwd_pkts`, `subflow_bwd_pkts`, `pkt_len_min`, `pkt_len_max`, `pkt_len_mean`, `pkt_len_std`, `pkt_len_var`, `fwd_pkt_len_min`, `fwd_pkt_len_max`, `fwd_pkt_len_mean`, `fwd_pkt_len_std`, `bwd_pkt_len_min`, `bwd_pkt_len_max`, `bwd_pkt_len_mean`, `bwd_pkt_len_std`, `iat_mean`, `iat_std`, `iat_max`, `iat_min`, `fwd_iat_mean`, `fwd_iat_std`, `bwd_iat_mean`, `bwd_iat_std`, `flag_syn`, `flag_ack`, `flag_fin`, `flag_rst`, `flag_psh`, `flag_urg`, `fwd_header_len`, `init_win_fwd`

### Loading the Data

```python
import pandas as pd

df = pd.read_csv("BRIDGE.csv")
# Columns: 46 canonical features + 'label' (0=benign, 1=attack)
#          + 'dataset_source' (which of the 5 datasets each row came from)
```

Or via Hugging Face:

```python
from datasets import load_dataset
dataset = load_dataset("Ammar-ss/BRIDGE")
```

---

## TCH-Net Architecture

Three branches process a (B, 32, 46) sequence window in parallel, fused through CB-GAF.

```
Input: (B, 32, 46)  — batch × 32-step window × 46 canonical features

Shared Feature Projection (residual):
  Linear(46→92) → LayerNorm → GELU → Dropout
  → Linear(92→46) → LayerNorm    [X̃ = X + f_proj(X)]

T-Branch (Temporal) — 512d:
  Path 1: ResConvSE×3 + MaxPool → BiGRU(128/dir, 2L)         → 8×256
  Path 2: StrideConv(s=2) → BiGRU(64/dir, 1L) → AvgPool(8)   → 8×128
  Path 3: Linear(46→128) + LearnablePE
           → TransformerEncoder(Pre-LN, 2L, 8H) → AvgPool(8)  → 8×128
  Merge:  concat → LayerNorm(512) → MHA(8H) → mean pool        → 512d

H-Branch (Statistical) — 64d:
  mean(X̃, time) → MLP(46→128→64, BN+GELU+Dropout)             → 64d

C-Branch (Contextual) — 64d:
  Embed_dataset(5,32) ‖ Embed_device(6,32)                      → 64d

CB-GAF (Cross-Branch Gated Attention Fusion):
  Each branch → Linear projection → 128d
  Each branch queries both others via cross-attention
  Per-branch vector gate g^i ∈ (0,1)^128 (feature-wise, not scalar)
  x_fused = g^i ⊙ x_self + (1 − g^i) ⊙ x_cross
  concat(T, C, H fused) → LayerNorm                             → 384d

Classifier (residual head):
  raw_proj(mean X̃) → 64d
  concat(384d, 64d) → Linear(448→256) → Linear(256→128) + skip
  → Linear(128→2) → softmax

Aux Decoder (training only, λ=0.05):
  MLP(384→64→46) — prevents information collapse in CB-GAF
```

**2,692,696 trainable parameters.** Single-sample inference latency: **6.43 ± 0.18ms** on NVIDIA Tesla T4.

---

## Quickstart

### Requirements

```bash
pip install torch numpy pandas scikit-learn huggingface_hub tqdm
```

### Training TCH-Net from scratch

Open `bridge-and-tch-net.ipynb` on Kaggle (GPU recommended). Update the dataset paths in Cell 3:

```python
class Config:
    CICIDS_PATH  = "/kaggle/input/datasets/dhoogla/cicids2017"
    CICIOT_PATH  = "/kaggle/input/datasets/raqeeb24/ciciot-2023-stratified-dataset"
    BOTIOT_PATH  = "/kaggle/input/datasets/vigneshvenkateswaran/bot-iot-5-data"
    EDGE_PATH    = "/kaggle/input/datasets/mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot"
    NBAIOT_PATH  = "/kaggle/input/datasets/mkashifn/nbaiot-dataset"
```

Run all cells. Checkpoints save automatically to `tch_net_results/checkpoints/`.

### Running inference with a pretrained checkpoint

```python
import torch
import pickle
import numpy as np
import torch.nn.functional as F
from huggingface_hub import hf_hub_download

# Download pretrained weights and scaler
ckpt_path   = hf_hub_download("Ammar-ss/BRIDGE_and_TCH-Net", "tch_net_best.pth")
scaler_path = hf_hub_download("Ammar-ss/BRIDGE_and_TCH-Net", "scaler.pkl")

# Load scaler
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)

# Load checkpoint
ckpt   = torch.load(ckpt_path, map_location='cpu')
config = ckpt['config']

# Instantiate model (copy TCHNet class from bridge-and-tch-net.ipynb)
model = TCHNet(
    nf=config['n_features'],   # 46
    ws=config['window_size'],  # 32
    nc=config['n_classes'],    # 2
)
model.load_state_dict(ckpt['state_dict'])
model.eval()

# Preprocess: scale raw features
# X_raw: np.ndarray of shape (N, 46)
X_scaled = np.clip(scaler.transform(X_raw), -10, 10).astype(np.float32)

# Inference
# x:   FloatTensor (B, 32, 46)  — sliding window sequences
# ctx: LongTensor  (B, 2)       — [dataset_source_id, device_category_id]
#
# dataset_source_id:  0=CICIDS-2017  1=CIC-IoT-2023  2=Bot-IoT
#                     3=Edge-IIoTset  4=N-BaIoT
# device_category_id: 0=sensor  1=camera  2=appliance  3=IIoT  4=server  5=unknown
#
# If unknown, pass ctx = torch.zeros(B, 2, dtype=torch.long)
# (contextual branch has no independent predictive power — degrades gracefully)

with torch.no_grad():
    logits, _ = model(x, ctx)
    probs = F.softmax(logits, dim=-1)
    preds = logits.argmax(dim=-1)  # 0=benign, 1=attack
```

---

## Ablation Results

### Branch Ablation (2 seeds, CB-GAF replaced with concat)

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| **T+C+H Full** | **0.8296** | — |
| T+H | 0.7756 | −0.054 |
| T+C | 0.7752 | −0.054 |
| T only | 0.7753 | −0.054 |
| H only | 0.7054 | −0.124 |
| C+H | 0.7061 | −0.124 |
| C only | 0.6000 | −0.230 |

C-branch alone = near-random (AUC ≈ 0.50). Its role is fusion conditioning, not independent prediction.

### Novelty Component Ablation (2 seeds)

| Variant | F1 | ΔF1 |
|---------|-----|-----|
| **Full TCH-Net** | **0.8296** | — |
| w/o CB-GAF | 0.7759 | −0.054 |
| w/o MSTE (Three-Path) | 0.7760 | −0.054 |
| w/o Aux Loss | 0.7755 | −0.054 |
| w/o All (v2) | 0.7752 | −0.054 |

Removing any single novel component costs ~0.054 F1.

---

## Training Configuration

| Hyperparameter | Value |
|---------------|-------|
| Optimizer | AdamW |
| Learning rate | 5×10⁻⁴ |
| Weight decay | 5×10⁻⁵ |
| Scheduler | Cosine annealing, 2-epoch warmup |
| Loss | Focal (γ=2.0, α-weighted, ε=0.05) + Aux (λ=0.05) |
| Batch size | 512 |
| Max epochs / patience | 30 / 5 |
| Window size / stride | 32 / 4 |
| Max train sequences | 800,000 |
| Max test sequences | 200,000 |
| Dropout | 0.15 |
| Augmentation | Gaussian noise (σ=0.01, p=0.30, train only) |
| AMP | fp16 on CUDA |
| Hardware | NVIDIA Tesla T4 (Kaggle) |

---

## Computational Efficiency (NVIDIA Tesla T4)

| Model | Params | Latency | Throughput | Memory | F1 |
|-------|--------|---------|-----------|--------|-----|
| **TCH-Net** | 2.692M | 6.43±0.18ms | 20.5k sps | 10.27MB | **0.8296** |
| Transformer-IDS | 0.618M | 1.22±0.03ms | 36.8k sps | 2.36MB | 0.7958 |
| BiLSTM-IDS | 0.609M | 0.74±0.02ms | 34.2k sps | 2.32MB | 0.7805 |
| 1D-CNN-IDS | 0.068M | 0.69±0.03ms | 406.9k sps | 0.26MB | 0.7932 |
| CNN-LSTM | 0.142M | 0.88±0.05ms | 273.5k sps | 0.54MB | 0.7919 |

---

## Limitations

**Cross-dataset generalisation.** The LODO mean F1 of 0.5577 confirms TCH-Net doesn't generalise robustly to entirely unseen network environments in its current form. This isn't a TCH-Net-specific failure — all 12 evaluated baselines show the same structural gap. Deployment in a new environment requires fine-tuning on local traffic or domain adaptation components not present in the current architecture.

**Testbed data.** All five source datasets were collected in controlled environments, not live operational networks.

**Binary classification only.** TCH-Net is evaluated as a binary detector (benign vs. attack). Multi-class attack type identification is a natural extension not covered here.

**Edge deployment.** The 10.27MB footprint and 6.43ms latency are fine for NVIDIA Jetson hardware. For microcontroller-class endpoints (Cortex-M, ESP32), quantisation or knowledge distillation would be needed.

---

## Citation

If you use BRIDGE, TCH-Net, or the canonical vocabulary in your work, please cite:

```bibtex
@article{bhilwarawala2026bridge,
  title   = {{BRIDGE} and {TCH-Net}: Heterogeneous Benchmark and Multi-Branch
             Baseline for Cross-Domain {IoT} Botnet Detection},
  author  = {Bhilwarawala, Ammar and Rongmei, Likhamba and Sharma, Harsh
             and Jena, Arya and Singh, Kaushal and Piri, Jayashree and Dey, Raghunath},
  journal = {arXiv preprint arXiv:2604.11324},
  year    = {2026}
}
```

---

## License

This repository is released under the [Apache 2.0 License](LICENSE).

The five source datasets (CICIDS-2017, CIC-IoT-2023, Bot-IoT, Edge-IIoTset, N-BaIoT) are subject to their own respective licenses. Please consult each dataset's original source before commercial or derivative use.

---

## Acknowledgements

We thank the creators of CICIDS-2017, CIC-IoT-2023, Bot-IoT, Edge-IIoTset, and N-BaIoT for making their datasets publicly available. Experiments were conducted on Kaggle with NVIDIA Tesla T4 GPU instances.
