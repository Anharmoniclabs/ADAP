# ADAP: AD-Alpha-Parameterization
## Posterior Alpha Topography, Spectral Parameterization, and Physiological State Sensitivity in Retrospective EEG Cohorts

**Luis Minier**  
**Independent Researcher and Student**  
Manuscript draft: September 14, 2026

## Abstract

**Background:** A scalp EEG pattern associated with a diagnostic group can reflect several overlapping influences, including regional oscillatory power, spectral background, peak-frequency placement, recording reference, and physiological state. ADAP examines these influences to clarify the interpretation of an Alzheimer-associated alpha pattern rather than treating statistical separation as evidence of a specific biological mechanism.

**Methods:** A retrospective control analysis considered 88 OpenNeuro ds004504 derivative recordings: 36 Alzheimer’s disease (AD), 29 control, and 23 frontotemporal dementia (FTD) recordings. Original eight-second samples and first, middle, and last 60-second periods were analyzed. An external Florida dataset contributed eight-second recordings from 80 AD and 12 healthy participants. Regional band-power measures were supplemented with FOOOF spectral parameterization and an exploratory individualized-frequency analysis. A 19-channel relative-alpha deviation score, frozen from the source-control mean map, was evaluated in 34 older healthy MPI-LEMON participants with paired eyes-closed and eyes-open recordings. CAP sleep controls considered 16 healthy candidates, of whom 11 supplied eligible recordings. Inference used participants as the sampling units, with separate Holm corrections for 81 group tests, eight healthy-state tests, and six exploratory individualized-frequency tests.

**Results:** Source posterior absolute alpha and posterior/frontal alpha ratios were lower in AD across all three 60-second periods after correction. The individualized-band posterior/frontal contrast also survived its exploratory correction in all three periods, whereas candidate peak-frequency differences did not. Background-adjusted posterior alpha survived correction in the first and middle periods, but not the last; the periodic spatial contrast survived only in the middle period. Florida posterior/frontal alpha was lower in AD (adjusted p = 0.00651). Healthy eye opening increased the frozen score in 30/34 participants (mean paired change 0.322; pointwise 95% CI 0.212–0.421; adjusted p = 0.000800). CAP stage 2 increased theta/alpha in 11/11 eligible participants (mean paired log-ratio change 1.224; CI 0.764–1.701; adjusted p = 0.00400). No AD-versus-FTD factor contrast survived the group correction.

**Conclusions:** The recorded analyses support an AD-associated posterior-alpha/topographic difference and establish physiological state sensitivity of the measured features. They do not establish AD specificity, a causal molecular mechanism, or clinical diagnostic validity. The contribution is an inspectable analysis and control framework, including negative findings and explicit limits on interpretation.

**Keywords:** EEG; Alzheimer’s disease; alpha power; scalp topography; spectral parameterization; physiological state; reproducibility.

## 1. Introduction

An EEG feature may distinguish groups without identifying the biological process responsible for that distinction. A regional alpha difference can arise alongside changes in spectral background, peak frequency, vigilance, recording reference, or other clinical and acquisition factors. A scientifically useful analysis must therefore describe both the association and the conditions under which the measurement changes.

ADAP, expanded as AD-Alpha-Parameterization, addresses this measurement problem. The present paper documents the September 14 control package: the data considered, transformations applied, statistical families evaluated, outcomes retained, and conclusions that remain unsupported. It consolidates the later control analyses rather than silently presenting the earlier manuscript as having already included them.

The work asks four questions. First, does the source regional difference persist beyond an initial short recording segment? Second, how much of the observed pattern remains under spectral-background modeling and individualized frequency bands? Third, does a frozen source-derived score respond to ordinary healthy physiological changes? Fourth, do comparison-disease recordings establish AD specificity?

Spectral parameterization provides a framework for distinguishing fitted periodic peaks from aperiodic background [1]. Independent work relating alpha reactivity to cholinergic-system measures supplies relevant biological context [2], but those measurements were not collected for the AD participants in this package. Accordingly, mechanistic interpretations remain hypotheses rather than results of the present study.

