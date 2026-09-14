---
title: "From Zeta-Zero Experiments to Alpha-Band EEG Topography"
subtitle: "A retrospective research account, numerical audit, and plan for independent validation"
author: "Luis M. Minier"
date: "11 September 2026"
lang: en-US
---

**Manuscript status:** Finalized computational research manuscript, version 1.0. Not peer reviewed and not a clinical validation study. The numerical replay is documented from the locally available OpenNeuro derivative EEG payloads, the Florida processed release, and the uploaded Czech archive. Clinical interpretation remains subject to independent review.

# Abstract

This paper describes a research path that began with questions about representations of Riemann zeta zeros, numerical rank, and the difference between a pattern in a coordinate system and a property of the underlying object. Those questions were carried into an existing EEG research program. Initial experiments combined spectral, recurrence, concentration, and multiscale features to search for Alzheimer’s disease (AD) markers. An approximately 400-feature representation produced weak held-out classification and a non-significant pooled effective-rank contrast. These negative results led to a simpler question: does the distribution of relative alpha power across scalp electrodes differ from a healthy reference pattern?

A score defined as one minus the spatial Pearson correlation with a training-control template was evaluated in OpenNeuro ds004504, a Florida State/OSF-derived feature table, and a Czech/Figshare archive. The present audit reproduced alpha AD/control AUCs of 0.8573, 0.8323, and 0.9546 using cohort-specific training-fold control templates. Applying the OpenNeuro control template without fitting external controls gave AUCs of 0.8188 in Florida and 0.7841 in the Czech cohort. Independently scrambling electrode assignments reduced median external alpha AUCs to approximately 0.50. Seven Czech participants labeled mild cognitive impairment (MCI) had an exploratory source-template AUC of 0.9272 against 102 controls.

These numbers support coordinate-dependent discrimination in the supplied representations. They do not establish causation, AD specificity, prospective early detection, or a transportable diagnostic threshold. OpenNeuro raw reconstruction matched the supplied features to floating-point precision. Florida was rechecked at the derived-feature level. Czech reconstruction reproduced the results using the 19-channel order reported in the original peer-reviewed Czech study. That published sequence exactly matches the input order used by the reconstruction. The article does not separately document the MATLAB serialization indices for every stored array type, so the storage-to-label linkage is supported by the source publication but is not claimed as independently proven from file metadata alone. Preprocessing was not identical across cohorts. The proposed contribution is therefore an auditable hypothesis and baseline, not a clinical diagnostic claim or a connection between zeta zeros and neurodegeneration.

**Keywords:** EEG; alpha topography; Alzheimer’s disease; mild cognitive impairment; reference-template deviation; reproducibility; negative results; dimensionality.

# Plain-language summary

An EEG records changing electrical voltages at electrodes on the scalp. This work asks whether the *arrangement* of a familiar rhythm across those electrodes contains information that an average power value misses. The comparison is like comparing the shape of two temperature maps, rather than just comparing their average temperatures. It is not a map of individual neurons or a direct picture of damaged tissue.

The research did not follow a straight line. I initially looked for structure using more elaborate mathematical representations. Some apparent advantages disappeared when the comparison became fairer. A large collection of EEG measurements did not reliably identify the disease. The method that remained worth testing was simpler: compare one person’s alpha-power pattern with a reference made from healthy controls.

The resulting scores separated labeled groups in the available data. Important qualifications remain. The most dramatic Czech result could be affected by differences in how patient and control files were stored and mapped to electrode names. The Florida data had already been processed and were much shorter than the source recordings. A fixed decision cutoff did not transfer reliably in the earlier audit. The seven MCI cases are a reason to investigate further, not evidence that the score predicts Alzheimer’s disease.

# 1. How the question developed

## 1.1 Starting with zeros, coordinates, and numerical stability

My immediate route into this phase of the work came from experiments involving the Riemann zeta function and its zeros. I had also been working with signal representations and EEG, so this was a back-and-forth investigation rather than a clean progression from one field to another.

For real part greater than one, the zeta function is defined by

$$
\zeta(s)=\sum_{n=1}^{\infty}n^{-s}.
$$

Its continuation and zeros belong to analytic number theory. The Riemann hypothesis concerns the real parts of its nontrivial zeros. A finite image, spectral fit, or EEG experiment does not answer that question [1]. In my experiments, zero ordinates and arithmetic constructions were treated as inputs to numerical representations. I wanted to know which apparent structures survived a change of basis, which were artifacts of filtering, and which were unreliable because the matrices were poorly conditioned.

The retained research record is specific about what did not follow. Entropy reductions obtained by changing a smoothing parameter did not establish special arithmetic significance for the Basel constant or silver ratio. A proposed entropy law did not become an RH lemma. A finite positive matrix did not prove positivity over every possible test function. Very small eigenvalues required numerical error control, not stronger language [2].

The useful lesson was not that prime numbers explain brain disease. It was that a representation can manufacture a persuasive pattern. Before interpreting that pattern, I had to identify what was being measured, the comparison being made, and the transformations that would leave the result unchanged.

## 1.2 What the RFT work contributed, and what it did not

The project used “RFT” for related but non-identical experiments. One line concerned nonuniform phase grids and unitary or polar-factor constructions. Another encoded an EEG segment as a sequence of SU(2) matrices and summarized a recurrence-like phase-variance curve. These are not interchangeable algorithms. A claim made for a complete unitary transform cannot simply be transferred to a nonlinear encoding followed by feature selection.

The EEG recurrence experiments kept quantities such as a minimum variance, the lag of that minimum, basin width, local slopes, and a second minimum. The intention was to retain more information than a single favorable minimum. Historical signal-reconstruction improvements were motivation for using these tools, but improved reconstruction is not evidence of improved disease discrimination [2,3]. A transform can reconstruct both patients and controls better without helping tell them apart.

The eventual alpha-template baseline reported here uses Welch spectral power. It does not use zeta zeros, a silver-ratio parameter, or SU(2) operators. That separation is essential. The RFT work helped generate questions and negative controls; it is not the mechanism responsible for the baseline AUCs in this paper.

## 1.3 The Navier–Stokes connection was methodological

