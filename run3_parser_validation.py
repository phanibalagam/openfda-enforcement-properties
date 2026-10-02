# DISCLAIMER BEGIN
# This work was carried out independently, on personal time and equipment, and is not
# connected to the author's employment. The views expressed are the author's own and do
# not represent the views, positions or policies of any current, former or future employer
# or client. No proprietary, confidential or internal data of any organization was used.
# All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
# DISCLAIMER END
# Run 3 of concept A15: parser validation by era. No model, nothing fitted.
#   python3 -B run3_parser_validation.py
# The parser is IMPORTED from run2_ndc_recovery.py, not copied, so its accept and reject
# rules are the run 2 rules byte for byte; the script refuses to run if that file changed.
# Deterministic: every sample is drawn with a fixed, stated seed.
# Reads run3_marks.json (hand marks) if present; writes run3_results.json and RUN3-REPORT.md.
import hashlib, io, json, math, os, random, re, statistics, sys, zipfile

sys.dont_write_bytecode = True  # no __pycache__ in the program folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run2_ndc_recovery as R2  # parse(), norm_product(), ten_to_nine_candidates(), spearman(), pct()
from boundary_scan import load_terms

DATA = os.path.join(HERE, 'data', 'drug-enforcement-0001-of-0001.json.zip')
ENTRY = 'drug-enforcement-0001-of-0001.json'
WANT_SHA = 'c6eb46526a3ad52102a88b65727874c2e23c43300b27e704eada05960d755092'
WANT_N = 17975
# run2_ndc_recovery.py as it stood when run 2 closed (digest taken on the device 2026-09-28)
RUN2_SHA = '892aacebdeb522adef4ca4f2beef658b8ac9a61f843f4631cb26d77f4571b263'

ERAS = [('E1', 2013, 2016), ('E2', 2017, 2021), ('E3', 2022, 2026)]
YEARS = list(range(2013, 2027))
N_PER_ERA = 40
SEEDS_A = {'E1': 31001, 'E2': 31002, 'E3': 31003}  # precision samples (recovered records)
SEEDS_B = {'E1': 32001, 'E2': 32002, 'E3': 32003}  # recall samples (nothing recovered, no openfda NDC)
Z = 1.959963984540054

# Pre-registered test, fixed by the run 3 brief before any record was looked at.
COLLAPSE_MAX_ABS_SPEARMAN = 0.50
COLLAPSE_MAX_DEV_PP = 10.0

# Descriptive rules for Part D (not part of any gate)
NDC_TOKEN = re.compile(r'(?<![A-Za-z])ndc(?![A-Za-z])', re.I)
NDC_LIKE = re.compile(r'(?<!\d)\d{4,5}-\d{3,4}-\d{1,2}(?!\d)|(?<![\d-])\d{10,11}(?![\d-])')
# Bulk / API / non-finished-product signal. Each component is reported on its own.
BULK_RULES = [
    ('bulk', re.compile(r'\bbulk\b', re.I)),
    ('active pharmaceutical ingredient / API', re.compile(r'active pharmaceutical ingredient|\bAPIs?\b')),
    ('drug substance / raw material / intermediate', re.compile(r'drug substance|raw material|\bintermediate\b', re.I)),
    ('kilogram or drum quantity', re.compile(r'\d\s*(kg|kgs|kilograms?)\b|\bdrums?\b', re.I)),
]
# Added after Part B was read, to test the alternative the recall sample suggested; it is
# descriptive only and feeds no gate: the stem "compound" (compounded, compounding, compounder).
COMPOUND = re.compile(r'compound(?:ed|ing|er|s)?\b', re.I)
# A placeholder labeler segment: the labeler is one digit repeated (99999, 9999, 11111 ...).
PLACEHOLDER = re.compile(r'^(\d)\1{3,4}$')


def wilson(k, n):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (round(100 * (c - h), 2), round(100 * (c + h), 2))


def no_pad_zero(x):
    """An 11-digit form is a 10-digit NDC with one segment zero-padded, so a real one has a
    0 at position 1, 6 or 10. One without is structurally impossible as an FDA NDC."""
    d = x['digits11']
    return bool(d) and x['shape'] in ('5-4-2', '11-digit') and d[0] != '0' and d[5] != '0' and d[9] != '0'


