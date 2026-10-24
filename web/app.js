// The browser tool's page: systems added with questions or loaded from a file, classified by engine.js (checked
// against the Python register on every change), shown and downloaded. Nothing here talks to a server: inputs.json
// comes from this same page.
import { assess, classify, daysBetween, yesNo, annex, condition63, PROHIBITED, HIGH_RISK, DEROGATION, TRANSPARENCY, MINIMAL } from "./engine.js";
import { createI18n } from "./design/i18n.js";
import { readTable, parseCsv, matchColumns, applyMapping, download, normalise } from "./design/table.js";
import { writeXlsx } from "./design/xlsx.js";

const CFG = await fetch("./inputs.json").then((r) => r.json());

const UI = {
  en: {
    brand: "AI Act Readiness Kit for HR", eyebrow: "EU AI Act · Regulation (EU) 2024/1689, as amended in 2026",
    title: "Which of your HR team's AI systems are high-risk?",
    lead: "Answer a few plain questions about each AI system, or load a list. You get its class, what it owes and from when, and whom to tell in each country.",
    privacy: "Your answers stay on this computer: everything runs in this page and nothing is sent anywhere.",
    step1: "Your AI systems", step1sub: "Add them one at a time with the questions, or load a list you already have.",
    aggiungi: "Add a system", carica: "Load a list (Excel or CSV)", esempio: "Try the sample: 12 systems", modello: "List template",
    wizard: "About this system", wizardEdit: "Change «{n}»", qNome: "What is it called?", qNomePh: "For example: CV screening in the applicant tracking system",
    salva: "Save this system", annulla: "Cancel", modifica: "Change", rimuovi: "Remove", svuota: "Remove all",
    hSistema: "System", hClasse: "Class", hRuolo: "Your role", hPerche: "Why", hLavoratori: "Workers in scope",
    hObbligo: "Obligation", hArticolo: "Article", hDa: "From", hStato: "Status", hQuali: "Systems",
    inVigore: "In force", daVenire: "Ahead", nessuno: "none",
    vuoto: "No systems yet. Add one, load a list, or try the sample.",
    registro: "The register", registroSub: "Each system's class under the AI Act, and why.",
    obblighi: "What applies, and when", obblighiSub: "The duties for high-risk systems start on 2 December 2027, or at the next significant design change for a system already on the market (Art. 111(2)); the ban and AI literacy apply already.",
    avvisi: "Whom to tell, country by country", avvisiSub: "National rules on informing workers and their representatives. They apply now, whatever the AI Act's timetable.",
    nessunPaese: "No system is used in Italy, Germany, Spain or Poland, the four countries this tool knows.", nessunaRegola: "No rule applies to these systems.",
    kSistemi: "AI systems", kVietati: "To stop now", kAlto: "High-risk", kGiorni: "Days to 2 December 2027",
    scarica: "Download in Excel", stampa: "Print", stampaTitolo: "AI Act check", stampaMeta: "{n} systems · {oggi}",
    footer: "The same rules as the kit's Python register and Excel model, checked against each other on every change. Not legal advice.",
    rapporto: "Report", metodo: "Method", pacchetto: "Worker information pack", codice: "Code",
    na: "Considered and not applicable: {x}.", fornitore: "Provider and deployer", utilizzatore: "Deployer",
    cProhibited: "Prohibited", cHigh: "High-risk", cDerog: "Not high-risk (Art. 6(3))", cTransp: "Transparency only", cMinimal: "Minimal risk",
    pIntro: "With your answers so far:",
    wProhibited: "It infers emotions at work, and not for medical or safety reasons: prohibited since 2 February 2025 (Art. 5(1)(f)). It has to stop.",
    wHighProfile: "Used for {area}, and it scores or profiles people: high-risk whatever its task (Art. 6(3), last subparagraph).",
    wHigh: "Used for {area}, and none of the Art. 6(3) conditions applies: high-risk.",
    wDerog: "Used for {area}, but it only {cond} and profiles no one: not high-risk under Art. 6(3). The provider documents this; keep a copy.",
    wTransp: "Not in Annex III, but it talks to people, who must be told it is an AI (Art. 50(1)).",
    wMinimal: "Not in Annex III and it does not talk to people: AI literacy of the people who use it is the only duty (Art. 4).",
    wProvider: "You put it into service for your own use, so you are also its provider (Art. 3(3) and 16): the provider's duties apply too.",
    wLegacy: "It was on the market before 2 December 2027, so its high-risk duties start at its next significant design change (Art. 111(2)); cloud software that changes often should plan for December 2027.",
    wNew: "Its high-risk duties apply from 2 December 2027.",
    qMercato: "Was this system already on the market or in use before 2 December 2027?", qMercatoH: "The same type and model, from any customer: for a system you use today, the answer is yes.",
    area4a: "recruitment or selection", area4b: "decisions about people at work",
    cond_a: "performs a narrow procedural task", "cond_b": "improves the result of a task a person has finished",
    cond_c: "checks for deviations from earlier decisions without replacing a person's review", cond_d: "prepares an assessment that a person makes",
    sì: "Yes", no: "No",
    qSupplier: "Who made it?", supplierV: "A supplier", supplierI: "We built it in-house",
    qPaesi: "Where is it used?", qSu: "Whom is it used on?", suCand: "Applicants only", suDip: "Employees (also applicants)",
    qScope: "Which department?", tutti: "All departments",
    qEmo: "Does it read emotions from people's faces, voices or words?", qEmoH: "For example, from a video interview or a call recording.",
    qMed: "Is that only for medical or safety reasons?", qMedH: "For example, detecting fatigue in drivers.",
    qArea: "What is it used for?", a4a: "Recruitment or selection", a4aH: "Targeting job ads, screening or ranking applications, evaluating candidates.",
    a4b: "Decisions about people at work", a4bH: "Pay, promotion, termination, assigning tasks, monitoring or evaluating performance.",
    aNone: "Neither", aNoneH: "Answering questions, translating, suggesting courses, and similar.",
    qProf: "Does it score, rank or build a profile of individual people?", qProfH: "If it does, it is high-risk whatever else is true.",
    qCond: "Which describes its job best?", cNone: "None of these", cNoneH: "It does more than that.",
    qInt: "Does it chat or write to people directly?", qIntH: "A chatbot, an assistant that emails candidates.",
    qDec: "Does it make or help make decisions about specific people?", qDecH: "Even if a person signs them off.",
    qAuto: "Does it act without a person checking each result?", qAutoH: "For example, it publishes a rota or sends ads on its own.",
    qMon: "Does it monitor how workers work?", qMonH: "Time, activity, keystrokes, productivity scores.",
    qInp: "Do you choose or prepare the data it uses?", qInpH: "Your own records, the settings you pick.",
    eFile: "The file {f} could not be read: {e}", eNome: "Give the system a name.", eRighe: "Row {r}: «{v}» in column {c} is not a value the tool understands.",
    eNomi: "The file needs a column with the system's name.", caricati: "{n} systems loaded from {f}.",
    x_registro: "Register", x_obblighi: "Obligations", x_avvisi: "Telling workers", x_info: "About",
    xRisposte: "Answers", xFonte: "Source", xData: "Date", xNota: "Not legal advice. Rules as read on {d}.",
    hRegola: "Rule", hPaese: "Country", hCosa: "What it asks", hQuando: "When",
  },
  it: {
    brand: "Kit AI Act per l'HR", eyebrow: "AI Act dell'UE · Regolamento (UE) 2024/1689, modificato nel 2026",
    title: "Quali sistemi di AI dell'HR sono ad alto rischio?",
    lead: "Rispondi a poche domande semplici per ogni sistema di AI, oppure carica un elenco. Ottieni la classe, cosa deve fare l'azienda e da quando, e chi informare in ogni paese.",
    privacy: "Le risposte restano su questo computer: tutto gira in questa pagina e niente viene inviato altrove.",
    step1: "I sistemi di AI", step1sub: "Aggiungili uno alla volta con le domande, oppure carica un elenco che hai già.",
    aggiungi: "Aggiungi un sistema", carica: "Carica un elenco (Excel o CSV)", esempio: "Prova con l'esempio: 12 sistemi", modello: "Modello dell'elenco",
    wizard: "Questo sistema", wizardEdit: "Modifica «{n}»", qNome: "Come si chiama?", qNomePh: "Per esempio: selezione dei CV nel software di recruiting",
    salva: "Salva il sistema", annulla: "Annulla", modifica: "Modifica", rimuovi: "Rimuovi", svuota: "Rimuovi tutti",
    hSistema: "Sistema", hClasse: "Classe", hRuolo: "Il tuo ruolo", hPerche: "Perché", hLavoratori: "Lavoratori coinvolti",
    hObbligo: "Obbligo", hArticolo: "Articolo", hDa: "Dal", hStato: "Stato", hQuali: "Sistemi",
    inVigore: "In vigore", daVenire: "In arrivo", nessuno: "nessuno",
    vuoto: "Ancora nessun sistema. Aggiungine uno, carica un elenco o prova l'esempio.",
    registro: "Il registro", registroSub: "La classe di ogni sistema secondo l'AI Act, e perché.",
    obblighi: "Cosa si applica, e da quando", obblighiSub: "Gli obblighi per i sistemi ad alto rischio partono il 2 dicembre 2027, o alla prossima modifica significativa del design per un sistema già sul mercato (art. 111(2)); il divieto e la formazione si applicano già.",
    avvisi: "Chi informare, paese per paese", avvisiSub: "Le regole nazionali per informare lavoratori e rappresentanti. Valgono già oggi, qualunque sia il calendario dell'AI Act.",
    nessunPaese: "Nessun sistema è usato in Italia, Germania, Spagna o Polonia, i quattro paesi che lo strumento conosce.", nessunaRegola: "Nessuna regola si applica a questi sistemi.",
    kSistemi: "Sistemi di AI", kVietati: "Da fermare subito", kAlto: "Ad alto rischio", kGiorni: "Giorni al 2 dicembre 2027",
    scarica: "Scarica in Excel", stampa: "Stampa", stampaTitolo: "Verifica AI Act", stampaMeta: "{n} sistemi · {oggi}",
    footer: "Le stesse regole del registro in Python e del modello Excel del kit, confrontati a ogni modifica. Non è consulenza legale.",
    rapporto: "Rapporto", metodo: "Metodo", pacchetto: "Pacchetto informative", codice: "Codice",
    na: "Considerati e non applicabili: {x}.", fornitore: "Fornitore e utilizzatore", utilizzatore: "Utilizzatore",
    cProhibited: "Vietato", cHigh: "Alto rischio", cDerog: "Non alto rischio (art. 6(3))", cTransp: "Solo trasparenza", cMinimal: "Rischio minimo",
    pIntro: "Con le risposte date finora:",
    wProhibited: "Riconosce le emozioni sul lavoro, e non per motivi medici o di sicurezza: vietato dal 2 febbraio 2025 (art. 5(1)(f)). Va fermato.",
    wHighProfile: "Usato per {area}, e valuta o profila le persone: alto rischio qualunque sia il suo compito (art. 6(3), ultimo comma).",
    wHigh: "Usato per {area}, e nessuna delle condizioni dell'art. 6(3) si applica: alto rischio.",
    wDerog: "Usato per {area}, ma si limita a {cond} e non profila nessuno: non è ad alto rischio per l'art. 6(3). Lo documenta il fornitore; tienine una copia.",
    wTransp: "Non è nell'allegato III, ma parla con le persone, che devono sapere che è un'AI (art. 50(1)).",
    wMinimal: "Non è nell'allegato III e non parla con le persone: l'unico obbligo è la formazione di chi lo usa (art. 4).",
    wProvider: "L'avete messo in servizio per uso vostro, quindi siete anche il fornitore (art. 3(3) e 16): valgono anche gli obblighi del fornitore.",
    wLegacy: "Era già sul mercato prima del 2 dicembre 2027, quindi gli obblighi da alto rischio scattano alla prossima modifica significativa del suo design (art. 111(2)); un software in cloud che cambia spesso va pianificato per dicembre 2027.",
    wNew: "Gli obblighi da alto rischio si applicano dal 2 dicembre 2027.",
    qMercato: "Il sistema era già sul mercato o in uso prima del 2 dicembre 2027?", qMercatoH: "Lo stesso tipo e modello, presso qualunque cliente: per un sistema che usate oggi la risposta è sì.",
    area4a: "la selezione del personale", area4b: "decisioni sulle persone al lavoro",
    cond_a: "svolgere un compito procedurale limitato", cond_b: "migliorare il risultato di un lavoro già fatto da una persona",
    cond_c: "segnalare scostamenti da decisioni precedenti senza sostituire la revisione di una persona", cond_d: "preparare una valutazione che fa una persona",
    sì: "Sì", no: "No",
    qSupplier: "Chi l'ha realizzato?", supplierV: "Un fornitore", supplierI: "L'abbiamo costruito noi",
    qPaesi: "Dove si usa?", qSu: "Su chi si usa?", suCand: "Solo sui candidati", suDip: "Sui dipendenti (anche sui candidati)",
    qScope: "Quale reparto?", tutti: "Tutti i reparti",
    qEmo: "Riconosce le emozioni dal volto, dalla voce o dalle parole delle persone?", qEmoH: "Per esempio da un colloquio video o dalla registrazione di una chiamata.",
    qMed: "Lo fa solo per motivi medici o di sicurezza?", qMedH: "Per esempio per rilevare la stanchezza di chi guida.",
    qArea: "A cosa serve?", a4a: "Selezione del personale", a4aH: "Annunci mirati, screening o classifica delle candidature, valutazione dei candidati.",
    a4b: "Decisioni sulle persone al lavoro", a4bH: "Retribuzione, promozioni, licenziamenti, assegnazione dei compiti, monitoraggio o valutazione delle prestazioni.",
    aNone: "Nessuna delle due", aNoneH: "Rispondere a domande, tradurre, suggerire corsi e simili.",
    qProf: "Assegna punteggi, fa classifiche o costruisce un profilo delle singole persone?", qProfH: "Se sì, è ad alto rischio comunque.",
    qCond: "Quale descrive meglio il suo compito?", cNone: "Nessuna di queste", cNoneH: "Fa di più.",
    qInt: "Scrive o parla direttamente con le persone?", qIntH: "Un chatbot, un assistente che scrive ai candidati.",
    qDec: "Prende o aiuta a prendere decisioni su persone precise?", qDecH: "Anche se poi firma una persona.",
    qAuto: "Agisce senza che una persona controlli ogni risultato?", qAutoH: "Per esempio pubblica i turni o invia gli annunci da solo.",
    qMon: "Controlla come lavorano le persone?", qMonH: "Tempi, attività, tasti premuti, punteggi di produttività.",
    qInp: "Siete voi a scegliere o preparare i dati che usa?", qInpH: "I vostri archivi, le impostazioni che scegliete.",
    eFile: "Non riesco a leggere il file {f}: {e}", eNome: "Dai un nome al sistema.", eRighe: "Riga {r}: «{v}» nella colonna {c} non è un valore che lo strumento capisce.",
    eNomi: "Il file deve avere una colonna con il nome del sistema.", caricati: "{n} sistemi caricati da {f}.",
    x_registro: "Registro", x_obblighi: "Obblighi", x_avvisi: "Informare i lavoratori", x_info: "Informazioni",
    xRisposte: "Risposte", xFonte: "Fonte", xData: "Data", xNota: "Non è consulenza legale. Regole lette il {d}.",
    hRegola: "Regola", hPaese: "Paese", hCosa: "Cosa chiede", hQuando: "Quando",
  },
};