## 2. Study design and provenance

### 2.1 Retrospective design

This is a retrospective analysis with documented protocol amendments. The plan records settings fixed before new outcome calculations, but the project was not prospectively preregistered. The individualized-frequency sensitivity was added after the original fixed-band results and is explicitly exploratory.

The analysis does not count different windows from one participant as independent people. First, middle, and last periods provide within-cohort stability checks, not three independent replications. Healthy-state controls characterize responsiveness of the measurements; they are not matched substitutes for the clinical source cohort.

### 2.2 Datasets

| Dataset | Participants considered | Recording contribution | Analytic purpose |
|---|---:|---|---|
| OpenNeuro ds004504 v1.0.9 | 36 AD, 29 controls, 23 FTD | Original first 8 s and first/middle/last 60 s | Source contrasts, spectral analysis, recording-period stability, disease comparison |
| Florida OSF 2v5md | 80 AD, 12 healthy controls | Original eyes-closed 8 s | External regional-factor comparison |
| MPI-LEMON | 74 older candidates; 34 paired participants included | First 60 s of available preprocessed EC and EO conditions | Healthy eye-condition sensitivity |
| CAP Sleep Database v1.0.0 | 16 healthy candidates; 11 eligible recordings | Externally annotated W, S1, S2 epochs | Healthy sleep-state sensitivity |

Diagnostic labels are inherited from the source datasets. No independent clinical reassessment, biomarker confirmation, or prospective recruitment was performed for this analysis. The Florida recordings were used at their available duration; no longer recordings were synthesized.

LEMON eligibility required an age-bin lower bound of at least 55 years, paired conditions, the prescribed channel identities, and sufficient boundary-free windows. Missing electrodes were not interpolated. CAP paired sample sizes depended on eligible states within each participant; inclusion of 11 recordings does not imply that every comparison used all 11.

### 2.3 Audit records

The package preserves analysis scripts, a recorded plan, acquisition records, subject-level outputs, correction families, fit validations, execution logs, amendments, and checksums. These records allow readers to distinguish planned settings, subsequent changes, excluded observations, and retained negative outcomes. They document computational provenance, but do not independently establish that all historical choices were free of outcome influence.

## 3. Signal processing and feature definitions

### 3.1 Channels and sampling

The 19-channel features use named scalp channels. The posterior set is P3, P4, Pz, O1, and O2. The frontal set is Fp1, Fp2, F3, F4, F7, F8, and Fz. Named-channel selection is used rather than assuming array-position equivalence between datasets. LEMON aliases map T3/T4/T5/T6 to T7/T8/P7/P8.

Analysis signals are represented at 128 Hz. The source pipeline resamples 500 Hz inputs using a 32/125 polyphase ratio; LEMON acquisition resamples 250 Hz inputs using 64/125. Source 60-second extracts retain first, middle, and last periods, with extraction receipts recording source identity, hashes, sampling rate, and start positions.

### 3.2 Power spectra and bands

For channel c, let S_c(f) denote the Welch power spectral density estimate. The implementation uses a Hann window, constant detrending, and 1,024-sample segments. At 128 Hz these segments span eight seconds. Longer inputs use 512-sample overlap; eight-second inputs use one segment.

Band power is computed by trapezoidal integration over included frequency bins:

\[
P_{c,[a,b)}=\operatorname{trapz}\{S_c(f):a\leq f<b\}.
\]

The four bands are delta [1,4), theta [4,8), alpha [8,13), and beta [13,30) Hz. The upper bound is excluded by the code. Relative alpha is

\[
r_c=\frac{P_{c,\alpha}}{P_{c,\delta}+P_{c,\theta}+P_{c,\alpha}+P_{c,\beta}}.
\]

These definitions concern finite-grid numerical integration. Reproduction should use the recorded bin masks rather than substitute differently inclusive band conventions.

### 3.3 Regional alpha contrast

For posterior and frontal channel sets P and F, the regional feature is

