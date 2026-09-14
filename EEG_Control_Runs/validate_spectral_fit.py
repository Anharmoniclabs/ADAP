from pathlib import Path
import json,numpy as np
from fooof import FOOOF
f=np.arange(2,30.001,.125);rows=[]
for exponent,height,center in [(1.5,.5,10),(2.2,.5,10),(1.5,.2,10),(1.5,.5,8.5)]:
 p=10**(2-exponent*np.log10(f)+height*np.exp(-(f-center)**2/(2*1**2)))
 fm=FOOOF(peak_width_limits=[1,8],max_n_peaks=6,min_peak_height=.1,peak_threshold=2,aperiodic_mode='fixed',verbose=False);fm.fit(f,p,[2,30]);peak=fm.peak_params_[np.argmax(fm.peak_params_[:,1])]
 assert abs(fm.aperiodic_params_[1]-exponent)<.03 and abs(peak[0]-center)<.1 and abs(peak[1]-height)<.03
 rows.append({'true_exponent':exponent,'fit_exponent':float(fm.aperiodic_params_[1]),'true_peak_center':center,'fit_peak_center':float(peak[0]),'true_height':height,'fit_height':float(peak[1])})
(Path(__file__).resolve().parent/'results/synthetic_fit_validation.json').write_text(json.dumps({'passed':True,'scope':'software recovery of known idealized spectra; not validation of biological model','cases':rows},indent=2))
print('Known-spectrum recovery passed')
