import math
def normalize_scores(hyps):
    scores = [h.get('score',0.0) for h in hyps]
    min_s = min(scores) if scores else 0.0
    exps = [math.exp(-(s-min_s)) for s in scores]
    ssum = sum(exps) + 1e-12
    return [e/ssum for e in exps]
def expected_token_count(word, segment):
    hyps = segment.asr_lattice or []
    if not hyps:
        return float((segment.transcript or '').lower().split().count(word.lower()))
    probs = normalize_scores(hyps)
    total = 0.0
    for p,h in zip(probs, hyps):
        total += p * h.get('hypothesis','').lower().split().count(word.lower())
    return total
def token_present_probability(word, segment):
    hyps = segment.asr_lattice or []
    if not hyps:
        return 1.0 if word.lower() in (segment.transcript or '').lower() else 0.0
    probs = normalize_scores(hyps)
    p_not = 1.0
    for p,h in zip(probs, hyps):
        found = word.lower() in h.get('hypothesis','').lower()
        if found:
            p_not *= (1 - p)
    return 1 - p_not