// The obligations and national rules in Italian; the English text comes from inputs.json.
const IT_OBBLIGHI = {
  O01: "Formazione sull'AI di chi lo usa", O02: "Fermare l'uso vietato", O03: "Dire alle persone che parlano con un'AI: obbligo del fornitore, verificato dall'azienda",
  O04: "Uso secondo le istruzioni, con una persona che sorveglia", O05: "Dati in ingresso pertinenti e rappresentativi",
  O06: "Monitorare; segnalare rischi e incidenti gravi; sospendere", O07: "Conservare i log per almeno sei mesi",
  O08: "Informare rappresentanti e lavoratori prima dell'uso", O09: "Valutazione d'impatto sulla protezione dei dati, con le informazioni del fornitore",
  O10: "Informare le persone su cui si decide", O11: "Spiegare una decisione su richiesta", O12: "Obblighi del fornitore per un sistema costruito in casa",
  O13: "Valutazione di non alto rischio documentata",
};
const IT_REGOLE = {
  "W-IT1": ["Informativa sui sistemi decisionali o di monitoraggio integralmente automatizzati", "Per iscritto, a ogni lavoratore e alle RSA/RSU: aspetti del rapporto interessati, scopi, logica e funzionamento, dati e parametri principali, misure di controllo e correzione, accuratezza, robustezza e cybersicurezza, eventuali effetti discriminatori; in formato strutturato e leggibile da dispositivo automatico", "Prima dell'inizio del lavoro; almeno 24 ore prima di ogni modifica di quelle informazioni"],
  "W-IT2": ["Accordo o autorizzazione per strumenti che consentono il controllo a distanza", "Solo per esigenze organizzative e produttive, sicurezza del lavoro o tutela del patrimonio, con accordo delle rappresentanze sindacali o, in mancanza, autorizzazione dell'Ispettorato; esclusi gli strumenti per rendere la prestazione e quelli di registrazione delle presenze; dati utilizzabili solo con adeguata informazione ai lavoratori", "Prima dell'installazione"],
  "W-DE1": ["Informazione e consultazione sull'uso dell'AI nei processi di lavoro", "Informare il consiglio d'azienda con i documenti e consultarlo quando il suo parere può ancora cambiare il piano", "In fase di progettazione"],
  "W-DE2": ["Codecisione sugli strumenti tecnici che possono controllare comportamento o prestazioni", "Un accordo aziendale; senza, il sistema non si può usare legittimamente. I tribunali leggono «possono» in senso ampio: anche i sistemi che registrano l'uso da parte di persone identificabili possono richiederlo", "Prima dell'introduzione"],
  "W-DE3": ["Codecisione sui criteri di selezione", "Il consenso del consiglio d'azienda ai criteri di selezione che il sistema applica", "Prima dell'uso per assunzioni, trasferimenti o licenziamenti"],
  "W-DE4": ["Un esperto per il consiglio d'azienda, considerato necessario per l'AI", "Un esperto concordato con l'azienda quanto a persona, oggetto e costo; per l'AI la necessità si presume", "Quando il consiglio valuta il sistema"],
  "W-ES1": ["Informazione sui parametri degli algoritmi che incidono sul lavoro", "Parametri, regole e istruzioni su cui si basa il sistema, al comitato d'impresa", "Con la periodicità prevista; prima dell'uso è la lettura prudente"],
  "W-PL1": ["Avviso di monitoraggio diverso dalla videosorveglianza", "Consentito solo se necessario per il pieno uso dell'orario e il corretto uso degli strumenti di lavoro; scopo, ambito e modalità nel regolamento aziendale", "Almeno due settimane prima dell'avvio; ai nuovi assunti per iscritto prima dell'inizio"],
};
const PAESI_IT = { IT: "Italia", PL: "Polonia", DE: "Germania", ES: "Spagna" };
const PAESI_EN = { IT: "Italy", PL: "Poland", DE: "Germany", ES: "Spain" };

