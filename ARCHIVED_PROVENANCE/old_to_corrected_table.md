# OLD → CORRECTED Mapping (JData Study 3 provenance)

Prepared during the revision audit, 2026-09-20.
Purpose: the single authoritative basis for line-by-line corrections applied in the revision. All corrected values are final (sourced from the frozen results package, lineage recomputation, codebook verification, and dataset-year tracing).

| Item | OLD (previous value) | CORRECTED (sole correct value) | Status |
|---|---|---|---|
| Sample label (dataset naming) | "JData2018" (12 occurrences) | "JData2016" (or the neutral form "the JData user-behavior panel (2016)") | Final (codebook + file name + 105,321-row cross-check, three-way agreement) |
| Dataset year | 2018 ("February–April 2018 action tables") | **2016** (official competition data year; raw-timestamp verification: all three tables' time min/max fall within 2016) | Final |
| Observation window | "2018-02-01 to 2018-04-30" ("three-month panel") | **2016-02-01 to 2016-04-15** (merged min = 2016-01-31 23:59:02 / max = 2016-04-15 23:59:59; the 01-31 record is a boundary record one minute before the official window; per-file ranges 201602: 01-31–02-29 / 201603: 02-29–03-31 / 201604: 03-31–04-15; 50,601,736 rows scanned, 0 unparseable). Note: the "three-month panel" wording was inaccurate (02-01–04-15 is ~10.5 weeks); replaced with "approximately ten-week panel (2016-02-01 to 2016-04-15)" | Final |
| Sex coding | 0 = missing / 1 = male / 2 = female | **0 = male / 1 = female / 2 = undisclosed** | Final (one academic source plus three independent secondary transcriptions of the official documentation agree) |
| Gender N (analysis sample) | N = 12,699 (previously labeled "male 2,136 / female 10,563") | **N = 13,081 = male (sex = 0) 10,945 + female (sex = 1) 2,136** (excluding sex = 2 undisclosed, 10,563); the old 12,699 = female 2,136 + undisclosed 10,563 → invalid legacy coding | Final |
| Gender N (full sample, for reference) | N = 14,493 (previously labeled "male 2,334 / female 12,159") | **N = 14,084 = male 11,750 + female 2,334** (excluding sex = 2, 12,159, plus 1 sex-NaN); the old 14,493 = female 2,334 + undisclosed 12,159 → invalid legacy coding | Final |
| Gender statistics (Welch as primary) | Welch t(12,697.1) = 0.0076, p = .994, d = 0.000, diff = 0.0005 [−0.1446, +0.1457], SD 8.2546 / 8.0579, mean 3.9613 / 3.9608; Student p = .994; MWU p = .873 | **Primary (age-valid, N = 13,081)**: male mean = 4.2799, SD = 0.9540; female mean = 4.0023, SD = 0.9895; diff (M − F) = **+0.2776** [0.2319, 0.3232]; Welch **t = 11.9278, df = 2960.79, p = 4.5e-32**; Cohen's **d = 0.2892**. QA-only: Student t = 12.2252 (p = 3.5e-34); MWU = 13,644,759.5 (p = 1.7e-34). Reference (full sample N = 14,084): diff = +0.2808 [0.2370, 0.3245]; Welch t = 12.5703, df = 3257.07, p = 2.0e-35; d = 0.2914. Two-path recomputation (scipy vs. manual) passed. Result file: study3_gender_rerun_results.csv | Final — statistically significant, small effect; the old "d = 0.000, no gender difference" sentence was retired; reported as "statistically distinguishable but modest, no broader gender claim" |
| S0 sample size | 26,244 | 26,244 (unchanged) | Final (robust to codebook correction) |
| S1 analysis sample size | 23,644 (rule text: "age > 0 and sex non-missing") | 23,644 (unchanged); rule wording simplified to **age > 0** (the sex-non-missing clause is vacuous: the only sex-NaN user is already inside the age-invalid set) | Final |
| Stratification description (hl_split) | lo/hi 11,822 each; group means of level/orders/actions/age | Unchanged (sex-independent; confirmed by dependency audit) | Final |
| Full-sample sex descriptive counts | 1 = male 2,334 / 2 = female 12,159 / 0 = missing 11,750 / NaN 1 | **0 = male 11,750 (44.8%) / 1 = female 2,334 (8.9%) / 2 = undisclosed 12,159 (46.3%) / NaN 1** | Final (labels corrected, counts unchanged) |
| Analysis-sample sex descriptive counts | (old coding implicit in the 12,699 decomposition) | **0 = male 10,945 (46.3%) / 1 = female 2,136 (9.0%) / 2 = undisclosed 10,563 (44.7%) / NaN 0** | Final (labels corrected, counts unchanged) |
| level/age tests (Study 3) | ρ = 0.2861, F = 521.5666; ρ = −0.0407, F = 13.7874 | Unchanged (sex-independent) | Final |
| Deep-mechanism paragraph (Study 3 extension) | Candidate pinpoint: a "female-only scenario" paragraph (with p = .0047) | **Written off (2026-09-20)**: phantom reference — no "female-only" paragraph or p = .0047 exists in the manuscript, its ancestor version, or the frozen package. Gender-related content consists solely of the §6 descriptive comparison, Table A6/A7 labels, and the §6.4 "gender shows little association" sentence, all covered by the rows above | Written off (does not exist; no action needed) |

## Affected manuscript locations (summary)
Table A7 gender-test row; title/abstract/§1/Data Availability "JData2018"; §6 main text and Table 2 sex descriptives; Appendix A.3 Table A6 sex rows (scales and missingness counts); §6 sample-construction paragraph; IRB statement "JData2018 anonymized public dataset". Additionally, the §6 date sentence (year + window) was corrected as an eighth location outside the pinpoint list (year-tracing item).

## Closure record
- RERUN: closed 2026-09-20 — jdata_user_summary.csv uploaded; rerun saved to study3_gender_rerun_results.csv; gender-statistics row backfilled.
- TIMESTAMP AUDIT: closed 2026-09-20 — observation-window row backfilled (2016-02-01 to 04-15), with the linked "three-month" wording warning.
- DECISION: written off 2026-09-20 — the "female-only" deep-mechanism paragraph is a phantom reference and does not exist; no action required. All pending items cleared.
