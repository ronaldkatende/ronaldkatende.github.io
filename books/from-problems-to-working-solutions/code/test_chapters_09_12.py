"""Standard-library regression checks for chapters 9--12.

These test numerical examples and invariants, not field outcomes or causal validity.
Run from the book root: python code/test_chapters_09_12.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(stem):
    spec = importlib.util.spec_from_file_location(stem, HERE/(stem+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


c9 = load('ch09_impact_evaluation')
rows = c9.make_data()
_, estimate = c9.did(rows)
assert abs(estimate - 7.73895) < .00002, estimate
_, shifted = c9.did(c9.make_data(trend_difference=5))
assert abs((shifted - estimate)-5) < .00001
assert all(r['evidence'] == 'SYNTHETIC' for r in rows)

c10 = load('ch10_service_reliability')
assert abs(c10.availability(240,12) - 240/252)<1e-12
assert c10.replay(5,[('x',10),('x',10),('y',-3)]) == 12
assert c10.present_value(500000,280000,.1,3)>1000000

c11 = load('ch11_transport_audit')
assert abs(c11.risk([.3,.7],[.1,.3])-.24)<1e-12
assert abs(c11.effective_n([1,1,1,1])-4)<1e-12
assert 1 <= c11.effective_n([1,1,100]) < 2

c12 = load('ch12_integrated_capstone')
feasible = {pair:cost for pair,cost,travel,_ in c12.evaluate() if travel is not None}
assert feasible == {('S1','S3'):83,('S2','S3'):76}, feasible
travel = {pair:d for pair,c,d,_ in c12.evaluate() if d is not None}
assert travel == {('S1','S3'):315,('S2','S3'):395}, travel
for pair,cost,d,alloc in c12.evaluate():
    if alloc: c12.check_assignment(alloc, pair)

print('All Chapters 9-12 regression and invariant tests passed (synthetic fixtures).')