\[
L_\alpha=\ln\left[\frac{|P|^{-1}\sum_{c\in P}P_{c,\alpha}}{|F|^{-1}\sum_{c\in F}P_{c,\alpha}}\right].
\]

A lower value denotes less posterior alpha relative to frontal alpha. The ratio alone does not identify which region drives the contrast; separate regional log-power endpoints are therefore retained. Native amplitude conventions are inherited from the input recordings, so absolute log-power values should not be treated as directly harmonized across datasets without a separate units and acquisition audit.

### 3.4 Frozen spatial-deviation score

Let t be the average 19-channel relative-alpha map of the 29 source controls, constructed from their first eight-second recordings. For a participant map r, the deviation score is

\[
D(r,t)=1-\operatorname{corr}(r,t).
\]

The template is frozen before application to LEMON and is not fitted to its eye-condition labels. A separate sensitivity repeats template construction and scoring after common-average referencing across the same 19 channels. The native-reference and average-reference scores are distinct analyses.

Correlation distance describes spatial-pattern agreement, not disease probability or absolute alpha magnitude. It requires nonconstant maps for a defined Pearson correlation. Freezing a source template prevents fitting to LEMON outcomes, but does not erase historical feature selection in the source research.

### 3.5 Spectral parameterization

Regional PSDs are averaged across the designated channels and fitted using FOOOF 1.1.1. The model contains a fixed aperiodic background and Gaussian periodic components:

\[
\log_{10}S(f)=b-\chi\log_{10}f+\sum_j a_j\exp\left[-\frac{(f-\mu_j)^2}{2\sigma_j^2}\right].
\]

Settings are a 2–30 Hz fit range, peak-width limits of 1–8 Hz, at most six peaks, minimum peak height 0.1 log10 units, and peak threshold 2. Fits require R² ≥ 0.8 and mean absolute log10 error ≤ 0.15. Failed-fit parameters are treated as unavailable.

Periodic alpha is the mean fitted periodic log10 contribution over [8,13) Hz, including peak tails. It is not a direct neuronal oscillation amplitude. The periodic spatial contrast is posterior minus frontal periodic alpha. Aperiodic exponents and their regional contrast are retained as separate endpoints. Idealized known-spectrum tests assess software recovery, not biological truth.

### 3.6 Individualized-frequency sensitivity

For each eligible source 60-second spectrum, the highest fitted posterior peak with center in 4–14 Hz defines a band extending ±2 Hz around that center. The same band is integrated in posterior and frontal regions. Participants without an eligible peak or acceptable fit have missing individualized endpoints; no frequency is imputed.

Because the search interval includes frequencies below 8 Hz, its selected peak is termed a candidate peak rather than automatically identifying it as an alpha generator. This analysis tests sensitivity to frequency-band placement among participants meeting the selection rule.

### 3.7 Healthy-state aggregation and CAP amendments

LEMON features are calculated in eight-second windows stepped by four seconds, excluding windows crossed by a recorded boundary event. Each participant-condition endpoint is the median across eligible windows; at least three windows are required. The first/last 30-second subdivisions are retained as supplementary stability observations.

CAP uses up to the first ten complete 30-second epochs for each externally annotated state W, S1, or S2 anywhere in the recording. A state requires at least three epochs for paired inference. Participant-state endpoints are median regional log-alpha ratios and median log theta/alpha ratios. CAP uses regional signals and is not the original 19-channel score.

The original first-30-minute restriction was amended because that interval could precede scored sleep states. A parser error affecting annotations without an optional Position column was corrected and recorded. Epoch selection follows external sleep labels, not the alpha feature.

Where permitted by recorded channels and matching physical units, exact voltage identities reconstruct a shared reference:

\[
F4-A1=(F4-C4)+(C4-A1),
\]

\[
O2-A1=(C4-A1)-(C4-P4)-(P4-O2).
\]

These are algebraic combinations of recorded signals, not estimated spatial interpolation. Original direct-reference options and exclusion records are retained.

ECG sensitivity regresses regional EEG on standardized ECG at lags −10, −5, 0, 5, and 10 samples plus an intercept. A five-second circular ECG shift provides a descriptive sham. Edge samples are cropped before comparisons. These checks neither validate artifact removal nor establish autonomic causation; correlated neural activity may also be removed.