OpenAI’s September 2026 discussion of a Navier–Stokes construction prompted questions about concentration, scaling, and cancellation [4]. I asked whether related diagnostic quantities might expose structure in EEG that ordinary averages concealed. That motivated concentration and multiscale feature families, not a claim that scalp EEG satisfies the Navier–Stokes equations.

The shared idea was to examine how structure changes with scale and representation. There is no derivation here from fluid dynamics to Alzheimer pathology. A visually similar wave pattern is not evidence of the same governing equations. This paper treats that episode as part of the research history, not as a mathematical foundation for the clinical interpretation.

## 1.4 The practical problem: too many descriptions, too little stable information

The initial EEG feature table contained 65 AD/control subjects and 410 columns including metadata, with 404 candidate numeric features and approximately 400 surviving the pooled preprocessing. Spectral, recurrence, concentration, and multiscale measurements were aggregated across channels using mean, standard deviation, minimum, and maximum.

The strongest screened variable was cross-channel variability in relative theta power. Its apparent AUC was 0.7500 and its uncorrected p-value was 0.000587, but its false-discovery-rate-adjusted value was 0.229923. The top recurrence and multiscale variables also failed the multiple-testing threshold. The 16-feature model’s recorded outer-fold AUC was 0.613 and balanced accuracy was 0.546 [3].

These are negative findings for the proposed panel, not evidence that a hidden disease manifold had been located. Repeated feature selection across overlapping training folds was useful for describing stability, but it was not independent replication. The low held-out performance justified changing the question; it did not justify inventing a biological explanation for why the model struggled.

# 2. Why the dimensionality explanation had to change

## 2.1 Three meanings of “dimension”

A feature count, an effective covariance rank, and a dynamical complexity estimate answer different questions. A table with 400 columns has 400 measured coordinates. It need not contain 400 independent directions of variation. Nor does its rank tell us the number of dynamical degrees of freedom in a person’s brain.

For a centered subject-by-feature matrix, write the following, where superscript $H$ denotes complex conjugate transpose:

$$
X_c=U\,\mathrm{diag}(s_1,\ldots,s_r)\,V^{H},
\qquad \lambda_k=\frac{s_k^2}{n-1},
\qquad p_k=\frac{\lambda_k}{\sum_j\lambda_j}.
$$

The covariance-spectrum quantities used in the earlier experiments were

$$
D_{\mathrm{eff}}=\exp\!\left(-\sum_k p_k\log p_k\right),
\qquad
D_{\mathrm{PR}}=\frac{(\sum_k\lambda_k)^2}{\sum_k\lambda_k^2}.
$$

They summarize how evenly variance is distributed over linear modes. They are not correlation dimension, fractal dimension, or a direct count of neural processes. Here “effective rank” specifically uses normalized *covariance eigenvalues*, rather than an alternative definition based on unsquared singular values.

The pooled result at 28 retained coordinates was 12.5405 for AD and 8.2987 for controls. However, the recorded permutation p-value was 0.4228, with a bootstrap interval for the gap spanning zero. It did not establish population-level dimensionality inflation [3].

## 2.2 A numerical artifact in the earlier interpretation

For a centered matrix with $n$ subjects,

$$
\operatorname{rank}(X_c)\leq\min(p,n-1).
$$

The control group had 29 people. Its centered observations therefore occupy at most 28 linearly independent directions. A PCA fitted and reconstructed on those same observations can achieve zero reconstruction error at 28 components regardless of a biological explanation. The AD group had 36 people and a different rank ceiling. Earlier wording that treated the control reconstruction endpoint as evidence of a simpler healthy brain was wrong.

A fair rank comparison must address group size, scaling, missing features, and finite-sample uncertainty. Resampling with replacement creates duplicate rows and changes the number of distinct observations. Such effects matter especially when the sample is small relative to the feature count.

## 2.3 Within-person and between-person variation

A matrix whose rows are people describes differences *between people*. A matrix whose rows are EEG windows from one person describes variation *within that recording*. The corresponding covariance decomposition is

$$
\operatorname{Cov}(X)
=\mathbb{E}\{\operatorname{Cov}(X\mid I)\}
+\operatorname{Cov}\{\mathbb{E}(X\mid I)\},
$$

where $I$ identifies the person. Effective rank is nonlinear, so the effective ranks of these two terms do not add.

Lower temporal complexity within individuals can coexist with greater heterogeneity between individuals. But that possibility is not itself a result. Our spectral window-fingerprint experiments did not supply a convincing general within-person complexity difference. They also used non-overlapping windows, which should not have been called statistically independent merely because they did not overlap.

## 2.4 Spatial summaries were not spatial maps

The original mean/standard-deviation/minimum/maximum summaries discard electrode identity. Reordering a person’s electrodes leaves those summaries unchanged. Therefore an electrode-identity ablation cannot explain a change in that original table by itself: the identity was already absent.

The later scalp-topography test was a new representation. It kept one feature per named electrode. Its motivation came from the earlier negative results, but it did not retroactively prove that those earlier results were caused by anatomical heterogeneity.

# 3. Data and provenance

Three datasets entered the current numerical audit. The datasets are distinct; this is not three independent research teams reproducing an analysis. The same computational workflow was applied to different cohorts.

| Dataset | Records used in this audit | Representation and replay status |
|:--|:--|:--|
| OpenNeuro ds004504 | 36 AD, 29 controls, 23 FTD | All 88 locally available derivative `.set` EEG payloads reconstructed and checked |
| Florida State / OSF | 80 AD, 12 controls | Public processed ADFSU release (`X.dat`, `y.dat`, `meta.json`) plus derived feature table; processed/feature-level replay verified |
| Czech / Figshare | 57 usable AD, 102 controls, 7 MCI | Uploaded `dataset.zip`; reconstructed with the 19-channel sequence reported by Cejnek et al. |

## 3.1 OpenNeuro discovery dataset

The ds004504 data descriptor provides the clinical cohort and acquisition context [5]. The uploaded snapshot identifies version 1.0.9 and CC0 distribution [6]. The EEG files inspected here have 19 named scalp channels at 500 Hz; their stored reference field reads A1 A2. This is the derivative-data reference, not an assertion that every stage of original acquisition used the same reference.

