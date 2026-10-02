// DISCLAIMER BEGIN
// This work was carried out independently, on personal time and equipment, and is not
// connected to the author's employment. The views expressed are the author's own and do
// not represent the views, positions or policies of any current, former or future employer
// or client. No proprietary, confidential or internal data of any organization was used.
// All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
// DISCLAIMER END
// ---- BEGIN CODE ----
(function (root, factory) {
  if (typeof module === 'object' && module.exports) { module.exports = factory(); }
  else { root.A15 = factory(); }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  var VERSION = 'a15-core 1.0.0';
  var START = '20120601';
  var HORIZONS = [90, 180, 365];
  var FIELDS = ['reason_for_recall', 'product_description', 'voluntary_mandated',
    'initial_firm_notification', 'state', 'country', 'distribution_pattern',
    'recall_initiation_date', 'center_classification_date', 'report_date',
    'product_quantity', 'status', 'classification'];
  var PLACEHOLDERS = ['n/a', 'na', 'none', 'unknown', 'not available', 'null', '-', '--'];
  // Stop thresholds. Fixed in this file BEFORE the first run on the real corpus.
  var STOP = {
    min_coverage_pct: 30,          // Q1: product_ndc present in fewer than this % of records
    min_ndcs_multi_event: 200,     // Q2: fewer NDCs than this appear in 2+ distinct events, OR
    min_pct_ndcs_multi_event: 5,   // Q2: fewer than this % of NDCs appear in 2+ distinct events
    min_positives: 100,            // Q7: degenerate at a horizon if positives below this, OR
    min_prevalence_pct: 2          // Q7: prevalence below this %; stop only if degenerate at EVERY horizon
  };
  var CHECK_EVENTS = ['97369', '89450', '93456', '89106'];

  // ---------- small helpers ----------
  function dnum(s) {
    if (typeof s !== 'string' || !/^\d{8}$/.test(s)) { return null; }
    var y = +s.slice(0, 4), m = +s.slice(4, 6), d = +s.slice(6, 8);
    if (m < 1 || m > 12 || d < 1 || d > 31) { return null; }
    return Math.round(Date.UTC(y, m - 1, d) / 86400000);
  }
  function dstr(n) { return n == null ? null : new Date(n * 86400000).toISOString().slice(0, 10); }
  function isPresent(v) {
    if (v === null || v === undefined) { return false; }
    if (Array.isArray(v)) { return v.some(function (x) { return String(x).trim() !== ''; }); }
    if (typeof v === 'object') { return Object.keys(v).length > 0; }
    return String(v).trim() !== '';
  }
  function isPlaceholder(v) {
    return typeof v === 'string' && PLACEHOLDERS.indexOf(v.trim().toLowerCase()) >= 0;
  }
  function r2(x) { return Math.round(x * 100) / 100; }
  function pct(a, b) { return b ? r2(100 * a / b) : null; }
  function quantiles(arr) {
    if (!arr.length) { return { n: 0 }; }
    var s = arr.slice().sort(function (a, b) { return a - b; });
    function q(p) {
      var h = (s.length - 1) * p, lo = Math.floor(h), hi = Math.ceil(h);
      return r2(s[lo] + (s[hi] - s[lo]) * (h - lo));
    }
    var sum = 0; s.forEach(function (x) { sum += x; });
    return { n: s.length, min: s[0], q1: q(0.25), median: q(0.5), q3: q(0.75),
      p90: q(0.9), p95: q(0.95), p99: q(0.99), max: s[s.length - 1], mean: r2(sum / s.length) };
  }
  function inc(o, k, by) { o[k] = (o[k] || 0) + (by === undefined ? 1 : by); }
  function sortedKeys(o) { return Object.keys(o).sort(); }
  function productNdcs(r) {
    var o = r.openfda;
    if (!o || !Array.isArray(o.product_ndc)) { return []; }
    var seen = {}, out = [];
    o.product_ndc.forEach(function (x) {
      var k = String(x).trim();
      if (k && !seen[k]) { seen[k] = true; out.push(k); }
    });
    return out;
  }
  function evId(r) {
    if (r.event_id === null || r.event_id === undefined) { return null; }
    var k = String(r.event_id).trim();
    return k || null;
  }
  function cat(v) {
    if (!isPresent(v)) { return '(missing)'; }
    return String(v).trim();
  }
  function ndcBucket(n) {
    if (n === 0) { return '0'; }
    if (n === 1) { return '1'; }
    if (n === 2) { return '2'; }
    if (n <= 5) { return '3-5'; }
    if (n <= 10) { return '6-10'; }
    if (n <= 50) { return '11-50'; }
    return '51+';
  }

  // ---------- zip reader (single-entry openFDA archives) ----------
  var CRC_TABLE = (function () {
    var t = new Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) { c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1); }
      t[n] = c >>> 0;
    }
    return t;
  })();
  function crc32(u8) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < u8.length; i++) { c = CRC_TABLE[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); }
    return (c ^ 0xFFFFFFFF) >>> 0;
  }
  // inflateRaw: function(Uint8Array) -> Promise<Uint8Array> or Uint8Array
  function readZip(u8, inflateRaw) {
    var dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
    var eocd = -1;
    for (var i = u8.length - 22; i >= Math.max(0, u8.length - 65557); i--) {
      if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
    }
    if (eocd < 0) { throw new Error('zip: end of central directory not found'); }
    var nEntries = dv.getUint16(eocd + 10, true);
    var cdOff = dv.getUint32(eocd + 16, true);
    var entries = [], p = cdOff;
    for (var e = 0; e < nEntries; e++) {
      if (dv.getUint32(p, true) !== 0x02014b50) { throw new Error('zip: bad central header'); }
      var method = dv.getUint16(p + 10, true), crc = dv.getUint32(p + 16, true);
      var csize = dv.getUint32(p + 20, true), usize = dv.getUint32(p + 24, true);
      var nlen = dv.getUint16(p + 28, true), xlen = dv.getUint16(p + 30, true), clen = dv.getUint16(p + 32, true);
      var loff = dv.getUint32(p + 42, true);
      var name = '';
      for (var j = 0; j < nlen; j++) { name += String.fromCharCode(u8[p + 46 + j]); }
      entries.push({ name: name, method: method, crc: crc, csize: csize, usize: usize, loff: loff });
      p += 46 + nlen + xlen + clen;
    }
    if (entries.length !== 1) { throw new Error('zip: expected exactly 1 entry, found ' + entries.length); }
    var en = entries[0];
    var lnl = dv.getUint16(en.loff + 26, true), lxl = dv.getUint16(en.loff + 28, true);
    var start = en.loff + 30 + lnl + lxl;
    var comp = u8.subarray(start, start + en.csize);
    function finish(out) {
      if (out.length !== en.usize) { throw new Error('zip: size mismatch'); }
      var got = crc32(out);
      if (got !== en.crc) { throw new Error('zip: CRC mismatch'); }
      return { name: en.name, bytes: out, usize: en.usize, csize: en.csize,
        crc32: ('00000000' + en.crc.toString(16)).slice(-8), crc_ok: true };
    }
    if (en.method === 0) { return Promise.resolve(finish(comp)); }
    if (en.method !== 8) { throw new Error('zip: unsupported method ' + en.method); }
    return Promise.resolve(inflateRaw(comp)).then(function (out) { return finish(new Uint8Array(out)); });
  }

  // ---------- the analysis ----------
  function analyze(records) {
    var out = { core_version: VERSION, start_report_date: START, horizons: HORIZONS, stop_thresholds: STOP };

    // --- corpus definition ---
    var rawYear = {}, rawMonth = {}, bad = 0, before = 0, rawMin = null, rawMax = null, corpus = [];
    records.forEach(function (r) {
      var rd = r.report_date;
      if (dnum(rd) === null) { bad++; return; }
      inc(rawYear, rd.slice(0, 4));
      if (rd >= '20110101' && rd < '20140101') { inc(rawMonth, rd.slice(0, 6)); }
      if (rawMin === null || rd < rawMin) { rawMin = rd; }
      if (rawMax === null || rd > rawMax) { rawMax = rd; }
      if (rd < START) { before++; } else { corpus.push(r); }
    });
    out.corpus = {
      raw_records: records.length, invalid_report_date: bad, before_start: before,
      in_corpus: corpus.length, raw_report_date_min: rawMin, raw_report_date_max: rawMax,
      raw_by_year: rawYear, raw_by_month_2011_2013: rawMonth
    };

    // precompute
    var R = corpus.map(function (r) {
      return { r: r, ev: evId(r), ndcs: productNdcs(r), y: r.report_date.slice(0, 4),
        rep: dnum(r.report_date), init: dnum(r.recall_initiation_date),
        ccd: dnum(r.center_classification_date) };
    });
    var N = R.length;
    var dataEnd = null;
    R.forEach(function (x) { if (dataEnd === null || x.rep > dataEnd) { dataEnd = x.rep; } });
    out.corpus.data_end_report_date = dstr(dataEnd);

    // --- Q1 coverage ---
    var withN = 0, byYear = {}, bucket = {}, pkg = 0, anyOpenfda = 0, descNdcWith = 0, descNdcWithout = 0;
    var ndcRe = /\b\d{4,5}-\d{3,4}-\d{1,2}\b/;
    R.forEach(function (x) {
      var has = x.ndcs.length > 0;
      if (!byYear[x.y]) { byYear[x.y] = { n: 0, with_ndc: 0 }; }
      byYear[x.y].n++;
      if (has) { withN++; byYear[x.y].with_ndc++; }
      inc(bucket, ndcBucket(x.ndcs.length));
      if (x.r.openfda && Array.isArray(x.r.openfda.package_ndc) && x.r.openfda.package_ndc.length) { pkg++; }
      if (isPresent(x.r.openfda)) { anyOpenfda++; }
      var d = typeof x.r.product_description === 'string' && ndcRe.test(x.r.product_description);
      if (d && has) { descNdcWith++; }
      if (d && !has) { descNdcWithout++; }
    });
    var q1Year = sortedKeys(byYear).map(function (y) {
      return { year: y, n: byYear[y].n, with_ndc: byYear[y].with_ndc, pct: pct(byYear[y].with_ndc, byYear[y].n) };
    });
    out.q1 = { n: N, with_product_ndc: withN, pct: pct(withN, N), by_year: q1Year,
      product_ndc_count_per_record: bucket, with_package_ndc: pkg, with_any_openfda: anyOpenfda,
      ndc_pattern_in_description_with_openfda_ndc: descNdcWith,
      ndc_pattern_in_description_without_openfda_ndc: descNdcWithout };

    // --- Q2 recurrence across distinct event_ids ---
    function buildNdcEvents(filterFn) {
      var m = {};
      R.forEach(function (x) {
        if (!x.ev || !x.ndcs.length || (filterFn && !filterFn(x))) { return; }
        x.ndcs.forEach(function (k) {
          var evs = m[k] || (m[k] = {});
          var e = evs[x.ev] || (evs[x.ev] = { init: null, rep: null, nrec: 0 });
          e.nrec++;
          if (x.init !== null && (e.init === null || x.init < e.init)) { e.init = x.init; }
          if (e.rep === null || x.rep < e.rep) { e.rep = x.rep; }
        });
      });
      return m;
    }
    function recurrence(m) {
      var d = { '1': 0, '2': 0, '3': 0, '4+': 0 }, max = 0, total = 0;
      Object.keys(m).forEach(function (k) {
        var c = Object.keys(m[k]).length; total++;
        if (c > max) { max = c; }
        inc(d, c >= 4 ? '4+' : String(c));
      });
      var multi = total - d['1'];
      return { distinct_ndcs: total, events_per_ndc: d, ndcs_in_2plus_events: multi,
        pct_in_2plus: pct(multi, total), max_events_for_one_ndc: max };
    }
    var M = buildNdcEvents(null);
    var M1 = buildNdcEvents(function (x) { return x.ndcs.length === 1; });
    var missingEv = 0; R.forEach(function (x) { if (!x.ev) { missingEv++; } });
    out.q2 = { all_records: recurrence(M), single_ndc_records_only: recurrence(M1),
      records_missing_event_id: missingEv };

    // --- Q3 intervals ---
    function intervals(m, key) {
      var diffs = [], missing = 0, recurring = 0;
      Object.keys(m).forEach(function (k) {
        var evs = Object.keys(m[k]); if (evs.length < 2) { return; }
        recurring++;
        var ds = [];
        evs.forEach(function (e) { var v = m[k][e][key]; if (v === null) { missing++; } else { ds.push(v); } });
        ds.sort(function (a, b) { return a - b; });
        for (var i = 1; i < ds.length; i++) { diffs.push(ds[i] - ds[i - 1]); }
      });
      var b = { '0': 0, '1-7': 0, '8-30': 0, '31-90': 0, '91-180': 0, '181-365': 0, '366-730': 0, '731+': 0 };
      diffs.forEach(function (v) {
        if (v === 0) { b['0']++; } else if (v <= 7) { b['1-7']++; } else if (v <= 30) { b['8-30']++; }
        else if (v <= 90) { b['31-90']++; } else if (v <= 180) { b['91-180']++; }
        else if (v <= 365) { b['181-365']++; } else if (v <= 730) { b['366-730']++; } else { b['731+']++; }
      });
      return { recurring_ndcs: recurring, event_dates_missing: missing, stats_days: quantiles(diffs), buckets: b };
    }
    out.q3 = { by_recall_initiation_date: intervals(M, 'init'), by_report_date: intervals(M, 'rep'),
      single_ndc_records_by_recall_initiation_date: intervals(M1, 'init') };

    // --- Q4 selection ---
    function compare(getter) {
      var a = {}, b = {}, na = 0, nb = 0;
      R.forEach(function (x) {
        var v = getter(x);
        if (x.ndcs.length) { inc(a, v); na++; } else { inc(b, v); nb++; }
      });
      var keys = {}; Object.keys(a).concat(Object.keys(b)).forEach(function (k) { keys[k] = true; });
      return sortedKeys(keys).map(function (k) {
        var pa = pct(a[k] || 0, na), pb = pct(b[k] || 0, nb);
        return { value: k, with_n: a[k] || 0, with_pct: pa, without_n: b[k] || 0, without_pct: pb, diff_pp: r2(pa - pb) };
      });
    }
    out.q4 = {
      n_with: withN, n_without: N - withN,
      classification: compare(function (x) { return cat(x.r.classification); }),
      voluntary_mandated: compare(function (x) { return cat(x.r.voluntary_mandated); }),
      initial_firm_notification: compare(function (x) { return cat(x.r.initial_firm_notification); }),
      year: compare(function (x) { return x.y; }),
      status: compare(function (x) { return cat(x.r.status); })
    };

    // --- Q5 snapshot property ---
    function snapshot(list) {
      var ev = {};
      list.forEach(function (r) {
        var id = evId(r); if (!id) { return; }
        var e = ev[id] || (ev[id] = { n: 0, rd: {}, rid: {}, ccd: {}, cls: {}, firm: {}, vm: {} });
        e.n++;
        e.rd[String(r.report_date)] = 1; e.rid[String(r.recall_initiation_date)] = 1;
        e.ccd[String(r.center_classification_date)] = 1; e.cls[String(r.classification)] = 1;
        e.firm[String(r.recalling_firm)] = 1; e.vm[String(r.voluntary_mandated)] = 1;
      });
      var ids = Object.keys(ev), res = { events: ids.length, multi_record_events: 0,
        events_gt1_report_date: 0, events_gt1_recall_initiation_date: 0,
        events_gt1_center_classification_date: 0, events_gt1_classification: 0,
        events_gt1_recalling_firm: 0, events_gt1_voluntary_mandated: 0,
        examples_gt1_report_date: [] };
      var sizes = [];
      ids.forEach(function (id) {
        var e = ev[id]; sizes.push(e.n); if (e.n > 1) { res.multi_record_events++; }
        var nrd = Object.keys(e.rd).length;
        if (nrd > 1) {
          res.events_gt1_report_date++;
          if (res.examples_gt1_report_date.length < 20) {
            res.examples_gt1_report_date.push({ event_id: id, records: e.n, report_dates: sortedKeys(e.rd) });
          }
        }
        if (Object.keys(e.rid).length > 1) { res.events_gt1_recall_initiation_date++; }
        if (Object.keys(e.ccd).length > 1) { res.events_gt1_center_classification_date++; }
        if (Object.keys(e.cls).length > 1) { res.events_gt1_classification++; }
        if (Object.keys(e.firm).length > 1) { res.events_gt1_recalling_firm++; }
        if (Object.keys(e.vm).length > 1) { res.events_gt1_voluntary_mandated++; }
      });
      res.records_per_event = quantiles(sizes);
      res.check_events = CHECK_EVENTS.map(function (id) {
        var e = ev[id];
        return e ? { event_id: id, records: e.n, report_dates: sortedKeys(e.rd) } : { event_id: id, records: 0 };
      });
      return res;
    }
    var validRaw = records.filter(function (r) { return dnum(r.report_date) !== null; });
    out.q5 = { whole_file: snapshot(validRaw), corpus: snapshot(corpus) };

    // --- Q6 field completeness ---
    var q6 = {};
    FIELDS.forEach(function (f) {
      var p = 0, ph = 0, yr = {};
      R.forEach(function (x) {
        var v = x.r[f];
        if (!yr[x.y]) { yr[x.y] = { n: 0, present: 0 }; }
        yr[x.y].n++;
        if (isPresent(v)) { p++; yr[x.y].present++; }
        if (isPlaceholder(v)) { ph++; }
      });
      var ys = sortedKeys(yr).map(function (y) { return { year: y, n: yr[y].n, pct: pct(yr[y].present, yr[y].n) }; });
      var big = ys.filter(function (z) { return z.n >= 100; });
      var lo = null, hi = null;
      big.forEach(function (z) { if (lo === null || z.pct < lo.pct) { lo = z; } if (hi === null || z.pct > hi.pct) { hi = z; } });
      q6[f] = { present: p, pct: pct(p, N), placeholder_values: ph, by_year: ys,
        min_year: lo, max_year: hi, range_pp: lo && hi ? r2(hi.pct - lo.pct) : null };
    });
    out.q6 = q6;

    // --- Q7 outcome balance ---
    // reporting lag at event level: first report_date minus first recall_initiation_date
    var evAgg = {};
    R.forEach(function (x) {
      if (!x.ev) { return; }
      var e = evAgg[x.ev] || (evAgg[x.ev] = { init: null, rep: null });
      if (x.init !== null && (e.init === null || x.init < e.init)) { e.init = x.init; }
      if (e.rep === null || x.rep < e.rep) { e.rep = x.rep; }
    });
    var lags = [], negLag = 0;
    Object.keys(evAgg).forEach(function (k) {
      var e = evAgg[k];
      if (e.init !== null) { var l = e.rep - e.init; lags.push(l); if (l < 0) { negLag++; } }
    });
    var lagStats = quantiles(lags);
    var L = Math.ceil(lagStats.p95);

    // index units: (NDC, event) pairs with a valid initiation date
    var units = [];
    Object.keys(M).forEach(function (k) {
      var evs = M[k];
      var list = Object.keys(evs).filter(function (e) { return evs[e].init !== null; })
        .map(function (e) { return { ndc: k, ev: e, init: evs[e].init }; });
      list.sort(function (a, b) { return a.init - b.init; });
      list.forEach(function (u, i) {
        u.first = i === 0 || list[0].init === u.init;
        u.nextGap = null; u.sameDayOther = false;
        for (var j = 0; j < list.length; j++) {
          if (j === i) { continue; }
          var g = list[j].init - u.init;
          if (g === 0) { u.sameDayOther = true; }
          if (g > 0 && (u.nextGap === null || g < u.nextGap)) { u.nextGap = g; }
        }
        units.push(u);
      });
    });
    function labeler(ndc) { return ndc.split('-')[0]; }
    var q7 = { unit: '(product_ndc, event_id) pair; index date = earliest recall_initiation_date among the records of that event carrying that NDC',
      data_end_report_date: dstr(dataEnd), reporting_lag_days: lagStats, events_negative_lag: negLag,
      lag_allowance_days_L: L, index_units_total: units.length,
      index_units_before_start_init: units.filter(function (u) { return u.init < dnum(START); }).length,
      horizons: {} };
    HORIZONS.forEach(function (H) {
      function stat(filter, posFn) {
        var n = 0, pos = 0, nd = {}, ne = {}, nl = {};
        units.forEach(function (u) {
          if (!filter(u)) { return; }
          n++; nd[u.ndc] = 1; ne[u.ev] = 1; nl[labeler(u.ndc)] = 1;
          if (posFn(u)) { pos++; }
        });
        return { eligible: n, positive: pos, pct: pct(pos, n), distinct_ndcs: Object.keys(nd).length,
          distinct_events: Object.keys(ne).length, distinct_labelers: Object.keys(nl).length };
      }
      var primaryElig = function (u) { return u.init + H + L <= dataEnd; };
      var naiveElig = function (u) { return u.init + H <= dataEnd; };
      var pos = function (u) { return u.nextGap !== null && u.nextGap <= H; };
      var posSame = function (u) { return pos(u) || u.sameDayOther; };
      // event-level: an event is positive if any of its NDCs repeats within H
      var evPos = {}, evElig = {};
      units.forEach(function (u) {
        if (!primaryElig(u)) { return; }
        evElig[u.ev] = 1; if (pos(u)) { evPos[u.ev] = 1; }
      });
      var byYear = {};
      units.forEach(function (u) {
        if (!primaryElig(u)) { return; }
        var y = dstr(u.init).slice(0, 4);
        if (!byYear[y]) { byYear[y] = { eligible: 0, positive: 0 }; }
        byYear[y].eligible++; if (pos(u)) { byYear[y].positive++; }
      });
      q7.horizons[String(H)] = {
        primary: stat(primaryElig, pos),
        naive_right_edge: stat(naiveElig, pos),
        primary_counting_same_day_other_event: stat(primaryElig, posSame),
        primary_first_occurrence_only: stat(function (u) { return u.first && primaryElig(u); }, pos),
        event_level: { eligible_events: Object.keys(evElig).length, positive_events: Object.keys(evPos).length,
          pct: pct(Object.keys(evPos).length, Object.keys(evElig).length) },
        by_index_year: sortedKeys(byYear).map(function (y) {
          return { year: y, eligible: byYear[y].eligible, positive: byYear[y].positive, pct: pct(byYear[y].positive, byYear[y].eligible) };
        })
      };
    });
    out.q7 = q7;

    // --- leakage structure: connected components of the NDC-event graph ---
    var parent = {};
    function find(a) { while (parent[a] !== a) { parent[a] = parent[parent[a]]; a = parent[a]; } return a; }
    function union(a, b) { var ra = find(a), rb = find(b); if (ra !== rb) { parent[ra] = rb; } }
    Object.keys(M).forEach(function (k) {
      var nk = 'n:' + k; if (parent[nk] === undefined) { parent[nk] = nk; }
      Object.keys(M[k]).forEach(function (e) {
        var ne = 'e:' + e; if (parent[ne] === undefined) { parent[ne] = ne; }
        union(nk, ne);
      });
    });
    var comp = {};
    Object.keys(parent).forEach(function (node) {
      var c = find(node); var o = comp[c] || (comp[c] = { ndcs: 0, events: 0, units: 0 });
      if (node.charAt(0) === 'n') { o.ndcs++; } else { o.events++; }
    });
    units.forEach(function (u) { comp[find('n:' + u.ndc)].units++; });
    var compList = Object.keys(comp).map(function (c) { return comp[c]; });
    compList.sort(function (a, b) { return b.units - a.units; });
    var labUnits = {};
    units.forEach(function (u) { inc(labUnits, labeler(u.ndc)); });
    var labCounts = Object.keys(labUnits).map(function (k) { return labUnits[k]; }).sort(function (a, b) { return b - a; });
    out.leakage = {
      components: compList.length,
      largest_components: compList.slice(0, 5).map(function (c) {
        return { ndcs: c.ndcs, events: c.events, index_units: c.units, pct_of_units: pct(c.units, units.length) };
      }),
      labelers: labCounts.length,
      largest_labeler_units: labCounts.slice(0, 5).map(function (n) { return { index_units: n, pct_of_units: pct(n, units.length) }; })
    };

    // --- stop conditions ---
    var q7deg = HORIZONS.every(function (H) {
      var p = q7.horizons[String(H)].primary;
      return p.positive < STOP.min_positives || p.pct < STOP.min_prevalence_pct;
    });
    out.stop = {
      q1_low_coverage: out.q1.pct < STOP.min_coverage_pct,
      q2_recurrence_too_rare: out.q2.all_records.ndcs_in_2plus_events < STOP.min_ndcs_multi_event ||
        out.q2.all_records.pct_in_2plus < STOP.min_pct_ndcs_multi_event,
      q5_contradicts_snapshot: out.q5.whole_file.events_gt1_report_date > 0,
      q7_degenerate_all_horizons: q7deg
    };
    out.stop.any = out.stop.q1_low_coverage || out.stop.q2_recurrence_too_rare ||
      out.stop.q5_contradicts_snapshot || out.stop.q7_degenerate_all_horizons;
    return out;
  }

  return { VERSION: VERSION, analyze: analyze, readZip: readZip, crc32: crc32, dnum: dnum, dstr: dstr,
    quantiles: quantiles, productNdcs: productNdcs };
});