## 4. Statistical analysis

Independent diagnostic-group comparisons use two-sided Mann–Whitney tests. Effect summaries are differences of group medians with 5,000 within-group participant bootstrap resamples. Mann–Whitney tests concern distributional ordering and should not be interpreted as tests exclusively of median equality without additional distributional assumptions.

The group family contains nine endpoints across eight OpenNeuro combinations of period and diagnostic contrast, plus nine Florida endpoints: 81 planned comparisons. Unavailable comparisons remain in the table and are assigned p = 1 for Holm correction accounting. Their scientific estimates remain unavailable rather than being represented as null observations.

Healthy-state comparisons use the mean of within-participant differences. Two-sided Monte Carlo sign-flip tests use 10,000 draws and a plus-one adjustment; their interpretation assumes a suitable symmetric paired null. Participant bootstrap intervals use 5,000 resamples. Four LEMON endpoints and four CAP endpoints form one eight-test Holm family.

Candidate peak frequency and individualized regional ratio across three periods form a separate six-test exploratory family. The seed is 20260914. Bootstrap intervals are pointwise, not multiplicity-adjusted simultaneous intervals. They do not include uncertainty from historical endpoint selection, dataset acquisition, model specification, or cohort transport.

## 5. Results

### 5.1 Analysis accounting

The recorded run contains 444 spectral subject-window rows: 352 OpenNeuro rows from 88 participants across four periods and 92 Florida rows. It contains 34 paired LEMON participants, 16 CAP candidates, 11 included CAP recordings, 81 group tests, eight state tests, and six individualized-frequency tests. These counts describe data accounting, not additional independent participants.

### 5.2 Source regional results

Posterior absolute alpha and the posterior/frontal ratio were lower in AD in all three 60-second periods after the 81-test Holm correction. Frontal alpha differences did not survive correction; this is not evidence of equal frontal power.

| Endpoint | Period | AD − control median difference | Pointwise 95% CI | Adjusted p |
|---|---|---:|---|---:|
| Log posterior alpha | First 60 s | −0.6866 | −1.1825 to −0.1849 | 0.03595 |
| Log posterior alpha | Middle 60 s | −1.2435 | −1.6770 to −0.6765 | 0.0002990 |
| Log posterior alpha | Last 60 s | −0.9492 | −1.3201 to −0.1956 | 0.02358 |
| Log posterior/frontal alpha | First 60 s | −0.3887 | −0.8048 to −0.1963 | 0.002120 |
| Log posterior/frontal alpha | Middle 60 s | −0.5779 | −0.9283 to −0.4364 | 0.00001016 |
| Log posterior/frontal alpha | Last 60 s | −0.4512 | −0.7281 to −0.2720 | 0.0006661 |

Each listed source contrast uses 36 AD and 29 control participants. The original eight-second regional ratio also survived correction (difference −0.5235; adjusted p = 0.02990), while eight-second posterior absolute alpha did not (adjusted p = 0.09631).

### 5.3 External Florida regional contrast

The Florida posterior/frontal log-alpha ratio was lower in AD: median difference −1.7605, pointwise CI −2.2005 to −0.6384, adjusted p = 0.006513. Posterior absolute alpha was directionally lower but did not survive the full correction (adjusted p = 0.19844); frontal alpha also did not survive correction.

This provides an external regional-factor observation, not a complete replication of every spectral or temporal source analysis. The Florida control sample was small and the available recording duration was eight seconds.

### 5.4 Spectral background and failed fits

The original eight-second spectra in both cohorts failed the fixed spectral-model quality gate. Their raw band-power endpoints remain available, but their spectral-decomposition parameters are not interpreted.

For source 60-second recordings, posterior periodic alpha was lower in AD after correction in the first period (adjusted p = 0.04983) and middle period (0.001206), but not the last period (0.08643). The periodic posterior-minus-frontal contrast survived only in the middle period (0.001803). The posterior aperiodic exponent also differed in the middle period (0.006750).