const i18n = createI18n(UI, "en");
const t = i18n.t;
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const it = () => i18n.lang === "it";
const K = "strumenti.aiact.sistemi";
const store = {
  get() { try { return JSON.parse(localStorage.getItem(K)) ?? []; } catch { return []; } },
  set(v) { try { localStorage.setItem(K, JSON.stringify(v)); } catch { /* private mode: fine */ } },
};

const DEFAULT = { supplier: "Vendor", scope: "All", in_it: "No", in_pl: "No", in_de: "No", in_es: "No", applicants: "No",
  infers_emotions: "No", medical_or_safety: "No", annex_iii: "None", profiling: "No", art6_3_condition: "None",
  interacts: "No", decides_about_people: "No", fully_automated: "No", monitors_workers: "No", controls_input_data: "No",
  on_market_before: "Yes" };
// state: the systems (with any answer missing from an older save filled in), whether they are the sample, which
// comes with a headcount, and the one being edited
let sistemi = store.get().map((s) => ({ ...DEFAULT, ...s })), esempio = false, inModifica = null;
const YN = ["in_it", "in_pl", "in_de", "in_es", "applicants", "infers_emotions", "medical_or_safety", "profiling", "interacts",
  "decides_about_people", "fully_automated", "monitors_workers", "controls_input_data", "on_market_before"];

