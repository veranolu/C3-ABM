This repository corresponds to manuscript V9.39 (2026-08-23) under review at MDPI Information.

# C3-ABM: Fossil-Anchor Simulation for the Dual-Caliber Blind Spot

Companion agent-based model to the manuscript:

> **"Beyond Algorithmic Accuracy: Dual-Caliber Analytics and Preference Resilience in Consumer Adaptation"**  
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
