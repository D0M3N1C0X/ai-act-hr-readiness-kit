// The register's rules in the browser: a line-by-line twin of src/register.py. tests/js/check_engine.mjs runs it
// on the cases Python computed (tests/fixtures/js_vectors.json) and CI fails at the first difference. Nothing here
// touches the page or the network.

const YES = "Yes";
export const PROHIBITED = "Prohibited", HIGH_RISK = "High-risk", DEROGATION = "Not high-risk (Art. 6(3))",
  TRANSPARENCY = "Transparency only", MINIMAL = "Minimal risk";

// Article 5(1)(f), then Article 6(2)-(3) with Annex III point 4, then Article 50.
export function classify(s) {
  if (s.infers_emotions === YES && s.medical_or_safety !== YES) return PROHIBITED;
  if (s.annex_iii !== "None") {
    // Article 6(3), last subparagraph: a system that profiles people is always high-risk
    if (s.profiling === YES) return HIGH_RISK;
    return s.art6_3_condition !== "None" ? DEROGATION : HIGH_RISK;
  }
  return s.interacts === YES ? TRANSPARENCY : MINIMAL;
}

// Article 25: an employer that builds a high-risk system for its own use is its provider.
export const role = (s, cls) => (s.supplier === "In-house" && cls === HIGH_RISK ? "Provider and deployer" : "Deployer");

// Employees in the system's scope: its countries, and its department or everyone. headcount: [{country, department, workers}]
export function workers(s, headcount) {
  let n = 0;
  for (const h of headcount) {
    if (s[`in_${h.country.toLowerCase()}`] === YES && (s.scope === "All" || h.department === s.scope)) n += h.workers;
  }
  return n;
}

// When an obligation applies to a system: the same tests, in the same order, as register.applies.
export function applies(condition, s, cls) {
  const high = cls === HIGH_RISK;
  switch (condition) {
    case "in use": return cls !== PROHIBITED;
    case "prohibited": return cls === PROHIBITED;
    case "interacts": return s.interacts === YES && cls !== PROHIBITED;
    case "high-risk": return high;
    case "high-risk and input": return high && s.controls_input_data === YES;
    case "high-risk at work": return high && s.applicants !== YES;
    case "high-risk and decides": return high && s.decides_about_people === YES;
    case "high-risk in-house": return high && s.supplier === "In-house";
    case "derogation": return cls === DEROGATION;
    default: throw new Error(`unknown condition ${condition}`);
  }
}

// When a national rule on telling the workers applies to a system in a country: register.triggers.
export function triggers(condition, country, s, cls) {
  if (s[`in_${country.toLowerCase()}`] !== YES || cls === PROHIBITED) return false;
  const staff = s.applicants !== YES;
  const inAnnex = s.annex_iii !== "None" && s.art6_3_condition === "None";
  switch (condition) {
    case "fully automated": return s.fully_automated === YES && (inAnnex || s.monitors_workers === YES);
    case "monitors": return s.monitors_workers === YES;
    case "used on workers": return staff;
    case "processes performance": return s.monitors_workers === YES || (staff && inAnnex);
    case "selects": return s.annex_iii === "4(a)" && s.profiling === YES;
    case "affects work": return inAnnex;
    default: throw new Error(`unknown condition ${condition}`);
  }
}

// One result per system: class, role, workers in scope (null without a headcount), obligations and national rules.
export function assess(s, cfg, headcount = null) {
  const cls = classify(s);
  return {
    class: cls, role: role(s, cls), workers: headcount ? workers(s, headcount) : null,
    obligations: cfg.obligations.filter((o) => applies(o.when, s, cls)).map((o) => o.key),
    rules: cfg.worker_rules.filter((r) => triggers(r.when, r.country, s, cls)).map((r) => r.key),
  };
}

export function daysBetween(fromIso, toIso) {
  return Math.round((Date.parse(`${toIso}T00:00:00Z`) - Date.parse(`${fromIso}T00:00:00Z`)) / 86400000);
}

// ---- Reading answers from a user's file -----------------------------------------------------------------------
// Yes/No in the forms exports use, in English, Italian, German, Spanish and Polish; anything else is an error the
// page shows with the row number.
const YESES = new Set(["yes", "y", "si", "true", "1", "x", "ja", "tak", "vero"]);
const NOS = new Set(["no", "n", "false", "0", "", "nein", "nie", "falso"]);
export function yesNo(v) {
  const t = String(v ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").trim().toLowerCase();
  if (YESES.has(t)) return YES;
  if (NOS.has(t)) return "No";
  return null;
}
export function annex(v) {
  const t = String(v ?? "").toLowerCase().replace(/[\s()]/g, "");
  if (["", "none", "no", "nessuno", "-"].includes(t)) return "None";
  if (["4a", "a"].includes(t)) return "4(a)";
  if (["4b", "b"].includes(t)) return "4(b)";
  return null;
}
export function condition63(v) {
  const t = String(v ?? "").toLowerCase().replace(/[\s()]/g, "");
  if (["", "none", "no", "nessuna", "-"].includes(t)) return "None";
  return ["a", "b", "c", "d"].includes(t) ? `(${t})` : null;
}
