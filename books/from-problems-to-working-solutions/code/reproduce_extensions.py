"""Reproduce teaching-only figures and assertion checks for expanded Chapters 1--3.
No observational or person-level data is used. Python 3, numpy and matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)

# Chapter 1. Expected losses against the unknown state probability.
p = np.linspace(0, 1, 301)
reg = 2 * p + 12 * (1 - p)
lab = 9 * p + 3 * (1 - p)
threshold = 9 / 16
assert abs((2*threshold + 12*(1-threshold)) - (9*threshold+3*(1-threshold))) < 1e-12
fig, ax = plt.subplots(figsize=(7.4, 3.8))
ax.plot(p, reg, label='Improve registration')
ax.plot(p, lab, label='Improve laboratory workflow')
ax.axvline(threshold, color='0.45', ls='--', linewidth=1)
ax.annotate('Decision changes at p = 9/16', (threshold, 6.25), xytext=(0.35, 9),
            arrowprops=dict(arrowstyle='->', color='0.4'), fontsize=9)
ax.set_xlabel('Assumed probability that registration is the bottleneck')
ax.set_ylabel('Expected loss (illustrative units)')
ax.legend(loc='upper right', fontsize=9)
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(FIG / 'decision_threshold.pdf')
plt.close(fig)

# Chapter 2. Check Euler results against the analytical solution.
def exact(t): return 6 - 2*np.exp(-0.5*t)
def euler(h, T=4):
    times = np.arange(0, round(T / h)+1)*h
    y = [4.0]
    for _ in times[1:]:
        y.append(y[-1] + h*(3-0.5*y[-1]))
    return times, np.asarray(y)
assert abs(exact(1)-(6-2*np.exp(-0.5))) < 1e-14
assert abs(euler(1)[1][1]-5) < 1e-14
assert abs(euler(0.5)[1][2]-4.875) < 1e-14
fig, ax = plt.subplots(figsize=(7.4, 3.8))
t = np.linspace(0,4,301)
ax.plot(t, exact(t), label='Exact differential-equation solution', linewidth=2)
for h in [1.0, 0.5]:
    ti, yi=euler(h)
    ax.plot(ti, yi, marker='o', label=f'Forward Euler, step {h:g} day')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Stored volume (illustrative units)')
ax.legend(fontsize=9)
ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(FIG / 'euler_vs_exact.pdf')
plt.close(fig)

# Chapter 3. Independent and common measurement error.
n = np.unique(np.geomspace(1, 2000, 200).astype(int))
shared = np.sqrt(4 + 1/n)
wrong = np.sqrt(5/n)
fig, ax = plt.subplots(figsize=(7.4, 3.8))
ax.plot(n, shared, label='Shared calibration error plus independent noise')
ax.plot(n, wrong, ls='--', label='Incorrect: treat all noise as independent')
ax.set_xscale('log')
ax.set_xlabel('Number of repeated measurements')
ax.set_ylabel('Standard deviation of mean measurement error')
ax.set_ylim(bottom=0)
ax.grid(alpha=0.2)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(FIG / 'shared_measurement_error.pdf')
plt.close(fig)
print('All analytical consistency checks passed; figures generated.')
