# -*- coding: utf-8 -*-
"""
C3 / CDI 2.0 - G Task 1 (+ Task 2 CI): consumer cluster bootstrap, B=2000
-------------------------------------------------------------------------
Input : C:\\chelsea\\paperC_s1s3\\cdi_v2\\track1_panel.csv  (frozen: 242,771 obs / 60,423 users)
Output: C:\\chelsea\\paperC_s1s3\\cdi_v2\\cdi_bootstrap_2000.csv   (per-replicate detail)
        C:\\chelsea\\paperC_s1s3\\cdi_v2\\task1_report.json        (summary for G)

Design notes
------------
1. Pairs cluster bootstrap: resample CONSUMERS with replacement; each drawn consumer
   keeps their full wave history (mean_maxshare / dev per user unchanged).
2. Speed: per-user sufficient statistics + closed-form 3x3 OLS solve -> 2000 refits
   vectorized (no per-replicate statsmodels). Expected runtime: a few minutes.
3. Dual-path verification (statistics double-check rule):
   a) closed-form refit on the ORIGINAL sample must equal statsmodels OLS+cluster refit;
   b) closed-form point estimates must equal the 2026-09-08 frozen values (tol 1e-8);
   c) 3 random bootstrap replicates are refit with full statsmodels (expanded sample,
      fresh cluster ids) and must match the closed-form results (tol 1e-10).
4. BCa acceleration via vectorized leave-one-user-out jackknife (same sufficient stats).
5. Standardized CDI uses the common reference multiplier s_X/s_Y from the full frozen
   panel (Task 0 values), applied per replicate: CDI_std_b = CDI_b * (s_X/s_Y).

Seed: 20260915 (PCG64). All console output ASCII (GBK-safe).
"""
import json
import sys
import time

import numpy as np
import pandas as pd
from scipy import stats as sps
import statsmodels.api as sm

OUT_DIR = r"C:\chelsea\paperC_s1s3\cdi_v2"
PANEL = OUT_DIR + r"\track1_panel.csv"
BOOT_CSV = OUT_DIR + r"\cdi_bootstrap_2000.csv"
REPORT = OUT_DIR + r"\task1_report.json"

B = 2000
SEED = 20260915
SPOT_REPS = [7, 999, 1999]          # replicates spot-checked with full statsmodels
FROZEN = {"beta_B": -2.9957316191056362,
          "beta_W": -3.513151488094991,
          "CDI": 0.5174198689893545}
TASK0_CDI_STD = 0.11319907179394316  # from task0_report.json (crosscheck only)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
t0 = time.time()
print("[task1] loading frozen panel ...")

# ---------------- load & per-user sufficient statistics ----------------
df = pd.read_csv(PANEL)
df["_dev"] = df["maxshare"] - df["mean_maxshare"]
df["_dev2"] = df["_dev"] ** 2
df["_de"] = df["_dev"] * df["entropy"]

g = df.groupby("uid", sort=True)                     # users contiguous after groupby
n = g.size().to_numpy(float)                         # waves per user
m = g["mean_maxshare"].first().to_numpy(float)       # between component
d = g["_dev"].sum().to_numpy(float)                  # ~0 (kept general)
q = g["_dev2"].sum().to_numpy(float)                 # sum dev^2
E = g["entropy"].sum().to_numpy(float)               # sum y
C = g["_de"].sum().to_numpy(float)                   # sum dev*y
U = len(n)
N_obs = int(n.sum())
print("[task1] users=%d  obs=%d" % (U, N_obs))

# S_mat columns: [n, n*m, d, n*m^2, m*d, q, E, m*E, C]
S_mat = np.column_stack([n, n * m, d, n * m * m, m * d, q, E, m * E, C])
T = S_mat.sum(axis=0)


def solve3(S):
    """Closed-form OLS for y ~ 1 + m + dev from aggregated sufficient stats."""
    XtX = np.array([[S[0], S[1], S[2]],
                    [S[1], S[3], S[4]],
                    [S[2], S[4], S[5]]])
    Xty = np.array([S[6], S[7], S[8]])
    return np.linalg.solve(XtX, Xty)                 # [b0, bB, bW]


# ---------------- dual-path verification on original sample ----------------
beta_cf = solve3(T)
X_all = np.column_stack([np.ones(N_obs),
                         df["mean_maxshare"].to_numpy(),
                         df["_dev"].to_numpy()])
y_all = df["entropy"].to_numpy()
uid_arr = df["uid"].to_numpy()
fit0 = sm.OLS(y_all, X_all).fit(cov_type="cluster",
                                cov_kwds={"groups": uid_arr})
diff_sm = np.max(np.abs(fit0.params - beta_cf))
selfcheck_sm = bool(diff_sm < 1e-10)
diff_frozen = {k: abs(float(v) - FROZEN[k]) for k, v in
               zip(["beta_B", "beta_W", "CDI"],
                   [beta_cf[1], beta_cf[2], beta_cf[1] - beta_cf[2]])}