const nomeClasse = (c) => t({ [PROHIBITED]: "cProhibited", [HIGH_RISK]: "cHigh", [DEROGATION]: "cDerog", [TRANSPARENCY]: "cTransp", [MINIMAL]: "cMinimal" }[c]);
const pill = (c) => `<span class="s-pill ${c === PROHIBITED ? "is-high" : c === HIGH_RISK ? "is-medium" : "is-ok"}">${esc(nomeClasse(c))}</span>`;
const nomePaese = (c) => (it() ? PAESI_IT : PAESI_EN)[c] || c;
const data = (iso) => new Date(`${iso}T00:00:00`).toLocaleDateString(it() ? "it-IT" : "en-GB", { day: "numeric", month: "long", year: "numeric" });
const obbligo = (o) => (it() ? IT_OBBLIGHI[o.key] : o.name);
const regola = (r) => (it() ? IT_REGOLE[r.key] : [r.name, r.what, r.timing]);

function perche(s) {
  const cls = classify(s);
  const area = t(s.annex_iii === "4(a)" ? "area4a" : "area4b");
  let w = { [PROHIBITED]: t("wProhibited"), [TRANSPARENCY]: t("wTransp"), [MINIMAL]: t("wMinimal") }[cls];
  if (cls === HIGH_RISK) w = t(s.profiling === "Yes" ? "wHighProfile" : "wHigh", { area });
  if (cls === DEROGATION) w = t("wDerog", { area, cond: t(`cond_${s.art6_3_condition.replace(/[()]/g, "")}`) });
  if (s.supplier === "In-house" && cls === HIGH_RISK) w += ` ${t("wProvider")}`;
  if (cls === HIGH_RISK) w += ` ${t(s.on_market_before === "Yes" ? "wLegacy" : "wNew")}`;
  return w;
}

