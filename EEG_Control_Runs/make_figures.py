from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;O=R/'results';rng=np.random.default_rng(271)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
s=pd.read_csv(O/'spectral_subject_windows.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.6))
for ax,col,title in zip(axes,['log_posterior_alpha','posterior_periodic_alpha','posterior_exponent'],['Posterior alpha power (log)','Posterior alpha above fitted background','Posterior background exponent']):
 for i,w in enumerate(['first60','middle60','last60']):
  for g,shift,color in [('C',-.17,'#197c86'),('A',.17,'#c55d42')]:
   v=s.loc[(s.cohort=='OpenNeuro')&(s.window==w)&(s.group==g),col].dropna().to_numpy();pos=i+shift;ax.scatter(pos+rng.uniform(-.07,.07,len(v)),v,s=9,alpha=.45,color=color);ax.plot([pos-.10,pos+.10],[np.median(v)]*2,color=color,lw=3,label=('Controls' if g=='C' else 'AD') if i==0 else None)
 ax.set_title(title,fontsize=10);ax.set_xticks([0,1,2],['First minute','Middle minute','Last minute']);ax.grid(axis='y',alpha=.15)
axes[0].legend();axes[1].set_ylabel('Mean fitted periodic contribution, log10 PSD')
fig.suptitle('Source EEG: posterior alpha and spectral background, by recording period')
fig.tight_layout(rect=[0,.02,1,.93])
for ext in ['png','svg']:fig.savefig(O/f'spectral_controls.{ext}',dpi=180)
plt.close(fig)
l=pd.read_csv(O/'lemon_subject_states.csv');c=pd.read_csv(O/'cap_subject_states.csv');fig,axes=plt.subplots(2,2,figsize=(11,8))
for ax,col,title in zip(axes[0],['score','log_posterior_frontal_alpha'],['LEMON: frozen alpha-pattern deviation','LEMON: log posterior/frontal alpha']):
 for sid,q in l.groupby('subject'):
  q=q.set_index('state').reindex(['EC','EO']);ax.plot([0,1],q[col],color='#197c86',alpha=.35,marker='o',ms=3)
 ax.set_xticks([0,1],['Eyes closed','Eyes open']);ax.set_title(title);ax.grid(axis='y',alpha=.15)
for ax,col,title in zip(axes[1],['log_posterior_frontal_alpha','log_theta_alpha'],['CAP: log occipital/frontal alpha','CAP: log theta/alpha']):
 for sid,q in c.groupby('subject'):
  q=q.set_index('state').reindex(['W','S1','S2']);ax.plot([0,1,2],q[col],color='#7665a0',alpha=.5,marker='o',ms=4)
 ax.set_xticks([0,1,2],['Wake','Stage 1','Stage 2']);ax.set_title(title);ax.grid(axis='y',alpha=.15)
fig.suptitle('Healthy-state controls: each line is one person')
fig.text(.5,.015,'CAP uses a reduced, documented montage. These state effects do not establish Alzheimer’s causation.',ha='center',fontsize=10)
fig.tight_layout(rect=[0,.04,1,.95])
for ext in ['png','svg']:fig.savefig(O/f'healthy_state_controls.{ext}',dpi=180)
plt.close(fig)
