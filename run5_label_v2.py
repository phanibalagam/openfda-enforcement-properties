# DISCLAIMER BEGIN
# This work was carried out independently, on personal time and equipment, and is not
# connected to the author's employment. The views expressed are the author's own and do
# not represent the views, positions or policies of any current, former or future employer
# or client. No proprietary, confidential or internal data of any organization was used.
# All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
# DISCLAIMER END
# Run 5 of concept A15: label v2, its validation on fresh samples, and the decomposition
# under both labels. No model, nothing fitted.
#   python3 -B run5_label_v2.py --rules-only   write the v2 rule text, draw nothing
#   python3 -B run5_label_v2.py                full run
# The run 2 parser and the v1 label are IMPORTED unchanged (digests checked). Deterministic:
# every sample uses a fixed, stated seed. Reads run5_marks.json if present.
import hashlib, io, json, os, random, re, sys, zipfile

sys.dont_write_bytecode = True  # no __pycache__ in the program folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run2_ndc_recovery as R2
import run3_parser_validation as R3
import run4_label_validation as R4
from boundary_scan import load_terms

DATA = os.path.join(HERE, 'data', 'drug-enforcement-0001-of-0001.json.zip')
ENTRY = 'drug-enforcement-0001-of-0001.json'
WANT_SHA = 'c6eb46526a3ad52102a88b65727874c2e23c43300b27e704eada05960d755092'
WANT_N = 17975
DIGESTS = {'run2_ndc_recovery.py': '892aacebdeb522adef4ca4f2beef658b8ac9a61f843f4631cb26d77f4571b263',
           'run3_parser_validation.py': '2664f53f33943376233eb98fe4be2abbf7b0478e68f028886e053351ff9dad37',
           'run4_label_validation.py': '40bcc2bdce26c83339c3b4ada3e09da0a31b5ec2f457a579e498cf5dbce10393'}
ERAS = R3.ERAS
YEARS = list(range(2013, 2027))
N_PER_ERA = 40
SEEDS_A = {'E1': 51001, 'E2': 51002, 'E3': 51003}  # v2-flagged records (precision)
SEEDS_B = {'E1': 52001, 'E2': 52002, 'E3': 52003}  # v2-unflagged, no NDC from either source (miss rate)

# Pre-registered criteria from the run 5 brief. Not to be changed after results.
W1_MIN_POOLED, W1_MIN_LOWER = 85.0, 70.0
W2_MAX_GAP_PP = 20.0
W3_MAX_GAP_PP = 20.0
W4_MAX_MISS = 25.0

# ------------------------------------------------------------------ LABEL v2
# Derived ONLY from records already hand-read in runs 3 and 4 (their marks and notes).
# Compounding: keys on the PREPARER.
P1 = re.compile(r'compound(?:ed|ing|er|s)?\b', re.I)                        # the v1 stem, kept
P2 = re.compile(r'\bpharmac(?:y|ies)\b|\bapothecary\b', re.I)               # a pharmacy as preparer
P2_EXCLUDE = re.compile(r'\bcvs pharmacy\b|\bgood neighbor pharmacy\b', re.I)  # retail chains named as distributors of finished OTC products
P3 = re.compile(r'outsourc(?:ing|e|es)\b|\b503b\b', re.I)                  # outsourcing facility
P4 = re.compile(r'\bhome infusion\b|\binfusion,?\s+(?:pharmacy|services?|options|center|centre|care|llc|inc)\b', re.I)  # infusion pharmacy
P5 = re.compile(r'\b(?:pharmedium|sca pharmaceuticals|avella|anazaohealth|us specialty formulations|pharmakon|qualgen|belmar|genogenix|krs global biotechnology)\b', re.I)  # preparers identified in runs 3-4
# Bulk: substance, not packaging.
# B1: the run 3 substance terms; API is matched case-sensitively, the rest case-insensitively
B1_CI = re.compile(r'active pharmaceutical ingredient|drug substance|raw material|\bintermediate\b', re.I)
B1_API = re.compile(r'\bAPIs?\b')
B2 = re.compile(r'for\s+(?:rx\s+|prescription\s+)?compounding|for\s+manufacturing\s+use', re.I)
B3 = re.compile(r'\d\s*(?:kg|kgs|kilograms?)\b|\bdrums?\b|\bbulk\b', re.I)
B3_FINISHED = re.compile(r'pharmacy bulk package|\btablets?\b|\bcaplets?\b|\bcapsules?\b|\bsoftgels?\b|\bsyrup\b|\bspray\b|\blotion\b|\bcream\b|\bointment\b|'
                         r'\btowelettes?\b|\bwipes?\b|\bsanitizer\b|\binjection\b|\binjectable\b|\bvials?\b|\bsyringes?\b|\bsuppositor|\bdrops\b', re.I)

