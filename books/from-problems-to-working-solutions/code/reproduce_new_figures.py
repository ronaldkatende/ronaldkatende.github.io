"""Four vector figures for Chapters 9--12: illustrative or formula-derived only.

Run from the book root with matplotlib installed.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path('figures'); OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'pdf.fonttype':42})

# Chapter 9: all observations are invented teaching values.
fig, ax = plt.subplots(figsize=(6.5,3.5))
ax.plot([0,1],[60,78], '-o', lw=2, label='Early implementation (invented)')
ax.plot([0,1],[55,65], '-s', lw=2, label='Comparison (invented)')
ax.plot([0,1],[60,70], '--', lw=1.7, label='Treated counterfactual if parallel trends')
ax.annotate('Difference-in-differences = 8 points',xy=(1,74),xytext=(.11,76),
            arrowprops=dict(arrowstyle='->',lw=.8),fontsize=9)
ax.set(xticks=[0,1], xticklabels=['Before','After'], ylabel='Availability per 100 scheduled days',
       ylim=(50,86), title='Illustrative difference-in-differences')
ax.legend(loc='lower center',fontsize=8)
fig.tight_layout();fig.savefig(OUT/'ch09_did_illustrative.pdf');plt.close(fig)

# Chapter 10: analytic formula, not device measurements.
import numpy as np
recovery=np.linspace(.5,24,150)
availability=240/(240+recovery)
fig,ax=plt.subplots(figsize=(6.5,3.2))
ax.plot(recovery,100*availability,lw=2)
ax.scatter([3,12],[100*240/243,100*240/252],zorder=4)
ax.annotate('3 h repair',xy=(3,100*240/243),xytext=(6,99.0),
            arrowprops=dict(arrowstyle='->'),fontsize=9)
ax.annotate('12 h repair',xy=(12,100*240/252),xytext=(14,96.7),
            arrowprops=dict(arrowstyle='->'),fontsize=9)
ax.set(xlabel='Assumed mean repair time (hours)',ylabel='Modelled availability (%)',
       ylim=(90,100),title='Analytic availability with 240 h mean operation')
fig.tight_layout();fig.savefig(OUT/'ch10_repair_model.pdf');plt.close(fig)

# Chapter 11: invented population mixes; model errors held fixed.
fig,ax=plt.subplots(figsize=(6.5,3.2))
labels=['Urban','Rural'];xx=np.arange(2);w=.32
ax.bar(xx-w/2,[.8,.2],width=w,label='Source mixture (invented)')
ax.bar(xx+w/2,[.3,.7],width=w,label='Target mixture (invented)')
ax.set(xticks=xx,xticklabels=labels,ylabel='Population share',ylim=(0,1),
       title='Covariate shift: the same conditional errors, new mixture')
ax.legend(fontsize=9)
fig.tight_layout();fig.savefig(OUT/'ch11_shift_mixture.pdf');plt.close(fig)

# Chapter 12: correct solver-checked values from fully invented inputs.
fig,ax=plt.subplots(figsize=(6.5,3.2))
ax.scatter([76,83],[395,315],s=65)
ax.annotate('S2 + S3',xy=(76,395),xytext=(76.8,400),fontsize=10)
ax.annotate('S1 + S3',xy=(83,315),xytext=(78.5,324),fontsize=10)
ax.axvline(85,linestyle='--',lw=1,label='Invented budget limit = 85')
ax.set(xlim=(73,89),ylim=(285,425),xlabel='Opening cost (invented budget units)',
       ylabel='Weighted travel (person-km)',title='Two feasible plans: cost versus travel')
ax.legend(loc='upper right',fontsize=9)
fig.tight_layout();fig.savefig(OUT/'ch12_tradeoff.pdf');plt.close(fig)
print('Generated four labelled, vector PDF teaching figures.')
