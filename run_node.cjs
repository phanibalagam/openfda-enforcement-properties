// DISCLAIMER BEGIN
// This work was carried out independently, on personal time and equipment, and is not
// connected to the author's employment. The views expressed are the author's own and do
// not represent the views, positions or policies of any current, former or future employer
// or client. No proprietary, confidential or internal data of any organization was used.
// All data is public: the openFDA drug enforcement bulk export (US federal public domain, export date 2026-09-25), read from data/drug-enforcement-0001-of-0001.json.zip.
// DISCLAIMER END
// A15 end-to-end runner for Node >= 18.
//   node run_node.cjs                      download the current bulk file, then analyze
//   node run_node.cjs --zip <file.zip>     analyze a local copy (provenance still recorded)
//   node run_node.cjs --out <results.json> output path (default: results.node.json beside this file)
// The downloaded archive is written to the OS temp directory, never into the program folder.
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const A15 = require('./a15_core.js');

const INDEX_URL = 'https://api.fda.gov/download.json';
const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : dflt;
}

async function main() {
  const out = arg('--out', path.join(__dirname, 'results.node.json'));
  const zipArg = arg('--zip', null);
  const prov = { runner: 'run_node.cjs', core_version: A15.VERSION, node: process.version };
  let buf;
  if (zipArg) {
    buf = fs.readFileSync(zipArg);
    prov.source = 'local file';
    prov.local_path = path.relative(__dirname, path.resolve(zipArg)).split(path.sep).join('/');
  } else {
    const idxResp = await fetch(INDEX_URL);
    const idxText = await idxResp.text();
    const idx = JSON.parse(idxText);
    const enf = idx.results.drug.enforcement;
    if (enf.partitions.length !== 1) { throw new Error('expected 1 partition, found ' + enf.partitions.length); }
    prov.index = { url: INDEX_URL, bytes: Buffer.byteLength(idxText), sha256: sha256(idxText),
      last_updated: idx.meta.last_updated, export_date: enf.export_date,
      declared_records: enf.total_records, declared_size_mb: enf.partitions[0].size_mb };
    const url = enf.partitions[0].file;
    const resp = await fetch(url, { cache: 'no-store' });
    if (!resp.ok) { throw new Error('HTTP ' + resp.status + ' for ' + url); }
    buf = Buffer.from(await resp.arrayBuffer());
    prov.url = url;
    prov.retrieved_utc = new Date().toISOString();
    prov.http_last_modified = resp.headers.get('last-modified');
    prov.http_etag = resp.headers.get('etag');
    const keep = path.join(os.tmpdir(), 'a15', path.basename(new URL(url).pathname));
    fs.mkdirSync(path.dirname(keep), { recursive: true });
    fs.writeFileSync(keep, buf);
    prov.saved_to = keep;
  }
  prov.bytes = buf.length;
  prov.sha256 = sha256(buf);
  const z = await A15.readZip(new Uint8Array(buf), (c) => zlib.inflateRawSync(c));
  prov.zip_entry = z.name;
  prov.zip_entry_bytes = z.usize;
  prov.zip_entry_crc32 = z.crc32;
  prov.zip_entry_sha256 = sha256(Buffer.from(z.bytes));
  const doc = JSON.parse(Buffer.from(z.bytes).toString('utf8'));
  prov.file_meta_last_updated = doc.meta && doc.meta.last_updated;
  prov.records_in_file = doc.results.length;
  const results = A15.analyze(doc.results);
  const s = JSON.stringify({ provenance: prov, results: results });
  fs.writeFileSync(out, s + '\n');
  console.log('wrote', out, 'sha256', sha256(s + '\n'));
  console.log('results-only sha256', sha256(JSON.stringify(results)));
  console.log('stop flags', JSON.stringify(results.stop));
}
main().catch((e) => { console.error(e); process.exit(1); });