// ---- the list of systems ----------------------------------------------------------------------------------------
function disegnaLista() {
  $("lista-wrap").style.display = sistemi.length ? "block" : "none";
  $("lista").innerHTML = sistemi.length ? `<tr><th class="l">${esc(t("hSistema"))}</th><th class="l">${esc(t("hClasse"))}</th><th></th></tr>` +
    sistemi.map((s, i) => `<tr><td class="l"><b>${esc(s.system)}</b></td><td class="l">${pill(classify(s))}</td>
      <td><div class="row-actions"><button type="button" class="s-btn is-small" data-m="${i}">${esc(t("modifica"))}</button>
      <button type="button" class="s-btn is-small" data-r="${i}">${esc(t("rimuovi"))}</button></div></td></tr>`).join("") +
    `<tr><td class="l" colspan="3"><button type="button" class="s-btn is-small" id="svuota">${esc(t("svuota"))}</button></td></tr>` : "";
  $("lista").querySelectorAll("[data-m]").forEach((b) => b.addEventListener("click", () => apri(Number(b.dataset.m))));
  $("lista").querySelectorAll("[data-r]").forEach((b) => b.addEventListener("click", () => { sistemi.splice(Number(b.dataset.r), 1); salvaTutto(); }));
  $("svuota")?.addEventListener("click", () => { sistemi = []; esempio = false; salvaTutto(); });
}
function salvaTutto() { store.set(sistemi); disegnaLista(); mostra(); }

// ---- the questions -------------------------------------------------------------------------------------------------
const radio = (name, value, label, hint, checked) => `<label><input type="radio" name="${name}" value="${esc(value)}" ${checked ? "checked" : ""}>
  <span>${esc(label)}${hint ? `<small>${esc(hint)}</small>` : ""}</span></label>`;
const yesno = (name, q, h, s) => `<fieldset class="q" id="q-${name}"><legend>${esc(t(q))}</legend>${h ? `<p class="s-why">${esc(t(h))}</p>` : ""}
  <div class="opts row">${radio(name, "Yes", t("sì"), "", s[name] === "Yes")}${radio(name, "No", t("no"), "", s[name] !== "Yes")}</div></fieldset>`;

