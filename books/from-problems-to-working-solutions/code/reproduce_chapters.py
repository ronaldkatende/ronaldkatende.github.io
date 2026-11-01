"""Generate illustrative, synthetic figures and tables for Chapters 1-3.
All scenarios are invented teaching examples, NOT observed service data.
Run: python code/reproduce_chapters.py (from project root)
"""
from pathlib import Path
from math import factorial
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'; GEN=ROOT/'generated'
FIG.mkdir(exist_ok=True); GEN.mkdir(exist_ok=True)

def mmc(lam, mu, c):
    a=lam/mu
    rho=a/c
    if rho>=1: raise ValueError('unstable queue')
    p0=1/(sum(a**k/factorial(k) for k in range(c)) + a**c/(factorial(c)*(1-rho)))
    p_wait=a**c/(factorial(c)*(1-rho))*p0
    wq=p_wait/(c*mu-lam)
    return {'Wq':wq, 'W':wq+1/mu, 'Pwait':p_wait, 'rho':rho}

# All rates are illustrative, not measured.
options=[('Existing single desk', 6,8,1),('Faster desk',6,9,1),('Two service desks',6,8,2)]
with open(GEN/'queue_table.tex','w') as fh:
    for name,lam,mu,c in options:
        r=mmc(lam,mu,c)
        fh.write(f'{name} & {60*r["Wq"]:.1f} & {60*r["W"]:.1f} & {r["rho"]:.2f} \\\\\n')
xs=np.linspace(1,7.4,100)
plt.figure(figsize=(6.8,3.3))
plt.plot(xs,[60*mmc(x,8,1)['W'] for x in xs],label='One service desk')
plt.plot(xs,[60*mmc(x,8,2)['W'] for x in xs],label='Two service desks')
plt.xlabel('Arrival rate (patients per hour; illustrative)')
plt.ylabel('Mean time in service system (minutes)')
plt.ylim(0,150);plt.grid(alpha=.2);plt.legend(frameon=False)
plt.tight_layout();plt.savefig(FIG/'queue_sensitivity.pdf');plt.close()

# Balance: water available, actual delivery bounded by available water.
inflow=np.array([22,19,14,11,10,16,24,20,12,8,14,22,21,16,13,10,17,24,19,11],float)

def water_run(demand):
    s=55.; storage=[s]; unmet=[]; spill=[]
    for it in inflow:
        available=max(0.,s+it-2.) # fixed synthetic loss, before deliveries
        delivered=min(demand,available)
        shortage=demand-delivered
        remaining=available-delivered
        excess=max(remaining-75,0.)
        s=min(remaining,75.)
        storage.append(s);unmet.append(shortage);spill.append(excess)
    return np.array(storage), np.array(unmet), np.array(spill)
a,ua,sa=water_run(16); b,ub,sb=water_run(22)
with open(GEN/'water_table.tex','w') as fh:
    for demand,stor,unmet,spill in [(16,a,ua,sa),(22,b,ub,sb)]:
        fh.write(f'{demand} & {stor[-1]:.1f} & {unmet.sum():.1f} & {spill.sum():.1f} \\\\\n')
plt.figure(figsize=(6.8,3.1))
plt.plot(range(21),a,label='Demand: 16 m$^3$/day')
plt.plot(range(21),b,label='Demand: 22 m$^3$/day')
plt.axhline(75,linestyle=':',color='gray',label='Tank capacity')
plt.xlabel('Day');plt.ylabel('Water stored (m$^3$)');plt.grid(alpha=.2)
plt.legend(frameon=False,ncol=2,fontsize=8);plt.tight_layout()
plt.savefig(FIG/'water_storage.pdf');plt.close()

# Synthetic survey: oversampling a high-access region, deliberately, to illustrate weighting.
rng=np.random.default_rng(32)
size_a,size_b=7500,2500
truth=np.r_[rng.binomial(1,0.30,size_a),rng.binomial(1,0.80,size_b)]
ix_a=rng.choice(size_a,250,replace=False)
ix_b=rng.choice(size_b,250,replace=False)+size_a
obs=truth[np.r_[ix_a,ix_b]]
weights=np.r_[np.repeat(size_a/250,250),np.repeat(size_b/250,250)]
unweighted=obs.mean();weighted=np.average(obs,weights=weights);popmean=truth.mean()
with open(GEN/'survey_table.tex','w') as fh:
    fh.write(f'Unweighted sample mean & {100*unweighted:.1f} \\\\\n')
    fh.write(f'Population-weighted sample mean & {100*weighted:.1f} \\\\\n')
    fh.write(f'Synthetic finite-population mean (known here) & {100*popmean:.1f} \\\\\n')
plt.figure(figsize=(6.8,3.1))
labels=['Unweighted sample','Weighted sample','Full simulated population']
plt.bar(labels,[100*unweighted,100*weighted,100*popmean],width=.6)
plt.ylabel('Household electricity access (%)')
plt.ylim(0,100);plt.xticks(rotation=8);plt.tight_layout();plt.savefig(FIG/'survey_weighting.pdf');plt.close()

# Close generated LaTeX tabular bodies within the input file.
# booktabs rules must immediately follow the last row when expanded by TeX.
for filename in ('queue_table.tex','water_table.tex','survey_table.tex'):
    with open(GEN/filename,'a') as tabular:
        tabular.write('\\bottomrule\n')

# Automated checks for physical/statistical consistency.
assert all(0<=r['rho']<1 for _,la,mu,c in options for r in [mmc(la,mu,c)])
assert np.all((a>=0)&(a<=75)) and np.all((b>=0)&(b<=75))
assert abs(np.sum(ua)) < 1e-9
assert 0<=weighted<=1 and 0<=unweighted<=1
print('Illustrative figures, tables, and assertions generated.')
print('queue',[(n,round(mmc(l,mu,c)['W']*60,2)) for n,l,mu,c in options])
print('water',a[-1],ua.sum(),sa.sum(),b[-1],ub.sum(),sb.sum())
print('survey',unweighted, weighted, popmean)
