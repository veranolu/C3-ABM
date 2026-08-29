This repository corresponds to manuscript V9.39 (2026-08-23) under review at MDPI Information.

# C3-ABM: Fossil-Anchor Simulation for the Dual-Caliber Blind Spot

![Smoke Test](https://github.com/veranolu/C3-ABM/actions/workflows/smoke-test.yml/badge.svg)

Companion agent-based model to the manuscript:

> **"Beyond Algorithmic Accuracy: Dual-Caliber Analytics and Preference Resilience in Consumer Adaptation"**
> by Dan Lu, Hongwei Liu, Xiuli Yu, and Dongdong Shi  
> Manuscript V9.39 (2026-08-23), under review at *Information* (MDPI).

> by Dan Lu, Hongwei Liu, Xiuli Yu, and Dongdong Shi  
> Manuscript V9.39 (2026-08-23), under review at *Information* (MDPI).

## What it shows

One mechanism — a two-timescale engine with an exposure-accumulated
"consolidation" (fossil-anchor) slow channel — simultaneously generates:

| Quantity | Empirical (Study 1) | Simulation (N = 25,467, seed 7) |
|---|---|---|
| Within-person: baseline concentration → later diversity growth (Spearman ρ) | −0.130 | −0.148 |
| Between-person: engagement ↔ observed diversity (Pearson r) | +0.287 | +0.266 |
| **CDI = r_between − ρ_within** | **0.417** | **+0.415** |

**Counterfactual** (slow channel removed, w ≡ 0): the within-person
association flips to +0.109 — the sign reversal, and hence the dual-caliber
blind spot, disappears.

## Four experimental conditions (v2, Chaney-style anchors)

All at N = 25,467, seed 7:

| Condition | ρ_within | r_between | CDI |
|---|---|---|---|
| baseline (fossil anchor) | −0.148 | +0.266 | +0.415 |
| dynamic anchor (retraining loop) | −0.095 | +0.625 | +0.720 |
| ideal (slow channel removed) | +0.109 | +0.986 | +0.876 |
| random (lower anchor) | +0.172 | +0.990 | +0.818 |

The within-person consolidation signature appears only when the slow
channel is ON — an existence proof for the dual-caliber blind spot.

## Robustness

- Seeds 11/23/42 (N = 8,000): within = −0.166 / −0.177 / −0.152;
  between = +0.254 / +0.238 / +0.255; CDI ∈ [0.407, 0.420]. Sign flip stable.
- λ_g ∈ {0.04, 0.07} (frozen range endpoints): flip persists.
- δ = 0.0025 (frozen lower bound): flip persists (within = −0.052).
- δ = 0.008 (frozen upper bound): flip collapses (r_between turns negative)
  — an identified boundary condition: when consolidation is too strong it
  dominates the cross-sectional richness channel, so the between-person
  veneer disappears.

## Algorithm Overview

The simulation implements a minimal two-timescale mechanism that generates the dual-caliber blind spot.  
For readers who prefer pseudocode to Python, the logic of one replication is:

```text
Algorithm 1: Fossil-Agent Simulation (One Replication)

Input:  N = 25,467 consumers, T = 100 sessions, K = 1,000 categories
Output: within-person ρ, between-person r, CDI = r − ρ

Initialize for each consumer i:
    τ_i  ← LogNormal(0, 0.5²) normalized to mean 1       // activity trait
    s_i  ← 0.85 with prob 0.30, else 0.25                // susceptibility class
    θ_i  ← Dirichlet(0.5 · 1_K)                         // genuine taste
    z_i  ← 0.8·(top-3 of θ_i) + 0.2/K                   // fossil anchor
    w_i  ← 0                                            // consolidation weight

For each session t = 1 … 100:
    1. Taste shock (with prob λ_g = 0.05):
       θ_i ← 0.6·θ_i + 0.4·Dirichlet(0.5·1_K)
    2. Expressed profile:
       x_i ← (1 − w_i)·θ_i + w_i·z_i, renormalized
    3. Engagement & choice:
       n_i ~ Poisson(3·τ_i)
       c_i ~ Poisson(x_i · n_i)          // moment-equivalent to multinomial
    4. Consolidate:
       w_i ← min(w_i + δ·n_i·s_i·(1 + w_i), 0.95)
    5. Dynamic-anchor condition only:
       z_i ← 0.98·z_i + 0.02·(c_i / Σc_i)
    6. Accumulate counts into first-half (t ≤ 50) or second-half (t &gt; 50) bins

After session 100:
    ρ ← Spearman(first-half HHI, second-half entropy growth)
    r ← Pearson(log cumulative engagement, mean entropy)
    CDI ← r − ρ

Control conditions:
    Ideal:   skip step 4 (w ≡ 0)
    Random:  set x_i = 1/K in step 2

## Files

- `c3_abm.py` — the full model, runnable as-is (`python c3_abm.py`).
- `ODD_protocol.md` — model description following the ODD protocol
  (Grimm et al. 2006, 2010, 2020).
- `validation_report.docx` — calibration, counterfactual, and sensitivity
  results (Chinese).

## Requirements

Python 3.10+, `numpy`, `scipy`. No other dependencies.
Runtime ≈ 2–4 min for the full N = 25,467 baseline + counterfactual.

## License

MIT (code). Please cite the manuscript when using this model.


## V9.8 sensitivity & verification update (2026-08-21)

All new results reproducible via `run_sensitivity_v98b.py` / `run_final.py` / `run_heldout_v98.py`
(raw rows: `sensitivity_v98.csv`, 46 rows).

**Main condition, 10 seeds (N = 25,467; seeds 3, 7, 11, 13, 17, 19, 23, 29, 31, 37):**
- rho_within = -0.154 (95% CI [-0.159, -0.149]); every seed negative
- r_between  = +0.251 (95% CI [+0.245, +0.257]); every seed positive
- CDI        = +0.405 (95% CI [+0.401, +0.408])
- Seed-7 replication check: -0.1484 / +0.2663 -> matches the frozen headline (-0.148 / +0.266)

**Factorial grid share x delta (N = 3,000, seeds 3/7/11):**
- reversal survives in 4/9 cells; CDI positive in 8/9 (range +0.030 to +0.486)
- boundary: share=20% with mild delta (<=0.003) no reversal (susceptible-population floor);
  delta=0.008 collapses the between-person association in all three rows

**K sweep (N = 3,000, seeds 3/7/11):** K=100: CDI +0.096 (attenuated);
K=1,000: +0.415; K=10,000: +0.413 (identical within noise)

**Held-out checks (baseline world, N = 25,467, seed 7; moments never used in calibration):**
- maxshare-based within-person rho = -0.545 vs empirical -0.130 (sign correct, ~4x overshoot)
- activity-quartile gradient +0.279 / -0.286 / -0.431 / -0.596 (Q1-Q4) vs empirical
  -0.075 / -0.122 / -0.146 / -0.151 (monotone ordering matches; weakest-quartile sign missed)
- tercile ordering preserved (low-consolidation consumers lose less diversity), levels shifted down
- reading: qualitative corroboration of ordering/gradient, NOT distributional replication

## Citation
Lu, D., Liu, H., Yu, X., & Shi, D. Beyond Algorithmic Accuracy: Dual-Caliber Analytics and Preference Resilience in Consumer Adaptation. *Information* (under review).
