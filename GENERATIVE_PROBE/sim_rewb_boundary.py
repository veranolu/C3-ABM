# -*- coding: utf-8 -*-
# sim_rewb_boundary.py -- Simulation A: re-estimation under the revised caliber (panel REWB), v2 memory-optimized
# CHANGELOG:
#   v1 2026-09-12 adapted from c3_abm.py with windowed panel -> killed OOM at 2GB
#   v2 2026-09-12 memory optimization: theta deleted right after init; x*n uses float32 in-place multiply (out= reuses x)
#     avoids a 204MB float64 temporary; the rng call sequence is identical to the reference version (per-window settlement does not change the stream);
#     lowering lam from f64 to f32 is the only implementation difference -> headline may differ at the +-0.001 level
#   v3 2026-09-19 (GitHub release as sim_rewb_boundary.py) LABEL CLEANUP ONLY:
#     legacy split-half printout "CDI=" renamed to "delta_op=" and JSON key
#     "CDI_old" renamed to "delta_op_legacy". This legacy split-half quantity is
#     NOT the CDI under the revised matched-estimand definition (that estimand is
#     reported as CDI_v2_sim). No formula, parameter, seed, or numerical result
#     was changed; all printed/computed values are bit-identical to v2.
# Caliber: 10 windows x 10 periods; maxshare = within-window max behavior share; entropy = within-window Shannon entropy; n_click = within-window total choices
# Estimation: Mundlak OLS entropy ~ mean_maxshare + dev, clustered by uid; CDI_v2_sim = bB - bW
import sys, time, json
import numpy as np
from scipy.stats import spearmanr, pearsonr

T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)

def run_model_panel(N=25467, T=100, K=1000, delta=0.003, lam_g=0.05,
                    sig_tau=0.5, base_sess=3.0, q_susc=0.30, r_hi=0.85, r_lo=0.25,
                    seed=7, cond='baseline', win_len=10):
    rng = np.random.default_rng(seed)
    tau = rng.lognormal(0, sig_tau, N); tau /= tau.mean()
    s = np.where(rng.random(N) < q_susc, r_hi, r_lo)
    theta = rng.dirichlet(np.full(K, 0.5), N)
    z = np.zeros((N, K), dtype=np.float32)
    top = np.argsort(-theta, axis=1)[:, :3]
    th32 = theta.astype(np.float32)
    del theta                                    # v2: delete immediately, saves 204MB
    np.put_along_axis(z, top, 1.0, axis=1)
    del top
    z = 0.8 * z / z.sum(1, keepdims=True) + 0.2 / K
    z = z.astype(np.float32)
    w = np.zeros(N, dtype=np.float32)
    half = T // 2
    n_win = T // win_len
    pw_maxshare = np.zeros((N, n_win), dtype=np.float32)
    pw_entropy  = np.zeros((N, n_win), dtype=np.float32)
    C1 = np.zeros((N, K), dtype=np.float32); C2 = np.zeros((N, K), dtype=np.float32)
    Cw = np.zeros((N, K), dtype=np.float32)
    x = np.empty((N, K), dtype=np.float32)       # v2: persistent reuse
    tot = np.zeros(N); tot_early = np.zeros(N)
    for t in range(T):
        shock = rng.random(N) < lam_g
        if shock.any():
            th32[shock] = (0.6 * th32[shock] + 0.4 * rng.dirichlet(np.full(K, 0.5), shock.sum()).astype(np.float32))
        if cond == 'random':
            x[:] = np.float32(1.0 / K)
        else:
            np.multiply(th32, (1 - w)[:, None], out=x)
            x += w[:, None] * z
            x /= x.sum(1, keepdims=True)
        n = rng.poisson(base_sess * tau)
        tot += n
        if t < half: tot_early += n
        n32 = n.astype(np.float32)
        np.multiply(x, n32[:, None], out=x)      # v2: f32 in-place, no f64 temporary
        c = rng.poisson(x).astype(np.float32)    # one-off int64 temporary
        if cond in ('baseline', 'dynamic'):
            w = np.minimum(w + delta * n * s * (1 + w), 0.95)
        if cond == 'dynamic':
            f = c.sum(1, keepdims=True); cf = np.where(f > 0, c / np.where(f == 0, 1, f), 0)
            z = 0.98 * z + 0.02 * cf.astype(np.float32); z /= z.sum(1, keepdims=True)
        if t < half: C1 += c
        else: C2 += c
        Cw += c
        if (t + 1) % win_len == 0:
            wi = (t + 1) // win_len - 1
            # v2: chunked window statistics, avoiding another N x K temporary
            for a in range(0, N, 6000):
                b = min(a + 6000, N)
                Cb = Cw[a:b]; cs = Cb.sum(1, keepdims=True)
                cf = Cb / np.where(cs == 0, 1, cs)
                pw_maxshare[a:b, wi] = cf.max(1)
                pw_entropy[a:b, wi] = -(np.where(cf > 1e-12, cf * np.log(np.where(cf > 1e-12, cf, 1)), 0)).sum(1)
            Cw[:] = 0
        if (t + 1) % 25 == 0:
            log(f"  cond={cond} t={t+1}/100 w_mean={w.mean():.3f}")
    def shares(C): return C / np.where(C.sum(1, keepdims=True) == 0, 1, C.sum(1, keepdims=True))
    cf1, cf2 = shares(C1), shares(C2)
    del C1, C2
    HHI1 = (cf1 ** 2).sum(1)
    def ent(cf): return -(np.where(cf > 1e-12, cf * np.log(np.where(cf > 1e-12, cf, 1)), 0)).sum(1)
    e1, e2 = ent(cf1), ent(cf2)
    growth = e2 - e1; level = (e1 + e2) / 2
    rho_within = spearmanr(HHI1, growth).statistic
    r_between = pearsonr(np.log(tot + 1), level).statistic
    ms_early = cf1.max(1)
    x2 = {'loyW': spearmanr(ms_early, growth).statistic,
          'actB': spearmanr(tot_early, e1).statistic,
          'actW': spearmanr(tot_early, growth).statistic,
          'loyB': spearmanr(ms_early, e1).statistic}
    del cf1, cf2, x, z, th32
    return rho_within, r_between, pw_maxshare, pw_entropy, x2

