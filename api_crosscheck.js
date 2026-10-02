// DISCLAIMER BEGIN
// This work was carried out independently, on personal time and equipment, and is not
// connected to the author's employment. The views expressed are the author's own and do
// not represent the views, positions or policies of any current, former or future employer
// or client. No proprietary, confidential or internal data of any organization was used.
// All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
// DISCLAIMER END
// Independent cross-check of four bulk-file counts against the live openFDA API.
// Run in a browser page at https://open.fda.gov/ (api.fda.gov allows that origin).
// Captured 2026-09-28 05:38 UTC; the returned values are recorded in STATUS.md section 3.
(async function () {
  var base = 'https://api.fda.gov/drug/enforcement.json?limit=1&search=';
  var qs = { all: 'report_date:[20000101+TO+20301231]', ndc: '_exists_:openfda.product_ndc',
    ev97369: 'event_id:97369', c1: 'classification:"Class+I"' };
  var o = {};
  for (var k in qs) {
    var j = await fetch(base + qs[k]).then(function (r) { return r.json(); });
    o[k] = j.meta ? j.meta.results.total : j.error;
  }
  return o;
})();
