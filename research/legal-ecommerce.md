# Norms for the e-commerce pilot (EC-01…EC-03)
- Author: Alii, Role 2 (legal research), prepared with Claude Code
- Date/time: 21.11.2026, 09:00
- Based on passport version: 0.14 (D-027; task 5 in `research/README-v2.md`)
- Method:
  - I found the articles in the local lex.uz corpus.
  - I read them on **live lex.uz on 21.11.2026**: the official Uzbek text (Cyrillic and lex.uz's Latin version) and the
    LexUZ Russian text. The acts are ZRU-792 «On electronic commerce», Law 221-I «On the protection of consumer rights»,
    the Law «On the state language» and the Administrative Code.
  - I also read the **future edition of ZRU-792** that lex.uz already publishes (in force 12.12.2026).
  - All quotes in `rules/EC-0*.yaml` were checked by script against the live text.
- Confidence: **high** for the texts and dates. **Medium** for the sanctions (which article an inspector would use).

## Conclusions

1. **All three pilot checks have a direct basis in law. All three stay 🟡 risk**, because the scanner sees only the
   pages it opened.
   - EC-01, seller identity: the offer must name the seller with postal and e-mail address and phone (ZRU-792 art. 16
     part 3); the seller must tell consumers its firm name, legal address and working hours (Law 221-I art. 5 part 2).
   - EC-02, offer and returns: the offer must state how the contract is concluded, the delivery and payment terms and
     the prices (art. 16 part 3); the seller must give full information on the trading rules (Law 221-I art. 5 part 4)
     and say where goods are returned (ZRU-792 art. 26 part 1).
   - EC-03, Uzbek version: e-commerce contract terms must be in the state language (ZRU-792 art. 21 part 1); seller and
     goods information must be in the state language (Law 221-I arts. 5 and 6). Other languages are allowed only in
     addition.
2. **The law changes on 12.12.2026 — a ready "law changed" demo (F-16).** ZRU-1173 of 10.09.2026 adds a new paragraph
   to art. 16 part 3: the offer must contain «порядок и условия возврата товаров (работ, услуг) и (или) возврата
   уплаченных денежных средств покупателю» ("the order and conditions of returning goods and/or the money").
   - Today an offer without return terms is a weaker finding, which is why the draft downgrades it.
   - From 12.12.2026 it is a direct requirement.
   - Proposal for Role 1: add a law version "2026-12-12" in `backend/data/law_versions.yaml` that raises the "offer
     without returns" case of EC-02.
   - ZRU-1173 also rewrites the definitions (art. 3), the platform operators' duties (arts. 12–13) and adds
     cross-border e-commerce (art. 10¹). That is not needed for the three checks.
3. **Sanctions are possible but not certain.**
   - Administrative Code art. 178 part 6 (not giving consumers information about goods; the seller's full name and
     address are part of that information under Law 221-I art. 6): **3–7 BCA** for citizens, **7–10 BCA** for officials.
   - Art. 164 part 1 (breach of the rules of trade): **10 / 20 BCA**.
   - Art. 42 (neglect of the state language): **1–2 BCA**.
   - The YAML files mark these as "possible, interpretation".
4. **Special regime.** Both ZRU-792 (art. 2 part 2) and the language law (art. 3 part 3) were amended by ZRU-1158
   (Tashkent International Financial Centre, in force 25.07.2026). A special legal regime may have its own rules. Same
   caveat as for ZRU-547 (R-10, F-32).

## Data

| Rule | Norm | Text (ru, LexUZ translation; uz in the YAML) | Edition |
|---|---|---|---|
| EC-01 | ZRU-792 art. 16 part 3, paras 2–3 | «наименование (фамилию, имя, отчество самозанятого лица) лица, направившего оферту; почтовый и электронный адрес, номер телефона лица, направившего оферту» | 25.07.2026 |
| EC-01 | Law 221-I art. 5 part 2 | «Продавец (исполнитель) обязан довести до сведения потребителя фирменное наименование своей организации, место ее нахождения (юридический адрес) и режим работы.» | 19.01.2026 |
| EC-02 | ZRU-792 art. 16 part 3 | «порядок заключения договора, а также порядок отправки и отзыва акцепта» … «условия поставки и оплаты товаров (работ, услуг), а также предлагаемые цены (тарифы) на них» | 25.07.2026 |
| EC-02 | ZRU-792 art. 26 part 1 | «При расторжении договора продавец должен сообщить покупателю о месте, где будет осуществлен возврат товара.» | 25.07.2026 |
| EC-02 | ZRU-792 art. 16 part 3, **new para 8** | «порядок и условия возврата товаров (работ, услуг) и (или) возврата уплаченных денежных средств покупателю» | **from 12.12.2026** (ZRU-1173) |
| EC-02 | Law 221-I art. 5 part 4 | «Продавец (исполнитель) обязан предоставить потребителю полную информацию о правилах торговли товарами, бытового и иных видах обслуживания.» | 19.01.2026 |
| EC-03 | ZRU-792 art. 21 part 1 | «Условия договора должны быть сформулированы в конкретной, понятной форме на государственном языке.» | 25.07.2026 |
| EC-03 | Law 221-I art. 5 part 5, art. 6 | «…предоставляется потребителю на государственном языке. Данная информация может быть также дополнительно предоставлена и на других языках.» | 19.01.2026 |
| EC-03 | Law «On the state language» art. 20 | «Тексты вывесок, объявлений, ценников и другой наглядной, а также устной информации оформляются и объявляются на государственном языке и могут быть продублированы на других языках.» | 25.07.2026 |

Sanction texts (Administrative Code, live lex.uz):
- art. 178 part 6: «непредставление потребителям информации или предоставление заведомо недостоверных сведений о
  товарах (работах, услугах)…»
- art. 164 part 1: «Нарушение правил торговли или оказания услуг — влечет наложение штрафа на граждан в размере
  десяти, а на должностных лиц — в размере двадцати базовых расчетных величин.»
- art. 42: «…пренебрежение к государственному языку… — влечет наложение штрафа от одной до двух базовых расчетных
  величин.»

## Fact check (passport §11.4)

| ID | Claim | Status | Source |
|---|---|---|---|
| D-027 / EC-01 | The seller's details are required on an online store | **CONFIRMED** (offer content + consumer law) | https://lex.uz/ru/docs/6213428 ; https://lex.uz/ru/docs/14643 |
| D-027 / EC-02 | Return terms are required in the offer | **PARTIAL now, CONFIRMED from 12.12.2026** (ZRU-1173) | https://lex.uz/ru/docs/6213428?ONDATE=12.12.2026%2001 |
| D-027 / EC-03 | An Uzbek-language version is required | **CONFIRMED in substance**: contract terms, seller and goods information in the state language; no norm names "website version" | ZRU-792 art. 21; Law 221-I arts. 5–6; language law art. 20 |
| Q13 | Does Uzbek law require consumer information in Uzbek? | **CONFIRMED** (as above) | — |

## Feature ideas (passport §10 format)

- F-51 · **Law version 12.12.2026 for EC-02.** Saved store scans are re-scored under the edition that takes effect on
  12.12.2026, so the report shows "from 12 December this finding becomes stricter" · a second live example of F-16,
  this time a future change · S · this file · Final

## Questions for the team

- **Q-L20 (Role 1).** Add `STATELANG` (lex:121051, «Davlat tili toʻgʻrisida») to `ACTS` in
  the citation list? It would cite like ECOM and CONSUMER. Until then EC-03 shows the
  YAML quote.
- **Q-L21 (Role 1).** Do F-51 now (one more `law_versions.yaml` entry), or after the checkpoint?

## Sources

- ZRU-792 «On electronic commerce»: https://lex.uz/docs/6213382 · https://lex.uz/docs/-6213382 · https://lex.uz/ru/docs/6213428 ;
  edition from 12.12.2026: https://lex.uz/ru/docs/6213428?ONDATE=12.12.2026%2001
- Law 221-I «On the protection of consumer rights»: https://lex.uz/docs/4704 · https://lex.uz/docs/-4704 · https://lex.uz/ru/docs/14643
- Law «On the state language»: https://lex.uz/docs/121051 · https://lex.uz/docs/-121051 · https://lex.uz/ru/docs/121433
- Administrative Code (arts. 42, 164, 178): https://lex.uz/docs/97664 · https://lex.uz/ru/docs/97661
- Related: `backend/rules_draft/EC-0*.yaml` (Role 1 drafts), `rules/EC-0*.yaml` (this work), `research/legal-liability.md` (BCA)