All 88 uploaded payloads matched the SHA-256 values encoded in the derivative pointers of the supplied GitHub/DataLad snapshot. Duplicate uploads were deduplicated by subject and byte hash. Recomputing the five-band features from the actual EEG samples reproduced the saved feature table with maximum absolute difference $4.44\times10^{-16}$. This is strong computational provenance for the source table. It is not independent verification of clinical labels.

## 3.2 Florida external dataset

The associated publication describes 80 probable-AD and 12 healthy eyes-closed recordings, 19 scalp electrodes, 128-Hz sampling, and eight-second segments previously limited to 0.5–30 Hz [7,8]. Earlier execution used a processed LEAD release derived from the OSF data, with resampled, overlapping segments [9]. The stored feature table is the input replayed in the present audit.

The original Florida signal-to-feature reconstruction was not independently repeated during this manuscript build. A second technical problem is unavoidable: a 4096-sample Welch window with 2048-sample overlap cannot be applied literally to an 800-sample processed or 1024-sample original eight-second recording. The historical external run shortened the spectral window. The score formula and band definitions were retained, but the raw extractor was not unchanged. Prior filtering above 30 Hz also prevents a truly equivalent five-band denominator.

## 3.3 Czech archive and channel provenance

The Czech dataset contains nominally 59 AD, seven MCI, and 102 controls [10,11]. AD33 and AD44 have no usable fragments. Ten additional patient fragments with 17, 18, or 20 columns were excluded rather than guessing the missing or extra channels. The retained sample is 57 AD, seven MCI, and 102 controls.

The archive combines patient `export` arrays with control `segmenty` arrays and two additional control fragment folders. The reconstruction retained 19 columns from valid patient fragments and the first 19 rows from the control arrays. The peer-reviewed source reports its per-channel analysis in the sequence `Fp1, Fp2, F7, Fz, F3, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz, P4, T6, O1, O2` [10]. This is exactly the input sequence used by the reconstruction before reordering to the frozen OpenNeuro output order. That agreement materially strengthens channel provenance. The paper does not separately state that every MATLAB `export` column and `segmenty` row was serialized in that sequence, so this manuscript does not elevate the match into a stronger file-format claim than the source supports.

The archive readme specifies original rates of 256 or 128 Hz. The original study describes harmonization to 128 Hz [10]. The replay follows the documented resampling and within-fragment PSD rules. The seven MCI/control alpha maps reproduce the saved table exactly. Final input checks identified zero total five-band power at the mapped Cz coordinate in controls `26887fir` and `7147fir`. The denominator floor converts those entries to zero relative power rather than a normalized five-band distribution. They are retained in the recorded primary calculation and explicitly flagged so that future replication can prespecify exclusion or missing-channel handling.

# 4. The spectral-topography method

## 4.1 From time series to band power

Let $x_{i,c}[n]$ be the EEG for subject $i$, electrode $c$, and sample $n$. Welch’s method averages windowed periodograms [12]. With a window $w[n]$ of length $L$, sampling rate $F_s$, and $K$ windows, a one-sided density estimate is

$$
\widehat S_{i,c}(f_k)=
\frac{g_k}{K F_s\sum_{n=0}^{L-1}w[n]^2}
\sum_{j=1}^{K}
\left|\sum_{n=0}^{L-1}
 w[n]\,\widetilde x_{i,c,j}[n]e^{-2\pi\mathrm{i}kn/L}\right|^2.
$$

Here $\widetilde x$ is the detrended segment and $g_k$ is the one-sided doubling factor, except at DC and the Nyquist frequency. The source computation uses a Hann window, constant detrending, $L=4096$, and 2048 overlapping samples. It operates over the available full derivative recording.

The five band intervals are delta 1–4 Hz, theta 4–8 Hz, alpha 8–13 Hz, beta 13–30 Hz, and gamma 30–45 Hz. Bins use a lower-inclusive, upper-exclusive rule, except gamma includes its upper boundary. Power is calculated by trapezoidal integration over the included bins:

$$
P_{i,b,c}=\int_{f\in b}\widehat S_{i,c}(f)\,df.
$$

The discrete bin rule is part of reproducibility: it is not identical to analytically integrating a continuous spectrum exactly to every band edge.

For Czech fragments, spectra are computed within each retained fragment, not across concatenation boundaries. A 256-Hz fragment is resampled to 128 Hz. Window length is capped at available samples and overlap at half that length, up to the original 2048 samples. Fragment powers are combined with duration-proportional weights. These are documented adaptations, not a claim of identical spectral resolution across datasets.

## 4.2 Relative power and a 19-electrode vector

At each electrode,

$$
R_{i,b,c}=\frac{P_{i,b,c}}{\sum_{q=1}^{5}P_{i,q,c}},
\qquad
\mathbf{x}_{i,\alpha}=(R_{i,\alpha,c})_{c=1}^{19}.
$$

This removes a common multiplicative gain in the band powers at that electrode. It does not remove reference effects, differences in noise spectra, or changes in the denominator caused by other bands. A change in relative alpha can occur because alpha changes, because another band changes, or both.

The vector preserves electrode names. Its entries are not interchangeable when it is compared with an anatomically labeled reference. However, the word “topography” here means a scalp-electrode pattern, not a reconstructed cortical source map.

## 4.3 A healthy-reference deviation score

For training controls $H_{\mathrm{train}}$, define

$$
\mathbf{h}_{\alpha}=
\frac{1}{|H_{\mathrm{train}}|}
\sum_{j\in H_{\mathrm{train}}}\mathbf{x}_{j,\alpha}.
$$

The score is

$$
M_\alpha(\mathbf{x})=1-\rho(\mathbf{x},\mathbf{h}_\alpha),
$$

where correlation is computed across electrodes, not across time. After centering and normalizing the vectors,

$$
\mathbf{u}=\frac{\mathbf{x}-\bar x\mathbf{1}}
{\|\mathbf{x}-\bar x\mathbf{1}\|_2},\qquad
\mathbf{v}=\frac{\mathbf{h}-\bar h\mathbf{1}}
{\|\mathbf{h}-\bar h\mathbf{1}\|_2},
$$