function domande(s) {
  const paesi = CFG.countries.map((c) => `<label><input type="checkbox" name="in_${c.toLowerCase()}" ${s[`in_${c.toLowerCase()}`] === "Yes" ? "checked" : ""}><span>${esc(nomePaese(c))}</span></label>`).join("");
  const reparti = [["All", t("tutti")], ...CFG.departments.map((d) => [d, d])]
    .map(([v, l]) => `<option value="${esc(v)}" ${s.scope === v ? "selected" : ""}>${esc(l)}</option>`).join("");
  const cond = ["(a)", "(b)", "(c)", "(d)"].map((c) => radio("art6_3_condition", c, t(`cond_${c[1]}`).replace(/^./, (x) => x.toUpperCase()), "", s.art6_3_condition === c)).join("")
    + radio("art6_3_condition", "None", t("cNone"), t("cNoneH"), s.art6_3_condition === "None");
  return `
    <fieldset class="q"><legend>${esc(t("qSupplier"))}</legend><div class="opts row">${radio("supplier", "Vendor", t("supplierV"), "", s.supplier !== "In-house")}${radio("supplier", "In-house", t("supplierI"), "", s.supplier === "In-house")}</div></fieldset>
    <fieldset class="q"><legend>${esc(t("qPaesi"))}</legend><div class="opts row">${paesi}</div></fieldset>
    <fieldset class="q"><legend>${esc(t("qSu"))}</legend><div class="opts">${radio("applicants", "Yes", t("suCand"), "", s.applicants === "Yes")}${radio("applicants", "No", t("suDip"), "", s.applicants !== "Yes")}</div></fieldset>
    <div class="q"><label class="lab" for="f-scope">${esc(t("qScope"))}</label><select class="s-select" id="f-scope" name="scope">${reparti}</select></div>
    ${yesno("infers_emotions", "qEmo", "qEmoH", s)}
    ${yesno("medical_or_safety", "qMed", "qMedH", s)}
    <fieldset class="q" id="q-annex_iii"><legend>${esc(t("qArea"))}</legend><div class="opts">
      ${radio("annex_iii", "4(a)", t("a4a"), t("a4aH"), s.annex_iii === "4(a)")}${radio("annex_iii", "4(b)", t("a4b"), t("a4bH"), s.annex_iii === "4(b)")}${radio("annex_iii", "None", t("aNone"), t("aNoneH"), s.annex_iii === "None")}</div></fieldset>
    ${yesno("profiling", "qProf", "qProfH", s)}
    <fieldset class="q" id="q-art6_3_condition"><legend>${esc(t("qCond"))}</legend><div class="opts">${cond}</div></fieldset>
    ${yesno("interacts", "qInt", "qIntH", s)}
    ${yesno("decides_about_people", "qDec", "qDecH", s)}
    ${yesno("fully_automated", "qAuto", "qAutoH", s)}
    ${yesno("monitors_workers", "qMon", "qMonH", s)}
    ${yesno("controls_input_data", "qInp", "qInpH", s)}
    ${yesno("on_market_before", "qMercato", "qMercatoH", s)}`;
}

function leggiForm() {
  const f = $("form"), s = { ...DEFAULT, system: $("f-name").value.trim() };
  for (const k of ["supplier", "applicants", "annex_iii", "art6_3_condition", ...YN.filter((k) => !k.startsWith("in_"))]) {
    const v = f.querySelector(`input[name="${k}"]:checked`)?.value;
    if (v) s[k] = v;
  }
  for (const c of CFG.countries) s[`in_${c.toLowerCase()}`] = f.querySelector(`input[name="in_${c.toLowerCase()}"]`).checked ? "Yes" : "No";
  s.scope = $("f-scope").value;
  // answers that only matter after an earlier one are reset when they no longer apply, as the questions hide them
  if (s.infers_emotions !== "Yes") s.medical_or_safety = "No";
  if (s.annex_iii === "None") { s.profiling = "No"; s.art6_3_condition = "None"; }
  if (s.profiling === "Yes") s.art6_3_condition = "None";
  return s;
}

function aggiornaForm() {
  const s = leggiForm();
  $("q-medical_or_safety").style.display = s.infers_emotions === "Yes" ? "block" : "none";
  $("q-profiling").style.display = s.annex_iii !== "None" ? "block" : "none";
  $("q-art6_3_condition").style.display = s.annex_iii !== "None" && s.profiling !== "Yes" ? "block" : "none";
  const cls = classify(s);
  $("verdetto").innerHTML = `${esc(t("pIntro"))} ${pill(cls)}`;
  $("perche").textContent = perche(s);
}

function apri(i = null) {
  inModifica = i;
  const s = i === null ? { ...DEFAULT, system: "" } : sistemi[i];
  $("wizard").style.display = "block";
  $("wizard-title").textContent = i === null ? t("wizard") : t("wizardEdit", { n: s.system });
  $("f-name").value = s.system;
  $("domande").innerHTML = domande(s);
  $("form").querySelectorAll("input, select").forEach((el) => el.addEventListener("change", aggiornaForm));
  aggiornaForm();
  $("wizard").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  $("f-name").focus({ preventScroll: true });
}
function chiudi() { $("wizard").style.display = "none"; inModifica = null; }

$("aggiungi").addEventListener("click", () => apri());
$("annulla").addEventListener("click", chiudi);
$("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const s = leggiForm();
  if (!s.system) { messaggio(t("eNome")); $("f-name").focus(); return; }
  messaggio("");
  if (inModifica === null) sistemi.push({ system_id: `U${Date.now()}`, ...s });
  else sistemi[inModifica] = { ...sistemi[inModifica], ...s };
  esempio = esempio && inModifica !== null;
  chiudi();
  salvaTutto();
});

function messaggio(text, kind = "error") {
  const m = $("errore");
  m.textContent = text;
  m.className = `s-msg is-${kind}${text ? " is-shown" : ""}`;
}