RULE_TEXT = """LABEL v2 = COMPOUNDED-v2 OR BULK-v2, applied to product_description (case-insensitive unless stated).

COMPOUNDED-v2 fires if ANY of:
  P1  the run 3 stem: compound, compounded, compounding, compounder, compounds.
  P2  the word pharmacy, pharmacies or apothecary, UNLESS the only such mention is in "CVS Pharmacy"
      or "Good Neighbor Pharmacy" (retail chains that appear in read records as distributors of
      finished OTC products). Implemented as: P2 matches after those two phrases are removed.
  P3  outsourcing, outsource, outsources, or the token 503B.
  P4  "home infusion", or "infusion" followed by pharmacy, service(s), options, center, centre,
      care, LLC or Inc.
  P5  one of ten preparer names that runs 3 and 4 showed to be compounders or outsourcing
      facilities: PharMEDium, SCA Pharmaceuticals, Avella, AnazaoHealth, US Specialty Formulations,
      Pharmakon, Qualgen, Belmar, GenoGenix, KRS Global Biotechnology.

BULK-v2 fires if ANY of:
  B1  the run 3 substance terms: "active pharmaceutical ingredient", the uppercase token API or APIs
      (case-sensitive), "drug substance", "raw material", "intermediate".
  B2  "for compounding", "for Rx compounding", "for prescription compounding", "for manufacturing use".
  B3  a kilogram quantity, the word drum(s), or the word bulk, ONLY IF the text contains none of
      these finished-dosage-form indicators: "pharmacy bulk package", tablet(s), caplet(s),
      capsule(s), softgel(s), syrup, spray, lotion, cream, ointment, towelette(s), wipe(s),
      sanitizer, injection, injectable, vial(s), syringe(s), suppositor-, drops.

LABEL v1 (run 3, unchanged, imported) = the run 3 compounding stem OR the run 3 bulk rule.

Provenance of each change. P2-P5 come from the run 4 Part B misses (pharmacies, infusion
pharmacies and outsourcing facilities named without the stem) and from run 3/4 records that name
the preparer. B2 comes from run 4 Part A (APIs sold "for prescription compounding") and Part B E2 #36
("For Manufacturing Use Only"). The B3 exclusion list comes from the nine run 4 E3 errors (bulk
containers of tablets, a bulk spray, drummed sanitizer, bulk towelettes, a pharmacy bulk package).
No record outside the run 2, run 3 and run 4 samples was read to write these rules.
Known limits carried in: P5 is a firm list and will not generalize beyond those firms; a raw
material in grams with no substance term (run 4 B E1 #23) is still missed; a retail botanical
sold by the kilogram (run 4 A E2 #38) is still flagged."""


def compounded_v2(t):
    hits = []
    if P1.search(t):
        hits.append('P1')
    if P2.search(P2_EXCLUDE.sub(' ', t)):
        hits.append('P2')
    if P3.search(t):
        hits.append('P3')
    if P4.search(t):
        hits.append('P4')
    if P5.search(t):
        hits.append('P5')
    return hits


def bulk_v2(t):
    hits = []
    if B1_CI.search(t) or B1_API.search(t):
        hits.append('B1')
    if B2.search(t):
        hits.append('B2')
    if B3.search(t) and not B3_FINISHED.search(t):
        hits.append('B3')
    return hits