we have

$$
M_\alpha=1-\mathbf{u}^{T}\mathbf{v}
=\frac12\|\mathbf{u}-\mathbf{v}\|_2^2.
$$

Thus the score compares the *shape* of the maps. It is unchanged by a positive scalar amplification and uniform offset of either map, considered at this vector stage. Its range is zero to two; it is not a probability. At the input level, normalized band powers should sum to one except for the two explicitly flagged legacy Czech zero-power channels. A flat map has undefined correlation and must be flagged, not assigned a convenient score.

Earlier descriptions called this a “healthy manifold.” The implementation is more modest: it is a mean healthy template followed by correlation distance. It does not fit a nonlinear manifold. Healthy-reference novelty detection is not a new general idea; the original Czech study itself investigated novelty detection [10]. No claim of worldwide priority is made for the formula.

## 4.4 Two different validation questions

**Local out-of-fold scoring.** Five stratified subject folds are used. For each test fold, the healthy template is built only from controls in the other four folds. The score has no learned feature weights. AD or FTD labels identify the comparison and fold stratification, but no test subject supplies the reference for its own prediction.

**Source-template transfer.** The mean map from all 29 OpenNeuro controls is applied to every external subject. No Florida or Czech control is used to fit that reference. This is the stricter transfer test of a specific reference. Local external OOF scoring instead asks whether the same method works after a new cohort supplies training controls. Those questions must not be presented as the same experiment.

# 5. Statistical tests and their limits

## 5.1 What AUC measures

With case scores $s_i$ and control scores $s_j$, empirical AUC is

$$
\widehat{\mathrm{AUC}}=
\frac{1}{n_A n_H}
\sum_{i\in A}\sum_{j\in H}
\left[\mathbf{1}(s_i>s_j)+\tfrac12\mathbf{1}(s_i=s_j)\right].
$$

It measures how often a case is ranked above a control. It is not the fraction of patients correctly diagnosed. Accuracy and balanced accuracy require a specified decision threshold. The score direction was kept fixed: larger healthy-template deviation means a higher case score. Values below 0.5 were not flipped after seeing the outcome.

## 5.2 Confidence intervals and permutations

The reported intervals use 5,000 stratified subject bootstrap resamples of the *already computed scores*. They are conditional on the fitted references and available sample. For OOF results, they do not include uncertainty from refitting the pipeline, earlier feature selection, or shared training samples. They should not be advertised as complete clinical-performance uncertainty. Small clinical samples require particular caution [13].

For label permutations, local OOF analysis repeats the split and training-template construction under every shuffled label vector. Source-template analysis keeps the external scores fixed and permutes only labels. For an observed statistic $T$ and $B$ draws,

$$
p=\frac{1+\sum_{b=1}^{B}\mathbf{1}(T_b\geq T)}{B+1}.
$$

The plus-one correction prevents a Monte Carlo p-value from being reported as zero [14]. The current AUC audit uses 2,000 permutations. Its smallest reportable value is $1/2001=0.00049975$. These are one-sided tests of the recorded larger-deviation hypothesis. They do not correct for confounding that makes labels non-exchangeable with respect to acquisition conditions.

Holm adjustment across the 12 replayed AUC endpoints is included in the machine-readable table. It is not a correction for every decision made during the preceding exploratory search. The initial feature search used Benjamini–Hochberg correction [15]. Neither adjustment converts the conversation’s sequential choices into a prospective registered trial.

## 5.3 Group agreement without a diagnostic score

For group $G$, define

$$
\bar r_G=\frac{2}{n_G(n_G-1)}
\sum_{i<j;\,i,j\in G}\rho(\mathbf{x}_{i,\alpha},\mathbf{x}_{j,\alpha}),
\qquad T=\bar r_H-\bar r_A.
$$

Although there are many pairs, pairs sharing a person are not independent observations. Significance was therefore assessed by permuting *subject labels*, not by treating pair counts as a larger sample. The current audit uses 5,000 permutations for this test.

## 5.4 What coordinate scrambling can establish

Two controls are necessary. If the **same** permutation is applied to every subject and the reference, the score must remain unchanged. That is a mathematical check on indexing. If a **different** permutation is applied to each subject while the reference stays fixed, electrode correspondence is broken.

Loss of discrimination under the second test shows that the implementation uses coordinate correspondence. It does not identify the origin of that information. Genuine physiology, reference differences, and group-specific channel-mapping mistakes can all depend on coordinates.

Sorting each subject’s values is a separate ablation. It keeps the distribution but changes every map into order statistics. Sorting mechanically makes many vectors more alike; the rise in correlation is not a causal estimate of the percentage of disease “explained by location.” Appendix A gives the algebra.

# 6. Results from the present replay

## 6.1 Alpha deviation

Table 1 contains results recomputed for this manuscript from the supplied source and Florida tables and the reconstructed Czech table. Numbers from earlier messages are not silently averaged together. Slight interval differences from earlier reports reflect the present fixed resampling seeds.

**Table 1. Alpha-template discrimination.** Confidence intervals are fixed-score, subject-bootstrap intervals, with the limitations in Section 5.2.

| Comparison | Reference | AUC | Conditional 95% CI |
|:--|:--|--:|:--|
| OpenNeuro AD / control | Training-fold controls | 0.8573 | 0.7567–0.9406 |
| OpenNeuro FTD / control | Training-fold controls | 0.8291 | 0.7061–0.9295 |
| Florida AD / control | Training-fold controls | 0.8323 | 0.6604–0.9771 |
| Florida AD / control | OpenNeuro controls | 0.8188 | 0.6500–0.9542 |
| Czech AD / control | Training-fold controls | 0.9546 | 0.9226–0.9811 |
| Czech AD / control | OpenNeuro controls | 0.7841 | 0.7021–0.8566 |
| Czech MCI / control | OpenNeuro controls | 0.9272 | 0.8151–0.9986 |


For every alpha endpoint in Table 1, the current AUC permutation p-value is 0.00049975 at the 2,000-draw resolution. The corrected value across the 12 audit endpoints is approximately 0.0060. These tests support discrimination under the current assumptions; they do not resolve the Czech row-mapping issue or the selection history.