selfcheck_frozen = bool(max(diff_frozen.values()) < 1e-8)
print("[task1] selfcheck vs statsmodels: max|diff|=%.3e -> %s"
      % (diff_sm, "PASS" if selfcheck_sm else "FAIL"))
print("[task1] selfcheck vs frozen 9/8 : max|diff|=%.3e -> %s"
      % (max(diff_frozen.values()), "PASS" if selfcheck_frozen else "FAIL"))
if not (selfcheck_sm and selfcheck_frozen):
    print("[task1] ABORT: self-check failed, no bootstrap run.")
    sys.exit(2)

# standardized multiplier (common reference = full frozen panel)
sX = float(df["maxshare"].std())
sY = float(df["entropy"].std())
mult = sX / sY
cdi_std_point = (beta_cf[1] - beta_cf[2]) * mult
cdi_std_crosscheck = bool(abs(cdi_std_point - TASK0_CDI_STD) < 1e-6)
print("[task1] s_X=%.7f s_Y=%.7f mult=%.7f CDI_std=%.6f crosscheck=%s"
      % (sX, sY, mult, cdi_std_point,
         "PASS" if cdi_std_crosscheck else "FAIL"))

# ---------------- bootstrap B=2000 ----------------
print("[task1] bootstrap B=%d seed=%d ..." % (B, SEED))
rng = np.random.default_rng(np.random.PCG64(SEED))
boot = np.empty((B, 3))
spot_idx = {}
for b in range(B):
    idx = rng.integers(0, U, U)
    if b in SPOT_REPS:
        spot_idx[b] = idx.copy()
    cnt = np.bincount(idx, minlength=U)
    boot[b, :] = solve3(cnt @ S_mat)
    if (b + 1) % 500 == 0:
        print("[task1]   ... %d/%d done (%.1fs)" % (b + 1, B, time.time() - t0))

cdi_boot = boot[:, 1] - boot[:, 2]

# ---------------- spot-check: full statsmodels refit on 3 replicates ----------------
# users are contiguous in the grouped (uid-sorted) frame -> expand by offsets
df_sorted = df.sort_values("uid", kind="stable").reset_index(drop=True)
Xs = np.column_stack([np.ones(N_obs),
                      df_sorted["mean_maxshare"].to_numpy(),
                      (df_sorted["maxshare"] - df_sorted["mean_maxshare"]).to_numpy()])
ys = df_sorted["entropy"].to_numpy()
starts = np.concatenate([[0], np.cumsum(n)[:-1]]).astype(np.int64)
spot_checks = []
for b, idx in spot_idx.items():
    rep_n = n[idx].astype(np.int64)
    total = int(rep_n.sum())
    exp_start = np.repeat(starts[idx], rep_n)
    block_start = np.repeat(np.cumsum(rep_n) - rep_n, rep_n)
    rows = exp_start + (np.arange(total) - block_start)
    grp = np.repeat(np.arange(U), rep_n)             # fresh cluster id per drawn instance
    f = sm.OLS(ys[rows], Xs[rows]).fit(cov_type="cluster",
                                       cov_kwds={"groups": grp})
    dmax = float(np.max(np.abs(f.params - boot[b, :])))
    spot_checks.append({"b": int(b), "max_abs_diff": dmax,
                        "pass": bool(dmax < 1e-10)})
    print("[task1] spot-check b=%d max|diff|=%.3e -> %s"
          % (b, dmax, "PASS" if dmax < 1e-10 else "FAIL"))
spot_all_pass = all(s["pass"] for s in spot_checks)

# ---------------- jackknife (vectorized) for BCa acceleration ----------------
Tm = T[None, :] - S_mat                              # leave-one-user-out aggregates
XtXj = np.zeros((U, 3, 3))
XtXj[:, 0, 0] = Tm[:, 0]; XtXj[:, 0, 1] = Tm[:, 1]; XtXj[:, 0, 2] = Tm[:, 2]
XtXj[:, 1, 0] = Tm[:, 1]; XtXj[:, 1, 1] = Tm[:, 3]; XtXj[:, 1, 2] = Tm[:, 4]
XtXj[:, 2, 0] = Tm[:, 2]; XtXj[:, 2, 1] = Tm[:, 4]; XtXj[:, 2, 2] = Tm[:, 5]
Xtyj = np.stack([Tm[:, 6], Tm[:, 7], Tm[:, 8]], axis=1)
beta_j = np.linalg.solve(XtXj, Xtyj[:, :, None])[:, :, 0]
cdi_jack = beta_j[:, 1] - beta_j[:, 2]


