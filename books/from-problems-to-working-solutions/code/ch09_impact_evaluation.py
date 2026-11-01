"""Chapter 9: a synthetic difference-in-differences teaching example.

No external/operational data. The treatment and counterfactual parameters
are part of an invented data-generating process; output is never field evidence.
"""
import argparse
import csv
import random
from pathlib import Path


def make_data(n_per_group=40, treatment_effect=8.0, trend_difference=0.0, seed=2309):
    rng = random.Random(seed)
    rows = []
    for treated in (0, 1):
        for i in range(n_per_group):
            site_id = f"{'T' if treated else 'C'}{i+1:03d}"
            facility_shift = rng.gauss(0.0, 5.0)
            for period in (0, 1):
                # This data-generating process is explicitly artificial.
                outcome = (60.0 + 4 * treated + facility_shift
                           + 10 * period + trend_difference * treated * period
                           + treatment_effect * treated * period
                           + rng.gauss(0.0, 1.5))
                rows.append({"facility": site_id, "treated": treated,
                             "period": period, "outcome": round(outcome, 5),
                             "evidence": "SYNTHETIC"})
    return rows


def did(rows):
    groups = {}
    for g in (0, 1):
        for t in (0, 1):
            values = [r['outcome'] for r in rows if r['treated'] == g and r['period'] == t]
            assert values, 'empty group-period cell'
            groups[(g, t)] = sum(values)/len(values)
    estimate = ((groups[(1, 1)] - groups[(1, 0)])
                - (groups[(0, 1)] - groups[(0, 0)]))
    return groups, estimate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trend-difference', type=float, default=0.0,
                    help='Additional untreated trend in treated group; breaks parallel trends')
    ap.add_argument('--out', default='generated')
    args = ap.parse_args()
    rows = make_data(trend_difference=args.trend_difference)
    group_means, estimate = did(rows)
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir/'ch09_synthetic_panel.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    with (output_dir/'ch09_did_summary.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['evidence', 'group', 'period', 'mean'])
        for (g, t), y in sorted(group_means.items()):
            writer.writerow(['SYNTHETIC', g, t, f'{y:.5f}'])
        writer.writerow(['SYNTHETIC', 'difference-in-differences', '', f'{estimate:.5f}'])
    assert len(rows) == 160
    print(f'SYNTHETIC DiD={estimate:.5f}; known effect=8.0; '
          f'counterfactual trend difference={args.trend_difference:.1f}')
    print('No causal effect on actual facilities is estimated.')


if __name__ == '__main__':
    main()
