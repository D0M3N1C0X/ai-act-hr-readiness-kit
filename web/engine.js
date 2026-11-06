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

// Article 3(3) and (11): an employer that puts a high-risk system into service for its own use is its provider.
export const role = (s, cls) => (s.supplier === "In-house" && cls === HIGH_RISK ? "Provider and deployer" : "Deployer");

export const PRIVATE = "Private employer", PUBLIC_BODY = "Public body";
export const LEGACY = "At its next significant design change",
  LEGACY_PUBLIC = "At its next significant design change, by 2 August 2030 at the latest";

// Article 111(2) as amended by Reg. 2026/1744: a high-risk type and model already on the market before 2 December 2027
// falls under the Regulation only once its design changes significantly; a public body's by 2 August 2030 in any case.
export function timing(s, cls, deployer = PRIVATE) {
  if (cls !== HIGH_RISK) return "";
  if (s.on_market_before !== YES) return "From 2 December 2027";
  return deployer === PUBLIC_BODY ? LEGACY_PUBLIC : LEGACY;
}

// Employees in the system's scope: its countries, and its department or everyone. headcount: [{country, department, workers}]
export function workers(s, headcount) {
  let n = 0;
  for (const h of headcount) {
    if (s[`in_${h.country.toLowerCase()}`] === YES && (s.scope === "All" || h.department === s.scope)) n += h.workers;
  }
  return n;
}

// When an obligation, a question for the supplier or a literacy module applies: register.applies.
export function applies(condition, s, cls, deployer = PRIVATE) {
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
    case "high-risk and public": return high && deployer !== PRIVATE;
    case "high-risk and public body": return high && deployer === PUBLIC_BODY;
    case "high-risk on the market": return high && s.on_market_before === YES;
    case "high-risk or monitors": return cls !== PROHIBITED && (high || s.monitors_workers === YES);
    case "monitors": return cls !== PROHIBITED && s.monitors_workers === YES;
    default: throw new Error(`unknown condition ${condition}`);
  }
}

// A question goes to the supplier of a bought system: register.asks.
export const asks = (condition, s, cls) => s.supplier === "Vendor" && applies(condition, s, cls);

// When a national rule on telling the workers applies to a system in a country: register.triggers.
export function triggers(condition, country, s, cls) {
  if (s[`in_${country.toLowerCase()}`] !== YES || cls === PROHIBITED) return false;
  const staff = s.applicants !== YES;
  const high = cls === HIGH_RISK;
  switch (condition) {
    // art. 1-bis informs the worker: systems used only on applicants are left out
    case "fully automated": return staff && s.fully_automated === YES && (high || s.monitors_workers === YES);
    case "monitors": return s.monitors_workers === YES;
    case "in the country": return true;
    case "processes performance": return s.monitors_workers === YES || (staff && high);
    case "selects": return s.annex_iii === "4(a)" && s.profiling === YES && s.decides_about_people === YES;
    case "affects work": return high;
    case "on employees": return staff;
    case "changes work organisation": return s.monitors_workers === YES || (staff && high);
    default: throw new Error(`unknown condition ${condition}`);
  }
}

// One result per system: class, role, workers in scope (null without a headcount), obligations, national rules,
// questions for the supplier and literacy modules. deployer: one of cfg.deployer_types.
export function assess(s, cfg, headcount = null, deployer = cfg.deployer) {
  const cls = classify(s);
  return {
    class: cls, role: role(s, cls), timing: timing(s, cls, deployer), workers: headcount ? workers(s, headcount) : null,
    obligations: cfg.obligations.filter((o) => applies(o.when, s, cls, deployer)).map((o) => o.key),
    rules: cfg.worker_rules.filter((r) => triggers(r.when, r.country, s, cls)).map((r) => r.key),
    questions: cfg.vendor_questions.filter((q) => asks(q.when, s, cls)).map((q) => q.key),
    literacy: cfg.literacy.filter((m) => applies(m.when, s, cls)).map((m) => m.key),
  };
}

export function daysBetween(fromIso, toIso) {
  return Math.round((Date.parse(`${toIso}T00:00:00Z`) - Date.parse(`${fromIso}T00:00:00Z`)) / 86400000);
}

// ---- Reading answers from a user's file -----------------------------------------------------------------------
// Yes/No in the forms exports use, in English, Italian, German, Spanish, Polish, French and Dutch; anything else is an
// error the page shows with the row number.
const YESES = new Set(["yes", "y", "si", "true", "1", "x", "ja", "tak", "vero", "oui"]);
const NOS = new Set(["no", "n", "false", "0", "", "nein", "nie", "falso", "non", "nee"]);
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
