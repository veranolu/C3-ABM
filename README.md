# C3-ABM: Companion Code for "Two Timescales, Two Calibers"

Companion analysis and simulation code for the manuscript:

> **"Two Timescales, Two Calibers: Auditing Consumer Adaptation in Algorithmically Mediated Environments"**
> by Dan Lu, Hongwei Liu, Xiuli Yu, and Dongdong Shi
> Manuscript information-4549232, revised version V9.60B.6, under review at *Information* (MDPI).

**Archived snapshot:** [https://doi.org/10.5281/zenodo.22913316](https://doi.org/10.5281/zenodo.22913316) (Zenodo; concept DOI, always resolves to the latest release; v1.0.1 is byte-identical to the locked tags except for this line).

## Repository structure (three tiers)

| Tier | Contents | Role in manuscript |
|---|---|---|
| `PRIMARY_REVISED_ANALYSIS/` | Frozen analysis code and full-precision result tables behind the revised Study 1 matched-estimand REWB/Mundlak results, the 18-specification portability envelope, and the Study 2/3 result tables | Sections 4.3–4.4, 5, 6; Appendix Tables C3–C9 |
| `ARCHIVED_PROVENANCE/` | Old-to-corrected mapping documenting the retired mixed-estimator/split-half lineage | Section 4.3 archived provenance diagnostic; Appendix C.1 (Tables C1–C5) — retained solely for analytical lineage, explicitly non-evidentiary |
| `GENERATIVE_PROBE/` | Minimal two-timescale slow-memory agent-based model and its summary results | Section 7 — a generative sufficiency probe with openly stated correspondence boundaries |

## What the generative probe is (and is not)

The probe asks a narrow computational question: whether one explicitly
specified slow-memory process is generatively sufficient to reproduce
selected qualitative signatures. It is an existence proof, not an estimator,
and it is **not** a replication or validation of the revised matched-estimand
REWB CDI. No simulated regime reproduces the focal empirical CDI (+0.5174);
the falsifiable boundary of the modeled process is stated in Section 7.4 of
the manuscript (at δ = 0.008 the reversal collapses and the between-person
association itself turns negative).

## Data availability

- **JDsearch (Study 1)** and **JData (Study 3)** raw data are governed by
  data-use agreements and **cannot be redistributed**; they are not part of
  this repository.
- **Amazon Reviews 2023** (Study 2) is public.
- This release supports computational transparency; it does not provide
  unrestricted independent reproduction of the restricted-data analyses.

## Frozen anchors (bit-level reproducibility)

- Primary REWB/Mundlak: N = 60,423 consumers / 242,771 observations;
  βB = −2.9957 (SE 0.0194), βW = −3.5132 (SE 0.0110),
  CDI = +0.5174 (SE 0.0210; Wald χ²(1) = 609.61); consumer-cluster BCa
  bootstrap [+0.4757, +0.5573], B = 2,000, seed 20260915.
- Portability headline states: +0.5174 / −0.4812 / −0.8077 / −0.0007 / +0.0565.
- Full-precision values: `PRIMARY_REVISED_ANALYSIS/c3_portability_master_table.csv`
  and `portability_multiverse_master.csv` (18 reported specifications,
  17 estimable; T3 not identifiable in the released dataset).

## Locked tags

- `submission-V9.60B.6` — repository state exactly as cited in the submitted manuscript.
- `red-team-green-2026-09-23` — snapshot of the repository as independently audited on 2026-09-23.

Both tags point at the same commit; they exist so that the submission record
and the audit record are independently citable.
