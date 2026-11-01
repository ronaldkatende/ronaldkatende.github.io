"""Exact small-instance enumerations; no field-data or operational impact claims."""
from itertools import combinations
from pathlib import Path
import csv
# Villages' populations and route travel times for illustrative scenario.
population=[300,200,100]
times={'A':[20,40,60],'B':[50,20,15],'C':[30,25,45]}
def cost(chosen):
    return sum(p*min(times[s][i] for s in chosen) for i,p in enumerate(population))
results=[]
for k in (1,2):
    for subset in combinations(times,k):
        results.append({'sites':'+'.join(subset),'count':k,'weighted_minutes':cost(subset)})
for r in results:print(r)
assert min(r['weighted_minutes'] for r in results if r['count']==1)==min(cost((s,)) for s in times)
assert cost(('A',))==20000 and cost(('B',))==20500
out=Path(__file__).resolve().parents[1]/'generated';out.mkdir(exist_ok=True)
with (out/'ch05_sites.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['sites','count','weighted_minutes']);w.writeheader();w.writerows(results)

# A compact, independently checkable visual of the six enumerated choices.
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7,3.5))
ax.bar([r['sites'] for r in results],[r['weighted_minutes'] for r in results])
ax.set(xlabel='Illustrative candidate site set',ylabel='Population-weighted travel minutes',title='Exact enumeration: invented distances and populations')
fig.tight_layout()
fig.savefig(Path(__file__).resolve().parents[1]/'figures'/'ch05_enumeration.pdf')
plt.close(fig)