// ---- files ---------------------------------------------------------------------------------------------------------
const CAMPI = [
  ["system", true, ["ai system", "system", "name", "sistema", "nome", "nome del sistema", "tool", "strumento"]],
  ["supplier", false, ["fornitore", "vendor or in-house", "made by"]],
  ["scope", false, ["department", "reparto", "department in scope"]],
  ...CFG.countries.map((c) => [`in_${c.toLowerCase()}`, false, [`used in ${c.toLowerCase()}`, `usato in ${c.toLowerCase()}`, c.toLowerCase()]]),
  ["applicants", false, ["used on applicants", "candidati", "solo candidati"]],
  ["infers_emotions", false, ["infers emotions", "emozioni", "emotion recognition"]],
  ["medical_or_safety", false, ["for medical or safety reasons", "motivi medici o di sicurezza"]],
  ["annex_iii", false, ["annex iii", "annex iii point 4", "allegato iii"]],
  ["profiling", false, ["profiles people", "profilazione"]],
  ["art6_3_condition", false, ["art. 6(3) condition", "article 6(3)", "condizione art. 6(3)"]],
  ["interacts", false, ["talks to people", "chatbot", "interagisce"]],
  ["decides_about_people", false, ["decides or helps decide about people", "decisioni sulle persone"]],
  ["fully_automated", false, ["fully automated", "integralmente automatizzato"]],
  ["monitors_workers", false, ["monitors workers", "monitoraggio"]],
  ["controls_input_data", false, ["employer controls the input data", "dati in ingresso"]],
  ["on_market_before", false, ["type and model on the market before 2 dec 2027", "on the market before", "gia sul mercato"]],
].map(([key, required, aliases]) => ({ key, required, aliases }));

$("file-lista").addEventListener("change", async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  try {
    const table = await readTable(f);
    const { mapping, missing } = matchColumns(table.headers, CAMPI);
    if (missing.length) throw new Error(t("eNomi"));
    const errori = [];
    const letti = applyMapping(table.rows, mapping).map((r, i) => {
      const s = { ...DEFAULT, system_id: `F${i + 1}`, system: String(r.system ?? "").trim() };
      for (const [k, v] of Object.entries(r)) {
        if (k === "system") continue;
        let x = v;
        if (YN.includes(k)) x = yesNo(v);
        else if (k === "annex_iii") x = annex(v);
        else if (k === "art6_3_condition") x = condition63(v);
        else if (k === "supplier") x = /house|interno|nostro|own/.test(normalise(v)) ? "In-house" : "Vendor";
        else if (k === "scope") x = CFG.departments.find((d) => normalise(d) === normalise(v)) || "All";
        if (x === null) errori.push(t("eRighe", { r: i + 2, v, c: mapping[k] }));
        else s[k] = x;
      }
      return s;
    }).filter((s) => s.system);
    if (errori.length) throw new Error(errori.slice(0, 5).join(" "));
    sistemi = letti;
    esempio = false;
    salvaTutto();
    messaggio(t("caricati", { n: letti.length, f: f.name }), "info");
  } catch (err) {
    messaggio(t("eFile", { f: f.name, e: err.message }));
  } finally { e.target.value = ""; }
});

$("esempio").addEventListener("click", async () => {
  try {
    const text = await fetch("ai_systems.csv").then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); });
    sistemi = parseCsv(text).rows.map((r) => ({ ...DEFAULT, ...r }));
    esempio = true;
    messaggio("");
    salvaTutto();
  } catch (e) { messaggio(t("eFile", { f: "sample", e: e.message })); }
});

// ---- results -------------------------------------------------------------------------------------------------------
function risultati() {
  const hc = esempio ? CFG.headcount : null;
  return sistemi.map((s) => ({ s, r: assess(s, CFG, hc) }));
}

function mostra() {
  const out = risultati();
  $("risultati").style.display = out.length ? "block" : "none";
  if (!out.length) return;
  const giorni = daysBetween(CFG.assessment, CFG.dates.annex_iii);
  const oggi = new Date().toISOString().slice(0, 10);
  const daOggi = Math.max(0, daysBetween(oggi, CFG.dates.annex_iii));
  const n = (c) => out.filter((x) => x.r.class === c).length;
  $("kpis").innerHTML = [[t("kSistemi"), out.length, ""], [t("kVietati"), n(PROHIBITED), n(PROHIBITED) ? "is-bad" : "is-good"],
    [t("kAlto"), n(HIGH_RISK), ""], [t("kGiorni"), (oggi > CFG.assessment ? daOggi : giorni).toLocaleString(it() ? "it-IT" : "en-GB"), ""]]
    .map(([k, v, c]) => `<div class="s-kpi ${c}"><div class="k">${esc(k)}</div><div class="v">${esc(v)}</div></div>`).join("");
  $("stampa-meta").textContent = t("stampaMeta", { n: out.length, oggi: data(oggi) });

  const conLavoratori = out.some((x) => x.r.workers !== null);
  $("tab-registro").innerHTML = `<tr><th class="l">${esc(t("hSistema"))}</th><th class="l">${esc(t("hClasse"))}</th><th class="l">${esc(t("hRuolo"))}</th>
    ${conLavoratori ? `<th>${esc(t("hLavoratori"))}</th>` : ""}<th class="l">${esc(t("hPerche"))}</th></tr>` +
    out.map(({ s, r }) => `<tr><td class="l"><b>${esc(s.system)}</b></td><td class="l">${pill(r.class)}</td>
      <td class="l">${esc(r.role === "Deployer" ? t("utilizzatore") : t("fornitore"))}</td>
      ${conLavoratori ? `<td>${r.workers.toLocaleString(it() ? "it-IT" : "en-GB")}</td>` : ""}<td class="l">${esc(perche(s))}</td></tr>`).join("");

  const ordine = [...CFG.obligations].sort((a, b) => a.from.localeCompare(b.from) || a.key.localeCompare(b.key));
  $("tab-obblighi").innerHTML = `<tr><th class="l">${esc(t("hObbligo"))}</th><th class="l">${esc(t("hArticolo"))}</th><th>${esc(t("hDa"))}</th>
    <th class="l">${esc(t("hStato"))}</th><th class="l">${esc(t("hQuali"))}</th></tr>` +
    ordine.map((o) => {
      const quali = out.filter((x) => x.r.obligations.includes(o.key)).map((x) => x.s.system);
      const vigore = o.from <= oggi;
      return `<tr><td class="l"><b>${esc(obbligo(o))}</b></td><td class="l">${esc(o.article)}</td><td>${esc(data(o.from))}</td>
        <td class="l"><span class="s-pill ${vigore ? "is-high" : "is-ok"}">${esc(t(vigore ? "inVigore" : "daVenire"))}</span></td>
        <td class="l">${quali.length ? esc(quali.join(", ")) : `<span class="note">${esc(t("nessuno"))}</span>`}</td></tr>`;
    }).join("");
  $("nota-na").textContent = t("na", { x: CFG.not_applicable.map((x) => `${x.name} (${x.article})`).join("; ") });

  const usati = CFG.countries.filter((c) => out.some((x) => x.s[`in_${c.toLowerCase()}`] === "Yes"));
  $("paesi").innerHTML = usati.length ? usati.map((c) => {
    const regole = CFG.worker_rules.filter((r) => r.country === c).map((r) => {
      const quali = out.filter((x) => x.r.rules.includes(r.key)).map((x) => x.s.system);
      const [nome, cosa, quando] = regola(r);
      return quali.length ? `<li><b>${esc(nome)}</b> <span>(${esc(r.source)})</span><br>${esc(quali.join(", "))}.<br><span>${esc(cosa)} · ${esc(quando)}</span></li>` : "";
    }).join("");
    return `<div class="country"><h3>${esc(nomePaese(c))}</h3>${regole ? `<ul>${regole}</ul>` : `<p class="note">${esc(t("nessunaRegola"))}</p>`}</div>`;
  }).join("") : `<p class="note">${esc(t("nessunPaese"))}</p>`;
}

