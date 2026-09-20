# C3-ABM: Generative Probe for "Two Timescales, Two Calibers"

Companion simulation and analysis code for the manuscript:

> **"Two Timescales, Two Calibers: Auditing Consumer Adaptation in Algorithmically Mediated Environments"**
> by Dan Lu, Hongwei Liu, Xiuli Yu, and Dongdong Shi
> Manuscript information-4549232, revised version V9.59k, under review at *Information* (MDPI).

## What this repository contains

A minimal two-timescale slow-memory agent-based model used as a **generative
sufficiency probe** (Section 7 of the manuscript), plus the frozen analysis
code behind the revised Study 1 matched-estimand results.

The probe asks a narrow computational question: whether one explicitly
specified slow-memory process is generatively sufficient to reproduce
**selected qualitative signatures of the archived split-half analysis**.
It is an existence proof, not an estimator, and it is **not** a replication
or validation of the revised matched-estimand REWB CDI.

## Headline simulation results (agent world, N = 25,467, seed 7)

Under the archived split-half (2 × 2) protocol:

| Condition | ρ (within-person) | r (between-person) | archived contrast |
|---|---|---|---|
| baseline (slow memory on) | −0.545 | — | — |
| dynamic anchor (retraining loop) | −0.344 | — | — |
| ideal (slow channel removed) | +0.159 | — | — |
| random (lower anchor) | +0.174 | — | — |

Ten independent replications of the reference world reproduce both signs
(ρ = −0.154, r = +0.251, archived split-half contrast = +0.405).

## Empirical-correspondence boundary (Section 7.4)

Under the within–between (REWB) panel decomposition of Study 1, the baseline
world produces statistically indistinguishable between- and within-consumer
components (βB = −4.87, βW = −4.90; simulated between-minus-within contrast
+0.03, n.s., against the empirical +0.5174), while the dynamic-anchor regime
produces a much more negative simulated between-minus-within contrast (−3.21).
**The simulation does not reproduce the revised REWB CDI (+0.5174).** This
mismatch is reported in the manuscript as a falsification boundary, not as a
failure to be repaired by retuning.

## Revised Study 1 primary results (frozen; see results CSVs)

- REWB panel: N = 60,423 consumers, 242,771 consumer-wave observations
- βB = −2.9957 (SE 0.0194); βW = −3.5132 (SE 0.0110)
- CDI = βB − βW = +0.5174 (SE 0.0210; Wald χ²(1) = 609.61)
- Consumer-cluster bootstrap (B = 2,000), BCa 95% CI [0.4757, 0.5573]
- Standardized companion CDI* = 0.1132, BCa 95% CI [0.1041, 0.1219]
- Portability audit: relative wave-position adjustment reverses the caliber
  ordering (D2: CDI = −0.8077); brand-HHI representation nearly eliminates
  the separation (CDI = 0.0565 [−0.0039, 0.1171])

## Repository layout

| File | Role |
|---|---|
| `c3_abm.py` | Agent-based simulation (Section 7; Algorithm 1 in Appendix B.7) |
| `ODD_protocol.md` | ODD protocol for the agent world |
| `multinomial_check.py` | Monte Carlo check of the multinomial choice draw |
| `sensitivity_v98.csv` | Disclosed 3 × 3 sensitivity grid outputs |
| `bootstrap_cdi.py` | Consumer-cluster bootstrap (B = 2,000) for CDI / BCa intervals |
| `sim_rewb_boundary.py` | REWB-protocol boundary check behind Section 7.4 |
| `results_study1_rewb.csv` | Frozen Study 1 estimates (REWB, audit grid D2–D4, HHI) |
| `results_study2_study3.csv` | Frozen Study 2 / Study 3 estimates |
| `simA_summary.csv` | Simulation recalculation summary (2026-09-12 frozen run) |
| `requirements.txt` | Python dependencies |
| `.github/workflows/smoke-test.yml` | CI smoke test |

## Reproducibility tiers

1. **Generative probe (fully reproducible from public code):** `c3_abm.py`
   and `sim_rewb_boundary.py` run the agent world standalone; all simulation
   outputs in the manuscript (Section 7, Figures B1–B4, `simA_summary.csv`)
   can be regenerated without any restricted data.
2. **Restricted-data Studies 1 and 3 (computational transparency):** the
   exact analysis scripts, frozen result tables, and model specifications are
   supplied, but the JDsearch- and JData-derived panels are **not
   redistributed** under data-use agreements. `bootstrap_cdi.py` documents the
   exact consumer-cluster bootstrap implementation (B = 2,000, seed 20260915)
   behind the reported BCa intervals; its input `track1_panel.csv` is derived
   from restricted JDsearch data, and authorized users should update the
   local `PANEL`/`OUT_DIR` paths before running.
3. **Amazon Study 2 (public source data):** the Amazon Reviews 2023 dataset
   is publicly available from its original source; frozen result tables and
   processing specifications are provided in `results_study2_study3.csv`.

*Legacy field notice:* `simA_summary.csv` is a byte-frozen artifact of the
2026-09-12 recalculation run; its `CDI_old` column is a deprecated legacy
field denoting the archived split-half operationalization contrast Δop,
**not a CDI** under the revised matched-estimand definition.

## Environment

- Python ≥ 3.9; see `requirements.txt`
- Runtime: ~3 min per full replication (N = 25,467) on a commodity core

## Data availability

The raw JDsearch and JData behavioral data were obtained under data-use
agreements and **cannot be redistributed**. The Amazon Reviews 2023 dataset
is publicly available from its original source. Accordingly, this repository
supports computational transparency but does **not** by itself provide
unrestricted independent reproduction of the primary raw-data estimates;
primary-study analysis scripts and user-level aggregate tables are available
from the corresponding author upon reasonable request, subject to those
agreements.
