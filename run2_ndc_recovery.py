# DISCLAIMER BEGIN
# This work was carried out independently, on personal time and equipment, and is not
# connected to the author's employment. The views expressed are the author's own and do
# not represent the views, positions or policies of any current, former or future employer
# or client. No proprietary, confidential or internal data of any organization was used.
# All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
# DISCLAIMER END
# Run 2 of concept A15: can NDCs parsed from product_description restore coverage that is
# stable over time? One test only. No model, no fitting.
#   python3 -B run2_ndc_recovery.py
# Deterministic: the only randomness is the precision sample, drawn with SEED below.
# Writes run2_results.json and RUN2-REPORT.md in this folder. Reads run2_precision_marks.json
# (hand marks for the 30 sampled records) if it exists.
import hashlib, io, json, os, random, re, sys, zipfile
from datetime import date, timedelta

sys.dont_write_bytecode = True  # no __pycache__ in the program folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from boundary_scan import load_terms  # the scanner the brief names as correct

DATA = os.path.join(HERE, 'data', 'drug-enforcement-0001-of-0001.json.zip')
ENTRY = 'drug-enforcement-0001-of-0001.json'
WANT_SHA = 'c6eb46526a3ad52102a88b65727874c2e23c43300b27e704eada05960d755092'
WANT_N = 17975
SEED = 20260928
SAMPLE_N = 30
YEARS = list(range(2013, 2027))

# Pass criterion, fixed by the brief before the parse ran. Not to be changed after results.
C1_MIN_POOLED_PCT = 35.0
C2_MAX_DEV_PP = 10.0
C3_MAX_ABS_SPEARMAN = 0.50

# ---------------------------------------------------------------- parse rules
# ACCEPT shapes (hyphenated): 4-4-2, 5-3-2, 5-4-1, 5-4-2. Unhyphenated: 10 or 11 digits.
# A candidate must not touch another digit or hyphen on either side, so a longer
# hyphenated run (UPC-like 1-5-5-1, lot codes) is never cut into an NDC.
HYPH = re.compile(r'(?<![\d-])(\d{4,5})-(\d{3,4})-(\d{1,2})(?![\d-])')
PLAIN = re.compile(r'(?<![\d-])(\d{10,11})(?![\d-])')
SHAPES = {(4, 4, 2), (5, 3, 2), (5, 4, 1), (5, 4, 2)}
# Label keywords. The last keyword before a candidate, within LABEL_WINDOW characters,
# is its label. "ndc/upc" and "upc/ndc" count as an NDC label.
LABEL = re.compile(r'ndc\s*/\s*upc|upc\s*/\s*ndc|ndc|upc|gtin|bar\s*code|barcode|lot|exp|batch|'
                   r'sku|item|cat(?:alog)?\b|serial|mfg|model', re.I)
LABEL_WINDOW = 40
REJECT_LABELS = {'upc', 'gtin', 'barcode', 'lot', 'exp', 'batch', 'sku', 'item', 'cat', 'catalog',
                 'serial', 'mfg', 'model'}


def label_before(text, start):
    win = text[max(0, start - LABEL_WINDOW):start]
    last = None
    for m in LABEL.finditer(win):
        last = m.group(0).lower()
    if last is None:
        return None
    last = re.sub(r'\s+', '', last)
    if 'ndc' in last:
        return 'ndc'
    return last


