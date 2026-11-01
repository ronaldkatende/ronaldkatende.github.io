"""Chapter 11: covariate shift and cross-context audit, all values invented."""
import csv
from pathlib import Path


def risk(weights, conditional_errors):
    return sum(w * e for w, e in zip(weights, conditional_errors))


def effective_n(weights):
    if not weights or any(w < 0 for w in weights) or sum(weights) <= 0:
        raise ValueError('Weights must be nonnegative with positive total')
    return sum(weights)**2 / sum(w*w for w in weights)


def main():
    out = Path('generated'); out.mkdir(exist_ok=True)
    source_mix = [0.8, 0.2]
    target_mix = [0.3, 0.7]
    errors = [0.10, 0.30]
    importance = [t/s for t,s in zip(target_mix, source_mix)]
    source = risk(source_mix, errors)
    target_direct = risk(target_mix, errors)
    target_from_source = sum(s*w*e for s,w,e in zip(source_mix, importance, errors))
    assert abs(source-.14)<1e-12
    assert abs(target_direct-.24)<1e-12
    assert abs(target_from_source-target_direct)<1e-12
    expanded_weights = [importance[0]]*80 + [importance[1]]*20
    ess = effective_n(expanded_weights)
    assert 1 <= ess <= len(expanded_weights)
    # Concept shift: rural conditional error changes from .30 to .45.
    shifted_actual = risk(target_mix, [.10, .45])
    assert abs(shifted_actual - .345) < 1e-12
    with (out/'ch11_synthetic_shift.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['evidence','metric','value'])
        for label,value in [('source_risk',source),('target_covariate_risk',target_direct),
                            ('weighted_source_risk',target_from_source),
                            ('effective_sample_size_proxy',ess),
                            ('target_risk_after_conditional_shift',shifted_actual)]:
            writer.writerow(['SYNTHETIC',label,f'{value:.7f}'])
    # Country names are contexts for classroom research, not source of these numbers.
    examples=[('Uganda',100,60),('Kenya',120,70),('Nepal',80,50),('Peru',110,55)]
    with (out/'ch11_illustrative_contexts.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['evidence','proposed_case_country','assumed_demand_units',
                         'assumed_budget_units'])
        for name,demand,budget in examples:
            writer.writerow(['INVENTED, NOT COUNTRY DATA',name,demand,budget])
    print(f'SYNTHETIC source risk {source:.4f}, target risk {target_direct:.4f}, '
          f'weighted source {target_from_source:.4f}, ESS proxy {ess:.2f}')
    print(f'SYNTHETIC concept-shift target risk {shifted_actual:.4f}; '
          'source weighting alone would still report 0.2400')


if __name__ == '__main__':
    main()