The strongest Czech local AUC, 0.9546, uses Czech training controls and can exploit cohort-specific regularities. The source-template AUC, 0.7841, is the more demanding transfer result. Florida shows the same distinction: 0.8323 with local training controls and 0.8188 with the source reference. The source-template values are the appropriate numbers when discussing transport of a fixed healthy reference.

Across 100 fold seeds, source alpha AD/control AUC averaged 0.8504 with a standard deviation of 0.0061; Florida averaged 0.8308 with standard deviation 0.0050; Czech averaged 0.9551 with standard deviation 0.0008. Those narrow ranges indicate limited sensitivity to fold assignment within these fixed samples. They are not 100 new clinical replications.


![Figure 1. Alpha AUCs from the executed audit. Error bars are conditional fixed-score bootstrap intervals, not complete clinical-performance uncertainty. Czech results retain the channel-mapping qualification.](figures/alpha_auc_audit.png){width=5.2in}

## 6.2 Delta did not transfer as well

Delta was the earlier primary marker and is retained in the record rather than replaced by a favorable alpha-only narrative.

**Table 2. Delta-template discrimination.**

| Comparison | Reference | AUC | Conditional 95% CI |
|:--|:--|--:|:--|
| OpenNeuro AD / control | Training-fold controls | 0.8764 | 0.7845–0.9521 |
| OpenNeuro FTD / control | Training-fold controls | 0.8546 | 0.7406–0.9460 |
| Florida AD / control | Training-fold controls | 0.7354 | 0.5229–0.9167 |
| Florida AD / control | OpenNeuro controls | 0.7469 | 0.5469–0.9177 |


The current Florida delta permutation p-values are 0.0030, but the AUCs are materially lower than in the source cohort. Alpha therefore became the prioritized cross-cohort candidate after Florida, not before the entire investigation began. The Czech alpha test followed that decision. A future study must treat this as the end of discovery and begin a genuinely prespecified evaluation.

## 6.3 Alpha agreement between people

**Table 3. Mean pairwise alpha-map correlations.** “Case” refers to the group in the first column.

| Cohort and case group | Case agreement | Control agreement | Difference |
|:--|--:|--:|--:|
| Source A | 0.5164 | 0.8627 | 0.3462 |
| Source F | 0.5975 | 0.8627 | 0.2652 |
| Florida A | 0.3232 | 0.6517 | 0.3285 |
| Czech A | 0.0254 | 0.6492 | 0.6238 |
| Czech MCI | -0.0626 | 0.6492 | 0.7118 |


The current subject-permutation p-value is 0.0026 for the Florida agreement gap and 0.00020, at Monte Carlo resolution, for the other rows. The repeated use of the same controls in AD and MCI comparisons is explicit; these are not independent replications of each other.

The large Czech gap deserves skepticism as well as attention. It is a numerical fact under the implemented mapping, but the patient/control storage-layout difference is aligned with diagnosis. An indexing or acquisition explanation must be excluded before calling that gap a biological loss of organization.

## 6.4 Spatial controls

**Table 4. External alpha scores under coordinate ablations.** Scramble ranges describe 1,000 independent subject-wise channel randomizations, not uncertainty intervals for the clinical AUC.

| External comparison | Actual alpha AUC | Scrambled median | Scramble 95% range | Sorted AUC |
|:--|--:|--:|:--|--:|
| Florida AD / control | 0.8188 | 0.4948 | 0.3197–0.6729 | 0.5240 |
| Czech AD / control | 0.7841 | 0.5019 | 0.4114–0.5882 | 0.4097 |
| Czech MCI / control | 0.9272 | 0.4972 | 0.2744–0.7073 | 0.3950 |


A common permutation of subjects and template preserved every score to within $4.44\times10^{-16}$. That exact control passed. Independently scrambled maps produced median AUCs near chance. This is evidence of coordinate dependence, not proof that values occur randomly in diseased brains.

The Czech sorted AUCs are below 0.5. They are reported in the fixed direction rather than inverted. They must not be described as exactly chance or as proof that value distributions contain no information.

## 6.5 The seven MCI cases

The source-template MCI/control AUC was 0.9272, with a conditional interval of 0.8151–0.9986. The case mean score was 1.1023 and the control mean 0.4552. The corresponding one-sided Mann–Whitney calculation was $7.18\times10^{-6}$; the separately recomputed permutation test reached the stated 2,000-draw resolution. The seven individual scores are supplied in Appendix C and in the data supplement.

This establishes separation of the **seven participants labeled MCI** from the supplied controls under the implemented representation. It does not establish that the same individuals were measured before their later AD diagnosis. No conversion outcome or biological confirmation of AD etiology was used. MCI is a clinical syndrome; its identification is not interchangeable with a diagnosis of MCI due to AD [16].

The MCI mean was higher than the Czech AD mean of 0.9184 under the same source template. Thus this result does not provide a monotonic healthy-to-MCI-to-AD severity scale. The local MCI AUC of 0.9902 is included in the audit CSV but is not emphasized as a clinical estimate. Seven cases, shared controls, and the mapping uncertainty make such an interpretation untenable.

## 6.6 Failures and stress tests retained from earlier records

Earlier audit files report that common-average rereferencing reduced source delta AUC from approximately 0.876 to 0.674 and alpha from approximately 0.857 to 0.785. They report lower, but above-chance, performance after restricting recordings to a common duration. They also report failure of source-trained numerical cutoffs in Florida, including delta balanced accuracy of 0.50 when all external records were called positive [3].

Those are **historical stress-test results**, not newly rerun endpoints in the present score replay. They are archived and marked accordingly. Their proper role is to identify vulnerability and direct independent testing, not to add unverified rows to the main table. Likewise, earlier age/sex regression p-values do not justify stating that demographic confounding has been eliminated.

# 7. What the evidence does and does not mean

## 7.1 The finding that survives

The clearest supported statement is: **in the supplied and reconstructed feature representations, alpha scalp-map deviation contains information associated with the clinical group labels, and part of that discrimination depends on electrode correspondence.**

