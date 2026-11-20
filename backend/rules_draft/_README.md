# Draft rules (Role 1)

Drafts written by Role 1 so the engine produces findings before Role 2's rules arrive.
**All are `verified: false`.** Role 2 owns the authoritative versions in `/rules/<ID>.yaml` — a rule with the same `id` there overrides the draft.

Quotes of art. 27¹ were checked on 20.11: Uzbek text via lex-rag (edition 2026-09-12), Russian is lex.uz's unofficial translation. Everything else (choice of article, level, sanction) is NOT VERIFIED.

## Fields added on 21.11 (Role 1) — keep them when you write `/rules/<ID>.yaml`

A rule in `/rules` now **merges field by field** with the draft (`rules_engine._merge_rule`): your fields win, fields you
leave out are taken from the draft. So you can override only `level`, `legal_basis` quotes or `verified`.

| Field | Where | What it does |
|---|---|---|
| `legal_basis[].articles` | e.g. `["18", "21"]`, `["5:5"]` (article 5, part 5) | Article numbers for verbatim citations from lex.uz via lex-rag (`python -m qalqon.legal.citations` → `backend/data/law_quotes.json`). Shown in every finding, marked "not verified by a lawyer" |
| `legal_basis[].act_id` | `ZRU-547` (default), `ECOM`, `CONSUMER` | Which act the article numbers belong to (`qalqon/legal/citations.py` `ACTS`) |
| `legal_basis[].act_ru` | text | Russian name of the act for the Russian UI |
| `sanction_uz`, `sanction_ru`, `sanction_source` | text | "Possible consequences" line in the report (R-02 templates T1–T3, `research/legal-liability.md`). Leave out to show nothing |

Changes from R-01 / R-02 on 21.11: PD-CNS-01 is 🟡 (art. 18, model procedure item 9); article map per
`research/legal-norms.md` §1; sanctions per `research/legal-liability.md` (no fine shown for PD-TRK-01 until V-08,
none for policy, security and e-commerce rules).
