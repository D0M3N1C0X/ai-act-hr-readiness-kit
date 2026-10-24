// Recomputes with web/engine.js every case Python computed, and exits with 1 at the first difference.
import { readFileSync } from "node:fs";
import { assess, yesNo, annex, condition63 } from "../../web/engine.js";

const V = JSON.parse(readFileSync(new URL("../fixtures/js_vectors.json", import.meta.url)));
let checks = 0, failures = 0;
const expect = (ok, what) => { checks++; if (!ok) { failures++; if (failures <= 20) console.error("difference:", what); } };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

for (const c of V.cases) {
  const r = assess(c.system, V.cfg, V.cfg.headcount);
  for (const k of ["class", "role", "workers", "obligations", "rules"])
    expect(same(r[k], c[k]), `${c.system.system_id} ${k}: ${JSON.stringify(r[k])} vs ${JSON.stringify(c[k])}`);
}
// Reading answers the way files write them
for (const [v, w] of [["Yes", "Yes"], ["sì", "Yes"], ["Ja", "Yes"], ["TAK", "Yes"], ["x", "Yes"], ["No", "No"], ["", "No"], ["maybe", null]])
  expect(yesNo(v) === w, `yesNo(${v})`);
for (const [v, w] of [["4(a)", "4(a)"], ["4a", "4(a)"], ["4 (b)", "4(b)"], ["None", "None"], ["", "None"], ["5", null]])
  expect(annex(v) === w, `annex(${v})`);
for (const [v, w] of [["(a)", "(a)"], ["d", "(d)"], ["None", "None"], ["e", null]]) expect(condition63(v) === w, `condition63(${v})`);
console.log(`${checks - failures} of ${checks} values agree with Python in ${V.cases.length} systems`);
process.exit(failures ? 1 : 0);