def write_rules_only():
    s = '# A15 Run 5 - label v2 rule text, written BEFORE any run 5 sample was drawn\n\n' \
        'SHA-256 of the rule text block below: `%s`\n\n```\n%s\n```\n' % (hashlib.sha256(RULE_TEXT.encode('utf-8')).hexdigest(), RULE_TEXT)
    with open(os.path.join(HERE, 'RUN5-RULES-PRESAMPLE.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(s)
    print('wrote RUN5-RULES-PRESAMPLE.md; rule text SHA-256', hashlib.sha256(RULE_TEXT.encode('utf-8')).hexdigest())


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def overlap(w1, w2):
    return not (w1[1] < w2[0] or w2[1] < w1[0])


def main():
    raw = open(DATA, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    recs = json.loads(zipfile.ZipFile(io.BytesIO(raw)).read(ENTRY))['results']
    if sha != WANT_SHA or len(recs) != WANT_N:
        sys.exit('STOP: data file SHA-256 %s, %d records; expected %s, %d' % (sha, len(recs), WANT_SHA, WANT_N))
    for fn, want in DIGESTS.items():
        got = hashlib.sha256(open(os.path.join(HERE, fn), 'rb').read()).hexdigest()
        if got != want:
            sys.exit('STOP: %s has changed (%s)' % (fn, got))
    pre = open(os.path.join(HERE, 'RUN5-RULES-PRESAMPLE.md'), encoding='utf-8').read()
    rule_sha = hashlib.sha256(RULE_TEXT.encode('utf-8')).hexdigest()
    if rule_sha not in pre or RULE_TEXT not in pre:
        sys.exit('STOP: rule text differs from the pre-sample snapshot')
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
    v1 = [R4.compounding(t) or R4.bulk(t) for t in desc]
    ch = [compounded_v2(t) for t in desc]
    bh = [bulk_v2(t) for t in desc]
    v2 = [bool(ch[i] or bh[i]) for i in range(len(recs))]

    # records hand-read in runs 2, 3 and 4 are excluded from every run 5 sample
    excl = set()
    for fn in ('run3_marks.json', 'run4_marks.json'):
        m = json.load(open(os.path.join(HERE, fn), encoding='utf-8'))
        for part in ('A', 'B'):
            for k in m[part]:
                excl.add(int(k.rsplit('#', 1)[1]))
    by_recall = {}
    for i, r in enumerate(recs):
        by_recall.setdefault(r.get('recall_number'), []).append(i)
    r2m = json.load(open(os.path.join(HERE, 'run2_precision_marks.json'), encoding='utf-8'))
    n_r2 = 0
    for k in r2m:
        for i in by_recall.get(k, []):
            if i not in excl:
                n_r2 += 1
            excl.add(i)
    out = {'data': {'sha256': sha, 'records': len(recs)}, 'rule_sources': DIGESTS, 'rule_text_sha256': rule_sha,
           'date_field': 'report_date (year), as in runs 1-4', 'seeds_A': SEEDS_A, 'seeds_B': SEEDS_B,
           'excluded_ids': len(excl), 'excluded_from_run2_marks_not_already_in_3_4': n_r2}
    marks_path = os.path.join(HERE, 'run5_marks.json')
    marks = json.load(open(marks_path, encoding='utf-8')) if os.path.exists(marks_path) else {'A': {}, 'B': {}}
    red_total = 0
    drawn = set()

    # ---------------- Part A
    A = {}
    for e, a, b in ERAS:
        pop = sorted(i for i in range(len(recs)) if a <= year[i] <= b and v2[i] and i not in excl)
        ids = random.Random(SEEDS_A[e]).sample(pop, N_PER_ERA)
        drawn.update(ids)
        rows = []
        for i in ids:
            d, n = redact(' '.join(desc[i].split()))
            red_total += n
            key = '%s#%d' % (recs[i].get('recall_number'), i)
            mk = marks['A'].get(key, {})
            rows.append({'key': key, 'year': year[i], 'subrules': ch[i] + bh[i], 'v1': v1[i], 'has_ndc': has_ndc[i],
                         'description': d, 'mark': mk.get('mark'), 'kind': mk.get('kind', ''), 'note': mk.get('note', '')})
        marked = [x for x in rows if x['mark'] in ('correct', 'incorrect')]
        k = sum(1 for x in marked if x['mark'] == 'correct')
        full = len(marked) == N_PER_ERA
        sub = {}
        for x in marked:
            for s in x['subrules']:
                c = sub.setdefault(s, [0, 0])
                c[1] += 1
                c[0] += x['mark'] == 'correct'
        A[e] = {'population': len(pop), 'sample': rows, 'marked': len(marked), 'correct': k,
                'precision_pct': pct(k, len(marked)) if full else None, 'wilson95': R3.wilson(k, len(marked)) if full else None,
                'correct_kind': {kd: sum(1 for x in marked if x['mark'] == 'correct' and x['kind'] == kd) for kd in ('compounded', 'bulk', 'both')},
                'subrule_correct_of_fired': dict(sorted(sub.items()))}
    kk = sum(A[e]['correct'] for e in A)
    nn = sum(A[e]['marked'] for e in A)
    out['A'] = A
    out['A_pooled'] = {'correct': kk, 'marked': nn, 'precision_pct': pct(kk, nn), 'wilson95': R3.wilson(kk, nn)}

    # ---------------- Part B
    B = {}
    for e, a, b in ERAS:
        pop = sorted(i for i in range(len(recs)) if a <= year[i] <= b and not v2[i] and not has_ndc[i] and i not in excl)
        ids = random.Random(SEEDS_B[e]).sample(pop, N_PER_ERA)
        drawn.update(ids)
        rows = []
        for i in ids:
            d, n = redact(' '.join(desc[i].split()))
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
    out['overlap_with_excluded'] = len(drawn & excl)
    out['samples_drawn'] = len(drawn)
    out['boundary_redactions'] = red_total

    # ---------------- Part C
    complete = all(A[e]['precision_pct'] is not None for e in A) and all(B[e]['miss_rate_pct'] is not None for e in B)
    C = {'complete': complete}
    if complete:
        ap = out['A_pooled']
        w1 = ap['precision_pct'] >= W1_MIN_POOLED and ap['wilson95'][0] > W1_MIN_LOWER
        pairs = [('E1', 'E2'), ('E1', 'E3'), ('E2', 'E3')]
        w2_br = [(x, y) for x, y in pairs if abs(A[x]['precision_pct'] - A[y]['precision_pct']) > W2_MAX_GAP_PP and not overlap(A[x]['wilson95'], A[y]['wilson95'])]
        w3_br = [(x, y) for x, y in pairs if abs(B[x]['miss_rate_pct'] - B[y]['miss_rate_pct']) > W3_MAX_GAP_PP and not overlap(B[x]['wilson95'], B[y]['wilson95'])]
        w4_br = [e for e in B if B[e]['miss_rate_pct'] > W4_MAX_MISS]
        C.update({'W1_pooled_pct': ap['precision_pct'], 'W1_lower_pct': ap['wilson95'][0], 'W1_pass': w1,
                  'W2_max_gap_pp': round(max(abs(A[x]['precision_pct'] - A[y]['precision_pct']) for x, y in pairs), 2),
                  'W2_breaching_pairs': w2_br, 'W2_pass': not w2_br,
                  'W3_max_gap_pp': round(max(abs(B[x]['miss_rate_pct'] - B[y]['miss_rate_pct']) for x, y in pairs), 2),
                  'W3_breaching_pairs': w3_br, 'W3_pass': not w3_br,
                  'W4_max_miss_pct': max(B[e]['miss_rate_pct'] for e in B), 'W4_breaching_eras': w4_br, 'W4_pass': not w4_br})
        C['verdict'] = 'LABEL v2 FIT FOR USE' if (w1 and not w2_br and not w3_br and not w4_br) else 'LABEL v2 NOT FIT FOR USE'
    out['C'] = C

    # ---------------- Part E (agreement; computed whatever the verdict)
    agree = {}
    for e, a, b in ERAS:
        idx = [i for i in range(len(recs)) if a <= year[i] <= b]
        agree[e] = {'n': len(idx), 'v1_flags': sum(v1[i] for i in idx), 'v2_flags': sum(v2[i] for i in idx),
                    'both': sum(v1[i] and v2[i] for i in idx), 'v1_only': sum(v1[i] and not v2[i] for i in idx),
                    'v2_only': sum(v2[i] and not v1[i] for i in idx),
                    'v2_only_by_subrule': {s: sum(1 for i in idx if v2[i] and not v1[i] and s in ch[i] + bh[i]) for s in ('P2', 'P3', 'P4', 'P5', 'B1', 'B2', 'B3')},
                    'v1_only_with_ndc': sum(1 for i in idx if v1[i] and not v2[i] and has_ndc[i])}
    out['E_agreement'] = agree

    # ---------------- Part D (only if v2 passes)
    if complete and C['verdict'] == 'LABEL v2 FIT FOR USE':
        def table(flag, extra=None):
            # extra: {year: records moved from unflagged no-NDC into flagged}
            rows = []
            for y in YEARS:
                idx = [i for i in range(len(recs)) if year[i] == y]
                nf = sum(flag[i] for i in idx)
                nf_ndc = sum(1 for i in idx if flag[i] and has_ndc[i])
                no = len(idx) - nf
                no_ndc = sum(1 for i in idx if not flag[i] and has_ndc[i])
                mv = (extra or {}).get(y, 0.0)
                rows.append({'year': y, 'n': len(idx), 'flagged': round(nf + mv, 2), 'other': round(no - mv, 2),
                             'flagged_with_ndc': nf_ndc, 'other_with_ndc': no_ndc, 'moved': round(mv, 2)})
            return rows

        def dec(rows, y0, y1):
            def agg(rs):
                n = sum(r['n'] for r in rs)
                f_ = sum(r['flagged'] for r in rs)
                o_ = sum(r['other'] for r in rs)
                return f_ / n, sum(r['flagged_with_ndc'] for r in rs) / f_, sum(r['other_with_ndc'] for r in rs) / o_
            sb, pfb, pob = agg(rows)
            p0 = agg([r for r in rows if y0[0] <= r['year'] <= y0[1]])
            p1 = agg([r for r in rows if y1[0] <= r['year'] <= y1[1]])
            return R4.decompose(p0[0], p0[1], p0[2], p1[0], p1[1], p1[2], sb, pfb, pob)

        miss = {e: B[e]['missed'] / B[e]['marked'] for e in B}
        extra = {}
        for y in YEARS:
            idx = [i for i in range(len(recs)) if year[i] == y and not v2[i] and not has_ndc[i]]
            extra[y] = miss[R3.era_of(y)] * len(idx)
        cols = {'v1': table(v1), 'v2': table(v2), 'v2_corrected': table(v2, extra)}
        D = {}
        for k, rows in cols.items():
            for r in rows:
                r['flagged_share_pct'] = round(100 * r['flagged'] / r['n'], 2)
                r['flagged_ndc_pct'] = round(100 * r['flagged_with_ndc'] / r['flagged'], 2) if r['flagged'] else None
                r['other_ndc_pct'] = round(100 * r['other_with_ndc'] / r['other'], 2) if r['other'] else None
            D[k] = {'years': rows, 'y2013_to_y2026': dec(rows, (2013, 2013), (2026, 2026)), 'E1_to_E3': dec(rows, (2013, 2016), (2022, 2026))}
        out['D'] = D

    with open(os.path.join(HERE, 'run5_results.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write('\n')
    write_report(out)
    print('excluded', len(excl), 'overlap', out['overlap_with_excluded'], '| A', out['A_pooled'], '| B', {e: (B[e]['missed'], B[e]['marked']) for e in B},
          '| C', C.get('verdict'), '| agree', {e: (agree[e]['v1_flags'], agree[e]['v2_flags'], agree[e]['both']) for e in agree})


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
    A, B, C, G = o['A'], o['B'], o['C'], o['E_agreement']
    D = o.get('D')
    L = []
    if C.get('complete'):
        L += ['# A15 Run 5 - label v2: %s' % C['verdict'], '',
              '- **Label v2** (full text in section 0, written to `RUN5-RULES-PRESAMPLE.md` before any sample was drawn; rule-text SHA-256 `%s...`): COMPOUNDED-v2 = the compound stem OR a pharmacy/apothecary named (retail CVS and Good Neighbor excluded) OR outsourcing/503B OR an infusion pharmacy OR one of ten named preparers; BULK-v2 = substance terms (API, active pharmaceutical ingredient, drug substance, raw material, intermediate) OR "for (prescription) compounding / manufacturing use" OR kg/drum/bulk only when no finished-dosage-form word is present.' % o['rule_text_sha256'][:16],
              '- **W1** pooled precision %s%% (needs >= 85), lower Wilson %s%% (needs > 70): **%s**' % (C['W1_pooled_pct'], C['W1_lower_pct'], f(C['W1_pass'])),
              '- **W2** largest precision gap %s pp; pairs breaching (> 20 pp AND non-overlapping 95%% intervals): %s: **%s**' % (C['W2_max_gap_pp'], ', '.join('%s-%s' % p for p in C['W2_breaching_pairs']) or 'none', f(C['W2_pass'])),
              '- **W3** largest miss-rate gap %s pp; pairs breaching: %s: **%s**' % (C['W3_max_gap_pp'], ', '.join('%s-%s' % p for p in C['W3_breaching_pairs']) or 'none', f(C['W3_pass'])),
              '- **W4** highest era miss rate %s%% (needs every era <= 25); eras breaching: %s: **%s**' % (C['W4_max_miss_pct'], ', '.join(C['W4_breaching_eras']) or 'none', f(C['W4_pass'])),
              '- **VERDICT: %s.** Criteria pre-registered in the run 5 brief; not adjusted.' % C['verdict'],
              '- Precision by era: ' + '; '.join('%s %s%% (%s/40, CI %s)' % (e, A[e]['precision_pct'], A[e]['correct'], ci(A[e]['wilson95'])) for e in A) + '.',
              '- Miss rate by era: ' + '; '.join('%s %s%% (%s/40, CI %s)' % (e, B[e]['miss_rate_pct'], B[e]['missed'], ci(B[e]['wilson95'])) for e in B) + '.']
        if D:
            L.append('- **Decomposition 2013 -> 2026, composition / within-group / interaction as shares of the change:** v1 %s / %s / %s%%; v2 %s / %s / %s%%; v2 corrected %s / %s / %s%%.' % tuple(
                x for k in ('v1', 'v2', 'v2_corrected') for x in (D[k]['y2013_to_y2026']['composition_share_pct'], D[k]['y2013_to_y2026']['within_share_pct'], D[k]['y2013_to_y2026']['interaction_share_pct'])))
            L.append('- **Same, E1 -> E3:** v1 %s / %s / %s%%; v2 %s / %s / %s%%; v2 corrected %s / %s / %s%%.' % tuple(
                x for k in ('v1', 'v2', 'v2_corrected') for x in (D[k]['E1_to_E3']['composition_share_pct'], D[k]['E1_to_E3']['within_share_pct'], D[k]['E1_to_E3']['interaction_share_pct'])))
        else:
            L.append('- **Decomposition: NOT RUN.** The brief makes Part D conditional on v2 passing Part C. The fallback stands: the paper ships its first three findings with attribution reported as attempted and unresolved.')
            L.append('')
        L += ['- Fresh samples: %d records hand-read in runs 2-4 excluded; overlap with the 240 run 5 records = %d. Data SHA-256 `%s`, %s records, confirmed first. Run 2 parser and v1 label imported, digests checked.' % (o['excluded_ids'], o['overlap_with_excluded'], o['data']['sha256'][:16] + '...', f(o['data']['records'])),
              '- No model, nothing fitted, no paper writing. `run5_label_v2.py` -> `run5_results.json`; marks in `run5_marks.json`.', '']
    else:
        L += ['# A15 Run 5 - INCOMPLETE: marks missing'] + [''] * 14
    L += ['---', '', '## 0. Label v2 rule text (verbatim; identical to the pre-sample snapshot)', '', '```', RULE_TEXT, '```', '',
          'The script refuses to run if this text differs from `RUN5-RULES-PRESAMPLE.md`, which was written by `run5_label_v2.py --rules-only` before any run 5 sample was drawn. Year = year of `report_date`. Eras E1 2013-2016, E2 2017-2021, E3 2022-2026. Seeds A E1 %d, E2 %d, E3 %d; B E1 %d, E2 %d, E3 %d. Excluded: every record hand-marked in run 3 (240) and run 4 (240) and the 30 run 2 precision records, %d distinct ids in all (%d of the run 2 records were not already in runs 3-4); overlap of the run 5 samples with them: %d. Employer-boundary replacements in quoted text: %d.'
          % (o['seeds_A']['E1'], o['seeds_A']['E2'], o['seeds_A']['E3'], o['seeds_B']['E1'], o['seeds_B']['E2'], o['seeds_B']['E3'], o['excluded_ids'], o['excluded_from_run2_marks_not_already_in_3_4'], o['overlap_with_excluded'], o['boundary_redactions']), '']

    L += ['## A. Precision of label v2', '', 'Correct = the item really is a compounded preparation, bulk substance, API, raw material or intermediate.', '',
          '| Era | v2-flagged records (fresh) | Correct | Precision % | Wilson 95% | Kind: compounded / bulk / both | Sub-rule: correct of fired |', '|---|---|---|---|---|---|---|']
    for e in A:
        a = A[e]
        k = a['correct_kind']
        L.append('| %s | %s | %s / %s | %s | %s | %s / %s / %s | %s |' % (e, f(a['population']), a['correct'], a['marked'], a['precision_pct'], ci(a['wilson95']), k['compounded'], k['bulk'], k['both'],
                                                                    ', '.join('%s %d/%d' % (s, c[0], c[1]) for s, c in a['subrule_correct_of_fired'].items())))
    ap = o['A_pooled']
    L += ['| pooled | | %s / %s | %s | %s | | |' % (ap['correct'], ap['marked'], ap['precision_pct'], ci(ap['wilson95'])), '']
    for e in A:
        L += ['### A-%s (seed %d)' % (e, o['seeds_A'][e]), '', '| # | Record | Year | Sub-rules | v1 flags too | NDC | Mark | Full product_description |', '|---|---|---|---|---|---|---|---|']
        for n, x in enumerate(A[e]['sample'], 1):
            mk = (x['mark'] or 'UNMARKED') + ((' (' + x['kind'] + ')') if x['kind'] else '') + ((' - ' + x['note']) if x['note'] else '')
            L.append('| %d | %s | %d | %s | %s | %s | %s | %s |' % (n, x['key'], x['year'], '+'.join(x['subrules']), 'yes' if x['v1'] else 'no', 'yes' if x['has_ndc'] else 'no', mk, md(x['description'])))
        L.append('')
    L += ['## B. Miss rate of label v2', '', 'Population: records with no NDC from either source that v2 does not flag. missed = in fact a compounded or bulk item.', '',
          '| Era | Unflagged no-NDC records (fresh) | Missed | Miss rate % | Wilson 95% | Kind: compounded / bulk / both |', '|---|---|---|---|---|---|']
    for e in B:
        b = B[e]
        k = b['missed_kind']
        L.append('| %s | %s | %s / %s | %s | %s | %s / %s / %s |' % (e, f(b['population']), b['missed'], b['marked'], b['miss_rate_pct'], ci(b['wilson95']), k['compounded'], k['bulk'], k['both']))
    L.append('')
    for e in B:
        L += ['### B-%s (seed %d)' % (e, o['seeds_B'][e]), '', '| # | Record | Year | Mark | Full product_description |', '|---|---|---|---|---|']
        for n, x in enumerate(B[e]['sample'], 1):
            mk = (x['mark'] or 'UNMARKED') + ((' (' + x['kind'] + ')') if x['kind'] else '') + ((' - ' + x['note']) if x['note'] else '')
            L.append('| %d | %s | %d | %s | %s |' % (n, x['key'], x['year'], mk, md(x['description'])))
        L.append('')
    if C.get('complete'):
        L += ['## C. Pre-registered criteria, and what would breach each on this data', '',
              '- W1: pooled %s%% (%s/%s), Wilson %s. **%s.** Breach: pooled precision below 85%% (fewer than 102 of 120 correct), or a lower bound at or below 70%%. Can fail.' % (ap['precision_pct'], ap['correct'], ap['marked'], ci(ap['wilson95']), f(C['W1_pass'])),
              '- W2: era precisions %s; intervals %s. **%s.** Breach: two eras more than 20 pp apart with disjoint intervals; with n = 40 that needs roughly 39/40 against 30/40 or wider (for example 97.5%% [87.1-99.6] against 70%% [54.6-81.9]). Can fail.' % (', '.join('%s %s%%' % (e, A[e]['precision_pct']) for e in A), '; '.join('%s %s' % (e, ci(A[e]['wilson95'])) for e in A), f(C['W2_pass'])),
              '- W3: era miss rates %s; intervals %s. **%s.** Breach: two eras more than 20 pp apart with disjoint intervals, for example 2/40 against 14/40 (5%% [1.4-16.5] against 35%% [22.1-50.5]); run 4\'s 27/40 against 7/40 would have breached. Can fail, in either direction.' % (', '.join('%s %s%%' % (e, B[e]['miss_rate_pct']) for e in B), '; '.join('%s %s' % (e, ci(B[e]['wilson95'])) for e in B), f(C['W3_pass'])),
              '- W4: miss rates %s. **%s.** Breach: any era above 25%%, i.e. 11 or more of 40 missed. Can fail.' % (', '.join('%s %s%%' % (e, B[e]['miss_rate_pct']) for e in B), f(C['W4_pass'])),
              '- **Verdict: %s.**' % C['verdict'], '',
              'A note on W2 and W3: requiring BOTH a gap over 20 pp AND disjoint intervals makes them harder to breach than a gap alone at n = 40. They can still fail on plausible outcomes, as the examples show, so they are reported as tests, not as formalities.', '']
    L += ['## E. v1 against v2', '', 'All records in each era (not just samples).', '',
          '| Era | Records | v1 flags | v2 flags | Both | v1 only | v2 only | v1-only records carrying an NDC | v2-only by sub-rule (P2 P3 P4 P5 B1 B2 B3) |', '|---|---|---|---|---|---|---|---|---|']
    for e in G:
        g = G[e]
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (e, f(g['n']), f(g['v1_flags']), f(g['v2_flags']), f(g['both']), f(g['v1_only']), f(g['v2_only']), f(g['v1_only_with_ndc']),
                                                           ' '.join(str(g['v2_only_by_subrule'][s]) for s in ('P2', 'P3', 'P4', 'P5', 'B1', 'B2', 'B3'))))
    L.append('')
    if C.get('complete') and not D:
        L += ['## F. What run 5 shows (no decomposition; Part D is conditional on a pass)', '',
              '- **v2 fixed the precision defect.** Pooled precision rose to %s%% and every era is at or above %s%%. The two remaining errors are the run 4 defect in a form the B3 exclusion list did not anticipate: a finished product in a "Bulk Container" whose description names no dosage-form word.' % (ap['precision_pct'], min(A[e]['precision_pct'] for e in A)),
              '- **v2 did not fix the recall defect.** Miss rates are %s, %s and %s%% (E1, E2, E3), against run 4\'s 67.5, 45.0 and 17.5%% for v1 on a different sample. The misses still run high early and low late, the same direction as run 4, so a decomposition using v2 would still understate the early compounded share.' % (B['E1']['miss_rate_pct'], B['E2']['miss_rate_pct'], B['E3']['miss_rate_pct']),
              '- **What the remaining misses have in common.** Every missed record names a preparer, but not in words a rule can separate from a manufacturer: a "Drug" store, a "Laboratories" or "Labs", a "Health Solutions", an "Rx" business name, an infusion firm named without a service word, or no firm at all with a non-commercial product form (a beyond-use date, an Rx number, a combination with no commercial equivalent). A reader recognizes them from the product plus the firm; the vocabulary does not. That is a finding about the source text, recorded here, not a proposal for a third label.',
              '- **v1 against v2 (section E).** v2 flags more in every era and almost everything v1 flags; the additions come mainly from P2 (a named pharmacy) and P5 (named preparers), and in E3 also P3 and P4. Most v1-only records in E2 and E3 carry an NDC, consistent with the finished-bulk exclusion working as intended.',
              '- **Consistency note on run 4.** Run 5 B-E2 #3 marks a hydroxocobalamin vial from a compounding pharmacy as missed; run 4 B-E2 #17 marked a product from the same firm "not". The run 4 mark looks wrong in hindsight. It is recorded, not changed: run 4 is closed.',
              '- **Parser observation, for the limitations section only.** Four of the 40 E3 Part B records carry an NDC in a form the run 2 parser does not accept (spaced digits, a three-digit package segment, an unhyphenated labeler-product run, a product-level code). Run 3 measured 1 in 40 in the comparable E3 population. Run 3 is not reopened; this goes beside the dotted and product-level forms already listed.',
              '- **Per the brief:** v2 fails and the run stops. No third label was built. The fallback applies: the paper ships its first three findings, with attribution reported as attempted and unresolved.', '']
    if D:
        L += ['## D. Decomposition under three labels', '',
              'Arithmetic as in run 4: C = s x pF + (1 - s) x pO; composition = ds x (pFbar - pObar); within-group = sbar x dpF + (1 - sbar) x dpO; interaction = dC - composition - within-group; bars are each column\'s own pooled 2013-2026 values. Residual-bias correction: in each year, (era miss rate of v2) x (v2-unflagged records with no NDC) records are moved from "other" to "flagged"; they carry no NDC, so only the counts move.', '',
              '| Comparison | Label | Coverage from -> to | Total pp | Composition pp (share) | Within-group pp (share) | Interaction pp (share) |', '|---|---|---|---|---|---|---|']
        for lab, key in (('2013 -> 2026', 'y2013_to_y2026'), ('E1 -> E3', 'E1_to_E3')):
            for k in ('v1', 'v2', 'v2_corrected'):
                v = D[k][key]
                L.append('| %s | %s | %s%% -> %s%% | %+.2f | %+.2f (%s%%) | %+.2f (%s%%) | %+.2f (%s%%) |' % (lab, k, v['coverage_from_pct'], v['coverage_to_pct'], v['total_change_pp'], v['composition_pp'], v['composition_share_pct'],
                                                                                         v['within_pp'], v['within_share_pct'], v['interaction_pp'], v['interaction_share_pct']))
        L.append('')
        for k in ('v2', 'v2_corrected'):
            L += ['Per-year, %s:' % k, '', '| Year | n | Flagged (share %) | Flagged with NDC (%) | Other with NDC (%) | Moved by correction |', '|---|---|---|---|---|---|']
            for r in D[k]['years']:
                L.append('| %d | %s | %s (%s) | %s (%s) | %s (%s) | %s |' % (r['year'], f(r['n']), r['flagged'], r['flagged_share_pct'], r['flagged_with_ndc'], r['flagged_ndc_pct'], r['other_with_ndc'], r['other_ndc_pct'], r['moved']))
            L.append('')
    with open(os.path.join(HERE, 'RUN5-REPORT.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    if '--rules-only' in sys.argv:
        write_rules_only()
    else:
        main()
