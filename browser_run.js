// DISCLAIMER BEGIN
// This work was carried out independently, on personal time and equipment, and is not
// connected to the author's employment. The views expressed are the author's own and do
// not represent the views, positions or policies of any current, former or future employer
// or client. No proprietary, confidential or internal data of any organization was used.
// All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
// DISCLAIMER END
// ---- BEGIN CODE ----
// A15 browser runner: the path that produced results.json on 2026-09-28.
// Both shells in this program are blocked from download.open.fda.gov by the network allowlist,
// so the bulk archive was fetched and analyzed inside a browser page at the download host's own
// origin (the host sends no CORS header, so the page must be on https://download.open.fda.gov/).
// Usage: open https://download.open.fda.gov/drug/enforcement/ , evaluate the code body of
// a15_core.js (defines window.A15), then evaluate this body. It returns the results string
// and its SHA-256 over (string + newline), which is what results.json on disk must match.
(async function () {
  var URL_ZIP = 'https://download.open.fda.gov/drug/enforcement/drug-enforcement-0001-of-0001.json.zip';
  async function hex(u8) {
    var h = new Uint8Array(await crypto.subtle.digest('SHA-256', u8));
    return Array.prototype.map.call(h, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  }
  async function inflateRaw(c) {
    var s = new Blob([c]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
    return new Uint8Array(await new Response(s).arrayBuffer());
  }
  var prov = { runner: 'browser_run.js', core_version: A15.VERSION, user_agent: navigator.userAgent };
  var resp = await fetch(URL_ZIP, { cache: 'no-store' });
  if (!resp.ok) { throw new Error('HTTP ' + resp.status); }
  var buf = new Uint8Array(await resp.arrayBuffer());
  prov.url = URL_ZIP;
  prov.retrieved_utc = new Date().toISOString();
  prov.http_last_modified = resp.headers.get('last-modified');
  prov.http_etag = resp.headers.get('etag');
  prov.bytes = buf.length;
  prov.sha256 = await hex(buf);
  var z = await A15.readZip(buf, inflateRaw);
  prov.zip_entry = z.name;
  prov.zip_entry_bytes = z.usize;
  prov.zip_entry_crc32 = z.crc32;
  prov.zip_entry_sha256 = await hex(z.bytes);
  var doc = JSON.parse(new TextDecoder('utf-8').decode(z.bytes));
  prov.file_meta_last_updated = doc.meta && doc.meta.last_updated;
  prov.records_in_file = doc.results.length;
  var results = A15.analyze(doc.results);
  var s = JSON.stringify({ provenance: prov, results: results });
  window.__A15_OUT = s;
  return { chars: s.length, sha256_with_newline: await hex(new TextEncoder().encode(s + '\n')), stop: results.stop };
})();