def parse(text):
    """Return (accepted, rejected) candidate lists for one description."""
    acc, rej = [], []
    if not isinstance(text, str):
        return acc, rej
    for m in HYPH.finditer(text):
        segs = m.groups()
        shape = tuple(len(s) for s in segs)
        lab = label_before(text, m.start())
        item = {'raw': m.group(0), 'shape': '%d-%d-%d' % shape, 'start': m.start(), 'end': m.end(), 'label': lab}
        if shape not in SHAPES:
            rej.append(dict(item, why='shape not accepted')); continue
        if lab in REJECT_LABELS:
            rej.append(dict(item, why='labeled ' + lab)); continue
        if int(segs[0]) == 0 or int(segs[1]) == 0:
            rej.append(dict(item, why='all-zero labeler or product segment')); continue
        if shape == (4, 4, 2) and 1990 <= int(segs[0]) <= 2039 and lab != 'ndc':
            rej.append(dict(item, why='year-like first segment without NDC label')); continue
        a, b, c = segs
        if shape == (4, 4, 2):
            d11 = '0' + a + b + c
        elif shape == (5, 3, 2):
            d11 = a + '0' + b + c
        elif shape == (5, 4, 1):
            d11 = a + b + '0' + c
        else:
            d11 = a + b + c
        acc.append(dict(item, digits11=d11, digits10=None))
    for m in PLAIN.finditer(text):
        lab = label_before(text, m.start())
        dg = m.group(1)
        item = {'raw': dg, 'shape': '%d-digit' % len(dg), 'start': m.start(), 'end': m.end(), 'label': lab}
        if lab != 'ndc':
            rej.append(dict(item, why='unhyphenated without NDC label' if lab is None else 'labeled ' + lab)); continue
        if int(dg[:5 if len(dg) == 11 else 4]) == 0:
            rej.append(dict(item, why='all-zero labeler')); continue
        acc.append(dict(item, digits11=dg if len(dg) == 11 else None, digits10=dg if len(dg) == 10 else None))
    return acc, rej


def norm_product(p):
    """openfda product_ndc 'LLLL-PPPP' / 'LLLLL-PPP' / 'LLLLL-PPPP' -> 9 digits."""
    a, b = p.split('-')[:2]
    return a.zfill(5) + b.zfill(4)


def norm_package(p):
    """openfda package_ndc 'L-P-K' -> 11 digits; None for a value not in three segments."""
    parts = p.split('-')
    if len(parts) != 3:
        return None
    a, b, c = parts
    return a.zfill(5) + b.zfill(4) + c.zfill(2)


def ten_to_nine_candidates(d10):
    """A 10-digit unhyphenated NDC can be 4-4-2, 5-3-2 or 5-4-1."""
    return {'0' + d10[0:4] + d10[4:8], d10[0:5] + '0' + d10[5:8], d10[0:5] + d10[5:9]}


