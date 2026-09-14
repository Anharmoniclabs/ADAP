# Executed EEG control results

The source-cohort posterior/frontal alpha difference survives an individualized frequency-band sensitivity, and the frozen19channel score responds to ordinary eye-condition changes in older healthy adults. These results narrow the measurement interpretation; they do not identify a molecular cause or establish Alzheimer-specific diagnosis.

## Scope

Source:88participants, with36AD/29controls for primary contrasts and23FTD for specificity contrasts; first8seconds and first/middle/last60seconds. Florida:80AD/12controls, eight seconds only. LEMON:74older candidates, 34included paired participants after availability/channel requirements. CAP:16healthy candidates, 11recordings with eligible signals/epochs; each paired comparison reports its own eligible n. Exclusion receipts, parser corrections and protocol amendments are included.

## Main results

1. Source posterior absolute alpha is lower in AD in all three60second periods after Holm correction across81planned group comparisons. Frontal alpha has no corrected group difference in these periods. A nonsignificant frontal result does not prove equal frontal power.
2. The posterior/frontal ratio remains lower in AD using an individualized band around each participant's highest fitted4–14Hz posterior peak: all three exploratory contrasts survive the separate six-test correction. Candidate peak frequency itself does not survive correction. Sub-8Hz peaks are not automatically identified as slowed alpha.
3. Background-adjusted posterior alpha is lower in AD after correction in the first and middle periods, but not the last; the background-adjusted spatial contrast survives correction only in the middle period. Therefore the effect is not demonstrated to be wholly independent of spectral background in every period.
4. The original8second spectra fail the fixed spectral-model quality gate in both cohorts. Their raw band-power tests remain available, but their spectral-decomposition parameters are not interpreted. Longer source spectra mostly pass; no Florida long recordings are invented.
5. In LEMON, eyes opening increases the frozen deviation score in30/34participants and lowers posterior/frontal alpha in29/34. Mean score changeEO−EC=0.322,95%CI[0.212,0.421], Holm p≈0.0008. The common19channel average-reference score also changes. This is evidence of state sensitivity, not a clinical false-positive rate or proof that eye opening explains the AD/control difference.
6. CAP stage2 increased theta/alpha in all11eligible participants (mean log-ratio change1.224;95%CI0.764–1.701;Holm p0.0040). The posterior/frontal alpha contrasts and stage1 theta/alpha contrast did not survive correction. These results are not a worst-case microsleep bound. CAP wake labels do not establish eye closure; states can come from different times of night and recording contexts differ from the clinical cohort. ECG regression/sham results are descriptive contamination sensitivities, not evidence for autonomic causation.
7. None of the source AD-versus-FTD factor contrasts survives the81-test correction. This does not prove equivalence, but AD specificity remains unestablished.

## CAP state results

cohort,condition,reference,factor,n,reference_mean,condition_mean,mean_paired_difference,ci_low,ci_high,p,n_increase,n_decrease,holm_state_tests
CAP,S1,W,log_posterior_frontal_alpha,10,0.2990082772448659,0.0965727418195456,-0.2024355354253202,-0.4433896933647338,0.0060932048934045,0.1491850814918508,3,7,0.1491850814918508
CAP,S1,W,log_theta_alpha,10,-0.6520069040358066,0.1014538779854774,0.7534607820212841,0.2537154988385737,1.279861539024859,0.0334966503349665,8,2,0.0923907609239076
CAP,S2,W,log_posterior_frontal_alpha,11,0.2949641368944536,-0.0271049006630412,-0.3220690375574949,-0.5596802236729259,-0.0838881721169772,0.0307969203079692,2,9,0.0923907609239076
CAP,S2,W,log_theta_alpha,11,-0.6408358101140369,0.5833270287310536,1.2241628388450905,0.7639664592941038,1.7005302902014758,0.000999900009999,11,0,0.003999600039996

## Supported interpretation

An AD-associated posterior alpha-power/topography difference is reproducible in the analyzed recordings and is robust to the tested individualized-band definition in the source cohort. The score also responds to normal eye-condition changes. The literature provides biological hypotheses, but this package does not measure synaptic loss, cholinergic integrity, amyloid, tau, or AD alpha reactivity.

The proposed follow-up is paired eyes-open/closed EEG in AD and comparison groups, ideally linked to MRI or other independent biomarkers. Schumacher et al.2020 is a concrete precedent with EEG and NBM-volume measurements; its data are available on reasonable request, not as a verified direct download here. https://doi.org/10.1186/s13195-020-00613-6

## Reproduction

See README.md for the offline command sequence. Exact analysis waveform extracts, full Florida archive, scripts, requirements, formulas, input hashes, person-level outputs, and PNG/SVG graphs are included. Full-length source/LEMON/CAP recordings are not duplicated in this control package. Statistical intervals are pointwise and these are retrospective analyses with documented amendments, not a preregistered causal experiment.
