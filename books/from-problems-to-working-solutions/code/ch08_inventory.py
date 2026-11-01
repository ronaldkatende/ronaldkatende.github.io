"""Invented demand experiment, not measured health-centre inventory results."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
rng=np.random.default_rng(164)
T=150
# common generated scenario across policies
seasonal=9+2*np.sin(np.arange(T)/14)
demand=rng.poisson(seasonal).astype(int)

def run(target,review_every=7,lead_time=5):
    stock=45
    arrivals={}
    rows=[]
    for t,d in enumerate(demand):
        opening=stock; r=arrivals.pop(t,0)
        available=stock+r
        issue=min(d,available); unfilled=d-issue
        stock=available-issue
        on_order=sum(v for day,v in arrivals.items() if day>=t)
        if t%review_every==0:
            order=max(0,target-(stock+on_order))
            if order: arrivals[t+lead_time]=arrivals.get(t+lead_time,0)+order
        else:order=0
        assert stock>=0 and opening+r==issue+stock
        rows.append((t,d,opening,r,issue,unfilled,stock,order))
    return pd.DataFrame(rows,columns=['day','true_demand','opening_stock','receipts','dispensed','unmet_demand','closing_stock','ordered'])
A=run(70);B=run(100)
root=Path(__file__).resolve().parents[1]
out=root/'generated';out.mkdir(exist_ok=True)
A.to_csv(out/'ch08_policy_A.csv',index=False); B.to_csv(out/'ch08_policy_B.csv',index=False)
summary=pd.DataFrame([
 {'illustrative_policy':'S=70','unmet_units':int(A.unmet_demand.sum()),'stockout_days':int((A.unmet_demand>0).sum()),'mean_closing_stock':float(A.closing_stock.mean())},
 {'illustrative_policy':'S=100','unmet_units':int(B.unmet_demand.sum()),'stockout_days':int((B.unmet_demand>0).sum()),'mean_closing_stock':float(B.closing_stock.mean())}])
print(summary.to_string(index=False)); summary.to_csv(out/'ch08_summary.csv',index=False)
fig,ax=plt.subplots(figsize=(7,3.4))
ax.plot(A.day,A.closing_stock,label='Target 70')
ax.plot(B.day,B.closing_stock,label='Target 100',alpha=0.8)
ax.set(xlabel='Illustrative day',ylabel='Closing units',title='Invented-demand inventory scenario: not field evidence')
ax.legend();fig.tight_layout();fig.savefig(root/'figures'/'ch08_inventory.pdf');plt.close(fig)