def dnum(s):
    try:
        return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    except Exception:
        return None


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0 + 1
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def main():
    raw = open(DATA, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    recs = json.loads(zipfile.ZipFile(io.BytesIO(raw)).read(ENTRY))['results']
    if sha != WANT_SHA or len(recs) != WANT_N:
        sys.exit('STOP: data file SHA-256 %s, %d records; expected %s, %d' % (sha, len(recs), WANT_SHA, WANT_N))
    terms = load_terms()
    out = {'data': {'sha256': sha, 'bytes': len(raw), 'records': len(recs)}, 'seed': SEED,
           'criterion': {'C1_min_pooled_pct': C1_MIN_POOLED_PCT, 'C2_max_dev_pp': C2_MAX_DEV_PP,
                         'C3_max_abs_spearman': C3_MAX_ABS_SPEARMAN}}

    # openfda-derived sets
    of_prod9, of_pkg11, bad_pkg = set(), set(), []
    for r in recs:
        o = r.get('openfda') or {}
        for p in o.get('product_ndc') or []:
            of_prod9.add(norm_product(p))
        for p in o.get('package_ndc') or []:
            k = norm_package(p)
            if k is None:
                bad_pkg.append(p)
            else:
                of_pkg11.add(k)
    run1_re = re.compile(r'\b\d{4,5}-\d{3,4}-\d{1,2}\b')

    has_of = [bool((r.get('openfda') or {}).get('product_ndc')) for r in recs]
    parsed, reject_counts, shape_counts = {}, {}, {}
    for i, r in enumerate(recs):
        if has_of[i]:
            continue
        acc, rej = parse(r.get('product_description'))
        for x in rej:
            reject_counts[x['why']] = reject_counts.get(x['why'], 0) + 1
        for x in acc:
            shape_counts[x['shape']] = shape_counts.get(x['shape'], 0) + 1
        if acc:
            parsed[i] = acc
    no_of = [i for i in range(len(recs)) if not has_of[i]]
    run1_set = [i for i in no_of if isinstance(recs[i].get('product_description'), str)
                and run1_re.search(recs[i]['product_description'])]
    run1_lookup = set(run1_set)
    multi = set(i for i in parsed if len({(x['digits11'] or x['digits10']) for x in parsed[i]}) > 1)
    out['yield'] = {
        'records_without_openfda_ndc': len(no_of),
        'run1_pattern_records': len(run1_set),
        'run1_pattern_records_with_accepted_ndc': sum(1 for i in run1_set if i in parsed),
        'run1_pattern_records_with_more_than_one': sum(1 for i in run1_set if i in multi),
        'all_records_with_accepted_ndc': len(parsed),
        'all_records_with_more_than_one': len(multi),
        'recovered_outside_run1_pattern': sum(1 for i in parsed if i not in run1_lookup),
        'accepted_by_shape': dict(sorted(shape_counts.items())),
        'rejected_by_reason': dict(sorted(reject_counts.items()))}

    # corroboration against openfda-assigned codes (all from other records by construction)
    distinct = {}
    for i, acc in parsed.items():
        for x in acc:
            distinct[x['digits11'] or ('10:' + x['digits10'])] = x
    pk = pr = 0
    for k, x in distinct.items():
        if x['digits11']:
            pk += x['digits11'] in of_pkg11
            pr += x['digits11'][:9] in of_prod9
        else:
            pr += bool(ten_to_nine_candidates(x['digits10']) & of_prod9)
    rec_corr = 0
    for i, acc in parsed.items():
        ok = False
        for x in acc:
            if x['digits11'] and x['digits11'][:9] in of_prod9:
                ok = True
            if x['digits10'] and ten_to_nine_candidates(x['digits10']) & of_prod9:
                ok = True
        rec_corr += ok
    out['corroboration'] = {
        'distinct_parsed_codes': len(distinct),
        'match_openfda_package_ndc': pk, 'match_openfda_package_pct': pct(pk, len(distinct)),
        'match_openfda_product_ndc': pr, 'match_openfda_product_pct': pct(pr, len(distinct)),
        'recovered_records_with_a_product_match': rec_corr,
        'recovered_records_with_a_product_match_pct': pct(rec_corr, len(parsed)),
        'openfda_distinct_product_ndcs': len(of_prod9), 'openfda_distinct_package_ndcs': len(of_pkg11),
        'openfda_package_values_not_three_segments': len(bad_pkg)}

    # precision sample
    rng = random.Random(SEED)
    sample_ids = rng.sample(sorted(parsed), SAMPLE_N)

    def redact(s):
        n = 0
        for p in terms:
            s, k = p.subn('[REDACTED]', s)
            n += k
        return s, n
    marks_path = os.path.join(HERE, 'run2_precision_marks.json')
    marks = json.load(open(marks_path, encoding='utf-8')) if os.path.exists(marks_path) else {}
    sample, red_total = [], 0
    for rank, i in enumerate(sample_ids, 1):
        r = recs[i]
        t = r['product_description']
        acc = parsed[i]
        a = max(0, min(x['start'] for x in acc) - 70)
        b = min(len(t), max(x['end'] for x in acc) + 30)
        snip = ('...' if a > 0 else '') + t[a:b] + ('...' if b < len(t) else '')
        snip, n = redact(' '.join(snip.split()))
        red_total += n
        key = r.get('recall_number') or str(i)
        mk = marks.get(key, {})
        sample.append({'n': rank, 'recall_number': key, 'report_year': r['report_date'][:4],
                       'extracted': [x['raw'] for x in acc], 'snippet': snip,
                       'mark': mk.get('mark'), 'note': mk.get('note', '')})
    marked = [s for s in sample if s['mark'] in ('correct', 'incorrect')]
    correct = sum(1 for s in marked if s['mark'] == 'correct')
    out['precision'] = {'seed': SEED, 'n': SAMPLE_N, 'population': len(parsed), 'marked': len(marked),
                        'correct': correct,
                        'precision_pct': pct(correct, len(marked)) if len(marked) == SAMPLE_N else None,
                        'boundary_redactions': red_total, 'sample': sample}

    # year table on report_date year, the field run 1 used for its curve
    tab = {}
    for i, r in enumerate(recs):
        t = tab.setdefault(int(r['report_date'][:4]), [0, 0, 0])
        t[0] += 1
        if has_of[i]:
            t[1] += 1
        elif i in parsed:
            t[2] += 1
    rows = []
    for y in sorted(tab):
        tot, of, rc = tab[y]
        rows.append({'year': y, 'total': tot, 'openfda': of, 'recovered': rc, 'combined': of + rc,
                     'combined_pct': pct(of + rc, tot), 'openfda_pct': pct(of, tot), 'in_gate': y in YEARS})
    out['year_table'] = rows
    g = [r for r in rows if r['in_gate']]
    if [r['year'] for r in g] != YEARS:
        sys.exit('STOP: a gate year has no records')
    tot = sum(r['total'] for r in g)
    comb = sum(r['combined'] for r in g)
    pooled = 100.0 * comb / tot
    devs = [(r['year'], round(100.0 * r['combined'] / r['total'] - pooled, 2)) for r in g]
    worst = max(devs, key=lambda d: abs(d[1]))
    rho = spearman([r['year'] for r in g], [r['combined'] / r['total'] for r in g])
    rho_of = spearman([r['year'] for r in g], [r['openfda'] / r['total'] for r in g])
    c1 = pooled >= C1_MIN_POOLED_PCT
    c2 = all(abs(d) <= C2_MAX_DEV_PP for _, d in devs)
    c3 = abs(rho) <= C3_MAX_ABS_SPEARMAN
    out['gate'] = {'pooled_total': tot, 'pooled_combined': comb, 'C1_pooled_pct': round(pooled, 2), 'C1_pass': c1,
                   'C2_deviations_pp': devs, 'C2_worst_year': worst[0], 'C2_worst_dev_pp': worst[1],
                   'C2_years_outside': [y for y, d in devs if abs(d) > C2_MAX_DEV_PP], 'C2_pass': c2,
                   'C3_spearman': round(rho, 4), 'C3_pass': c3, 'openfda_only_spearman': round(rho_of, 4),
                   'verdict': 'PASS' if (c1 and c2 and c3) else 'FAIL'}

    # right-censoring note: index unit = (9-digit product key, event_id) with a valid initiation date
    maxd = max(dnum(r['report_date']) for r in recs)

    def units(use_parsed):
        m = {}
        for i, r in enumerate(recs):
            keys = set(norm_product(p) for p in ((r.get('openfda') or {}).get('product_ndc') or []))
            if use_parsed and not keys and i in parsed:
                for x in parsed[i]:
                    if x['digits11']:
                        keys.add(x['digits11'][:9])
                    else:
                        c = ten_to_nine_candidates(x['digits10']) & of_prod9
                        keys.add(sorted(c)[0] if len(c) == 1 else '10:' + x['digits10'])
            ev = r.get('event_id')
            d0 = dnum(r.get('recall_initiation_date') or '')
            if not keys or not ev or d0 is None:
                continue
            for k in keys:
                cur = m.get((k, ev))
                if cur is None or d0 < cur:
                    m[(k, ev)] = d0
        return {'index_units': len(m),
                'censored_naive_365': sum(1 for d0 in m.values() if d0 > maxd - timedelta(days=365)),
                'censored_365_plus_lag168': sum(1 for d0 in m.values() if d0 > maxd - timedelta(days=365 + 168))}
    out['censoring'] = {'max_report_date': maxd.isoformat(), 'openfda_only': units(False), 'combined': units(True)}

    with open(os.path.join(HERE, 'run2_results.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write('\n')
    write_report(out)
    print('verdict', out['gate']['verdict'], 'C1', out['gate']['C1_pooled_pct'], 'C2 worst', worst,
          'C3', out['gate']['C3_spearman'], 'marked', len(marked))


def f(v):
    if isinstance(v, bool):
        return 'PASS' if v else 'FAIL'
    if isinstance(v, int):
        return '{:,}'.format(v)
    return str(v)


def write_report(o):
    g, y, c, p, cz = o['gate'], o['yield'], o['corroboration'], o['precision'], o['censoring']
    prec = ('%d of %d correct = %s%%' % (p['correct'], p['n'], p['precision_pct'])
            if p['precision_pct'] is not None else 'NOT YET MARKED')
    L = ['# A15 Run 2 - NDC recovery from product_description: %s' % g['verdict'], '',
         '- **C1 pooled combined coverage 2013-2026: %s%%** (needs >= 35%%): **%s**' % (g['C1_pooled_pct'], f(g['C1_pass'])),
         '- **C2 worst single-year deviation from the pooled figure: %+.2f pp (%d)**; years outside +/-10 pp: %s (needs none): **%s**'
         % (g['C2_worst_dev_pp'], g['C2_worst_year'], ', '.join(str(v) for v in g['C2_years_outside']) or 'none', f(g['C2_pass'])),
         '- **C3 Spearman(year, annual combined coverage): %s** (needs |rho| <= 0.50): **%s**' % (g['C3_spearman'], f(g['C3_pass'])),
         '- **VERDICT: %s.** Criterion as fixed in the brief before the parse ran; not adjusted.' % g['verdict'],
         '- Hand-marked precision on 30 sampled recoveries (seed %d): %s.' % (p['seed'], prec),
         '- Data confirmed first: SHA-256 `%s`, %s records.' % (o['data']['sha256'], f(o['data']['records'])),
         '- No model, no fitting, no paper construction. Generated by `run2_ndc_recovery.py`; numbers in `run2_results.json`.',
         '', '---', '',
         '## 1. Parse rules', '',
         'Applied to `product_description` of every record with no `openfda.product_ndc` (%s records).' % f(y['records_without_openfda_ndc']),
         '', 'ACCEPT:', '',
         '- Hyphenated `\\d{4,5}-\\d{3,4}-\\d{1,2}` with segment lengths exactly 4-4-2, 5-3-2, 5-4-1 or 5-4-2.',
         '- Unhyphenated runs of exactly 10 or 11 digits, ONLY when the label is NDC.',
         '- No candidate may touch a digit or hyphen on either side, so nothing is cut out of a longer hyphenated or digit run.',
         '- Label = the last of these keywords within %d characters before the candidate: ndc, ndc/upc, upc/ndc, upc, gtin, barcode, bar code, lot, exp, batch, sku, item, cat, catalog, serial, mfg, model. ndc/upc and upc/ndc count as NDC.' % LABEL_WINDOW,
         '', 'REJECT:', '',
         '- any other segment shape (4-3-2, 5-3-1, 4-4-1, 4-3-1 ...);',
         '- a candidate labeled upc, gtin, barcode, lot, exp, batch, sku, item, cat, catalog, serial, mfg or model (UPCs, lot numbers, expiry dates, catalog numbers);',
         '- an unhyphenated 10 or 11 digit run with no NDC label (UPC and barcode digits);',
         '- an all-zero labeler or product segment;',
         '- a 4-4-2 whose first segment is 1990-2039 without an NDC label (date-like);',
         '- quantities are excluded by construction: no accepted shape is a count, a decimal or a unit.',
         '',
         'Normalization for matching: hyphenated forms are padded to 11 digits (4-4-2 pads the labeler, 5-3-2 the product, 5-4-1 the package); 5-4-2 and 11-digit forms are used as is. The first 9 digits are the product key, compared with openfda `product_ndc` padded the same way. A 10-digit unhyphenated code has three possible splits; it matches if any split does.',
         '', '## 2. Parse yield', '', '| Measure | Records |', '|---|---|']
    for k, lab in [('records_without_openfda_ndc', 'Records with no openfda NDC'),
                   ('run1_pattern_records', 'Of those, run 1 NDC-shaped pattern present (the "6002")'),
                   ('run1_pattern_records_with_accepted_ndc', '... with at least one ACCEPTED NDC'),
                   ('run1_pattern_records_with_more_than_one', '... with more than one distinct accepted NDC'),
                   ('all_records_with_accepted_ndc', 'All no-openfda records with at least one accepted NDC (used in the gate)'),
                   ('all_records_with_more_than_one', '... with more than one distinct accepted NDC'),
                   ('recovered_outside_run1_pattern', 'Recovered records outside the run 1 pattern (NDC-labeled unhyphenated)')]:
        L.append('| %s | %s |' % (lab, f(y[k])))
    L += ['', 'Accepted candidates by shape: ' + ', '.join('%s %s' % (k, f(v)) for k, v in y['accepted_by_shape'].items()) + '.',
          '', 'Rejected candidates by reason: ' + '; '.join('%s %s' % (k, f(v)) for k, v in y['rejected_by_reason'].items()) + '.',
          '', '## 3. Corroboration against openfda-assigned NDCs', '', '| Measure | Value |', '|---|---|',
          '| Distinct parsed codes | %s |' % f(c['distinct_parsed_codes']),
          '| ... equal to an openfda package_ndc assigned to another record | %s (%s%%) |' % (f(c['match_openfda_package_ndc']), c['match_openfda_package_pct']),
          '| ... whose product part equals an openfda product_ndc assigned to another record | %s (%s%%) |' % (f(c['match_openfda_product_ndc']), c['match_openfda_product_pct']),
          '| Recovered records with at least one product-level match | %s of %s (%s%%) |' % (f(c['recovered_records_with_a_product_match']), f(y['all_records_with_accepted_ndc']), c['recovered_records_with_a_product_match_pct']),
          '| openfda distinct product / package NDCs in the file | %s / %s |' % (f(c['openfda_distinct_product_ndcs']), f(c['openfda_distinct_package_ndcs'])),
          '', 'A match is evidence the parse is real. A non-match is not evidence against it: openfda annotates only products it can match, which is the gap being filled.',
          '', '## 4. Precision check by hand', '',
          'Population: the %s recovered records. Sample: `random.Random(%d).sample(sorted(record indexes), %d)`, drawn before any record was looked at. Snippet: description from 70 characters before the first accepted match to 30 after the last, whitespace collapsed. Employer-boundary terms are replaced by `[REDACTED]` (%d replacements in this sample); nothing else is altered. Marks are the run author\'s own, stored in `run2_precision_marks.json`. Correct = the extracted string is an NDC as the description presents it (NDC-labeled or in an NDC position) and every extracted code is one; one wrong code makes the record incorrect.'
          % (f(p['population']), p['seed'], p['n'], p['boundary_redactions']),
          '', '| # | recall_number | Year | Extracted | Mark | Snippet |', '|---|---|---|---|---|---|']
    for s in p['sample']:
        L.append('| %d | %s | %s | %s | %s | %s |' % (
            s['n'], s['recall_number'], s['report_year'], ', '.join('`%s`' % e for e in s['extracted']),
            (s['mark'] or 'UNMARKED') + ((' - ' + s['note']) if s['note'] else ''), s['snippet'].replace('|', '/')))
    L += ['', 'Precision: %s.' % prec,
          '', '## 5. Year table', '',
          'Year = year of `report_date`, the field run 1 used for its coverage curve. Recovered = no openfda NDC and at least one accepted parsed NDC. Combined = openfda + recovered (disjoint by construction).',
          '', '| Year | Total | openfda NDC | Recovered | Combined | Combined % | openfda-only % | In gate |', '|---|---|---|---|---|---|---|---|']
    for r in o['year_table']:
        L.append('| %d | %s | %s | %s | %s | %s | %s | %s |' % (r['year'], f(r['total']), f(r['openfda']), f(r['recovered']),
                                                         f(r['combined']), r['combined_pct'], r['openfda_pct'], 'yes' if r['in_gate'] else 'no'))
    L += ['', '## 6. Criterion', '',
          '- C1: pooled combined coverage 2013-2026 = %s / %s = **%s%%** (>= 35): **%s**' % (f(g['pooled_combined']), f(g['pooled_total']), g['C1_pooled_pct'], f(g['C1_pass'])),
          '- C2: each year minus the pooled figure, pp: ' + ', '.join('%d %+.2f' % (yy, d) for yy, d in g['C2_deviations_pp'])
          + '. Outside +/-10: %s. **%s**' % (', '.join(str(v) for v in g['C2_years_outside']) or 'none', f(g['C2_pass'])),
          '- C3: Spearman rank correlation of year with annual combined coverage, 14 years = **%s** (|rho| <= 0.50): **%s**. Same statistic on openfda-only coverage, for reference: %s.'
          % (g['C3_spearman'], f(g['C3_pass']), g['openfda_only_spearman']),
          '- **Verdict: %s.**' % g['verdict'],
          '', '## 7. Right-censoring (design note, not a gate)', '',
          'Maximum `report_date` in the snapshot: **%s**. Index unit = (9-digit product key, event_id) with a valid `recall_initiation_date`, dated by the earliest initiation date among that event\'s records carrying the key.' % cz['max_report_date'],
          '', '| Population | Index units | Initiated within 365 d of the max date | Within 365 + 168 d (run 1 lag allowance) |', '|---|---|---|---|']
    for k, lab in [('openfda_only', 'openfda NDC only'), ('combined', 'openfda + recovered')]:
        v = cz[k]
        L.append('| %s | %s | %s | %s |' % (lab, f(v['index_units']), f(v['censored_naive_365']), f(v['censored_365_plus_lag168'])))
    yt = {r['year']: r for r in o['year_table']}
    L += ['', '## 8. Notes', '',
          '- **How the parse rules were set.** From counts of candidate shapes and of the label word preceding each candidate in the no-openfda records, before the gate was computed. No rule was changed after C1-C3 were seen. One code fix preceded the first complete run: %s openfda `package_ndc` values that are not three hyphenated segments crashed the normalizer and are now skipped (they affect only the package-level corroboration row).' % f(c['openfda_package_values_not_three_segments']),
          '- **What the FAIL is.** The parse works (precision above, %s%% of the "6002" yield an accepted code) and lifts pooled coverage well past 35%%, but it does not flatten the curve: combined coverage is %s%% in 2013 and %s%% in 2015 against %s%% in 2024 and %s%% in 2026, and still rank-correlates %s with year (openfda alone: %s). The parse adds records in every year but does not offset the rise in openfda coverage; why 2013 and 2015 recover so little was not investigated (out of scope for this run).'
          % (pct(y['run1_pattern_records_with_accepted_ndc'], y['run1_pattern_records']), yt[2013]['combined_pct'], yt[2015]['combined_pct'],
             yt[2024]['combined_pct'], yt[2026]['combined_pct'], g['C3_spearman'], g['openfda_only_spearman']),
          '- **Low corroboration is expected, and is not the evidence.** Only %s%% of distinct parsed codes match a product openfda assigned elsewhere. The recovered records mostly name products openfda never annotated, which is the gap by definition. The hand precision is the evidence that the parse reads real NDCs.' % c['match_openfda_product_pct'],
          '- **The criterion is not disputed.** C1 passes; C2 and C3 fail independently of each other, and no reasonable re-reading of either would change the verdict.',
          '- **Boundary.** Snippets are quoted verbatim from public FDA records; the employer-boundary redaction ran over all 30 and replaced %d strings. `boundary_scan.py` covers this report.' % p['boundary_redactions']]
    L.append('')
    with open(os.path.join(HERE, 'RUN2-REPORT.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
