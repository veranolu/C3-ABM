# -*- coding: utf-8 -*-
"""
S5 validation: independent Poisson(x*n) vs exact multinomial(n, x) sampler.
Paper claim (Section 2.9, assumption S5): Poisson is moment-equivalent to
multinomial sampling. This script verifies the equivalence directly.

Part 1 (moment check): 100 replications, K=100 categories, n=30 draws;
  compare induced HHI and Shannon entropy moments.
Part 2 (slope check): mini-world runs (N=2000, T=100, K=100, baseline
  condition) under both samplers, 10 seeds; compare within-person rho.
"""
import numpy as np
from scipy.stats import spearmanr

def moments_check(R=100, K=100, n=30, seed=20260822):
    rng = np.random.default_rng(seed)
    out = {k: [] for k in ('hhi_p', 'hhi_m', 'ent_p', 'ent_m')}
    for _ in range(R):
        x = rng.dirichlet(np.full(K, 0.5))
        cP = rng.poisson(x * n).astype(float)
        cM = rng.multinomial(n, x).astype(float)
        for c, hk, ek in ((cP, 'hhi_p', 'ent_p'), (cM, 'hhi_m', 'ent_m')):
            cf = c / c.sum() if c.sum() > 0 else np.full(K, 1.0 / K)
            out[hk].append((cf ** 2).sum())
            out[ek].append(-(np.where(cf > 1e-12, cf * np.log(np.where(cf > 1e-12, cf, 1)), 0)).sum(0) if cf.ndim else 0)
    return {k: np.array(v) for k, v in out.items()}

def run_world(N=2000, T=100, K=100, delta=0.003, lam_g=0.05, sig_tau=0.5,
              base_sess=3.0, q_susc=0.30, r_hi=0.85, r_lo=0.25, seed=7,
              sampler='poisson'):
    rng = np.random.default_rng(seed)
    tau = rng.lognormal(0, sig_tau, N); tau /= tau.mean()
    s = np.where(rng.random(N) < q_susc, r_hi, r_lo)
    th = rng.dirichlet(np.full(K, 0.5), N)
    z = np.zeros((N, K)); top = np.argsort(-th, axis=1)[:, :3]
    np.put_along_axis(z, top, 1.0, axis=1); z = 0.8 * z / z.sum(1, keepdims=True) + 0.2 / K
    w = np.zeros(N); half = T // 2
    C1 = np.zeros((N, K)); C2 = np.zeros((N, K))
    for t in range(T):
        shock = rng.random(N) < lam_g
        if shock.any():
            th[shock] = 0.6 * th[shock] + 0.4 * rng.dirichlet(np.full(K, 0.5), shock.sum())
        x = (1 - w[:, None]) * th + w[:, None] * z; x /= x.sum(1, keepdims=True)
        n = rng.poisson(base_sess * tau)
        if sampler == 'poisson':
            c = rng.poisson(x * n[:, None]).astype(float)
        else:
            c = np.zeros((N, K))
            for i in np.where(n > 0)[0]:
                c[i] = rng.multinomial(n[i], x[i])
        w = np.minimum(w + delta * n * s * (1 + w), 0.95)
        if t < half: C1 += c
        else: C2 += c
    sh = lambda C: C / np.where(C.sum(1, keepdims=True) == 0, 1, C.sum(1, keepdims=True))
    ent = lambda cf: -(np.where(cf > 1e-12, cf * np.log(np.where(cf > 1e-12, cf, 1)), 0)).sum(1)
    cf1, cf2 = sh(C1), sh(C2)
    return spearmanr((cf1 ** 2).sum(1), ent(cf2) - ent(cf1)).statistic

if __name__ == '__main__':
    m = moments_check()
    dH = abs(m['hhi_p'].mean() - m['hhi_m'].mean()); seH = (m['hhi_p'] - m['hhi_m']).std() / np.sqrt(len(m['hhi_p']))
    dE = abs(m['ent_p'].mean() - m['ent_m'].mean()); seE = (m['ent_p'] - m['ent_m']).std() / np.sqrt(len(m['ent_p']))
    print(f'Part 1 (R=100, K=100, n=30):')
    print(f'  mean HHI    : Poisson {m["hhi_p"].mean():.6f} vs Multinomial {m["hhi_m"].mean():.6f}  |diff| = {dH:.2e} (MC se {seH:.2e})')
    print(f'  mean entropy: Poisson {m["ent_p"].mean():.6f} vs Multinomial {m["ent_m"].mean():.6f}  |diff| = {dE:.2e} (MC se {seE:.2e})')
    seeds = [3, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    rp = [run_world(seed=s, sampler='poisson') for s in seeds]
    rm = [run_world(seed=s, sampler='multinomial') for s in seeds]
    d = np.abs(np.array(rp) - np.array(rm))
    print(f'Part 2 (N=2000, T=100, K=100, 10 seeds):')
    print(f'  rho Poisson     : {np.round(rp, 4)}')
    print(f'  rho Multinomial : {np.round(rm, 4)}')
    print(f'  mean |d rho| = {d.mean():.4f}, max |d rho| = {d.max():.4f} (single-rho MC se ~ {1/np.sqrt(2000):.4f})')