def rewb(pw_maxshare, pw_entropy, tag):
    import statsmodels.api as sm
    N, W = pw_maxshare.shape
    uid = np.repeat(np.arange(N), W)
    ms = pw_maxshare.reshape(-1); en = pw_entropy.reshape(-1)
    mean_ms = pw_maxshare.mean(1)
    mm = np.repeat(mean_ms, W); dev = ms - mm
    X = sm.add_constant(np.column_stack([mm, dev]))
    m = sm.OLS(en, X).fit(cov_type='cluster', cov_kwds={'groups': uid})
    bB, bW = m.params[1], m.params[2]
    cov = m.cov_params()
    se_cdi = np.sqrt(cov[1, 1] + cov[2, 2] - 2 * cov[1, 2])
    cdi = bB - bW
    wt = m.wald_test(np.array([[0, 1, -1]]), scalar=True)
    log(f"{tag}: beta_B={bB:+.4f}({m.bse[1]:.4f}) beta_W={bW:+.4f}({m.bse[2]:.4f}) CDI_v2_sim={cdi:+.4f}(se={se_cdi:.4f}) Wald={float(wt.statistic):.2f} N={N} obs={N*W}")
    return {'beta_B': float(bB), 'se_B': float(m.bse[1]), 'beta_W': float(bW), 'se_W': float(m.bse[2]),
            'CDI_v2_sim': float(cdi), 'se_cdi': float(se_cdi), 'Wald': float(wt.statistic), 'p': float(wt.pvalue)}

if __name__ == '__main__':
    quick = '--quick' in sys.argv
    conds = ['baseline'] if '--baseonly' in sys.argv else ['baseline', 'dynamic', 'ideal', 'random']
    N = 5000 if quick else 25467
    out = {}
    for cond in conds:
        log(f"=== cond={cond} N={N} seed=7 ===")
        rw, rb, pms, pen, x2 = run_model_panel(N=N, cond=cond)
        log(f"headline(legacy split-half): rho_within={rw:+.3f} r_between={rb:+.3f} delta_op={rb-rw:+.3f}  [legacy split-half diagnostic, NOT CDI under the revised matched-estimand definition; frozen -0.148/+0.266/+0.415 @N=25467]")
        log(f"2x2 trial: loyW={x2['loyW']:+.4f} actB={x2['actB']:+.4f} actW={x2['actW']:+.4f} loyB={x2['loyB']:+.4f} CDI_xsec_sim(actB-loyB)={x2['actB']-x2['loyB']:+.4f}")
        r = rewb(pms, pen, cond)
        r.update({'rho_within_old': float(rw), 'r_between_old': float(rb), 'delta_op_legacy': float(rb - rw), 'x2': x2, 'N': N})
        out[cond] = r
        with open('simA_results.json', 'w') as f:
            json.dump(out, f, indent=1)
    log("saved simA_results.json")
