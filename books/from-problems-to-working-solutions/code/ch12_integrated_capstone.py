"""Chapter 12: exact two-site divisible-demand allocation, INVENTED fixtures.

Greedy allocation is exact only for this two-site continuous special case.
The code deliberately does not claim to be a general integer-programming solver.
"""
import csv
from itertools import combinations
from pathlib import Path

SETTLEMENTS = ('A', 'B', 'C', 'D')
DEMAND = {'A':30, 'B':25, 'C':20, 'D':15}
SITES = ('S1', 'S2', 'S3')
CAPACITY = {'S1':45, 'S2':50, 'S3':55}
OPEN_COST = {'S1':48, 'S2':41, 'S3':35}
DISTANCE = {
    'A':{'S1':2,'S2':6,'S3':12},
    'B':{'S1':3,'S2':3,'S3':10},
    'C':{'S1':11,'S2':2,'S3':4},
    'D':{'S1':12,'S2':6,'S3':2},
}
BUDGET = 85


def optimal_two_sites(site_j, site_k):
    total = sum(DEMAND.values())
    if CAPACITY[site_j]+CAPACITY[site_k] < total:
        return None
    # Relative to assigning all demand to k, save (distance to k - distance to j)
    # per unit moved to j. Continuous allocations permit a greedy exchange proof.
    savings = sorted(((DISTANCE[i][site_k]-DISTANCE[i][site_j],i)
                      for i in SETTLEMENTS), reverse=True)
    min_to_j = max(0, total-CAPACITY[site_k])
    moves = {i:0.0 for i in SETTLEMENTS}
    allocated = 0.0
    for saving,i in savings:
        # Move positive-saving demand to j, even if the minimum has been met.
        if saving <= 0 and allocated >= min_to_j:
            continue
        amount = min(DEMAND[i], CAPACITY[site_j]-allocated)
        if amount <= 0: continue
        moves[i] = amount
        allocated += amount
    if allocated < min_to_j-1e-8:
        # A negative-saving group may need capacity moved for feasibility.
        for saving,i in savings:
            if allocated >= min_to_j-1e-8: break
            extra = min(DEMAND[i]-moves[i], min_to_j-allocated)
            moves[i] += extra
            allocated += extra
    if allocated < min_to_j-1e-8: return None
    assignments = [(i,site_j,moves[i]) for i in SETTLEMENTS if moves[i]>0]
    assignments += [(i,site_k,DEMAND[i]-moves[i]) for i in SETTLEMENTS
                    if DEMAND[i]-moves[i]>0]
    check_assignment(assignments, (site_j,site_k))
    travel = sum(amount*DISTANCE[i][j] for i,j,amount in assignments)
    return travel,assignments


def check_assignment(assignments, open_sites):
    for i in SETTLEMENTS:
        assigned = sum(x for ii,j,x in assignments if ii==i)
        assert abs(assigned-DEMAND[i])<1e-10
    for j in SITES:
        load = sum(x for i,jj,x in assignments if jj==j)
        if j in open_sites: assert load<=CAPACITY[j]+1e-10
        else: assert load==0
    assert all(x>=0 for _,_,x in assignments)


def evaluate(budget=BUDGET):
    candidates=[]
    for pair in combinations(SITES,2):
        opening = sum(OPEN_COST[j] for j in pair)
        if opening>budget:
            candidates.append((pair,opening,None,None))
            continue
        result=optimal_two_sites(*pair)
        if result is None: candidates.append((pair,opening,None,None))
        else: candidates.append((pair,opening,*result))
    return candidates


def main():
    outcomes=evaluate()
    feasible=[x for x in outcomes if x[2] is not None]
    assert {p for p,_,_,_ in feasible} == {('S1','S3'),('S2','S3')}
    assert {pair:travel for pair,_,travel,_ in feasible}=={
        ('S1','S3'):315.0,('S2','S3'):395.0}
    # Tightening a budget must not add feasible pairs.
    old={p for p,_,travel,_ in outcomes if travel is not None}
    tight={p for p,_,travel,_ in evaluate(budget=80) if travel is not None}
    assert tight.issubset(old)
    out=Path('generated');out.mkdir(exist_ok=True)
    with (out/'ch12_invented_allocation.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['evidence','opened_sites','opening_cost_units',
                         'travel_person_km','feasibility'])
        for pair,opening,travel,alloc in outcomes:
            writer.writerow(['INVENTED', '+'.join(pair),opening,
                             '' if travel is None else f'{travel:.2f}',
                             'feasible' if travel is not None else 'infeasible'])
    with (out/'ch12_invented_assignments.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['evidence','opened_sites','settlement','site','allocated_units',
                         'assumed_distance_km'])
        for pair,opening,travel,alloc in outcomes:
            if alloc is not None:
                for i,j,x in alloc:
                    writer.writerow(['INVENTED','+'.join(pair),i,j,f'{x:.2f}',DISTANCE[i][j]])
    for pair,opening,travel,alloc in outcomes:
        print('INVENTED', '+'.join(pair), f'cost={opening}',
              'infeasible' if travel is None else f'travel={travel:.0f}')
    print('Conservation, capacity, budget and monotone feasible-set tests: passed')


if __name__=='__main__':
    main()
