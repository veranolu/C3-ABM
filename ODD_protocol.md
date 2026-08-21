# ODD Protocol Description of C3-ABM

Model description follows the ODD (Overview, Design concepts, Details)
protocol for describing individual- and agent-based models
(Grimm et al. 2006, 2010, 2020).

## 1. Purpose and patterns

**Purpose.** To test whether the manuscript's two-timescale engine — a fast
channel of session-level recommendation gains plus a slow channel of
exposure-accumulated consolidation around the recommended repertoire — is
sufficient to generate the paper's central empirical pattern: the same
exposure–concentration association carries opposite signs at the
between-person and within-person levels (the dual-caliber reversal), with
Caliber Divergence Index CDI = 0.417.

**Patterns used as evaluation criteria** (pattern-oriented modeling):
- P1: within-person Spearman ρ between first-half concentration (HHI) and
  second-half diversity growth ≈ −0.130 (sign mandatory, magnitude target).
- P2: between-person Pearson r between log cumulative engagement and
  observed diversity level ≈ +0.287.
- P3: CDI = r − ρ ≈ +0.417.
- P4 (counterfactual): removing the slow channel eliminates the
  within-person negative sign.

## 2. Entities, state variables, and scales

| Entity | State variables |
|---|---|
| Consumer i (N = 25,467) | genuine taste θ_i,t (K-simplex); fossil anchor z_i; consolidation weight w_i,t ∈ [0, 0.95]; activity trait τ_i (lognormal, time-invariant); susceptibility class s_i ∈ {r_lo, r_hi} |
| Environment | K = 1,000 categories; no explicit recommender agent — the anchor z_i represents the recommended repertoire the slow channel consolidates around |

Time: discrete sessions, T = 100 (matching the manuscript's computational
calibration). Half-window split at T/2 mirrors Study 1's measurement design.

## 3. Process overview and scheduling

Each session t, in fixed order:
1. **Genuine taste shock**: each consumer with probability λ_g has θ reset
   toward a fresh draw (60% retention) — genuine preference change.
2. **Choice generation**: expressed profile x_i,t = (1−w_i,t)·θ_i,t + w_i,t·z_i;
   session count n_i,t ~ Poisson(base·τ_i); category counts
   c_i,t ~ Poisson(x_i,t · n_i,t) (multinomial-equivalent in moments).
3. **Slow channel (consolidation)**: w_i,t+1 = min(w + δ·n_i,t·s_i·(1+w), 0.95)
   — exposure-accumulated, self-reinforcing, susceptibility-weighted.
4. **Measurement**: first/second-half count aggregates C1, C2.

## 4. Design concepts

- **Basic principles**: the manuscript's Eq. (1) two-timescale
  exploration–exploitation engine; fossilization as the slow-channel endpoint.
- **Emergence**: the dual-caliber sign reversal (P1–P3) is NOT imposed — it
  emerges from the interaction of heterogeneous activity traits,
  susceptibility classes, and the self-reinforcing consolidation loop.
  Counterfactual removal of the loop (w ≡ 0) removes the reversal (P4).
- **Adaptation / Learning**: consumers do not optimize; the only adaptive
  element is path-dependent consolidation (behavior affects future behavior).
- **Sensing**: implicit — consolidation is anchored to each consumer's own
  early top categories (the recommended repertoire).
- **Interaction**: none between consumers (diagnostic of a measurement
  phenomenon, not of social influence); indirect coupling to the
  recommender is compressed into z_i and the w-dynamics.
- **Stochasticity**: activity traits, susceptibility classes, taste shocks,
  session counts, and category draws are all stochastic.
- **Collectives**: susceptibility classes (share q_susc = 0.30) are imposed
  population structure, not emergent.
- **Observation**: HHI of first-half shares; Shannon entropy of half shares;
  diversity growth = ent2 − ent1; engagement = Σ n_i,t.

## 5. Initialization

θ_i ~ Dirichlet(0.5·1_K); z_i concentrated on i's initial top-3 categories
(80%) + uniform noise (20%); w_i,0 = 0; τ_i ~ LogNormal(0, 0.5), mean-one
normalized; s_i = r_hi with probability q_susc else r_lo.

## 6. Input data

No external input data. Calibration anchors are taken from the manuscript's
frozen results: N = 25,467; T = 100; δ ∈ [0.0025, 0.008]; λ_g ∈ [0.04, 0.07].
Free parameters (q_susc, r_hi, r_lo, base, σ_τ, K) were calibrated to
patterns P1–P2 within those frozen bounds and are reported in full.

## 7. Submodels

All processes are specified in Sections 3–5 and implemented in `c3_abm.py`
(single file, fully commented). No further submodels.

## Pseudocode

```
initialize consumers: theta, z, tau, s, w=0
for t = 1..T:
    for each consumer i (vectorized):
        with prob lambda_g: theta_i <- 0.6*theta_i + 0.4*Dirichlet(0.5)
        x_i <- normalize((1-w_i)*theta_i + w_i*z_i)        # expressed profile
        n_i ~ Poisson(base * tau_i)                        # engagement
        c_i ~ Poisson(x_i * n_i)                           # choices (fast channel)
        if slow channel ON:                                # counterfactual: OFF
            w_i <- min(w_i + delta * n_i * s_i * (1 + w_i), 0.95)
        accumulate c_i into C1 (t <= T/2) or C2 (t > T/2)
measure:
    HHI1_i  = HHI(shares(C1_i))
    growth_i = Entropy(shares(C2_i)) - Entropy(shares(C1_i))
    level_i  = (Entropy(shares(C1_i)) + Entropy(shares(C2_i))) / 2
    E_i = sum_t n_i,t
report:
    rho_within = Spearman(HHI1, growth)          # pattern P1
    r_between  = Pearson(log E, level)           # pattern P2
    CDI        = r_between - rho_within          # pattern P3
```

## Evaluation summary (TRACE-style)

| Test | Result |
|---|---|
| Condition anchors (N = 25,467) | baseline −0.148/+0.266; dynamic −0.095/+0.625; ideal +0.109/+0.986; random +0.172/+0.990 ✓ |
| Pattern P1 (within ρ ≈ −0.130) | −0.148 (N = 25,467) ✓ |
| Pattern P2 (between r ≈ +0.287) | +0.266 ✓ |
| Pattern P3 (CDI ≈ 0.417) | +0.415 ✓ |
| Pattern P4 (counterfactual removes reversal) | ρ → +0.109 ✓ |
| Seed stability (11/23/42) | CDI ∈ [0.407, 0.420] ✓ |
| Sensitivity λ_g ∈ {0.04, 0.07} | flip persists ✓ |
| Sensitivity δ = 0.0025 | flip persists (ρ = −0.052) ✓ |
| Boundary δ = 0.008 | flip collapses — reported as boundary condition |