Thus, a periodic contribution is supported for some periods, but the full spatial effect is not demonstrated to be wholly independent of spectral background in every period. Failed short-segment fits should not be interpreted as absence of physiological oscillations.

### 5.5 Individualized bands

| Period | AD / control n | Individualized log-ratio difference | Pointwise 95% CI | Exploratory adjusted p |
|---|---:|---:|---|---:|
| First 60 s | 33 / 29 | −0.4155 | −0.8157 to −0.1812 | 0.0003512 |
| Middle 60 s | 33 / 28 | −0.6640 | −0.9324 to −0.4820 | 0.000002352 |
| Last 60 s | 35 / 29 | −0.5413 | −0.7575 to −0.2999 | 0.00007955 |

The spatial contrast persisted in each period among eligible participants. Candidate peak-frequency differences did not survive correction: adjusted p = 0.5164, 0.1600, and 0.1600 for first, middle, and last periods, respectively. This does not prove equal peak frequencies or eliminate selection effects introduced by requiring a detectable peak.

### 5.6 Healthy eye opening

The native frozen score increased from a mean of 0.4445 during eyes closed to 0.7665 during eyes open. Thirty of 34 participants increased; four decreased. The mean paired change was 0.3220 (pointwise CI 0.2117–0.4213; adjusted p = 0.0007999).

The average-reference score also increased (mean paired change 0.3731; CI 0.2615–0.4814; adjusted p = 0.0007999). Posterior/frontal log-alpha decreased in 29/34 participants (mean paired change −0.6975; CI −0.8860 to −0.5108; adjusted p = 0.0007999). Log theta/alpha increased (mean paired change 0.8241; CI 0.6116–1.0329; adjusted p = 0.0007999).

These are within-person physiological condition effects. They are not estimates of diagnostic false-positive rates because no clinical decision threshold was validated here.

### 5.7 Healthy sleep

| Contrast | Feature | Paired n | Mean paired difference | Pointwise 95% CI | Adjusted p |
|---|---|---:|---:|---|---:|
| S1 − W | Log posterior/frontal alpha | 10 | −0.2024 | −0.4434 to 0.0061 | 0.1492 |
| S1 − W | Log theta/alpha | 10 | 0.7535 | 0.2537 to 1.2799 | 0.09239 |
| S2 − W | Log posterior/frontal alpha | 11 | −0.3221 | −0.5597 to −0.0839 | 0.09239 |
| S2 − W | Log theta/alpha | 11 | 1.2242 | 0.7640 to 1.7015 | 0.004000 |

Only stage-2 theta/alpha survived the eight-test state correction among the CAP endpoints. All 11 eligible participants increased on that measure. Pointwise intervals excluding zero alongside nonsignificant adjusted p-values are not contradictory: the intervals and corrected tests have different inferential coverage.

### 5.8 Disease comparison

None of the AD-versus-FTD factor comparisons survived correction across the 81 group tests. This does not establish equivalence between AD and FTD; it means AD specificity was not demonstrated with the present endpoints, sample, and inferential procedure.

## 6. Discussion

### 6.1 What the evidence supports

The combined results support a posterior-alpha/topographic association in the studied AD recordings. Its direction persists across source recording periods and under the tested individualized-band definition. The Florida regional ratio provides additional external evidence for that particular feature. These observations justify continued investigation of the measurement, while leaving broad clinical generalization unresolved.

The result is not simply a statement that every alpha-related endpoint succeeds. Background-adjusted effects vary by recording period, short-segment spectral models fail their quality gate, candidate peak-frequency tests are not significant after correction, and the AD/FTD comparison does not establish specificity. These outcomes materially constrain the interpretation.

### 6.2 What healthy-state controls contribute

The frozen score responds strongly to eye condition in healthy adults, and theta/alpha responds to stage-2 sleep. Therefore these measurements contain physiological-state information. A change in score cannot be interpreted as a disease change without considering recording state and acquisition context.

