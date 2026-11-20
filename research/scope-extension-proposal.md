# Scope extension: lex.uz legal engine + product check for software builders

- Author: [name], research team; prepared with Claude Code
- Date/time: 20.11, night
- Based on passport version: 0.1 (the repo is now at 0.4, see the box below)
- Confidence: medium for feasibility and design; every legal claim below is NOT VERIFIED until Role 2 checks it on lex.uz
- Status: proposal. It widens decision D-002, so it needs team agreement and a new decision-log entry

> **Read first: conflicts with passport v0.4**
> 1. **The legal engine already exists.** Conclusion 2 and P-F3 are covered by lex-rag: 55,000 lex.uz acts, hybrid search and code-checked quotes, called as an external service (D-013). Rules decide violations; RAG only quotes and explains (D-010). lex.uz changes are tracked through its RSS feed and article hashes (D-011). **What stays new in this file: the product check for builders (P-F4) and the combined report (P-F5).**
> 2. **Active security checks (P-F7) contradict D-008:** the team doesn't search for vulnerabilities or do pentests. Withdrawn unless the team changes D-008. The passive check for secrets in page JavaScript (part of P-F6) is close to vulnerability scanning, so it is a question for the team under D-008. Personal data in URLs is already covered by PD-LEAK-01.
> 3. **Canary form tests** run only on clients' sites with written consent (D-009).
> 4. **Localization changed in 2026** (ЗРУ-1125, ПКМ № 415, passport §2). Any example below that assumes "all data must stay in Uzbekistan" is outdated.
> 5. **lex.uz terms of use** (V-17) may limit storing and reusing the corpus commercially.
> 6. **IDs renamed to avoid clashes:** F-13…F-17 became P-F3…P-F7, and the suggested decision D-013 became P-D6, because those IDs are already taken in the passport. Role 1 assigns real IDs to anything accepted.

## Conclusions

1. **Keep the website scanner as the core.** "Check every action of any app against all of Uzbek law" can't be built reliably before the checkpoint. A version that tries becomes a legal chatbot that makes things up, which is what D-002 ruled out.
2. **Turn the lex.uz scrape into a legal engine** that every part of the product uses: citations in scan findings, candidate articles for Role 2's rule files, and "law changed" alerts later.
3. **Add a structured product check for builders**: a fixed questionnaire, not a chat. Answers map to a list of regulated activities owned by Role 2. For each activity the output gives the exact norm, what to change and questions for a lawyer.
4. **Combine it with the scan**: the product compares what the law requires (lex.uz), what the product says it does (policy + questionnaire) and what it actually does (scan).
5. **Security checks**: passive checks for any URL; active checks only after the owner proves they own the site.

## Data

### Why the full scope doesn't fit
- The scanner MVP alone is a full ~18-hour plan for one developer (see `architecture-proposal.md` §16).
- The legal engine adds about 3–4 hours if the scrape is clean: one record per article with document ID, edition date and language.
- The product check adds about 4 more hours.
- A black-box scan can't see server-side business logic (for example, how payouts are routed), so judging "every action" needs input from the builder, not just a scan.

### IP or domain for server location
- **IP.** A domain says nothing about where the server is: a .uz domain can be hosted abroad and a .com in Uzbekistan.
- The design takes the IP address the browser actually connected to, looks up its country and network owner (ASN), and records the company behind known services and that company's country.
- Limits stated in every report: behind a CDN the country is "undetermined", and nobody outside can see where the backend or database sends data next.

### lex.uz as the only source of law
Matches D-006. Three caveats:
- **Current edition only.** Store each document with its ID, edition date and article number. Old editions must not drive findings.
- **Split by article (modda), not by page.** Citations, the verbatim quote check and change alerts all work at article level.
- **Enforcement isn't on lex.uz.** Actual fines and regulator explanations stay with Role 2.

### Language and AI cost
- **Don't translate the corpus.** The cost difference is small because the whole lex.uz never goes to the model: search picks about 10–30 relevant articles per check (roughly 10–40 thousand tokens).
- Uzbek and Russian use more tokens than English for the same meaning. The exact ratio should be measured on 10 real articles with Anthropic's token-counting endpoint (NOT VERIFIED yet). Even at twice as many tokens, a check goes from about $0.04 to $0.08 on Sonnet 5.5 and stays under $0.01 on Haiku 5.5, at Anthropic's published prices.
- Translation is the real cost: legal terms get mistranslated, quotes stop being verbatim (D-006 and the quote check depend on exact text), and every amendment means translating again.
- **Plan:** keep the original texts (Uzbek, plus Russian where lex.uz has it). A user asks in any language; Claude turns the question into Uzbek and Russian search terms; the answer comes in the interface language with the original quote and an "unofficial translation".

