# Worker information pack

Who has to be told about an AI system used on workers, what the notice must contain, and when, in the four
countries of the register. Each section ends with a model text to adapt. The AI Act's own duty for high-risk systems
(Art. 26(7): inform workers' representatives and the affected workers before use) starts on 2 December 2027; the
national rules below apply now.

Which systems trigger which rule is computed in the register (`Workers` sheet of
[`ai_act_hr_register.xlsx`](../deliverables/ai_act_hr_register.xlsx)); the sources and how far each was checked are
in [verification.md](verification.md). Not legal advice: a labour lawyer in each country confirms the text before it
goes out.

## What every notice should say

Whatever the country, a notice that would satisfy all four regimes covers the same ground:

1. **Which system**, from which supplier, and since or from when.
2. **What it is for**: the decisions or tasks it supports, and which ones it does not touch.
3. **How it works**, in plain words: the data it uses, the parameters that weigh most, what it produces.
4. **Who decides**: the human role that reviews the output and can override it.
5. **Controls**: accuracy, the checks for discriminatory effects, how errors are corrected.
6. **Rights**: how to ask for an explanation, a correction or human review, and whom to ask.

## Italy

| | |
|---|---|
| **Rule** | D.lgs. 152/1997, art. 1-bis, as recalled by L. 132/2025, art. 11(2); Statuto dei lavoratori, art. 4 for tools that can monitor workers |
| **Applies to** | Decision or monitoring systems that are *integralmente automatizzati* (fully automated) and bear on hiring, management, termination, task assignment, or monitoring and evaluating workers |
| **Tell** | Each worker, in writing, and the company union representatives (RSA/RSU), or the regional offices of the most representative unions where there are none |
| **When** | Before work starts; for a system introduced later, at least 24 hours before |
| **Content** | Purposes, logic and functioning, categories of data and main parameters, control and correction measures, accuracy, robustness and cybersecurity levels, possible discriminatory effects of the metrics (art. 1-bis, co. 2); in a structured, machine-readable format (co. 6) |
| **Monitoring tools** | Art. 4: an agreement with the union representatives or, failing that, authorisation from the labour inspectorate, before installation |
| **Open point** | Whether "fully automated" still limits the duty now that L. 132/2025 extends it to the use of AI "in the cases and in the manner" of art. 1-bis. The register applies the narrow reading and flags it |

**Modello (italiano)**

> Oggetto: informativa sull'utilizzo di sistemi automatizzati (art. 1-bis D.lgs. 152/1997; art. 11 L. 132/2025)
>
> Dal [data] l'azienda utilizza [nome del sistema], fornito da [fornitore], per [finalità: es. comporre i turni del
> magazzino]. Il sistema elabora [categorie di dati: es. competenze certificate, disponibilità, presenze dei sei mesi
> precedenti] e propone [risultato]. I parametri che pesano di più sono [elenco]. Le proposte sono pubblicate
> automaticamente; [ruolo] può modificarle in ogni momento. Verifichiamo ogni [periodo] l'accuratezza del sistema e
> l'assenza di effetti discriminatori, con [misura]. Può chiedere spiegazioni, la correzione dei dati o la revisione di
> una decisione a [contatto]; risponderemo per iscritto entro 30 giorni. La presente informativa è inviata anche alle
> RSA/RSU.

## Germany

| | |
|---|---|
| **Rule** | Betriebsverfassungsgesetz (BetrVG) §90(1) Nr. 3 and §90(2); §87(1) Nr. 6; §95(1) and (2a); §80(3) |
| **Information and consultation** | Planning the use of AI in work procedures: inform the works council in good time, with the documents, and consult it while its proposals can still change the plan (§90) |
| **Co-determination** | Any technical device able to monitor conduct or performance needs the works council's agreement before introduction, usually a works agreement (§87(1) Nr. 6). Courts read "able to" broadly: a system that processes performance data qualifies |
| **Selection** | Guidelines for selection in hiring, transfers, regrading and dismissals need the works council's consent, also where AI is used to draw them up (§95(2a)) |
| **Expert** | Where the works council has to assess the introduction or use of AI, an expert is deemed necessary (§80(3)); the employer pays |
| **When** | At the planning stage; the system is not used before the agreement |

**Model (to translate into German)**

> Subject: Planned use of [system] – information under §90 BetrVG and request to agree under §87(1) Nr. 6 BetrVG
>
> We plan to introduce [system], supplied by [supplier], from [date] for [purpose] in [departments]. Enclosed: the
> supplier's description, the data it processes, the outputs and who sees them, the human review, the retention of logs,
> and the data protection impact assessment. We propose a works agreement covering purpose limitation, the data used,
> the exclusion of individual performance evaluation from [outputs], access rights, evaluation after six months and the
> works council's right to an expert under §80(3). We ask to discuss it at the meeting on [date].

## Spain

| | |
|---|---|
| **Rule** | Estatuto de los Trabajadores, art. 64.4.d |
| **Tell** | The works council (*comité de empresa*), or the staff delegates |
| **Applies to** | Algorithms or AI systems that affect decisions which may bear on working conditions, access to employment or keeping it, profiling included |
| **Content** | The parameters, rules and instructions the system is based on |
| **When** | With the periodicity that applies in each case: before use, and again when the system changes |

**Model (to translate into Spanish)**

> Subject: Information under art. 64.4.d of the Estatuto de los Trabajadores on [system]
>
> [System], supplied by [supplier], is used from [date] for [purpose]. It takes into account [parameters, in order of
> weight], applies the rules [rules: thresholds, exclusions] and follows these instructions [what the user is told to
> do with the output]. Decisions are taken by [role], who can depart from the output. The system builds a profile of
> [who], based on [data]. We will inform the committee again whenever the parameters, rules or instructions change.

## Poland

| | |
|---|---|
| **Rule** | Kodeks pracy, art. 22³ (monitoring other than video, such as of e-mail or work tools) |
| **Applies to** | Monitoring needed to organise work so that working time and work tools are used fully and properly |
| **Tell** | Each worker; purpose, scope and method in the workplace rules (collective agreement, work regulations or a notice) |
| **When** | At least two weeks before the monitoring starts; to new hires before they start work |
| **Also** | The Act of 3 July 2026 on artificial intelligence systems (Dz.U. 2026 poz. 1003) sets up the supervisory authority (KRiBSI); it adds no information duty for employers beyond the AI Act (secondary sources) |

**Model (to translate into Polish)**

> Subject: Notice of monitoring under art. 22³ of the Labour Code
>
> From [date, at least two weeks ahead] the company will use [system] to measure [metrics] of work done in [tool], in
> order to [purpose]. Monitoring covers [scope] and does not cover [exclusions, such as private messages]. The data are
> kept for [period] and seen by [roles]. The purpose, scope and method are set out in the work regulations, section
> [number].

## The AI Act duty from December 2027

From 2 December 2027, before a high-risk system is put into service or used at the workplace, the employer informs
workers' representatives and the affected workers that they will be subject to it, through the national procedures
above (Art. 26(7)), and tells the people a decision is made about that a high-risk system is being used (Art.
26(11)). A notice that follows the six points at the top of this page already covers both.