def era_of(y):
    for e, a, b in ERAS:
        if a <= y <= b:
            return e
    return None


def labeler_of(x):
    if x['digits11']:
        raw = x['raw']
        return raw.split('-')[0] if '-' in raw else raw[:5]
    return None  # a 10-digit unhyphenated code has no determinable labeler segment


def quart(v):
    if not v:
        return {'n': 0}
    s = sorted(v)
    q = statistics.quantiles(s, n=4, method='inclusive') if len(s) > 1 else [s[0]] * 3
    return {'n': len(s), 'median': q[1], 'q1': q[0], 'q3': q[2]}


def main():
    raw = open(DATA, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    recs = json.loads(zipfile.ZipFile(io.BytesIO(raw)).read(ENTRY))['results']
    if sha != WANT_SHA or len(recs) != WANT_N:
        sys.exit('STOP: data file SHA-256 %s, %d records; expected %s, %d' % (sha, len(recs), WANT_SHA, WANT_N))
    r2sha = hashlib.sha256(open(os.path.join(HERE, 'run2_ndc_recovery.py'), 'rb').read()).hexdigest()
    if r2sha != RUN2_SHA:
        sys.exit('STOP: run2_ndc_recovery.py has changed (%s); the parser must be the run 2 parser' % r2sha)
    terms = load_terms()

    def redact(s):
        n = 0
        for p in terms:
            s, k = p.subn('[REDACTED]', s)
            n += k
        return s, n

    of_prod9 = set()
    for r in recs:
        for p in (r.get('openfda') or {}).get('product_ndc') or []:
            of_prod9.add(R2.norm_product(p))
    has_of = [bool((r.get('openfda') or {}).get('product_ndc')) for r in recs]
    parsed = {}
    for i, r in enumerate(recs):
        if not has_of[i]:
            acc, _ = R2.parse(r.get('product_description'))
            if acc:
                parsed[i] = acc
    year = [int(r['report_date'][:4]) for r in recs]
    out = {'data': {'sha256': sha, 'records': len(recs)}, 'run2_parser_sha256': r2sha,
           'date_field': 'report_date (year), as in runs 1 and 2',
           'eras': ERAS, 'seeds_A': SEEDS_A, 'seeds_B': SEEDS_B, 'n_per_era': N_PER_ERA,
           'recovered_total_check': len(parsed)}

    marks_path = os.path.join(HERE, 'run3_marks.json')
    marks = json.load(open(marks_path, encoding='utf-8')) if os.path.exists(marks_path) else {'A': {}, 'B': {}}

    # ---------------- Part A: precision by era
    A = {}
    red_total = 0
    for e, a, b in ERAS:
        pop = sorted(i for i in parsed if a <= year[i] <= b)
        ids = random.Random(SEEDS_A[e]).sample(pop, N_PER_ERA)
        rows = []
        for i in ids:
            r = recs[i]
            t = r['product_description']
            acc = parsed[i]
            s0 = max(0, min(x['start'] for x in acc) - 70)
            s1 = min(len(t), max(x['end'] for x in acc) + 30)
            snip = ('...' if s0 > 0 else '') + t[s0:s1] + ('...' if s1 < len(t) else '')
            snip, n = redact(' '.join(snip.split()))
            red_total += n
            key = '%s#%d' % (r.get('recall_number'), i)
            mk = marks['A'].get(key, {})
            rows.append({'key': key, 'year': year[i], 'extracted': [x['raw'] for x in acc],
                         'placeholder_codes': [x['raw'] for x in acc if labeler_of(x) and PLACEHOLDER.match(labeler_of(x))],
                         'snippet': snip, 'mark': mk.get('mark'), 'note': mk.get('note', '')})
        marked = [x for x in rows if x['mark'] in ('correct', 'incorrect')]
        k = sum(1 for x in marked if x['mark'] == 'correct')
        codes = [x for i in pop for x in parsed[i]]
        ph = [x for x in codes if labeler_of(x) and PLACEHOLDER.match(labeler_of(x))]
        A[e] = {'population_records': len(pop), 'sample': rows, 'marked': len(marked), 'correct': k,
                'precision_pct': R2.pct(k, len(marked)) if len(marked) == N_PER_ERA else None,
                'wilson95': wilson(k, len(marked)) if len(marked) == N_PER_ERA else None,
                'placeholder_codes_all_recovered': len(ph), 'codes_all_recovered': len(codes),
                'placeholder_records_all_recovered': sum(1 for i in pop if any(labeler_of(x) and PLACEHOLDER.match(labeler_of(x)) for x in parsed[i])),
                'placeholder_codes_in_sample': sum(len(x['placeholder_codes']) for x in rows),
                'no_pad_zero_codes_all_recovered': sum(1 for x in codes if no_pad_zero(x)),
                'no_pad_zero_codes_in_sample': sum(1 for i in ids for x in parsed[i] if no_pad_zero(x))}
    kk = sum(A[e]['correct'] for e in A)
    nn = sum(A[e]['marked'] for e in A)
    out['A'] = A
    out['A_pooled'] = {'correct': kk, 'marked': nn, 'precision_pct': R2.pct(kk, nn), 'wilson95': wilson(kk, nn)}

    # ---------------- Part B: recall by era
    B = {}
    for e, a, b in ERAS:
        pop = sorted(i for i in range(len(recs)) if a <= year[i] <= b and not has_of[i] and i not in parsed)
        ids = random.Random(SEEDS_B[e]).sample(pop, N_PER_ERA)
        rows = []
        for i in ids:
            r = recs[i]
            d, n = redact(' '.join((r.get('product_description') or '').split()))
            red_total += n
            key = '%s#%d' % (r.get('recall_number'), i)
            mk = marks['B'].get(key, {})
            rows.append({'key': key, 'year': year[i], 'description': d,
                         'mark': mk.get('mark'), 'note': mk.get('note', ''), 'upc_ndc': bool(mk.get('upc_ndc'))})
        marked = [x for x in rows if x['mark'] in ('missed', 'none')]
        k = sum(1 for x in marked if x['mark'] == 'missed')
        B[e] = {'population_records': len(pop), 'sample': rows, 'marked': len(marked), 'missed': k,
                'upc_derivable': sum(1 for x in marked if x['upc_ndc'] and x['mark'] == 'none'),
                'miss_rate_pct': R2.pct(k, len(marked)) if len(marked) == N_PER_ERA else None,
                'wilson95': wilson(k, len(marked)) if len(marked) == N_PER_ERA else None}
    out['B'] = B
    out['boundary_redactions'] = red_total

    # ---------------- Part C: pre-registered test
    per_year = []
    for y in range(2012, 2027):
        idx = [i for i in range(len(recs)) if year[i] == y]
        of = sum(1 for i in idx if has_of[i])
        rc = sum(1 for i in idx if i in parsed)
        un = len(idx) - of - rc
        per_year.append({'year': y, 'total': len(idx), 'openfda': of, 'recovered': rc, 'unrecovered': un,
                         'combined': of + rc, 'era': era_of(y)})
    complete = all(B[e]['miss_rate_pct'] is not None for e in B)
    C = {'complete': complete}
    if complete:
        def test(rate_of_era):
            g = []
            for row in per_year:
                if row['year'] not in YEARS:
                    continue
                est = rate_of_era(row['era']) * row['unrecovered']
                g.append(dict(row, est_missed=round(est, 2), adjusted=round(row['combined'] + est, 2),
                              adjusted_pct=round(100.0 * (row['combined'] + est) / row['total'], 2)))
            pooled = 100.0 * sum(x['adjusted'] for x in g) / sum(x['total'] for x in g)
            for x in g:
                x['dev_pp'] = round(x['adjusted_pct'] - pooled, 2)
            outside = [x['year'] for x in g if abs(x['dev_pp']) > COLLAPSE_MAX_DEV_PP]
            rho = R2.spearman([x['year'] for x in g], [x['adjusted'] / x['total'] for x in g])
            collapse = abs(rho) <= COLLAPSE_MAX_ABS_SPEARMAN and not outside
            return {'rows': g, 'A1_pooled_pct': round(pooled, 2), 'A2_years_outside': outside,
                    'A2_n_outside': len(outside), 'A3_abs_spearman': round(abs(rho), 4),
                    'verdict': 'SLOPE IS A PARSER ARTIFACT (finding collapses)' if collapse else 'TREND SURVIVES (finding stands)'}
        C['point'] = test(lambda e: B[e]['missed'] / B[e]['marked'])
        C['sensitivity_upper_wilson'] = test(lambda e: B[e]['wilson95'][1] / 100.0)
        C['sensitivity_upc_derivable_as_missed'] = test(lambda e: (B[e]['missed'] + B[e]['upc_derivable']) / B[e]['marked'])
        C['sensitivity_upper_E1_only'] = test(lambda e: (B[e]['wilson95'][1] if e == 'E1' else 100.0 * B[e]['missed'] / B[e]['marked']) / 100.0)
    out['C'] = C

    # ---------------- Part D: why the early years recover little
    def group_of(i):
        if has_of[i]:
            return 'openfda NDC'
        return 'parse-recovered' if i in parsed else 'no NDC'
    fields = ['product_type', 'classification', 'voluntary_mandated', 'initial_firm_notification', 'status']
    D = {}
    for e, a, b in ERAS:
        D[e] = {}
        for gname in ('openfda NDC', 'parse-recovered', 'no NDC'):
            idx = [i for i in range(len(recs)) if a <= year[i] <= b and group_of(i) == gname]
            descs = [recs[i].get('product_description') or '' for i in idx]
            n = len(idx)
            row = {'n': n, 'desc_len': quart([len(t) for t in descs]),
                   'ndc_token_pct': R2.pct(sum(1 for t in descs if NDC_TOKEN.search(t)), n),
                   'ndc_like_digits_pct': R2.pct(sum(1 for t in descs if NDC_LIKE.search(t)), n),
                   'bulk_any_pct': R2.pct(sum(1 for t in descs if any(rx.search(t) for _, rx in BULK_RULES)), n),
                   'bulk_components_pct': {nm: R2.pct(sum(1 for t in descs if rx.search(t)), n) for nm, rx in BULK_RULES},
                   'compounding_pct': R2.pct(sum(1 for t in descs if COMPOUND.search(t)), n),
                   'fields': {}}
            for fld in fields:
                cnt = {}
                for i in idx:
                    v = recs[i].get(fld)
                    v = v.strip() if isinstance(v, str) and v.strip() else '(missing)'
                    cnt[v] = cnt.get(v, 0) + 1
                row['fields'][fld] = {k: [cnt[k], R2.pct(cnt[k], n)] for k in sorted(cnt)}
            D[e][gname] = row
    out['D'] = D
    DY = []
    for y in YEARS:
        idx = [i for i in range(len(recs)) if year[i] == y and group_of(i) == 'no NDC']
        ds = [recs[i].get('product_description') or '' for i in idx]
        n = len(idx)
        DY.append({'year': y, 'no_ndc_records': n,
                   'ndc_token_pct': R2.pct(sum(1 for t in ds if NDC_TOKEN.search(t)), n),
                   'bulk_pct': R2.pct(sum(1 for t in ds if any(rx.search(t) for _, rx in BULK_RULES)), n),
                   'compounding_pct': R2.pct(sum(1 for t in ds if COMPOUND.search(t)), n),
                   'bulk_or_compounding_pct': R2.pct(sum(1 for t in ds if COMPOUND.search(t) or any(rx.search(t) for _, rx in BULK_RULES)), n)})
    out['D_years'] = DY

    # ---------------- Part E: corroboration by era
    E = {}
    for e, a, b in ERAS:
        dist = {}
        for i in parsed:
            if a <= year[i] <= b:
                for x in parsed[i]:
                    dist[x['digits11'] or ('10:' + x['digits10'])] = x
        m = 0
        for k2, x in dist.items():
            if x['digits11']:
                m += x['digits11'][:9] in of_prod9
            else:
                m += bool(R2.ten_to_nine_candidates(x['digits10']) & of_prod9)
        E[e] = {'distinct_codes': len(dist), 'match_openfda_product': m, 'pct': R2.pct(m, len(dist)),
                'wilson95': wilson(m, len(dist))}
    out['E'] = E

    with open(os.path.join(HERE, 'run3_results.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write('\n')
    write_report(out)
    print('A pooled', out['A_pooled'], '| B', {e: (B[e]['missed'], B[e]['marked']) for e in B},
          '| C', (C.get('point') or {}).get('verdict'))


def f(v):
    if isinstance(v, bool):
        return 'yes' if v else 'no'
    if isinstance(v, int):
        return '{:,}'.format(v)
    if isinstance(v, float):
        return ('%.2f' % v)
    return str(v)


def ci(w):
    return '%s-%s' % (w[0], w[1]) if w and w[0] is not None else 'n/a'


def md(s):
    return s.replace('|', '/')


def write_report(o):
    A, B, C, D, E = o['A'], o['B'], o['C'], o['D'], o['E']
    L = []
    if C.get('complete'):
        p = C['point']
        L += ['# A15 Run 3 - parser validation by era: %s' % p['verdict'], '',
              '- **A1 adjusted pooled coverage 2013-2026: %s%%**' % p['A1_pooled_pct'],
              '- **A2 years outside +/-10 pp of adjusted pooled: %d of 14** (%s)' % (p['A2_n_outside'], ', '.join(str(y) for y in p['A2_years_outside']) or 'none'),
              '- **A3 abs Spearman(year, adjusted coverage): %s** (collapse requires <= 0.50 AND no year outside)' % p['A3_abs_spearman'],
              '- **VERDICT: %s.** Test pre-registered in the run 3 brief; not adjusted.' % p['verdict'],
              '- Per-era miss rates (Part B): ' + '; '.join('%s %s%% (%s of %s, 95%% CI %s)' % (e, B[e]['miss_rate_pct'], B[e]['missed'], B[e]['marked'], ci(B[e]['wilson95'])) for e in B) + '.',
              '- Per-era precision (Part A): ' + '; '.join('%s %s%% (%s of %s, 95%% CI %s)' % (e, A[e]['precision_pct'], A[e]['correct'], A[e]['marked'], ci(A[e]['wilson95'])) for e in A) + '.',
              '- Parser imported unchanged from `run2_ndc_recovery.py` (SHA-256 `%s`, checked at run time). Data SHA-256 `%s`, %s records, confirmed first.' % (o['run2_parser_sha256'], o['data']['sha256'], f(o['data']['records'])),
              '- No model, nothing fitted, no paper writing. Generated by `run3_parser_validation.py`; numbers in `run3_results.json`; marks in `run3_marks.json`.', '']
    else:
        L += ['# A15 Run 3 - INCOMPLETE: marks missing', '', 'Part B marks are not all present, so Part C was not computed.', '', '', '', '', '', '', '']
    L += ['---', '', '## 0. Design', '',
          'Year = year of `report_date`, the field runs 1 and 2 used. Eras: E1 2013-2016, E2 2017-2021, E3 2022-2026. Parser: `parse()` imported from `run2_ndc_recovery.py`, whose digest is checked before anything runs. Samples: `random.Random(seed).sample(sorted(record indexes), 40)` per era; seeds A (precision) E1 %d, E2 %d, E3 %d; seeds B (recall) E1 %d, E2 %d, E3 %d. All 240 samples were drawn by the script before any was read. Employer-boundary terms in quoted text would be replaced by `[REDACTED]`; %d replacements were made. Wilson 95%% intervals throughout.'
          % (o['seeds_A']['E1'], o['seeds_A']['E2'], o['seeds_A']['E3'], o['seeds_B']['E1'], o['seeds_B']['E2'], o['seeds_B']['E3'], o['boundary_redactions']), '']

    # Part A
    L += ['## A. Precision by era', '',
          'Population: records with no openfda NDC from which the parser recovered at least one code. Correct = every extracted code is an NDC as the description presents it. A placeholder labeler (one digit repeated, e.g. 99999) is counted as its own category below, not argued; a record whose only code is a placeholder is marked incorrect, as in run 2.', '',
          '| Era | Recovered records | Sample correct | Precision % | Wilson 95% | Placeholder codes / all recovered codes | Records with a placeholder | Placeholder codes in sample | 11-digit codes with no pad zero (all / sample) |',
          '|---|---|---|---|---|---|---|---|---|']
    for e in A:
        a = A[e]
        L.append('| %s | %s | %s / %s | %s | %s | %s / %s | %s | %s | %s / %s |' % (e, f(a['population_records']), a['correct'], a['marked'], a['precision_pct'], ci(a['wilson95']),
                                                                      f(a['placeholder_codes_all_recovered']), f(a['codes_all_recovered']), f(a['placeholder_records_all_recovered']), a['placeholder_codes_in_sample'],
                                                                      f(a['no_pad_zero_codes_all_recovered']), a['no_pad_zero_codes_in_sample']))
    ap = o['A_pooled']
    L += ['| pooled | | %s / %s | %s | %s | | | | |' % (ap['correct'], ap['marked'], ap['precision_pct'], ci(ap['wilson95'])), '',
          'Two named categories, counted rather than argued. Placeholder: a labeler segment that is one digit repeated (99999). No pad zero: an 11-digit form with no 0 at position 1, 6 or 10, which no real 10-digit NDC can produce; these are codes printed by the firm (mostly compounders) that cannot be FDA NDCs. Both are marked incorrect in the samples.', '']
    for e in A:
        L += ['### A-%s sample (seed %d)' % (e, o['seeds_A'][e]), '', '| # | Record | Year | Extracted | Mark | Snippet |', '|---|---|---|---|---|---|']
        for n, x in enumerate(A[e]['sample'], 1):
            L.append('| %d | %s | %d | %s | %s | %s |' % (n, x['key'], x['year'], ', '.join('`%s`' % c for c in x['extracted']),
                                                      (x['mark'] or 'UNMARKED') + ((' - ' + x['note']) if x['note'] else ''), md(x['snippet'])))
        L.append('')

    # Part B
    L += ['## B. Recall by era', '',
          'Population: records with no openfda NDC from which the parser recovered nothing. Each full description was read. missed = a usable NDC is in the text and the parser did not return it; none = no usable NDC in the text (a UPC, lot number or catalog number is not an NDC).', '',
          '| Era | Unrecovered records | Missed in sample | Miss rate % | Wilson 95% | Marked none but NDC-derivable from a 3-prefixed UPC |', '|---|---|---|---|---|---|']
    for e in B:
        b = B[e]
        L.append('| %s | %s | %s / %s | %s | %s | %s |' % (e, f(b['population_records']), b['missed'], b['marked'], b['miss_rate_pct'], ci(b['wilson95']), b['upc_derivable']))
    L.append('')
    for e in B:
        L += ['### B-%s sample (seed %d)' % (e, o['seeds_B'][e]), '', '| # | Record | Year | Mark | Full product_description |', '|---|---|---|---|---|']
        for n, x in enumerate(B[e]['sample'], 1):
            L.append('| %d | %s | %d | %s | %s |' % (n, x['key'], x['year'], (x['mark'] or 'UNMARKED') + ((' - ' + x['note']) if x['note'] else ''), md(x['description'])))
        L.append('')

    # Part C
    if C.get('complete'):
        p = C['point']
        L += ['## C. Pre-registered test', '',
              'Estimated missed records in a year = (era miss rate) x (records that year with no openfda NDC and nothing recovered). Adjusted combined = combined + estimate. Collapse only if abs Spearman <= 0.50 AND every year 2013-2026 is within 10 pp of adjusted pooled.', '',
              '| Year | Era | Total | openfda | Recovered | Unrecovered | Est. missed | Adjusted | Adjusted % | Dev from pooled, pp |', '|---|---|---|---|---|---|---|---|---|---|']
        for x in p['rows']:
            L.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %+.2f |' % (x['year'], x['era'], f(x['total']), f(x['openfda']), f(x['recovered']), f(x['unrecovered']),
                                                                         f(x['est_missed']), f(x['adjusted']), f(x['adjusted_pct']), x['dev_pp']))
        L += ['', '- A1 = %s%%; A2 = %d of 14 years outside (%s); A3 = %s. **%s.**' % (p['A1_pooled_pct'], p['A2_n_outside'], ', '.join(str(y) for y in p['A2_years_outside']) or 'none', p['A3_abs_spearman'], p['verdict'])]
        for nm, lab in [('sensitivity_upper_wilson', 'every era at the UPPER Wilson bound of its miss rate'),
                        ('sensitivity_upc_derivable_as_missed', 'records whose only code is an NDC-derivable 3-prefixed UPC counted as MISSED'),
                        ('sensitivity_upper_E1_only', 'E1 at its upper Wilson bound, E2 and E3 at their point estimates (the case most favorable to the objection)')]:
            s = C[nm]
            L.append('- Sensitivity, not the gate - %s: A1 %s%%, %d years outside, A3 %s: %s.' % (lab, s['A1_pooled_pct'], s['A2_n_outside'], s['A3_abs_spearman'], s['verdict']))
        L.append('')

    # Part D
    L += ['## D. Why the early years recover little', '',
          'Three groups per era: records with an openfda NDC, records the parser recovered from, and records with no NDC from either source. NDC token = the letters NDC not inside a word, any case. NDC-like digits = any 4-5/3-4/1-2 hyphenated group or standalone 10-11 digit run, accepted by the parser or not. Bulk signal = any of: the word "bulk"; "active pharmaceutical ingredient" or the uppercase token API; "drug substance", "raw material" or "intermediate"; a kilogram quantity or the word drum. Each component is shown separately.', '']
    L += ['| Era | Group | n | Desc length median (IQR) | NDC token % | NDC-like digits % | Bulk signal % | ' + ' | '.join(nm for nm, _ in BULK_RULES) + ' | Compounding % (added) |',
          '|---|---|---|---|---|---|---|' + '---|' * (len(BULK_RULES) + 1)]
    for e in D:
        for gname, r in D[e].items():
            dl = r['desc_len']
            L.append('| %s | %s | %s | %s (%s-%s) | %s | %s | %s | %s |' % (e, gname, f(r['n']), dl.get('median'), dl.get('q1'), dl.get('q3'),
                                                                       r['ndc_token_pct'], r['ndc_like_digits_pct'], r['bulk_any_pct'],
                                                                       ' | '.join(str(r['bulk_components_pct'][nm]) for nm, _ in BULK_RULES) + ' | ' + str(r['compounding_pct'])))
    L += ['', 'Compounding % was NOT in the brief. It was added after the Part B sample showed that most unrecovered early records are compounded products, to test that alternative with a number. Rule: the stem "compound" (compounded, compounding, compounder) anywhere in the description.', '',
          'Records with no NDC from either source, by year:', '',
          '| Year | No-NDC records | NDC token % | Bulk signal % | Compounding % | Bulk or compounding % |', '|---|---|---|---|---|---|']
    for x in o['D_years']:
        L.append('| %d | %s | %s | %s | %s | %s |' % (x['year'], f(x['no_ndc_records']), x['ndc_token_pct'], x['bulk_pct'], x['compounding_pct'], x['bulk_or_compounding_pct']))
    L.append('')
    for fld in ['product_type', 'classification', 'voluntary_mandated', 'initial_firm_notification', 'status']:
        vals = sorted({v for e in D for g in D[e].values() for v in g['fields'][fld]})
        L += ['%s, %% within group (n in brackets):' % fld, '', '| Era | Group | ' + ' | '.join(md(v) for v in vals) + ' |', '|---|---|' + '---|' * len(vals)]
        for e in D:
            for gname, r in D[e].items():
                cells = []
                for v in vals:
                    c = r['fields'][fld].get(v)
                    cells.append('%s (%s)' % (c[1], c[0]) if c else '0')
                L.append('| %s | %s | %s |' % (e, gname, ' | '.join(cells)))
        L.append('')

    # Part E
    L += ['## E. Corroboration by era', '',
          'Distinct parsed codes whose product part equals a product openfda annotated on any record in the file. A code seen in two eras counts in each.', '',
          '| Era | Distinct parsed codes | Matching an openfda product | % | Wilson 95% |', '|---|---|---|---|---|']
    for e in E:
        L.append('| %s | %s | %s | %s | %s |' % (e, f(E[e]['distinct_codes']), f(E[e]['match_openfda_product']), E[e]['pct'], ci(E[e]['wilson95'])))
    L.append('')
    if C.get('complete'):
        dy = {x['year']: x for x in o['D_years']}
        d1 = D['E1']['no NDC']
        L += ['## F. Reading the results', '',
              '- **The objection is not supported.** Miss rates are %s, %s and %s%% in E1, E2 and E3 (one record in each 40). Precision is %s, %s and %s%%. Neither moves across eras in the direction the objection needs. Even at the upper 95%% bound of the E1 miss rate with the other eras at their point estimates, %d of 14 years stay outside the band and the rank correlation is unchanged at %s: the per-era adjustment is too small to reorder any year.'
              % (B['E1']['miss_rate_pct'], B['E2']['miss_rate_pct'], B['E3']['miss_rate_pct'], A['E1']['precision_pct'], A['E2']['precision_pct'], A['E3']['precision_pct'],
                 C['sensitivity_upper_E1_only']['A2_n_outside'], C['sensitivity_upper_E1_only']['A3_abs_spearman']),
              '- **Why A3 does not move at all.** Adding a constant fraction of each year\'s unrecovered records moves every year in the same direction by a small amount; with miss rates this low and this flat, no two years swap rank, so the Spearman statistic is identical to run 2\'s.',
              '- **What the misses look like.** All three are NDCs printed in forms outside the run 2 shapes: dotted (27854.101.01), a 10-digit code with its leading zero dropped (9 digits), and a product-level code with no package segment. Each is a one-off form; the samples show no early-era format that the parser systematically misses.',
              '- **Why 2013 and 2015 recover little: the text carries no NDC.** Among E1 records with no NDC from either source, %s%% contain the token NDC at all and %s%% contain any NDC-shaped digit group, against about 100%% in both NDC-carrying groups. The parser is not failing to read these records; there is nothing to read.'
              % (d1['ndc_token_pct'], d1['ndc_like_digits_pct']),
              '- **The bulk/API hypothesis holds for 2015 only, and only in part.** The bulk signal covers %s%% of 2015\'s no-NDC records (most of them one API distributor\'s series of recalls: "active pharmaceutical ingredient packaged in varying grams or kg in bags or drums") but %s%% in 2013 and %s%% in 2016. It does not explain 2013.'
              % (dy[2015]['bulk_pct'], dy[2013]['bulk_pct'], dy[2016]['bulk_pct']),
              '- **The evidence points to compounded products.** The compounding stem appears in %s%% of 2013\'s no-NDC records and %s%% of 2015\'s, against %s%% or less in each year 2024-2026. Compounded preparations often carry no NDC, so a recall of one may have no code to print; the E1 recall sample in Part B is mostly compounded products with no code in the text. Bulk or compounding together covers %s%% of 2013 and %s%% of 2015. This is a text signal, not a verified classification, and it was added after Part B was read (stated in Part D). Read with Part D\'s other columns (in E1 the no-NDC group has far more Telephone and Press Release notification, far fewer Letters and far fewer Class III recalls than the NDC-carrying groups), the early no-NDC records look like a different population of recall, not a worse-described one.'
              % (dy[2013]['compounding_pct'], dy[2015]['compounding_pct'], max(dy[2024]['compounding_pct'], dy[2025]['compounding_pct'], dy[2026]['compounding_pct']),
                 dy[2013]['bulk_or_compounding_pct'], dy[2015]['bulk_or_compounding_pct']),
              '- **Corroboration is not higher in late years.** It is %s%% in E1, %s%% in E2 and %s%% in E3. The free-text codes and the openfda-annotated codes describe largely different products in every era; the late-year rise in openfda coverage is not the parser converging on the same population.'
              % (E['E1']['pct'], E['E2']['pct'], E['E3']['pct']),
              '- **Named categories.** Placeholder labelers are an E1 phenomenon (%s of %s recovered codes, against %s and %s later). Codes with no pad zero are %s, %s and %s by era. All four incorrect sample records are no-pad-zero codes, two in E1 and two in E3. Invalid codes inflate recovered coverage slightly and about equally across eras (no-pad-zero codes are %s%%, %s%% and %s%% of recovered codes), so they cannot produce the slope.'
              % (A['E1']['placeholder_codes_all_recovered'], f(A['E1']['codes_all_recovered']), A['E2']['placeholder_codes_all_recovered'], A['E3']['placeholder_codes_all_recovered'],
                 A['E1']['no_pad_zero_codes_all_recovered'], A['E2']['no_pad_zero_codes_all_recovered'], A['E3']['no_pad_zero_codes_all_recovered'],
                 *[R2.pct(A[e]['no_pad_zero_codes_all_recovered'], A[e]['codes_all_recovered']) for e in ('E1', 'E2', 'E3')]),
              '- **No parser rule is disputed.** The misses are rare enough that changing a rule would not change any result here, and the brief forbids it. Recorded only: dotted NDCs and product-level NDCs are real forms the run 2 rules do not accept.', '']
    with open(os.path.join(HERE, 'RUN3-REPORT.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
