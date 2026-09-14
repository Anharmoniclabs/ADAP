from pathlib import Path
import json,html,base64
import pandas as pd
R=Path(__file__).resolve().parent;O=R/'results'
s=pd.read_csv(O/'spectral_group_tests.csv');p=pd.read_csv(O/'individual_peak_tests.csv');t=pd.read_csv(O/'state_tests.csv');l=pd.read_csv(O/'lemon_subject_states.csv');c=pd.read_csv(O/'cap_subject_states.csv');fits=pd.read_csv(O/'spectral_subject_windows.csv')
source=s[(s.cohort=='OpenNeuro')&(s.comparison=='C')&s.window.isin(['first60','middle60','last60'])&s.factor.isin(['log_posterior_alpha','log_frontal_alpha','log_posterior_frontal_alpha','posterior_periodic_alpha','periodic_alpha_contrast'])]
q=fits.groupby(['cohort','window'])[['posterior_fit_ok','frontal_fit_ok']].agg(['sum','count']);q.columns=['_'.join(x) for x in q.columns];q=q.reset_index()
cap_manifest=json.loads((O/'cap_download_manifest.json').read_text());lemon_manifest=json.loads((O/'lemon_download_manifest.json').read_text())
cap_inc=sum(r['status']=='included' for r in cap_manifest)
summary=f'''# Executed EEG control results

The source-cohort posterior/frontal alpha difference survives an individualized frequency-band sensitivity, and the frozen19channel score responds to ordinary eye-condition changes in older healthy adults. These results narrow the measurement interpretation; they do not identify a molecular cause or establish Alzheimer-specific diagnosis.

## Scope

Source:88participants, with36AD/29controls for primary contrasts and23FTD for specificity contrasts; first8seconds and first/middle/last60seconds. Florida:80AD/12controls, eight seconds only. LEMON:74older candidates, {l.subject.nunique()}included paired participants after availability/channel requirements. CAP:16healthy candidates, {cap_inc}recordings with eligible signals/epochs; each paired comparison reports its own eligible n. Exclusion receipts, parser corrections and protocol amendments are included.

## Main results

1. Source posterior absolute alpha is lower in AD in all three60second periods after Holm correction across81planned group comparisons. Frontal alpha has no corrected group difference in these periods. A nonsignificant frontal result does not prove equal frontal power.
2. The posterior/frontal ratio remains lower in AD using an individualized band around each participant's highest fitted4–14Hz posterior peak: all three exploratory contrasts survive the separate six-test correction. Candidate peak frequency itself does not survive correction. Sub-8Hz peaks are not automatically identified as slowed alpha.
3. Background-adjusted posterior alpha is lower in AD after correction in the first and middle periods, but not the last; the background-adjusted spatial contrast survives correction only in the middle period. Therefore the effect is not demonstrated to be wholly independent of spectral background in every period.
4. The original8second spectra fail the fixed spectral-model quality gate in both cohorts. Their raw band-power tests remain available, but their spectral-decomposition parameters are not interpreted. Longer source spectra mostly pass; no Florida long recordings are invented.
5. In LEMON, eyes opening increases the frozen deviation score in30/34participants and lowers posterior/frontal alpha in29/34. Mean score changeEO−EC=0.322,95%CI[0.212,0.421], Holm p≈0.0008. The common19channel average-reference score also changes. This is evidence of state sensitivity, not a clinical false-positive rate or proof that eye opening explains the AD/control difference.
6. CAP stage2 increased theta/alpha in all11eligible participants (mean log-ratio change1.224;95%CI0.764–1.701;Holm p0.0040). The posterior/frontal alpha contrasts and stage1 theta/alpha contrast did not survive correction. These results are not a worst-case microsleep bound. CAP wake labels do not establish eye closure; states can come from different times of night and recording contexts differ from the clinical cohort. ECG regression/sham results are descriptive contamination sensitivities, not evidence for autonomic causation.
7. None of the source AD-versus-FTD factor contrasts survives the81-test correction. This does not prove equivalence, but AD specificity remains unestablished.

## CAP state results

'''+t[t.cohort=='CAP'].to_csv(index=False)+'''
## Supported interpretation

An AD-associated posterior alpha-power/topography difference is reproducible in the analyzed recordings and is robust to the tested individualized-band definition in the source cohort. The score also responds to normal eye-condition changes. The literature provides biological hypotheses, but this package does not measure synaptic loss, cholinergic integrity, amyloid, tau, or AD alpha reactivity.

The proposed follow-up is paired eyes-open/closed EEG in AD and comparison groups, ideally linked to MRI or other independent biomarkers. Schumacher et al.2020 is a concrete precedent with EEG and NBM-volume measurements; its data are available on reasonable request, not as a verified direct download here. https://doi.org/10.1186/s13195-020-00613-6

## Reproduction

See README.md for the offline command sequence. Exact analysis waveform extracts, full Florida archive, scripts, requirements, formulas, input hashes, person-level outputs, and PNG/SVG graphs are included. Full-length source/LEMON/CAP recordings are not duplicated in this control package. Statistical intervals are pointwise and these are retrospective analyses with documented amendments, not a preregistered causal experiment.
'''
(R/'FINDINGS.md').write_text(summary)
def table(d):return d.to_html(index=False,float_format=lambda v:f'{v:.6g}',border=0,escape=True)
def img(name):return '<img alt="'+name+'" src="data:image/png;base64,'+base64.b64encode((O/(name+'.png')).read_bytes()).decode()+'">'
body='<h1>EEG control experiments</h1><p class="lead">Posterior alpha, spectral background, individualized frequency bands, and healthy-state controls.</p>'
body+='<p><b>Executed results.</b> The source spatial difference persists under individualized bands. The score is also sensitive to ordinary eye opening. Biological causation and AD-specific diagnosis remain unestablished.</p>'
body+=img('spectral_controls')+img('healthy_state_controls')
body+='<h2>Paired healthy-state tests</h2><p>One observation per participant and condition. Differences are condition minus reference. Holm correction across8planned state endpoints; pointwise bootstrap confidence intervals.</p>'+table(t)
body+='<h2>Individualized-frequency sensitivity</h2><p>Exploratory; highest fitted posterior peak4–14Hz,±2Hz band. Missing peaks remain missing. Separate six-test correction.</p>'+table(p)
body+='<h2>Source spectral and regional contrasts</h2><p>AD versus controls. These p-values account for all81planned group tests; the complete table is included in results/spectral_group_tests.csv.</p>'+table(source[['window','factor','n_case','n_comparison','case_median','comparison_median','median_difference','ci_low','ci_high','holm_all_group_tests']])
body+='<h2>Spectral-model quality</h2><p>Fit gate:R²≥0.8 and error≤0.15log10units. Eight-second failures are not used to infer background or peaks.</p>'+table(q)
body+='<h2>Interpretation and methods</h2><pre>'+html.escape(summary)+'</pre><h2>Limitations for the paper</h2><pre>'+html.escape((R/'LIMITATIONS_PARAGRAPH.md').read_text())+'</pre>'
body+='<h2>Literature context</h2><pre>'+html.escape((R/'LITERATURE_CONTEXT.md').read_text())+'</pre>'
(R/'REPORT.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Minier EEG Control Experiments</title><style>body{font:16px system-ui,sans-serif;color:#203037;max-width:1400px;margin:40px auto;padding:0 24px;line-height:1.55}h1{font-size:36px}h2{margin-top:42px;color:#17656e}.lead{font-size:20px}img{max-width:100%;height:auto;margin:22px 0}table{font-size:12px;width:100%;border-collapse:collapse;display:block;overflow:auto}th,td{padding:8px;text-align:left;border-bottom:1px solid #dce2e5}th{background:#edf4f5}pre{white-space:pre-wrap;font:14px system-ui;line-height:1.6;background:#f6f8f8;padding:20px;border-radius:8px}</style>'+body+'</html>')
print('Report generated',R/'REPORT.html')
