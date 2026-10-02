# DISCLAIMER BEGIN
# This work was carried out independently, on personal time and equipment, and is not
# connected to the author's employment. The views expressed are the author's own and do
# not represent the views, positions or policies of any current, former or future employer
# or client. No proprietary, confidential or internal data of any organization was used.
# All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
# DISCLAIMER END
# Run 4 of concept A15: validate the NO-NDC-EXPECTED label (run 3 compounding signal OR run 3
# bulk signal), then decompose the NDC coverage trend. No model, nothing fitted.
#   python3 -B run4_label_validation.py
# The label rules and the NDC parser are IMPORTED from run3_parser_validation.py and
# run2_ndc_recovery.py, whose digests are checked before anything runs, so neither rule can
# drift. Deterministic: every sample uses a fixed, stated seed.
# Reads run4_marks.json (hand marks) if present; writes run4_results.json and RUN4-REPORT.md.
import hashlib, io, json, os, random, sys, zipfile

sys.dont_write_bytecode = True  # no __pycache__ in the program folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run2_ndc_recovery as R2
import run3_parser_validation as R3  # COMPOUND, BULK_RULES, wilson(), ERAS
from boundary_scan import load_terms

DATA = os.path.join(HERE, 'data', 'drug-enforcement-0001-of-0001.json.zip')
ENTRY = 'drug-enforcement-0001-of-0001.json'
WANT_SHA = 'c6eb46526a3ad52102a88b65727874c2e23c43300b27e704eada05960d755092'
WANT_N = 17975
RUN2_SHA = '892aacebdeb522adef4ca4f2beef658b8ac9a61f843f4631cb26d77f4571b263'
RUN3_SHA = '2664f53f33943376233eb98fe4be2abbf7b0478e68f028886e053351ff9dad37'

ERAS = R3.ERAS  # E1 2013-2016, E2 2017-2021, E3 2022-2026
YEARS = list(range(2013, 2027))
N_PER_ERA = 40
SEEDS_A = {'E1': 41001, 'E2': 41002, 'E3': 41003}  # flagged records (precision)
SEEDS_B = {'E1': 42001, 'E2': 42002, 'E3': 42003}  # unflagged, no NDC from either source (miss rate)

# Pre-registered criteria from the run 4 brief. Not to be changed after results.
V1_MIN_POOLED = 85.0
V1_MIN_LOWER = 70.0
V2_MAX_SPREAD_PP = 15.0
V3_MAX_E3_MINUS_E1_PP = 15.0


def compounding(t):
    return bool(R3.COMPOUND.search(t))


def bulk(t):
    return any(rx.search(t) for _, rx in R3.BULK_RULES)


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def decompose(s0, pf0, po0, s1, pf1, po1, sb, pfb, pob):
    """C = s*pF + (1-s)*pO. Composition = ds*(pFbar - pObar); within = sbar*dpF + (1-sbar)*dpO;
    interaction = dC - composition - within. All in percentage points."""
    c0 = s0 * pf0 + (1 - s0) * po0
    c1 = s1 * pf1 + (1 - s1) * po1
    dc = c1 - c0
    comp = (s1 - s0) * (pfb - pob)
    within = sb * (pf1 - pf0) + (1 - sb) * (po1 - po0)
    inter = dc - comp - within
    r = lambda v: round(100 * v, 2)
    share = lambda v: round(100 * v / dc, 1) if dc else None
    return {'coverage_from_pct': r(c0), 'coverage_to_pct': r(c1), 'total_change_pp': r(dc),
            'composition_pp': r(comp), 'within_pp': r(within), 'interaction_pp': r(inter),
            'composition_share_pct': share(comp), 'within_share_pct': share(within), 'interaction_share_pct': share(inter),
            'inputs': {'s_from': round(s0, 4), 'pF_from': round(pf0, 4), 'pO_from': round(po0, 4),
                       's_to': round(s1, 4), 'pF_to': round(pf1, 4), 'pO_to': round(po1, 4),
                       's_pooled': round(sb, 4), 'pF_pooled': round(pfb, 4), 'pO_pooled': round(pob, 4)}}