This statement is narrower than “dementia scrambles the brain map.” It avoids saying the measurements are random, that alpha is the cause of impairment, or that every healthy brain shares a universal pattern. It also leaves the source-versus-external preprocessing and mapping qualifications attached to the result.

The source FTD/control result shows that the score is not established as AD-specific. No new FTD or Lewy body disease cohort was tested externally. No result here identifies Default Mode Network disconnection, compensatory frontal circuitry, or posterior neuronal loss directly. Those are mechanistic hypotheses that require different measurements and designs.

## 7.2 A simpler alternative: signal-to-noise ratio

Even a correct electrode mapping would not settle the mechanism. Suppose the true centered map is $\mathbf{h}$ and a measured map is

$$
\mathbf{x}=a\mathbf{h}+\boldsymbol\varepsilon,
\qquad \boldsymbol\varepsilon\perp\mathbf{h}.
$$

Then

$$
\rho(\mathbf{x},\mathbf{h})=
\frac{a\|\mathbf{h}\|_2}
{\sqrt{a^2\|\mathbf{h}\|_2^2+\|\boldsymbol\varepsilon\|_2^2}}.
$$

A lower signal-to-noise ratio reduces the correlation even if the underlying spatial shape has not reorganized. A reduction in alpha amplitude, a shorter recording, or different residual artifacts can therefore raise the deviation score. Matched-noise simulations and reliability analyses are needed before interpreting deviation as a particular anatomical rearrangement.

## 7.3 Reference and preprocessing are part of the measurement

EEG voltages are relative measurements. If rereferencing is represented by a linear matrix $R$ and the cross-spectral matrix is $S(f)$, then

$$
S'(f)=R S(f)R^T.
$$

The diagonal power values generally change. Relative power and correlation distance do not make the marker reference-invariant. In addition, the source 4096-sample window is 8.192 seconds at 500 Hz but 32 seconds at 128 Hz. Holding a sample count fixed does not hold temporal resolution fixed. Capping short windows adds a further difference.

The transferred results therefore test a fixed scoring idea with documented dataset adapters, not one unmodified end-to-end acquisition and analysis protocol. A manuscript must say that plainly, even when the AUC is favorable.

## 7.4 Why significant p-values do not finish the argument

A label-permutation result asks whether the observed association is unusual under a specified exchangeability null. A machine, file layout, or preprocessing convention correlated with diagnosis can still yield a small p-value. Cross-validation also preserves that correlation when both train and test folds come from the same acquisition process.

Independent datasets are useful, but they do not automatically remove parallel biases. The Czech mapping assumption is particularly consequential. Florida has only 12 controls and short processed records. Source and external confidence intervals are conditional. The datasets were selected for availability, not sampled as a representative clinical deployment population. These limits prevent a claim of definitive clinical validation.

# 8. Intended research

## 8.1 Lock measurement provenance before further model development

The Czech peer-reviewed channel sequence now matches the reconstruction exactly, resolving the earlier uncertainty about which 19 anatomical labels the analysis intended. Future work should still obtain or preserve export-code/file-format documentation that explicitly links those labels to the MATLAB array indices in each storage layout. Sampling-rate and device membership should remain attached to each subject, and patient/control layouts should be processed through matched extraction paths where possible.

The Florida processed ADFSU release is locally available and is included in the reproducibility record, but the original OSF subject-level signals should still be reconstructed from their earliest available form for a preprocessing-complete replication. The short-record and 30-Hz limitations of the Florida source remain real protocol differences rather than missing paperwork.

## 8.2 Prodromal sensitivity and prediction

A larger MCI cohort should first test the unchanged score without searching bands or channels. Its sample size should follow a precision or power calculation, not an arbitrary target chosen after a small positive study. Controls should be sampled and acquired comparably.

The clinically harder question is longitudinal: among people with MCI at baseline, does the score predict later AD dementia or a biomarker-confirmed AD outcome? That needs converters and non-converters, a defined follow-up period, competing diagnoses, and a reference and threshold fixed before outcomes are examined. Cross-sectional MCI/control separation cannot substitute for that test [16].

## 8.3 Etiological specificity

FTD already limits an AD-specific interpretation. The next comparisons should include other dementias and non-neurodegenerative causes of cognitive symptoms, not just healthy volunteers. Lewy body disease, vascular conditions, medications, sleepiness, and recording artifacts are relevant alternative explanations to examine, not labels to infer from this score. A marker of generalized abnormality may still be useful, but it answers a different question from identifying AD etiology.

## 8.4 Non-stationary and RFT benchmarks

Welch averages over time. Transient bursts or changes in local spectral shape may therefore be missed. A candidate dynamic method could measure the same scalp pattern in successive windows and describe its reliability, drift, and recurrence. Non-harmonic or RFT features should enter as prespecified additions to, not replacements for, the recorded baseline.

The relevant comparison is incremental held-out performance:

$$
\Delta\mathrm{AUC}=
\mathrm{AUC}(\text{baseline plus candidate})-
\mathrm{AUC}(\text{baseline}).
$$

Both arms must use the same subjects and folds, with all tuning confined to training data. Paired uncertainty estimates should reflect the shared test subjects. A prettier transform image, lower reconstruction error, or higher in-sample AUC is not diagnostic improvement. New methods should also beat simple Fourier, wavelet, and matched-noise controls rather than only a weak implementation of the baseline.

## 8.5 Cross-regional coupling

Power maps omit phase relationships. For a cross-spectrum $S_{ij}$, coherency is

$$
C_{ij}(f)=\frac{S_{ij}(f)}{\sqrt{S_{ii}(f)S_{jj}(f)}}.
$$

Its imaginary part and phase-lag measures can reduce particular zero-lag mixing effects [17–19]. Candidate posterior/frontal electrode sets can be specified in advance, but scalp electrodes should not be equated with identified cortical hubs. Ordinary imaginary coherence, PLI, and wPLI are not demonstrations of directed causal communication. Connectivity would be a new benchmark with its own volume-conduction, source-mixing, and sample-size controls.

## 8.6 Calibration and practical use

