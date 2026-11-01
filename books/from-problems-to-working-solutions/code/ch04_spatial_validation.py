"""Synthetic evaluation-design demonstration. Not measured Ugandan air quality.
Requires numpy, pandas, scikit-learn, matplotlib. Runs without network access.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

SEED=91
rng=np.random.default_rng(SEED)
N_SITES,N_DAYS=24,35
xy=rng.uniform(-1,1,size=(N_SITES,2))
site_levels=20+7*xy[:,0]-4*xy[:,1]+3*np.sin(3*xy[:,0])
records=[]
for site in range(N_SITES):
    for day in range(N_DAYS):
        hour_pattern=2*np.cos(day/5)
        val=site_levels[site]+hour_pattern+rng.normal(0,1.7)
        records.append((site,day,xy[site,0],xy[site,1],val))
df=pd.DataFrame(records,columns=['site','day','x','y','pm25_synthetic'])
X=df[['x','y','day']].to_numpy(); y=df.pm25_synthetic.to_numpy()
i=np.arange(len(y))
tr,te=train_test_split(i,test_size=0.25,random_state=SEED)
gss=GroupShuffleSplit(n_splits=1,test_size=0.25,random_state=SEED)
trg,teg=next(gss.split(X,y,groups=df.site))

def predict(train,test,baseline=False):
    model=(DummyRegressor(strategy='mean') if baseline else
           RandomForestRegressor(n_estimators=120,min_samples_leaf=2,
                                 random_state=SEED,n_jobs=1))
    model.fit(X[train],y[train])
    return model.predict(X[test])
random_error=mean_absolute_error(y[te],predict(tr,te))
heldout_predictions=predict(trg,teg)
new_site_error=mean_absolute_error(y[teg],heldout_predictions)
heldout_baseline=mean_absolute_error(y[teg],predict(trg,teg,baseline=True))
print('Teaching data ONLY. Random-row MAE:',round(random_error,3),
      'held-out-site MAE:',round(new_site_error,3),
      'held-out-site mean-baseline MAE:',round(heldout_baseline,3))
assert not (set(df.site.iloc[trg]) & set(df.site.iloc[teg]))
base=Path(__file__).resolve().parents[1]
out=base/'generated';out.mkdir(exist_ok=True)
pd.DataFrame([{'scheme':'Random rows (RF)','MAE':random_error},
              {'scheme':'Held-out sites (RF)','MAE':new_site_error},
              {'scheme':'Held-out sites (mean baseline)','MAE':heldout_baseline}]).to_csv(out/'ch04_validation.csv',index=False)
# Keep all records from a station in one split; report held-out station-level
# errors and their proximity to the nearest training station.
train_sites=np.unique(df.site.iloc[trg].to_numpy())
test_sites=np.unique(df.site.iloc[teg].to_numpy())
site_rows=[]
for site in test_sites:
    mask=df.site.iloc[teg].to_numpy()==site
    pos=np.flatnonzero(mask)
    xy_site=xy[site]
    nearest=float(np.sqrt(((xy[train_sites]-xy_site)**2).sum(axis=1)).min())
    site_rows.append({'site':int(site),
                      'n_test_days':int(len(pos)),
                      'MAE':float(mean_absolute_error(y[teg][pos],heldout_predictions[pos])),
                      'nearest_training_site_distance_synthetic_units':nearest})
pd.DataFrame(site_rows).to_csv(out/'ch04_heldout_site_errors.csv',index=False)
pd.DataFrame([{'site':int(site),'fold':'training'} for site in train_sites]+[
             {'site':int(site),'fold':'held_out'} for site in test_sites]).to_csv(
             out/'ch04_site_partition.csv',index=False)
assert all(row['n_test_days']==N_DAYS for row in site_rows)
fig,ax=plt.subplots(figsize=(6.5,3.2))
ax.bar(['Random rows','New sites'],[random_error,new_site_error])
ax.set_ylabel('MAE in synthetic PM2.5 units')
ax.set_title('Evaluation question changes the error estimate')
fig.tight_layout();fig.savefig(base/'figures'/'ch04_validation.pdf');plt.close(fig)