Nevertheless, healthy eye opening does not show that eye opening caused the source AD/control contrast: both source groups were recorded eyes closed. Likewise, a sleep-state effect does not show that source participants were asleep. These controls reveal plausible measurement sensitivities rather than retrospectively identifying the cause of a clinical-group difference.

### 6.3 Mechanistic boundaries

There are no paired cholinergic measures, synaptic markers, amyloid/tau measurements, drug manipulations, or relevant multimodal outcomes in this control analysis. Resting alpha power and EC-to-EO alpha reactivity are also different quantities. Because paired EO recordings are absent for the source AD group, an AD-by-eye-condition interaction cannot be estimated.

Mechanistic literature can motivate future measurements, but cannot supply missing measurements for these participants. The paper therefore does not equate lower alpha with demonstrated cholinergic injury or synaptic loss.

### 6.4 Contribution and novelty

The contribution is an explicit, auditable characterization of a particular source-derived spatial feature and its spectral and physiological sensitivities. It is not a claim to have first discovered AD-related alpha abnormalities or invented spectral parameterization. The documented amendments, negative results, frozen-transfer rule, and separation of numerical observations from causal interpretations are central to the research contribution.

## 7. Limitations

The analysis is retrospective and not prospectively preregistered. Multiplicity correction within declared families does not account for every historical choice made during feature development. Individualized-frequency results are exploratory and conditional on peak eligibility.

The clinical groups were not randomized. The reported unadjusted group tests do not fully control age, medication, clinical severity, comorbidity, recording conditions, or other covariates. Dataset labels and preprocessing are inherited, and the present analysis does not substitute for an independent diagnostic audit.

LEMON inclusion reduced 74 candidates to 34 paired participants. Availability, channel completeness, and boundary criteria may restrict generalizability. CAP uses a different montage and context from the clinical recordings. Its epochs may occur at different times of night; W labels do not establish eye closure. Thirty-second labels do not exclude brief sub-epoch vigilance changes. No quantitative worst-case microsleep bound follows from these data.

Source recording periods are correlated observations from the same people. Overlap or shared preprocessing further limits interpreting them as independent evidence. FOOOF fits are measurement models, and acceptable fit quality does not prove a biological decomposition. ECG regression is descriptive and can remove shared physiological neural variance.

No calibrated clinical threshold, prospective diagnostic assessment, or treatment-response evaluation is established by this control package. Earlier manuscript discrimination analyses, where present, must be evaluated under their own sampling and validation assumptions and must not be silently substituted for prospective clinical validation.

## 8. Reproducibility and availability

