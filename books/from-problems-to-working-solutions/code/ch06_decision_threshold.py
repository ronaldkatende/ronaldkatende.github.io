"""Illustrative decision math, not a trained model or health evidence."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
p=np.array([.08,.15,.23,.37,.48,.57,.73,.88])
y=np.array([0,0,0,1,0,1,1,1]) # invented observations
c_false_alarm,c_miss=2.0,7.0
threshold=c_false_alarm/(c_false_alarm+c_miss)
choice=(p>threshold).astype(int)
loss=np.where((choice==1)&(y==0),c_false_alarm,np.where((choice==0)&(y==1),c_miss,0))
def tally(actions):
    predicted_positive=(actions==1)
    predicted_negative=(actions==0)
    return {
        'false_positive':int(np.sum(predicted_positive & (y==0))),
        'false_negative':int(np.sum(predicted_negative & (y==1))),
        'warning':int(np.sum(predicted_positive)),
        'not_warning':int(np.sum(predicted_negative)),
        'deferred':int(np.sum(actions==-1))
    }
counts=tally(choice)
# Conditional expected losses from calibrated probabilities are different
# from realised losses observed in eight deliberately invented labels.
expected_auto=np.minimum((1-p)*c_false_alarm,p*c_miss)
# Illustrative fixed cost of human review, conditional on review being available.
c_defer=0.65
conditional_costs=np.column_stack((p*c_miss,(1-p)*c_false_alarm,
                                   np.full(len(p),c_defer)))
choice_with_review=np.argmin(conditional_costs,axis=1)
choice_with_review=np.where(choice_with_review==2,-1,choice_with_review)
review_counts=tally(choice_with_review)
print('Cost-based threshold:',round(threshold,6),
      'realised illustrative loss:',float(sum(loss)),
      'confusion counts:',counts)
print('Illustrative abstention at review cost',c_defer,
      ': counts',review_counts,
      '; total conditional expected cost',round(float(conditional_costs.min(axis=1).sum()),3))
assert abs(threshold-2/9)<1e-12
cutoffs=np.linspace(0,1,201)
losses=[]
for z in cutoffs:
    action=(p>z)
    losses.append(np.where(action & (y==0),c_false_alarm,np.where((~action)&(y==1),c_miss,0)).sum())
fig,ax=plt.subplots(figsize=(6.5,3.2))
ax.step(cutoffs,losses,where='post')
ax.axvline(threshold,linestyle='--',label='Theoretical threshold from costs')
ax.set(xlabel='Decision threshold',ylabel='Observed loss on invented examples',title='Decision consequences differ from generic accuracy')
ax.legend(fontsize=7)
fig.tight_layout()
root=Path(__file__).resolve().parents[1]
out=root/'generated';out.mkdir(exist_ok=True)
with (out/'ch06_decision_audit.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['case','invented_probability','invented_outcome','automatic_action',
                'realised_automatic_loss','conditional_expected_automatic_loss',
                'action_with_deferral_minus1','minimum_conditional_expected_loss'])
    for i in range(len(p)):
        w.writerow([i+1,float(p[i]),int(y[i]),int(choice[i]),float(loss[i]),
                    float(expected_auto[i]),int(choice_with_review[i]),
                    float(conditional_costs[i].min())])
with (out/'ch06_confusion_summary.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['rule','false_positive','false_negative',
                                 'warning','not_warning','deferred'])
    for name,c in [('cost_threshold',counts),('with_review',review_counts)]:
        w.writerow([name]+[c[k] for k in ('false_positive','false_negative',
                                         'warning','not_warning','deferred')])
fig.savefig(root/'figures'/'ch06_decisions.pdf');plt.close(fig)
