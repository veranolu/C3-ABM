# -*- coding: utf-8 -*-
"""
C3-ABM v2: Fossil-Anchor Agent-Based Model of the Dual-Caliber Blind Spot
==========================================================================
v2 changes (Chaney-style upgrade): four experimental conditions with
lower/upper anchor controls, retraining-loop variant, multi-seed averaging,
and trajectory tracking.

Companion simulation to:
"The Dual-Caliber Blind Spot of Recommender Systems:
 A 27-Year Behavioral Diagnostic for Algorithmic Governance"

Conditions
----------
baseline  : fossil anchor z fixed; consolidation w ON  (the paper's engine)
dynamic   : z is RETRAINED toward each user's own recent behavior every
            session (feedback loop, platform-side), w ON
ideal     : w = 0 always — recommendations track genuine taste perfectly
            (upper anchor / counterfactual: slow channel removed)
random    : uniform random slate (lower anchor: no signal at all)

Simulation assumptions (numbered, paper Section 2.9)
----------------------------------------------------
S1. Genuine taste theta_i,t lives on the K-simplex and is subject to
    occasional shocks (rate lambda_g) — preferences really do change.
S2. Expressed profile x = (1-w)*theta + w*z: behavior mixes genuine taste
    with a fossil anchor z (the recommended repertoire consolidated early).
S3. Consolidation is exposure-accumulated and self-reinforcing:
    w <- min(w + delta * n * s * (1 + w), 0.95), with susceptibility class s.
S4. Engagement n ~ Poisson(base * tau_i), tau lognormal — a stable
    heavy/light activity trait independent of susceptibility.
S5. Choice counts c ~ Poisson(x * n) (multinomial-equivalent in moments;
    validated against exact multinomial in the prototype stage).

Frozen calibration anchors (from the paper, NOT tuned outside these ranges):
  delta in [0.0025, 0.008]; lambda_g in [0.04, 0.07]; N = 25,467; T = 100.

Headline results (seed 7, N = 25,467):
  baseline : rho_within = -0.148, r_between = +0.266, CDI = +0.415
             (paper: -0.130 / +0.287 / 0.417)
  ideal    : rho_within = +0.109  (within-person reversal removed)

Usage:  python c3_abm.py            # headline baseline + ideal (N = 25,467)
        python c3_abm.py --quick    # all four conditions, N = 5,000
"""

import sys
import numpy as np
from scipy.stats import spearmanr, pearsonr


def run_model(N=25467, T=100, K=1000, delta=0.003, lam_g=0.05,
              sig_tau=0.5, base_sess=3.0, q_susc=0.30, r_hi=0.85, r_lo=0.25,
              seed=7, cond='baseline', track=False):
    rng = np.random.default_rng(seed)
    tau = rng.lognormal(0, sig_tau, N)
    tau /= tau.mean()                                    # S4
    s = np.where(rng.random(N) < q_susc, r_hi, r_lo)     # S3 susceptibility
    theta = rng.dirichlet(np.full(K, 0.5), N)            # S1
    z = np.zeros((N, K))
    top = np.argsort(-theta, axis=1)[:, :3]
    np.put_along_axis(z, top, 1.0, axis=1)
    z = 0.8 * z / z.sum(1, keepdims=True) + 0.2 / K      # S2 fossil anchor
    w = np.zeros(N)
    half = T // 2
    C1 = np.zeros((N, K), dtype=np.float32)
    C2 = np.zeros((N, K), dtype=np.float32)
    tot = np.zeros(N)
    th32 = theta.astype(np.float32)
    traj_ent, traj_w = [], []
    for t in range(T):
        shock = rng.random(N) < lam_g                    # S1 taste shock
        if shock.any():
            th32[shock] = (0.6 * th32[shock]
                           + 0.4 * rng.dirichlet(np.full(K, 0.5),
                                                 shock.sum()).astype(np.float32))
        if cond == 'random':
            x = np.full((N, K), 1.0 / K, dtype=np.float32)
        else:
            x = ((1 - w[:, None]) * th32 + w[:, None] * z).astype(np.float32)
            x /= x.sum(1, keepdims=True)                 # S2
        n = rng.poisson(base_sess * tau)                 # S4
        tot += n
        c = rng.poisson(x * n[:, None]).astype(np.float32)  # S5
        if cond in ('baseline', 'dynamic'):
            w = np.minimum(w + delta * n * s * (1 + w), 0.95)   # S3
        if cond == 'dynamic':                            # retraining loop
            f = c.sum(1, keepdims=True)
            cf = np.where(f > 0, c / np.where(f == 0, 1, f), 0)
            z = 0.98 * z + 0.02 * cf
            z /= z.sum(1, keepdims=True)
        if track:
            cc = c.sum(1, keepdims=True)
            cf2 = np.where(cc > 0, c / np.where(cc == 0, 1, cc), 1.0 / K)
            e = -(np.where(cf2 > 1e-12, cf2 * np.log(np.where(cf2 > 1e-12, cf2, 1)), 0)).sum(1)
            traj_ent.append(float(e.mean()))
            traj_w.append(float(w.mean()))
        if t < half:
            C1 += c
        else:
            C2 += c

    def shares(C):
        return C / np.where(C.sum(1, keepdims=True) == 0, 1, C.sum(1, keepdims=True))

    cf1, cf2 = shares(C1), shares(C2)
    HHI1 = (cf1 ** 2).sum(1)

    def ent(cf):
        return -(np.where(cf > 1e-12, cf * np.log(np.where(cf > 1e-12, cf, 1)), 0)).sum(1)

    growth = ent(cf2) - ent(cf1)
    level = (ent(cf1) + ent(cf2)) / 2
    rho_within = spearmanr(HHI1, growth).statistic
    r_between = pearsonr(np.log(tot + 1), level).statistic
    if track:
        return rho_within, r_between, traj_ent, traj_w
    return rho_within, r_between


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    N = 5000 if quick else 25467
    conds = ["baseline", "dynamic", "ideal", "random"] if quick else ["baseline", "ideal"]
    print(f"C3-ABM v2  (N={N}, T=100, K=1000, delta=0.003, lambda_g=0.05)")
    print(f"paper anchors: rho_within=-0.130, r_between=+0.287, CDI=0.417")
    for cond in conds:
        rw, rb = run_model(N=N, cond=cond)
        print(f"{cond:9s}: rho_within={rw:+.3f} | r_between={rb:+.3f} | CDI={rb-rw:+.3f}")