External ranking is only one component of usefulness. A deployable test needs a threshold, sensitivity and specificity, uncertainty for individual decisions, and stability across devices, references, and populations. A common reference learned from a representative training cohort may help, but fitting a new site’s controls is adaptation, not zero-shot deployment. That distinction must remain visible in every performance table.

# 9. Reproducibility, authorship, and data availability

The supplement contains source and external feature tables, fresh Czech reconstruction including MCI, subject-level scores, permutation distributions, exclusions, input manifests, code, an executed notebook, and the research notes supporting the historical account. CSVs are attached as analysis data, not as substitutes for the original EEG. The multi-gigabyte raw recordings are not duplicated in the supplement; their authoritative dataset identifiers and reconstruction commands are supplied.

The source raw replay, Czech reconstruction, score calculations, subject permutations, and coordinate checks were executed during preparation of this manuscript. Their outputs are written by the included scripts. Earlier narrative reports are kept separately under `archive/` and are not presented as new independent evidence. The source control template can be regenerated from the attached features rather than trusted as a rounded constant copied from a message.

The author’s research direction and interpretation are presented as an account of his project. AI assistance was used for code development, drafting, and audit preparation. That assistance does not constitute independent peer review or clinical adjudication. Luis M. Minier must approve the final manuscript, confirm funding and competing-interest disclosures, and verify source permissions and any applicable secondary-analysis requirements before submission. No new participants were recruited for this analysis.

# 10. Conclusion

The path from zeta-zero experiments to EEG was useful because it exposed the same methodological danger in two different settings: a compelling feature-space pattern can be mistaken for a property of the underlying system. The zeta work did not prove a connection to neurodegeneration. The original high-dimensional EEG panel did not establish a reliable marker. The pooled rank contrast did not establish AD dimensionality inflation.

A simpler alpha-template score produced reproducible numerical discrimination in the available tables and reconstructions, including source-template transfer and a small MCI comparison. Those results justify independent checking of a spatial EEG hypothesis. They do not justify a claim that Alzheimer’s pathology, future conversion, or a universal clinical cutoff has been identified. In particular, the Czech channel mapping must be resolved before its unusually large separation is treated as confirmed physiology.

The work’s present value is an explicit question, a measurable baseline, and a record of tests that can fail. The next advance would be a verified acquisition and mapping pipeline followed by prospective, independently executed validation, not another favorable number added to the same research narrative.

# Appendix A. Mathematical checks that prevent overinterpretation

## A.1 A complete unitary basis does not change the singular spectrum

If $Q^{H}Q=QQ^{H}=I$, then

$$
(XQ)(XQ)^{H}=XQQ^{H}X^{H}=XX^{H}.
$$

Therefore $X$ and $XQ$ have the same singular values and covariance-spectrum effective dimensions. A full-rank phase matrix $V$ can be orthogonalized through $Q=V(V^{H}V)^{-1/2}$, but orthogonality alone does not create additional discriminative information. Truncation, nonlinear feature construction, coordinate weighting, and noise treatment can change the subsequent geometry. Those changes must be identified rather than credited vaguely to a special constant.

## A.2 Concentration changes with window length even under a simple null

For sample energies $e_n=x_n^2/\sum_jx_j^2$, the inverse participation ratio is $\sum_ne_n^2$. Under a stable independent-sample model with second and fourth moments $\mu_2$ and $\mu_4$,

$$
\mathrm{IPR}\approx\frac{\mu_4}{N\mu_2^2}.
$$

Similarly, $\|x\|_4/\|x\|_2$ scales approximately as $N^{-1/4}$ for fixed moments. A multiscale slope can therefore arise from sample counting, not a disease-specific law. Signed excess kurtosis creates a separate problem: taking its logarithm is undefined for non-positive values. Conditional omission can produce different available feature sets across people. These details help explain why the earlier concentration screen required stronger null controls.

## A.3 Sorting forces nonnegative centered association

For two sequences sorted in the same order,

$$
\sum_i(a_i-\bar a)(b_i-\bar b)
=\frac{1}{2n}\sum_{i,j}(a_i-a_j)(b_i-b_j)\geq0.
$$

Each pairwise product on the right is nonnegative. High correlations between sorted scalp vectors therefore need a careful null interpretation. The useful question is whether the *group comparison* changes under a specified ablation, not whether sorted subjects look impressively alike.

## A.4 AUC and effect size are related, not separate confirmations

For a fixed score direction, rank-biserial effect size is $2\mathrm{AUC}-1$. Reporting both is useful, but they are not independent pieces of evidence. Likewise, many subject-pair comparisons in an AUC do not increase the number of independent participants.

# Appendix B. Exact channel and preprocessing record

**Frozen output order:** Fp1, Fp2, F3, F4, C3, C4, P3, P4, O1, O2, F7, F8, T3, T4, T5, T6, Fz, Cz, Pz.

**Published Czech analysis order:** Fp1, Fp2, F7, Fz, F3, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz, P4, T6, O1, O2 [10].

This published sequence exactly matches the reconstruction input order. The remaining qualification is narrower: the article reports the channel sequence used for analysis but does not separately document the serialization indices of every MATLAB array layout. The complete exclusion list and storage-layout field accompany each reconstructed Czech record.

OpenNeuro processing uses the native 500-Hz derivative signals, stored A1/A2 reference, full available duration, and 4096/2048 Welch parameters. Czech processing uses native-rate metadata from the archive readme, polyphase downsampling where needed, within-fragment window caps, duration-weighted powers, and then relative-power normalization. Florida features were previously derived from short processed data. No claim of identical raw preprocessing is made across these three inputs.

# Appendix C. All seven MCI source-template scores

| Participant | Original sampling rate | Alpha deviation |
|:--|--:|--:|
| MCI1 | 256 Hz | 1.044047 |
| MCI2 | 256 Hz | 1.057331 |
| MCI3 | 256 Hz | 0.856473 |
| MCI4 | 256 Hz | 0.512807 |
| MCI5 | 128 Hz | 1.248154 |
| MCI6 | 128 Hz | 1.307084 |
| MCI7 | 128 Hz | 1.690212 |

The AUC corresponds to 662 correctly ordered MCI/control pairs out of 714. Those pairs arise from seven cases and 102 controls, not 714 independent observations. The archive’s cognitive subscore total is out of 100 and must not be mislabeled as the source cohort’s MMSE.

