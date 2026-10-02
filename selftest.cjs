// DISCLAIMER BEGIN
// This work was carried out independently, on personal time and equipment, and is not
// connected to the author's employment. The views expressed are the author's own and do
// not represent the views, positions or policies of any current, former or future employer
// or client. No proprietary, confidential or internal data of any organization was used.
// All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
// DISCLAIMER END
// A15 self-test: synthetic records with hand-computed answers. Run: node selftest.cjs
'use strict';
const assert = require('assert');
const zlib = require('zlib');
const A15 = require('./a15_core.js');

function rec(ev, rd, init, ndcs, extra) {
  const r = Object.assign({ event_id: ev, report_date: rd, recall_initiation_date: init,
    center_classification_date: rd, classification: 'Class II', voluntary_mandated: 'Voluntary: Firm initiated',
    initial_firm_notification: 'Letter', status: 'Terminated', reason_for_recall: 'x', product_description: 'y',
    state: 'NJ', country: 'United States', distribution_pattern: 'US', product_quantity: '1', recalling_firm: 'F' }, extra || {});
  if (ndcs) { r.openfda = { product_ndc: ndcs }; }
  return r;
}
const recs = [
  rec('1', '20100101', '20091201', ['1111-111']),          // before start: excluded
  rec('10', '20130105', '20130101', ['1111-111']),
  rec('10', '20130105', '20130101', ['1111-111']),         // same event again: counts once
  rec('11', '20130305', '20130301', ['1111-111']),         // +59 days after event 10
  rec('12', '20140105', '20140101', ['1111-111', '2222-222']), // +306 days after event 11
  rec('13', '20130110', '20130105', ['3333-333']),
  rec('14', '20130110', '20130105', null),                 // no NDC
  rec('15', '20260901', '20260801', ['3333-333'])          // late event
];
const res = A15.analyze(recs);
assert.strictEqual(res.corpus.before_start, 1);
assert.strictEqual(res.corpus.in_corpus, 7);
assert.strictEqual(res.q1.with_product_ndc, 6);
assert.deepStrictEqual(res.q2.all_records.events_per_ndc, { '1': 1, '2': 1, '3': 1, '4+': 0 });
assert.strictEqual(res.q2.all_records.ndcs_in_2plus_events, 2);
// intervals: 1111: 59, 306 ; 3333: from 20130105 to 20260801
const d3 = A15.dnum('20260801') - A15.dnum('20130105');
assert.strictEqual(res.q3.by_recall_initiation_date.stats_days.n, 3);
assert.strictEqual(res.q3.by_recall_initiation_date.stats_days.min, 59);
assert.strictEqual(res.q3.by_recall_initiation_date.stats_days.max, d3);
assert.strictEqual(res.q3.by_recall_initiation_date.stats_days.median, 306);
assert.strictEqual(res.q5.whole_file.events_gt1_report_date, 0);
// Q5 detector must fire on a known-wrong input
const bad = A15.analyze(recs.concat([rec('13', '20130117', '20130105', ['3333-333'])]));
assert.strictEqual(bad.q5.whole_file.events_gt1_report_date, 1);
// Q7 at 90 days: units: 1111@10(pos, gap 59), 1111@11(gap 306 -> neg at 90, pos at 365), 1111@12(no next),
// 2222@12, 3333@13(gap large), 3333@15 (late -> ineligible)
const h90 = res.q7.horizons['90'].primary;
const h365 = res.q7.horizons['365'].primary;
assert.strictEqual(res.q7.index_units_total, 6);
assert.strictEqual(h90.positive, 1);
assert.strictEqual(h365.positive, 2);
assert.strictEqual(h90.eligible, 5);
// field completeness with a placeholder and a blank
const r2 = A15.analyze([rec('20', '20150101', '20141201', null, { state: '', country: 'N/A' })]);
assert.strictEqual(r2.q6.state.present, 0);
assert.strictEqual(r2.q6.country.present, 1);
assert.strictEqual(r2.q6.country.placeholder_values, 1);
// zip reader round trip against a zip produced by the system zip tool
const fs = require('fs');
if (process.argv[2]) {
  const u8 = new Uint8Array(fs.readFileSync(process.argv[2]));
  A15.readZip(u8, (c) => zlib.inflateRawSync(c)).then((z) => {
    assert.ok(z.crc_ok);
    console.log('zip ok', z.name, z.usize);
  });
}
console.log('selftest: all assertions passed');