The research repository is [Anharmoniclabs/ADAP](https://github.com/Anharmoniclabs/ADAP), with a [public research page](https://anharmoniclabs.github.io/ADAP/). Principal scripts are `spectral_controls.py`, `individual_peak_controls.py`, `state_controls.py`, `validate_spectral_fit.py`, `make_figures.py`, `build_report.py`, and `verify_run.py`. `audit_metrics.py` supplies shared definitions. The recorded environment uses Python 3.12.14 with versions in `requirements-lock.txt`.

The complete original control archive was recovered from saved research artifacts. Its `SHA256SUMS` matches the repository manifest, and all 423 listed files passed checksum verification. This establishes recovery and byte-level integrity. It is not a fresh end-to-end numerical rerun or an independent replication.

Large EEG inputs are acquired from their original public sources rather than redistributed in this Git repository. Run python3.12 reproduce.py to create an isolated environment, download the pinned inputs, verify all 423 original package hashes, run the analysis, and compare the resulting CSV tables with the frozen reference tables. The repository includes source URLs, source-file checksums, extraction receipts, and the acquisition code. A complete independent end-to-end numerical replication has not yet been completed. The separate multipart full-source archive is optional; its reassembly metadata are retained for historical provenance.

Once all inputs and the recorded environment are available, the documented sequence is:

```sh
python validate_spectral_fit.py
python spectral_controls.py
python individual_peak_controls.py
python state_controls.py
python make_figures.py
python build_report.py
python verify_run.py
```

`verify_repository.py` checks available files against the package hashes. `verify_run.py` checks selected row counts and array properties; it does not independently recompute and validate every scientific result. A stronger reproduction would run the full pipeline in a separate output directory and compare numerical outputs against frozen reference tables with declared tolerances.

## 9. Conclusions

ADAP documents an AD-associated posterior-alpha/topographic difference that is stable across the tested source recording periods and persists under an exploratory individualized-band definition. A corresponding regional ratio is observed in the external Florida recordings. Spectral parameterization offers partial, period-dependent support for a periodic contribution, while healthy eye-condition and sleep-state controls demonstrate physiological sensitivity.

The evidence supports further study of the measurement and its confounds. It does not establish AD specificity, a molecular cause, or clinical diagnostic validity. The next methodological priorities are a fresh numerical reproduction, explicit covariate and selection-sensitivity analyses, independent cohort evaluation, and paired EC/EO recordings in clinical comparison groups with independent biological measurements.

## Declarations

**Author identification:** Luis Minier, Independent Researcher and Student. No institutional affiliation is listed.

**Research context:** Secondary analysis of existing dataset recordings. No new participant recruitment or intervention is described here. Original dataset ethics, consent, licensing, and reuse conditions remain applicable. No new institutional ethics approval or exemption is asserted by this manuscript.

**AI assistance:** AI assistance was used in code preparation, analysis support, repository organization, and manuscript drafting. This disclosure does not imply independent human reimplementation or external validation. Responsibility for final factual review, analytic decisions, and submission remains with the author.

**Funding and competing interests:** Author declarations are not available in the reviewed records and must be completed before submission; absence of funding or competing interests is not assumed.

**Manuscript status:** Full research draft based on the recorded control package. A fresh numerical rerun and external peer review are not claimed.

## References and data sources

1. Donoghue T, et al. Parameterizing neural power spectra into periodic and aperiodic components. *Nature Neuroscience*. 2020. [doi:10.1038/s41593-020-00744-x](https://doi.org/10.1038/s41593-020-00744-x).
2. Schumacher J, et al. EEG alpha reactivity and cholinergic system integrity in Lewy body dementia and Alzheimer’s disease. *Alzheimer’s Research & Therapy*. 2020. [doi:10.1186/s13195-020-00613-6](https://doi.org/10.1186/s13195-020-00613-6).
3. [OpenNeuro ds004504, version 1.0.9](https://openneuro.org/datasets/ds004504/versions/1.0.9). Source clinical EEG dataset.
4. [Florida EEG dataset, OSF 2v5md](https://osf.io/2v5md/). Original `EEG_data.zip` revision identified by the package checksum.
5. [MPI-LEMON dataset portal](https://fcon_1000.projects.nitrc.org/indi/retro/MPI_LEMON.html). Paired healthy eye-condition recordings and source metadata.
6. [CAP Sleep Database, version 1.0.0](https://physionet.org/content/capslpdb/1.0.0/). Sleep recordings and external stage annotations.
7. Minier L. [ADAP research repository](https://github.com/Anharmoniclabs/ADAP). September 14, 2026 control package, plans, amendments, results, and checksums.

## Supplementary artifact guide

| Artifact | Contents |
|---|---|
| `results/spectral_subject_windows.csv` | 444 subject-window feature rows |
| `results/spectral_group_tests.csv` | All 81 group comparisons, including unavailable fits |
| `results/source_window_stability.csv` | Source cross-period stability summaries |
| `results/individual_peak_subjects.csv` | Peak eligibility and individualized participant features |
| `results/individual_peak_tests.csv` | Six exploratory tests |
| `results/lemon_subject_states.csv` | Paired participant-condition summaries |
| `results/cap_subject_states.csv` | Participant-state summaries and epoch counts |
| `results/state_tests.csv` | Eight paired state tests |
| `results/cap_ecg_sensitivity.csv` | Descriptive ECG/sham sensitivity summaries |
| `PLAN.json` and CAP amendment files | Recorded choices and subsequent changes |
| `SHA256SUMS` and `receipt.json` | File integrity and recorded execution metadata |