### What to add

| Add | Why | When |
|---|---|---|
| **Legal engine on the lex.uz scrape.** Article-level search index in SQLite (already in the stack, no new server). Every quote is checked against the stored text | Everything else uses it. Helps Role 2 right away with candidate articles and exact quotes for the 11 rules | Before the checkpoint, if the scrape is clean |
| **Product check for builders.** Questionnaire: what data you collect, who pays whom, where servers are, whether minors use it, ads, cross-border transfers. Answers map to regulated activities owned by Role 2. Per activity: does it apply, exact norm with link and edition date, what to change, questions for a lawyer | Covers cases like a gig platform that pays workers directly. Structure keeps it from becoming the chatbot D-002 rejected | Thin version at the checkpoint if time allows; full version for the final |
| **Combined report.** If the builder gives a URL, the scan fills half the questionnaire; the report shows law vs claims vs behavior | Strongest pitch line; extends the "policy vs behavior" check (PD-MIS-01) | Final |
| **Passive security checks on any URL:** secrets in the page's JavaScript (API keys, Telegram bot tokens — whoever has a bot token can take over the bot that receives leads); personal data in URLs sent to third parties; other people's personal data in API responses seen during normal browsing (keep only counts and masked samples); cookie security flags; permissive cross-origin settings | Covers "leaks and suspicious paths", using only what any visitor's browser already receives | After the checkpoint; 1–2 checks at most |
| **Active checks** (exposed `/.env`, `/.git`, backups, admin panels, API probing) only after the owner verifies the site with a DNS record or a file on the site | Probing someone else's server without permission may itself be illegal (NOT VERIFIED, see questions) | Roadmap |

### What to remove or limit
- **The promise to check "every action against all law"** → a fixed list of regulated activities Role 2 can verify. Start with personal data, payments and payouts, labor and gig work, consumer and e-commerce rules, advertising.
- **Verdicts.** Never "illegal"; keep "signs of violation" and "questions for your lawyer" (D-004).
- **Free-form chat over lex.uz.** Many teams will build one, and mentors will easily break it.
- **To make room before 14:00, cut first:** the policy-items check (PD-POL-02), HAR recording, the consent banner click, the world map (use a country table instead). Nothing from the scanner core.

## Feature ideas (passport §10 format)

| ID | Feature | What it gives | Complexity | Proposed by | Status |
|---|---|---|---|---|---|
| P-F3 | Legal engine on the lex.uz scrape (article index + verified quotes) | Citations in every finding; faster rule writing for Role 2; basis for "law changed" alerts | M | research team | Already covered by lex-rag (D-013) |
| P-F4 | Product check for builders (questionnaire → regulated activities → norms from lex-rag) | New audience: software builders before launch; strong T3 and S3 story | M | research team | Proposed for the final |
| P-F5 | Combined report: law vs claims vs behavior | The clearest pitch message | S (after P-F4) | research team | Proposed for the final |
| P-F6 | Passive security checks (secrets in JS, PII in API responses, cookie flags, CORS) | Covers data leaks without touching anything a visitor can't see | S–M | research team | Question for the team under D-008; PII in URLs is already PD-LEAK-01 |
| P-F7 | Active security checks for verified site owners | Deeper audit for paying clients | M | research team | Withdrawn: contradicts D-008 |

## Questions for the team / contradictions with the passport

1. **Widens D-002.** Suggested entry P-D6 (Role 1 assigns the real ID): "Qalqon = website scanner (core) + structured product check for builders on top of lex-rag. No free chat."
2. **Checkpoint scope.** Scanner + legal engine only, or the product check too? Not decided yet.
3. **Gig-platform example.** The claim that payments to workers must go through the government is NOT VERIFIED. Role 2 must find and check the norm on lex.uz before it appears in the demo or pitch. If it doesn't hold up, the demo uses the personal-data scenario.
4. **Licensing of automated legal advice.** Does giving automated legal guidance require a license? NOT VERIFIED (add to R-08).
5. **Legality of active security probing** of sites we don't own. NOT VERIFIED (add to R-08).
6. **The lex.uz corpus.** Partly answered in v0.4: it is lex-rag, called as an external service (D-013). Still open for the product check: can lex-rag's API search by regulated activity (for example "payouts to individuals"), and what do lex.uz's terms allow (V-17)?

## Sources

- `PASSPORT.md` v0.1: §5 (checks), §9.2 (tasks), §13 (mentor answers), §15 (decisions D-002, D-004, D-006)
- `research/architecture-proposal.md` — current architecture proposal
- lex.uz: https://lex.uz
- Anthropic pricing (cost estimates): https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic token counting (to measure the Uzbek/Russian token ratio): https://platform.claude.com/docs/en/build-with-claude/token-counting