# Appendix D. How to reproduce the audit

Extract the supplement. In its root directory, install the recorded dependencies and run:

```bash
python -m pip install -r requirements.txt
python code/test_invariants.py
python code/audit_metrics.py --root .
```

The default audit uses 2,000 AUC label permutations, 5,000 fixed-score bootstrap resamples, 5,000 group-agreement permutations, 1,000 independent coordinate scrambles, and 100 split seeds. It writes results to `results/`. The executed notebook displays the same computations and the provenance limitations.

For optional raw reconstruction, provide the original datasets locally:

```bash
python code/rebuild_source.py --raw-root /path/to/eeg --root .
python code/rebuild_czech.py --zip /path/to/dataset.zip --root .
```

The source raw folder must contain the EEG payloads, not Git-annex pointers. Metadata are read from the supplement’s source table. Raw reruns retain the documented Czech mapping assumption; they do not resolve it. File checksums are listed in `SHA256SUMS.txt`. Source raw hashes and the Czech archive hash are listed separately under `provenance/`.

# References

[1] Apostol TM. Zeta and Related Functions, §25.10, Zeros. In: *NIST Digital Library of Mathematical Functions*. https://dlmf.nist.gov/25.10. Accessed 11 September 2026.

[2] Minier LM. *Riemann and zeta research: consolidated evidence record*. Research notes consolidated 7 September 2026. Unpublished project record; supplied with this manuscript under `provenance/RIEMANN_RESEARCH_CONSOLIDATED.md`. Historical results in that record are not independently certified by this paper.

[3] Minier LM. *EEG research outputs, evidence audits, and notebook records*. September 2026. Unpublished project materials supplied in the supplement. Earlier narrative reports are retained under `archive/`; the present executable outputs are under `results/`.

[4] OpenAI. *On the Navier–Stokes Millennium Prize Problem*. 8 September 2026. https://openai.com/index/navier-stokes-solution/. Cited as research motivation, not as evidence about EEG.

[5] Miltiadous A, Tzimourta KD, Afrantou T, et al. A Dataset of Scalp EEG Recordings of Alzheimer’s Disease, Frontotemporal Dementia and Healthy Subjects from Routine EEG. *Data*. 2023;8(6):95. https://doi.org/10.3390/data8060095.

[6] OpenNeuro. *ds004504*, version 1.0.9. Dataset. https://doi.org/10.18112/openneuro.ds004504.v1.0.9. Public mirror: https://github.com/OpenNeuroDatasets/ds004504. Dataset metadata identify CC0 distribution.

[7] Vicchietti ML, Ramos FM, Betting LE, Campanharo ASLO. Computational methods of EEG signals analysis for Alzheimer’s disease classification. *Scientific Reports*. 2023;13:8184. https://doi.org/10.1038/s41598-023-32664-8.

[8] Florida State University / OSF EEG data associated with Vicchietti et al. *OSF project 2v5md*. https://osf.io/2v5md/. Eyes-closed portion used through the derived representation described in the text.

[9] DL4mHealth. *LEAD: An EEG Foundation Model for Alzheimer’s Disease Detection*. Code and processed-data release. https://github.com/DL4mHealth/LEAD. ADFSU preprocessing notebook, recorded commit `ec35aadb1bc068fcacdcd8d036964514ca2a708f`; path `data_preprocessing/ADFSU/ADFSU_preprocessing.ipynb`.

[10] Cejnek M, Vysata O, Valis M, Bukovsky I. Novelty detection-based approach for Alzheimer’s disease and mild cognitive impairment diagnosis from EEG. *Medical & Biological Engineering & Computing*. 2021;59:2287–2296. https://doi.org/10.1007/s11517-021-02427-6.

[11] Čejnek M. *dataset.zip*. Figshare dataset. 2017. https://doi.org/10.6084/m9.figshare.5450293.v1. Uploaded archive and its internal readme were used for the present reconstruction.

[12] Welch PD. The use of fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms. *IEEE Transactions on Audio and Electroacoustics*. 1967;15(2):70–73. https://doi.org/10.1109/TAU.1967.1161901.

[13] Varoquaux G. Cross-validation failure: Small sample sizes lead to large error bars. *NeuroImage*. 2018;180:68–77. https://doi.org/10.1016/j.neuroimage.2017.06.061.

[14] Phipson B, Smyth GK. Permutation P-values should never be zero: calculating exact P-values when permutations are randomly drawn. *Statistical Applications in Genetics and Molecular Biology*. 2010;9:Article 39. https://doi.org/10.2202/1544-6115.1585.

[15] Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society, Series B*. 1995;57(1):289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x.

[16] Albert MS, DeKosky ST, Dickson D, et al. The diagnosis of mild cognitive impairment due to Alzheimer’s disease: recommendations from the National Institute on Aging–Alzheimer’s Association workgroups on diagnostic guidelines for Alzheimer’s disease. *Alzheimer’s & Dementia*. 2011;7(3):270–279. https://doi.org/10.1016/j.jalz.2011.03.008.

[17] Nolte G, Bai O, Wheaton L, Mari Z, Vorbach S, Hallett M. Identifying true brain interaction from EEG data using the imaginary part of coherency. *Clinical Neurophysiology*. 2004;115(10):2292–2307. https://doi.org/10.1016/j.clinph.2004.04.029.

[18] Stam CJ, Nolte G, Daffertshofer A. Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. *Human Brain Mapping*. 2007;28:1178–1193. https://doi.org/10.1002/hbm.20346.

[19] Vinck M, Oostenveld R, van Wingerden M, Battaglia F, Pennartz CMA. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. *NeuroImage*. 2011;55(4):1548–1565. https://doi.org/10.1016/j.neuroimage.2011.01.055.

[20] Additional dataset-requested attribution: Miltiadous et al., *DICE-Net*, DOI https://doi.org/10.1109/ACCESS.2023.3294618; AHEPA dataset scoping/benchmark record, DOI https://doi.org/10.1007/s11571-026-10464-w. These identifiers are supplied by the ds004504 metadata; neither is an independent validation of the present score.