def bca_ci(boot_vals, theta_hat, jack_vals):
    Bn = len(boot_vals)
    prop = float(np.clip(np.mean(boot_vals < theta_hat),
                         1.0 / (2 * Bn), 1 - 1.0 / (2 * Bn)))
    z0 = sps.norm.ppf(prop)
    jm = jack_vals.mean()
    dif = jm - jack_vals
    num = float((dif ** 3).sum())
    den = 6.0 * float((dif ** 2).sum()) ** 1.5
    a = num / den if den > 0 else 0.0
    zl, zu = sps.norm.ppf(0.025), sps.norm.ppf(0.975)
    a1 = sps.norm.cdf(z0 + (z0 + zl) / (1 - a * (z0 + zl)))
    a2 = sps.norm.cdf(z0 + (z0 + zu) / (1 - a * (z0 + zu)))
    lo, hi = np.quantile(boot_vals, [a1, a2])
    return float(lo), float(hi), float(z0), float(a)


def summ(vals, theta_hat, jack_vals=None):
    out = {"point": float(theta_hat),
           "mean": float(vals.mean()),
           "median": float(np.median(vals)),
           "sd": float(vals.std(ddof=1)),
           "ci95_percentile": [float(x) for x in np.quantile(vals, [0.025, 0.975])],
           "skew": float(sps.skew(vals)),
           "kurtosis_excess": float(sps.kurtosis(vals))}
    if jack_vals is not None:
        lo, hi, z0, a = bca_ci(vals, theta_hat, jack_vals)
        out["ci95_BCa"] = [lo, hi]
        out["BCa_z0"] = z0
        out["BCa_accel"] = a
    return out


summary = {
    "beta_B": summ(boot[:, 1], beta_cf[1], beta_j[:, 1]),
    "beta_W": summ(boot[:, 2], beta_cf[2], beta_j[:, 2]),
    "CDI": summ(cdi_boot, beta_cf[1] - beta_cf[2], cdi_jack),
    "CDI_std": summ(cdi_boot * mult, cdi_std_point, cdi_jack * mult),
}
summary["CDI"]["P_gt0"] = float(np.mean(cdi_boot > 0))
summary["CDI_std"]["P_gt0"] = float(np.mean(cdi_boot * mult > 0))

# ---------------- deliverables ----------------
out_df = pd.DataFrame({"b": np.arange(B),
                       "beta_B": boot[:, 1],
                       "beta_W": boot[:, 2],
                       "CDI": cdi_boot,
                       "CDI_std": cdi_boot * mult})
out_df.to_csv(BOOT_CSV, index=False)
print("[task1] wrote %s (%d rows)" % (BOOT_CSV, len(out_df)))

report = {
    "task": "Task1 consumer cluster bootstrap B=2000 (+ Task2 standardized CI)",
    "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "input": PANEL,
    "design": {
        "resample_unit": "consumer (uid), with replacement, full wave history kept",
        "B": B, "seed": SEED, "rng": "PCG64",
        "solver": "closed-form sufficient statistics; verified vs statsmodels",
        "standardization": "CDI_std = CDI * (s_X/s_Y), common reference full panel",
        "s_X": sX, "s_Y": sY, "mult": mult,
    },
    "selfchecks": {
        "closed_form_vs_statsmodels_maxdiff": float(diff_sm),
        "closed_form_vs_statsmodels_pass": selfcheck_sm,
        "closed_form_vs_frozen_diff": {k: float(v) for k, v in diff_frozen.items()},
        "closed_form_vs_frozen_pass": selfcheck_frozen,
        "cdi_std_point": float(cdi_std_point),
        "cdi_std_vs_task0_crosscheck_pass": cdi_std_crosscheck,
        "spot_checks": spot_checks,
        "spot_checks_all_pass": spot_all_pass,
    },
    "summary": summary,
    "versions": {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": sps.__version__ if hasattr(sps, "__version__") else "see scipy",
        "statsmodels": sm.__version__,
    },
    "runtime_sec": round(time.time() - t0, 1),
}
import scipy
report["versions"]["scipy"] = scipy.__version__
with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("[task1] wrote %s" % REPORT)

c = summary["CDI"]
print("[task1] CDI point=%.6f  boot mean=%.6f median=%.6f sd=%.6f"
      % (c["point"], c["mean"], c["median"], c["sd"]))
print("[task1] CDI 95%% CI percentile=[%.6f, %.6f]  BCa=[%.6f, %.6f]  P(CDI>0)=%.4f"
      % (c["ci95_percentile"][0], c["ci95_percentile"][1],
         c["ci95_BCa"][0], c["ci95_BCa"][1], c["P_gt0"]))
cs = summary["CDI_std"]
print("[task1] CDI_std point=%.6f  BCa=[%.6f, %.6f]"
      % (cs["point"], cs["ci95_BCa"][0], cs["ci95_BCa"][1]))
print("TASK1_DONE boot_ok=%s selfcheck=%s spotcheck=%s runtime=%.1fs"
      % (True, selfcheck_sm and selfcheck_frozen and cdi_std_crosscheck,
         spot_all_pass, time.time() - t0))