$("stampa").addEventListener("click", () => print());
$("scarica").addEventListener("click", () => {
  const out = risultati();
  const oggi = new Date().toISOString().slice(0, 10);
  const yn = (v) => (v === "Yes" ? t("sì") : t("no"));
  const registro = [[t("hSistema"), t("hClasse"), t("hRuolo"), t("hPerche"), t("qSupplier"), ...CFG.countries.map(nomePaese), t("qSu"), t("qScope"),
    t("qEmo"), t("qMed"), t("qArea"), t("qProf"), t("qCond"), t("qInt"), t("qDec"), t("qAuto"), t("qMon"), t("qInp"), t("qMercato")],
  ...out.map(({ s, r }) => [s.system, nomeClasse(r.class), r.role === "Deployer" ? t("utilizzatore") : t("fornitore"), perche(s),
    s.supplier === "In-house" ? t("supplierI") : t("supplierV"), ...CFG.countries.map((c) => yn(s[`in_${c.toLowerCase()}`])),
    s.applicants === "Yes" ? t("suCand") : t("suDip"), s.scope === "All" ? t("tutti") : s.scope, yn(s.infers_emotions), yn(s.medical_or_safety),
    s.annex_iii, yn(s.profiling), s.art6_3_condition, yn(s.interacts), yn(s.decides_about_people), yn(s.fully_automated),
    yn(s.monitors_workers), yn(s.controls_input_data), yn(s.on_market_before)])];
  const obblighi = [[t("hObbligo"), t("hArticolo"), t("hDa"), t("hStato"), t("hQuali")],
    ...CFG.obligations.map((o) => [obbligo(o), o.article, o.from, t(o.from <= oggi ? "inVigore" : "daVenire"),
      out.filter((x) => x.r.obligations.includes(o.key)).map((x) => x.s.system).join(", ")])];
  const avvisi = [[t("hPaese"), t("hRegola"), t("xFonte"), t("hQuali"), t("hCosa"), t("hQuando")],
    ...CFG.worker_rules.map((r) => { const [nome, cosa, quando] = regola(r);
      return [nomePaese(r.country), nome, r.source, out.filter((x) => x.r.rules.includes(r.key)).map((x) => x.s.system).join(", "), cosa, quando]; })];
  const info = [[t("x_info"), ""], [t("xData"), oggi], [t("xNota", { d: data(CFG.assessment) }), ""],
    [t("metodo"), "https://github.com/D0M3N1C0X/ai-act-hr-readiness-kit/blob/main/docs/method.md"]];
  download(writeXlsx([
    { name: t("x_registro"), rows: registro, widths: [34, 22, 20, 70, 18, 10, 10, 10, 10, 22, 18, 14, 14, 14, 14, 16, 14, 14, 14, 14, 14] },
    { name: t("x_obblighi"), rows: obblighi, widths: [60, 22, 14, 12, 80] },
    { name: t("x_avvisi"), rows: avvisi, widths: [12, 60, 40, 60, 70, 40] },
    { name: t("x_info"), rows: info, widths: [60, 80] },
  ]), `${it() ? "verifica_ai_act" : "ai_act_check"}_${oggi}.xlsx`, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
});

i18n.apply();
i18n.onChange(() => { disegnaLista(); mostra(); if (inModifica !== null || $("wizard").style.display === "block") apri(inModifica); });
disegnaLista();
mostra();
