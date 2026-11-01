"""Chapter 10: synthetic reliability, lifecycle cost and idempotent replay.

This is a teaching model, not a measured outage or cost study.
"""
import csv
import random
from pathlib import Path


def availability(mean_uptime, mean_repair):
    if mean_uptime <= 0 or mean_repair < 0:
        raise ValueError('Invalid mean durations')
    return mean_uptime / (mean_uptime + mean_repair)


def simulated_availability(mean_uptime, mean_repair, seed=2310, cycles=50000):
    rng = random.Random(seed)
    operating = 0.0
    repairing = 0.0
    for _ in range(cycles):
        operating += rng.expovariate(1/mean_uptime)
        if mean_repair:
            repairing += rng.expovariate(1/mean_repair)
    return operating/(operating+repairing)


def present_value(initial, yearly, annual_discount, years):
    if annual_discount <= -1:
        raise ValueError('Discount rate must exceed -1')
    return initial + sum(yearly/(1+annual_discount)**t for t in range(1, years+1))


def replay(balance, events):
    applied = set()
    for event in events:
        tx_id, delta = event
        if tx_id not in applied:
            balance += delta
            applied.add(tx_id)
    return balance


def main():
    out = Path('generated')
    out.mkdir(exist_ok=True)
    rows = []
    for recovery in (12.0, 3.0):
        exact = availability(240.0, recovery)
        simulated = simulated_availability(240.0, recovery)
        rows.append(('SYNTHETIC', 240.0, recovery, f'{exact:.7f}', f'{simulated:.7f}'))
    with (out/'ch10_reliability.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['evidence', 'assumed_uptime_hours', 'assumed_repair_hours',
                         'model_availability', 'simulated_availability'])
        writer.writerows(rows)
    a = present_value(500000, 280000, 0.1, 3)
    b = present_value(900000, 150000, 0.1, 3)
    assert abs(a - 1196319.9) < 5.0, a
    assert abs(b - 1273030) < 50.0, b
    events = [('receipts-1', 100), ('issued-1', -12), ('issued-1', -12), ('waste-1', -2)]
    assert replay(0, events) == 86
    assert replay(0, events + [('receipts-1', 100)]) == 86
    print(f'SYNTHETIC lifecycle option A={a:.2f}; option B={b:.2f}')
    for row in rows:
        print(f'SYNTHETIC repair={row[2]:.0f}h; theoretical={row[3]} simulated={row[4]}')
    print('Idempotent transaction replay test: passed')


if __name__ == '__main__':
    main()