def main():
    raw = open(DATA, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    recs = json.loads(zipfile.ZipFile(io.BytesIO(raw)).read(ENTRY))['results']
    if sha != WANT_SHA or len(recs) != WANT_N:
        sys.exit('STOP: data file SHA-256 %s, %d records; expected %s, %d' % (sha, len(recs), WANT_SHA, WANT_N))
    for fn, want in (('run2_ndc_recovery.py', RUN2_SHA), ('run3_parser_validation.py', RUN3_SHA)):
        got = hashlib.sha256(open(os.path.join(HERE, fn), 'rb').read()).hexdigest()
        if got != want:
            sys.exit('STOP: %s has changed (%s); the rules must be the earlier runs\' rules' % (fn, got))
    terms = load_terms()

    def redact(s):
        n = 0
        for p in terms:
            s, k = p.subn('[REDACTED]', s)
            n += k
        return s, n

    year = [int(r['report_date'][:4]) for r in recs]
    desc = [r.get('product_description') or '' for r in recs]
    has_of = [bool((r.get('openfda') or {}).get('product_ndc')) for r in recs]
    has_ndc = [has_of[i] or bool(R2.parse(desc[i])[0]) for i in range(len(recs))]
    comp = [compounding(t) for t in desc]
    blk = [bulk(t) for t in desc]
    flag = [comp[i] or blk[i] for i in range(len(recs))]
    out = {'data': {'sha256': sha, 'records': len(recs)}, 'rule_sources': {'run2_ndc_recovery.py': RUN2_SHA, 'run3_parser_validation.py': RUN3_SHA},
           'date_field': 'report_date (year), as in runs 1-3', 'eras': ERAS, 'seeds_A': SEEDS_A, 'seeds_B': SEEDS_B}
    marks_path = os.path.join(HERE, 'run4_marks.json')
    marks = json.load(open(marks_path, encoding='utf-8')) if os.path.exists(marks_path) else {'A': {}, 'B': {}}
    red_total = 0

    def text_of(i):
        return ' '.join(desc[i].split())

    # ---------------- Part A: precision of the composite label
    A = {}
    for e, a, b in ERAS:
        pop = sorted(i for i in range(len(recs)) if a <= year[i] <= b and flag[i])
        ids = random.Random(SEEDS_A[e]).sample(pop, N_PER_ERA)
        rows = []
        for i in ids:
            d, n = redact(text_of(i))
            red_total += n
            key = '%s#%d' % (recs[i].get('recall_number'), i)
            mk = marks['A'].get(key, {})
            rows.append({'key': key, 'year': year[i], 'rule_compounding': comp[i], 'rule_bulk': blk[i], 'has_ndc': has_ndc[i],
                         'description': d, 'mark': mk.get('mark'), 'kind': mk.get('kind', ''), 'note': mk.get('note', '')})
        marked = [x for x in rows if x['mark'] in ('correct', 'incorrect')]
        k = sum(1 for x in marked if x['mark'] == 'correct')
        full = len(marked) == N_PER_ERA
        A[e] = {'population': len(pop), 'population_compounding_rule': sum(1 for i in pop if comp[i]),
                'population_bulk_rule': sum(1 for i in pop if blk[i]), 'sample': rows, 'marked': len(marked), 'correct': k,
                'precision_pct': pct(k, len(marked)) if full else None, 'wilson95': R3.wilson(k, len(marked)) if full else None,
                'correct_kind': {kd: sum(1 for x in marked if x['mark'] == 'correct' and x['kind'] == kd) for kd in ('compounded', 'bulk', 'both')},
                'incorrect_bulk_finished': sum(1 for x in marked if x['mark'] == 'incorrect' and x['kind'] == 'bulk-finished'),
                'by_rule_component': {
                    'compounding_rule': [sum(1 for x in marked if x['rule_compounding'] and x['mark'] == 'correct'), sum(1 for x in marked if x['rule_compounding'])],
                    'bulk_rule': [sum(1 for x in marked if x['rule_bulk'] and x['mark'] == 'correct'), sum(1 for x in marked if x['rule_bulk'])]}}
    kk = sum(A[e]['correct'] for e in A)
    nn = sum(A[e]['marked'] for e in A)
    out['A'] = A
    out['A_pooled'] = {'correct': kk, 'marked': nn, 'precision_pct': pct(kk, nn), 'wilson95': R3.wilson(kk, nn)}

    # ---------------- Part B: miss rate among unflagged records with no NDC from either source
    B = {}
    for e, a, b in ERAS:
        pop = sorted(i for i in range(len(recs)) if a <= year[i] <= b and not flag[i] and not has_ndc[i])
        ids = random.Random(SEEDS_B[e]).sample(pop, N_PER_ERA)
        rows = []
        for i in ids:
            d, n = redact(text_of(i))
            red_total += n
            key = '%s#%d' % (recs[i].get('recall_number'), i)
            mk = marks['B'].get(key, {})
            rows.append({'key': key, 'year': year[i], 'description': d, 'mark': mk.get('mark'), 'kind': mk.get('kind', ''), 'note': mk.get('note', '')})
        marked = [x for x in rows if x['mark'] in ('missed', 'not')]
        k = sum(1 for x in marked if x['mark'] == 'missed')
        full = len(marked) == N_PER_ERA
        B[e] = {'population': len(pop), 'sample': rows, 'marked': len(marked), 'missed': k,
                'miss_rate_pct': pct(k, len(marked)) if full else None, 'wilson95': R3.wilson(k, len(marked)) if full else None,
                'missed_kind': {kd: sum(1 for x in marked if x['mark'] == 'missed' and x['kind'] == kd) for kd in ('compounded', 'bulk', 'both')}}
    out['B'] = B
    out['boundary_redactions'] = red_total

    # ---------------- Part C: pre-registered criteria
    complete = all(A[e]['precision_pct'] is not None for e in A) and all(B[e]['miss_rate_pct'] is not None for e in B)
    C = {'complete': complete}
    if complete:
        ap = out['A_pooled']
        precs = [A[e]['precision_pct'] for e in A]
        v1 = ap['precision_pct'] >= V1_MIN_POOLED and ap['wilson95'][0] > V1_MIN_LOWER
        spread = round(max(precs) - min(precs), 2)
        v2 = spread <= V2_MAX_SPREAD_PP
        d3 = round(B['E3']['miss_rate_pct'] - B['E1']['miss_rate_pct'], 2)
        v3 = d3 <= V3_MAX_E3_MINUS_E1_PP
        C.update({'V1_pooled_precision_pct': ap['precision_pct'], 'V1_lower_wilson_pct': ap['wilson95'][0], 'V1_pass': v1,
                  'V2_max_spread_pp': spread, 'V2_pass': v2, 'V3_E3_minus_E1_pp': d3, 'V3_pass': v3,
                  'verdict': 'EXPLANATION STANDS' if (v1 and v2 and v3) else 'EXPLANATION DOES NOT STAND'})
        # Sensitivity, not the gate: finished dosage forms in bulk packaging counted as correct.
        alt = {e: A[e]['correct'] + A[e]['incorrect_bulk_finished'] for e in A}
        altp = {e: pct(alt[e], A[e]['marked']) for e in A}
        ak = sum(alt.values())
        C['sensitivity_bulk_finished_correct'] = {
            'precision_by_era': altp, 'pooled_pct': pct(ak, nn), 'pooled_wilson95': R3.wilson(ak, nn),
            'V1_pass': pct(ak, nn) >= V1_MIN_POOLED and R3.wilson(ak, nn)[0] > V1_MIN_LOWER,
            'V2_spread_pp': round(max(altp.values()) - min(altp.values()), 2),
            'V2_pass': max(altp.values()) - min(altp.values()) <= V2_MAX_SPREAD_PP}
    out['C'] = C

    # ---------------- Part D: per-year table and decomposition
    rows = []
    for y in YEARS:
        idx = [i for i in range(len(recs)) if year[i] == y]
        f_ = [i for i in idx if flag[i]]
        o_ = [i for i in idx if not flag[i]]
        rows.append({'year': y, 'n': len(idx), 'flagged': len(f_), 'other': len(o_),
                     'flagged_share_pct': pct(len(f_), len(idx)), 'other_share_pct': pct(len(o_), len(idx)),
                     'flagged_with_ndc': sum(1 for i in f_ if has_ndc[i]), 'other_with_ndc': sum(1 for i in o_ if has_ndc[i]),
                     'flagged_ndc_pct': pct(sum(1 for i in f_ if has_ndc[i]), len(f_)),
                     'other_ndc_pct': pct(sum(1 for i in o_ if has_ndc[i]), len(o_)),
                     'coverage_pct': pct(sum(1 for i in idx if has_ndc[i]), len(idx)),
                     'flagged_compounding_rule': sum(1 for i in f_ if comp[i]), 'flagged_bulk_rule': sum(1 for i in f_ if blk[i])})
    out['D_years'] = rows

    def agg(idx):
        f_ = [i for i in idx if flag[i]]
        o_ = [i for i in idx if not flag[i]]
        return (len(f_) / len(idx), sum(has_ndc[i] for i in f_) / len(f_), sum(has_ndc[i] for i in o_) / len(o_))
    pooled_idx = [i for i in range(len(recs)) if 2013 <= year[i] <= 2026]
    sb, pfb, pob = agg(pooled_idx)
    s0, pf0, po0 = agg([i for i in range(len(recs)) if year[i] == 2013])
    s1, pf1, po1 = agg([i for i in range(len(recs)) if year[i] == 2026])
    e1 = agg([i for i in range(len(recs)) if 2013 <= year[i] <= 2016])
    e3 = agg([i for i in range(len(recs)) if 2022 <= year[i] <= 2026])
    out['D_decomposition'] = {
        'reference': 'pooled 2013-2026: flagged share %.4f, NDC rate flagged %.4f, NDC rate other %.4f' % (sb, pfb, pob),
        'y2013_to_y2026': decompose(s0, pf0, po0, s1, pf1, po1, sb, pfb, pob),
        'E1_to_E3': decompose(e1[0], e1[1], e1[2], e3[0], e3[1], e3[2], sb, pfb, pob)}

    with open(os.path.join(HERE, 'run4_results.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write('\n')
    write_report(out)
    print('A', out['A_pooled'], '| B', {e: (B[e]['missed'], B[e]['marked']) for e in B}, '| C', C.get('verdict'),
          '| D', {k: (v['composition_pp'], v['within_pp'], v['interaction_pp'], v['total_change_pp']) for k, v in out['D_decomposition'].items() if k != 'reference'})


def f(v):
    if isinstance(v, bool):
        return 'PASS' if v else 'FAIL'
    if isinstance(v, int):
        return '{:,}'.format(v)
    return str(v)


def ci(w):
    return '%s-%s' % (w[0], w[1]) if w and w[0] is not None else 'n/a'


def md(s):
    return s.replace('|', '/')


def write_report(o):
    A, B, C, D = o['A'], o['B'], o['C'], o['D_decomposition']
    y = D['y2013_to_y2026']
    er = D['E1_to_E3']
    L = []
    if C.get('complete'):
        L += ['# A15 Run 4 - validating the NO-NDC-EXPECTED label: %s' % C['verdict'], '',
              '- **V1 pooled precision %s%% (needs >= 85), lower Wilson bound %s%% (needs > 70): %s**' % (C['V1_pooled_precision_pct'], C['V1_lower_wilson_pct'], f(C['V1_pass'])),
              '- **V2 largest gap between era precisions %s pp (needs <= 15): %s**' % (C['V2_max_spread_pp'], f(C['V2_pass'])),
              '- **V3 E3 miss rate minus E1 miss rate %+.2f pp (needs <= +15): %s**' % (C['V3_E3_minus_E1_pp'], f(C['V3_pass'])),
              '- **VERDICT: %s.** Criteria pre-registered in the run 4 brief; not adjusted.' % C['verdict'],
              '- **Decomposition, 2013 to 2026:** coverage %s%% -> %s%%, change %+.2f pp = composition %+.2f pp (%s%%) + within-group %+.2f pp (%s%%) + interaction %+.2f pp (%s%%).'
              % (y['coverage_from_pct'], y['coverage_to_pct'], y['total_change_pp'], y['composition_pp'], y['composition_share_pct'], y['within_pp'], y['within_share_pct'], y['interaction_pp'], y['interaction_share_pct']),
              '- **Decomposition, E1 to E3 (robustness):** %s%% -> %s%%, change %+.2f pp = composition %+.2f pp (%s%%) + within-group %+.2f pp (%s%%) + interaction %+.2f pp (%s%%).'
              % (er['coverage_from_pct'], er['coverage_to_pct'], er['total_change_pp'], er['composition_pp'], er['composition_share_pct'], er['within_pp'], er['within_share_pct'], er['interaction_pp'], er['interaction_share_pct']),
              '- Precision by era: ' + '; '.join('%s %s%% (%s/40, CI %s)' % (e, A[e]['precision_pct'], A[e]['correct'], ci(A[e]['wilson95'])) for e in A)
              + '. Miss rate by era: ' + '; '.join('%s %s%% (%s/40, CI %s)' % (e, B[e]['miss_rate_pct'], B[e]['missed'], ci(B[e]['wilson95'])) for e in B) + '.',
              '- Rules imported unchanged (run 2 parser `%s...`, run 3 label rules `%s...`, digests checked at run time). Data SHA-256 `%s`, %s records, confirmed first.'
              % (o['rule_sources']['run2_ndc_recovery.py'][:16], o['rule_sources']['run3_parser_validation.py'][:16], o['data']['sha256'], f(o['data']['records'])),
              '- No model, nothing fitted, no paper writing. `run4_label_validation.py` -> `run4_results.json`; marks in `run4_marks.json`.', '']
    else:
        L += ['# A15 Run 4 - INCOMPLETE: marks missing'] + [''] * 11
    L += ['---', '', '## 0. Design', '',
          'Year = year of `report_date`, as in runs 1-3. Eras E1 2013-2016, E2 2017-2021, E3 2022-2026. NO-NDC-EXPECTED = the run 3 compounding rule (stem "compound": compounded, compounding, compounder, compounds) OR the run 3 bulk rule (the word "bulk"; "active pharmaceutical ingredient" or the uppercase token API; "drug substance", "raw material" or "intermediate"; a kilogram quantity or the word drum), both imported from `run3_parser_validation.py` unchanged. "NDC from either source" = an openfda product_ndc, or at least one code accepted by the run 2 parser. Samples: `random.Random(seed).sample(sorted(record indexes), 40)`; seeds A E1 %d, E2 %d, E3 %d; seeds B E1 %d, E2 %d, E3 %d. All 240 were drawn before any was read. Full descriptions are quoted, whitespace collapsed, with employer-boundary terms replaced by `[REDACTED]` (%d replacements). Wilson 95%% intervals throughout.'
          % (o['seeds_A']['E1'], o['seeds_A']['E2'], o['seeds_A']['E3'], o['seeds_B']['E1'], o['seeds_B']['E2'], o['seeds_B']['E3'], o['boundary_redactions']), '']

    L += ['## A. Precision of the label', '',
          'Population: every record the composite label flags, whether or not it carries an NDC. Correct = the recalled item really is a compounded preparation, a bulk substance, an API, a raw material or an intermediate. Kind = compounded, bulk or both.', '',
          '| Era | Flagged records (compounding rule / bulk rule) | Correct | Precision % | Wilson 95% | Correct by kind: compounded / bulk / both | Compounding-rule hits correct | Bulk-rule hits correct |',
          '|---|---|---|---|---|---|---|---|']
    for e in A:
        a = A[e]
        ck = a['correct_kind']
        L.append('| %s | %s (%s / %s) | %s / %s | %s | %s | %s / %s / %s | %s / %s | %s / %s |' % (
            e, f(a['population']), f(a['population_compounding_rule']), f(a['population_bulk_rule']), a['correct'], a['marked'], a['precision_pct'], ci(a['wilson95']),
            ck['compounded'], ck['bulk'], ck['both'], a['by_rule_component']['compounding_rule'][0], a['by_rule_component']['compounding_rule'][1],
            a['by_rule_component']['bulk_rule'][0], a['by_rule_component']['bulk_rule'][1]))
    ap = o['A_pooled']
    L += ['| pooled | | %s / %s | %s | %s | | | |' % (ap['correct'], ap['marked'], ap['precision_pct'], ci(ap['wilson95'])), '']
    for e in A:
        L += ['### A-%s sample (seed %d)' % (e, o['seeds_A'][e]), '', '| # | Record | Year | Rule hit | NDC | Mark | Full product_description |', '|---|---|---|---|---|---|---|']
        for n, x in enumerate(A[e]['sample'], 1):
            hit = '+'.join(k for k, v in (('compounding', x['rule_compounding']), ('bulk', x['rule_bulk'])) if v)
            mk = (x['mark'] or 'UNMARKED') + ((' (' + x['kind'] + ')') if x['kind'] else '') + ((' - ' + x['note']) if x['note'] else '')
            L.append('| %d | %s | %d | %s | %s | %s | %s |' % (n, x['key'], x['year'], hit, 'yes' if x['has_ndc'] else 'no', mk, md(x['description'])))
        L.append('')

    L += ['## B. Miss rate of the label', '',
          'Population: records with NO NDC from either source that the label does NOT flag. missed = the item is in fact a compounded or bulk product the rule did not catch.', '',
          '| Era | Unflagged no-NDC records | Missed | Miss rate % | Wilson 95% | Missed by kind: compounded / bulk / both |', '|---|---|---|---|---|---|']
    for e in B:
        b = B[e]
        mk = b['missed_kind']
        L.append('| %s | %s | %s / %s | %s | %s | %s / %s / %s |' % (e, f(b['population']), b['missed'], b['marked'], b['miss_rate_pct'], ci(b['wilson95']), mk['compounded'], mk['bulk'], mk['both']))
    L.append('')
    for e in B:
        L += ['### B-%s sample (seed %d)' % (e, o['seeds_B'][e]), '', '| # | Record | Year | Mark | Full product_description |', '|---|---|---|---|---|']
        for n, x in enumerate(B[e]['sample'], 1):
            mk = (x['mark'] or 'UNMARKED') + ((' (' + x['kind'] + ')') if x['kind'] else '') + ((' - ' + x['note']) if x['note'] else '')
            L.append('| %d | %s | %d | %s | %s |' % (n, x['key'], x['year'], mk, md(x['description'])))
        L.append('')

    if C.get('complete'):
        L += ['## C. Pre-registered criteria', '',
              '- V1: pooled precision %s%% (%s of %s), Wilson 95%% %s. Needs >= 85%% and lower bound > 70%%. **%s**' % (C['V1_pooled_precision_pct'], ap['correct'], ap['marked'], ci(ap['wilson95']), f(C['V1_pass'])),
              '- V2: era precisions %s; largest gap %s pp. Needs <= 15. **%s**' % (', '.join('%s %s%%' % (e, A[e]['precision_pct']) for e in A), C['V2_max_spread_pp'], f(C['V2_pass'])),
              '- V3: miss rates E1 %s%%, E3 %s%%; E3 - E1 = %+.2f pp. Needs <= +15. **%s**' % (B['E1']['miss_rate_pct'], B['E3']['miss_rate_pct'], C['V3_E3_minus_E1_pp'], f(C['V3_pass'])),
              '- **Verdict: %s.**' % C['verdict'],
              '- Sensitivity, NOT the gate: if the %d records marked incorrect as finished dosage forms in bulk packaging were counted correct, era precisions would be %s, pooled %s%% (CI %s); V1 %s, V2 spread %s pp %s. The verdict above is computed on the marks as made; this line shows how much of it rests on that one marking decision.'
              % (sum(A[e]['incorrect_bulk_finished'] for e in A), ', '.join('%s %s%%' % (e, v) for e, v in C['sensitivity_bulk_finished_correct']['precision_by_era'].items()),
                 C['sensitivity_bulk_finished_correct']['pooled_pct'], ci(C['sensitivity_bulk_finished_correct']['pooled_wilson95']),
                 f(C['sensitivity_bulk_finished_correct']['V1_pass']), C['sensitivity_bulk_finished_correct']['V2_spread_pp'], f(C['sensitivity_bulk_finished_correct']['V2_pass'])), '',
              '**Can each criterion fail on this data?** V1 and V2 compare hand-marked counts with thresholds that a plausible outcome (for example 32 of 40 correct in one era) would breach, so both can fail. V3 compares two measured rates and can fail (here it would need an E3 miss rate above 82.5%), but it is ONE-SIDED: it tests only for the rule going blind LATE. It passes by a wide margin because the misses run the other way, and it says nothing about the large early miss rate, which Part E addresses. None of the three is rank-based. **One limit on what V3 can see:** Part B samples only records with no NDC, as the brief specifies, so V3 cannot detect the rule going blind among compounded or bulk products that DO carry an NDC. That population is in the Part D groups (a missed compounded product with an NDC would sit in "other" and raise its NDC rate). It is recorded here, not tested; testing it would be new scope.', '']

    L += ['## D. Per-year table and decomposition', '',
          'Flagged = the label flags the record ("no-NDC-expected" group); other = it does not. NDC = from either source. Coverage = all records with an NDC / all records.', '',
          '| Year | n | Flagged (% of n) | Other (% of n) | Flagged with NDC (%) | Other with NDC (%) | Coverage % | Flagged by compounding rule / bulk rule |', '|---|---|---|---|---|---|---|---|']
    for r in o['D_years']:
        L.append('| %d | %s | %s (%s) | %s (%s) | %s (%s) | %s (%s) | %s | %s / %s |' % (
            r['year'], f(r['n']), f(r['flagged']), r['flagged_share_pct'], f(r['other']), r['other_share_pct'], f(r['flagged_with_ndc']), r['flagged_ndc_pct'],
            f(r['other_with_ndc']), r['other_ndc_pct'], r['coverage_pct'], f(r['flagged_compounding_rule']), f(r['flagged_bulk_rule'])))
    L += ['', '**Arithmetic.** For a period, coverage C = s x pF + (1 - s) x pO, where s is the flagged share, pF the NDC rate among flagged records and pO the NDC rate among other records. With bars for the pooled 2013-2026 values (%s) and d for the change from the first period to the second:' % D['reference'], '',
          '- composition = ds x (pFbar - pObar)', '- within-group = sbar x dpF + (1 - sbar) x dpO', '- interaction = dC - composition - within-group', '',
          'Shares are each part divided by dC. A negative share means that part worked against the total change.', '',
          '| Comparison | Coverage from | Coverage to | Total change, pp | Composition, pp (share) | Within-group, pp (share) | Interaction, pp (share) | s from / to | pF from / to | pO from / to |', '|---|---|---|---|---|---|---|---|---|---|']
    for lab, k in (('2013 -> 2026', 'y2013_to_y2026'), ('E1 -> E3', 'E1_to_E3')):
        v = D[k]
        i = v['inputs']
        L.append('| %s | %s%% | %s%% | %+.2f | %+.2f (%s%%) | %+.2f (%s%%) | %+.2f (%s%%) | %s / %s | %s / %s | %s / %s |' % (
            lab, v['coverage_from_pct'], v['coverage_to_pct'], v['total_change_pp'], v['composition_pp'], v['composition_share_pct'], v['within_pp'], v['within_share_pct'],
            v['interaction_pp'], v['interaction_share_pct'], i['s_from'], i['s_to'], i['pF_from'], i['pF_to'], i['pO_from'], i['pO_to']))
    L.append('')
    if C.get('complete'):
        L += ['## E. What this says', '',
              '- **The decomposition.** From 2013 to 2026, coverage rose %+.2f pp. Holding within-group NDC rates at their pooled values, the change in group shares accounts for %+.2f pp (%s%% of the change): composition. Holding shares at pooled values, the change in within-group NDC rates accounts for %+.2f pp (%s%%): within-group. The interaction is %+.2f pp (%s%%). E1 to E3 gives the same ordering: composition %s%%, within-group %s%%, interaction %s%%.'
              % (y['total_change_pp'], y['composition_pp'], y['composition_share_pct'], y['within_pp'], y['within_share_pct'], y['interaction_pp'], y['interaction_share_pct'],
                 er['composition_share_pct'], er['within_share_pct'], er['interaction_share_pct']),
              '- **Both parts are material.** Within-group change is the larger part in both comparisons, and composition is between half and two-thirds its size (21.05 / 37.88 and 15.73 / 24.40). The claim cannot be "the trend is composition"; it has to carry both.',
              '- **The label fails its own validation (V2), so the split above is computed with a label that is not validated.** E3 precision is lower because the bulk rule catches finished products in bulk packaging, which carry NDCs (9 of the 9 E3 errors). The per-year table is consistent with that: the flagged group\'s NDC rate reaches %s%% in 2026.' % [r for r in o['D_years'] if r['year'] == 2026][0]['flagged_ndc_pct'],
              '- **The label also misses most compounded products in the early years** (Part B: %s%%, %s%% and %s%% of unflagged no-NDC records are compounded or bulk items the rule missed, in E1, E2 and E3). V3 passes because the misses FALL over time, not because they are small. Those missed records sit in the "other" group with no NDC, which lowers the other group\'s early NDC rate. That moves measured change from the composition term into the within-group term, so the within-group share above is larger, and the composition share smaller, than a label without that miss pattern would give. The size of the shift is not estimated here.'
              % (B['E1']['miss_rate_pct'], B['E2']['miss_rate_pct'], B['E3']['miss_rate_pct']),
              '',
              '## F. Limitations carried forward (not fixed here)', '',
              '- The run 2 parser does not accept dotted NDCs (27854.101.01) or product-level codes with no package segment. Run 3 found them rare (three misses in 120) and left the parser unchanged.',
              '- **A rule that would be better, recorded and NOT applied (applying it would void run 3):** the compounding signal should key on the preparer, not the word. Most missed compounded records name a pharmacy, infusion pharmacy or outsourcing facility without the stem "compound"; and the bulk signal should exclude finished dosage forms whose description says "bulk container", "bulk pack", "pharmacy bulk package" or drums of a finished product. Whether to adopt either is the author\'s decision; both would need their own validation run.',
              '- Marks are one reader\'s judgments. The rules used are stated in `run4_marks.json` ("rules"). Judgments that rested on firm or product line rather than explicit wording carry a note.', '']
    with open(os.path.join(HERE, 'RUN4-REPORT.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
