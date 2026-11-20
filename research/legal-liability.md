# Liability for personal-data violations and enforcement practice (R-02)
- Author: Role 2 (legal research), prepared with Claude Code
- Date/time: 21.11.2026, 04:10
- Based on passport version: 0.13 (researched against 0.12; IDs and F-20 status aligned with 0.13)
- Method: all law texts downloaded from **live lex.uz on 21.11.2026** (Python/httpx, saved HTML, article text
  extracted and compared). Article history was checked by opening the lex.uz editions of the codes on the dates
  09.07.2019, 01.12.2021, 12.09.2026 and the **future edition 05.02.2027** (lex.uz already lists editions that
  enter into force later). New acts were checked in the lex.uz "New in legislation" RSS (uz: 126 items,
  21.10–19.11.2026; ru: 93 items, 21.10–18.11.2026). Practice: the regulator's own pages through the Internet
  Archive (Uzkomnazorat press release of 02.07.2021; 30+ snapshots of the public register `pd.gov.uz/spoiler`,
  07.2021–09.2026), then news sites. Exchange rates: Central Bank of Uzbekistan (cbu.uz), 21.11.2026.
- Confidence: **high** for the texts, amounts and dates of the codes, the decree on the base calculation amount
  (BCA, Uzbek БҲМ / Russian БРВ) and the 2021–2022 register timeline (primary sources). **Medium** for the
  Q14 interpretation (section 8) and for "practice" (only one court case found, from a secondary source).
  Interpretations are a researcher's reading, not a lawyer's opinion.

Official texts are in Uzbek (lex.uz gives them in Cyrillic). Russian texts are LexUZ translations; for the newest
amendments LexUZ marks them «Неофициальный перевод» (e.g. art. 46² part 2 and art. 9 of the Administrative Code).

## Conclusions

1. **Two articles carry the sanctions; the law itself only refers to them.** ZRU-547 art. 33 says only that guilty
   persons "bear liability in the established order", and LexUZ's comment points to **Administrative Code art. 46²**
   and **Criminal Code art. 141²**. Art. 46² part 1 (unlawful processing **and** the localization requirement): a fixed
   fine of **7 BCA for citizens = 3,080,000 UZS** and **50 BCA for officials = 22,000,000 UZS**. Art. 46² part 2
   (new, ZRU-1115, 21.01.2026): **unlawful processing with AI** and its dissemination — **50–100 BCA
   (22–44 M UZS)** with confiscation. Criminal art. 141² applies only **after an administrative penalty for the same
   acts**: 100–150 BCA (44–66 M UZS) or other punishments; aggravated part 2 up to 3 years of imprisonment.
2. **Companies are not fined — people are.** The Administrative Code makes natural persons from 16 (art. 13) and
   **officials, including managers of private companies "regardless of the form of ownership"** (art. 15) liable;
   art. 46² names only "citizens" and "officials". The Criminal Code (art. 17) covers only natural persons. So the
   realistic target of a fine is the **director or the responsible person**, and the amounts are small
   (max ≈ $3.7k administrative vs GDPR €20 M / 4 %). **The real lever for a business is blocking**, not the fine.
3. **Q14 is confirmed: the codes still carry the old, blanket localization wording.** Art. 46² part 1 and art. 141²
   part 1 still punish failure to collect, systematize and store **all** citizens' data processed with IT "on
   technical means physically located in Uzbekistan and in databases registered in the State Register" — the
   2021 wording of art. 27¹ (ZRU-666). They were not amended by ZRU-1125 and are unchanged in the edition dated
   05.02.2027. The new art. 27¹ requires local storage only for biometric, genetic and telecom-user data. Our
   reading: the code punishes non-compliance with a *requirement* that the law no longer imposes on other data,
   so PD-LOC levels stay as in passport §5 (🔴 only for the three categories, 🟡 otherwise) — but reports must
   show a "legal uncertainty" note, because a literal reading of the code is still possible (Q-L6).
4. **Procedure.** Cases under art. 46² are heard by **criminal courts** (Administrative Code art. 245; unchanged in the
   2027 edition). The protocol is drawn up by the official of the body charged with control (art. 280); for
   localization, **CMR No. 707, annex 3** (added by CMR No. 255 of 29.04.2021) gives **Uzkomnazorat** the power to
   draw up protocols and send them to court. PP-14 of 19.01.2026 planned to give the same power to the **MoI
   Migration and Personalization Department** through a Code amendment due **May 2026 — not adopted** as of
   21.11.2026 (not in the code, not in the RSS). Limitation period **1 year** (art. 36; for a continuing offence —
   from detection); a person counts as penalized for **1 year** after the penalty is executed (art. 37) — the window
   for criminal art. 141².
5. **BCA = 440,000 UZS since 01.09.2026** (Presidential Decree PF-115 of 23.06.2026, item 3(b)(ii); before:
   412,000). The fine is calculated with the BCA in force **on the day of the offence**, or on the day of detection
   for a continuing offence (art. 25) — so a tracker running since summer 2026 is fined at today's BCA.
6. **2021 blocking (V-07) is fully documented from primary sources** — and the mechanism still exists. Legal
   basis: ZRU-547 art. 27¹ + CMR 707 annex 3 (register of violators → instruction → listing → access restriction
   within 12 hours). **02.07.2021:** Twitter, TikTok, VKontakte, Skype, WeChat listed and restricted (orders of
   07–16.06.2021). **03.11.2021:** Facebook, Instagram, Telegram, YouTube, LinkedIn, Odnoklassniki, Moi Mir listed and
   **removed the same day**; the head of Uzkomnazorat was dismissed. Skype was removed in spring 2022; Twitter, VK,
   WeChat on **01.08.2022**. **TikTok is still listed as restricted in the register snapshot of 26.09.2026.** The
   register is public (pd.gov.uz/spoiler), now under the MoI Department and the Ministry of Digital Technologies'
   inspection. **Administrative fines under art. 46²: no published case found**; one criminal case under
   art. 141² part 2 (two mobile-operator employees disclosed subscriber names and addresses, reported 23.12.2024).

## Data

### 1. Administrative Code art. 46² — full text (current edition)

Source: official Uzbek text https://lex.uz/docs/97664 (edition in force on 21.11.2026; last past edition
03.11.2026, future editions 11.12.2026, 30.12.2026, 05.02.2027 listed; article checked in all of them up to
05.02.2027 — unchanged). Russian: https://lex.uz/ru/docs/97661 (note: `lex.uz/ru/docs/97664` shows the Uzbek
text with a Russian interface; the Russian translation is document 97661).

> **uz (official):**
> **46²-модда. Шахсга доир маълумотлар тўғрисидаги қонунчиликни бузиш**
> (46²-модданинг номи Ўзбекистон Республикасининг 2021 йил 21 апрелдаги ЎРҚ-683-сонли Қонуни таҳририда — Қонунчилик маълумотлари миллий базаси, 21.04.2021 й., 03/21/683/0375-сон)
> Шахсга доир маълумотларни қонунга хилоф равишда йиғиш, тизимлаштириш, сақлаш, ўзгартириш, тўлдириш, улардан фойдаланиш, уларни бериш, тарқатиш, узатиш, эгасизлантириш ва йўқ қилиш, худди шунингдек ахборот технологияларидан фойдаланган ҳолда, шу жумладан Интернет жаҳон ахборот тармоғида Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ишлов берилаётганда жисман Ўзбекистон Республикаси ҳудудида жойлашган техник воситаларда ҳамда Шахсга доир маълумотлар базаларининг давлат реестрида белгиланган тартибда рўйхатдан ўтказилган шахсга доир маълумотлар базаларида шахсга доир маълумотларни йиғишга, тизимлаштиришга ва сақлашга оид талабларга риоя этмаслик, —
> фуқароларга базавий ҳисоблаш миқдорининг етти баравари, мансабдор шахсларга эса — эллик баравари миқдорида жарима солишга сабаб бўлади.
> (46²-модданинг матни Ўзбекистон Республикасининг 2021 йил 29 октябрдаги ЎРҚ-726-сонли Қонуни таҳририда — Қонунчилик маълумотлари миллий базаси, 30.10.2021 й., 03/21/726/1001-сон — 2022 йил 31 январдан кучга киради)
> Сунъий интеллект технологияларидан фойдаланган холда шахсга доир маълумотларга қонунга хилоф равишда ишлов бериш, уларни оммавий ахборот воситаларида, телекоммуникация тармоқларида ёки Интернет жаҳон ахборот тармоғида тарқатиш, —
> маъмурий ҳуқуқбузарликни содир этиш қуролларини мусодара қилиб, базавий ҳисоблаш миқдорининг эллик бараваридан юз бараваригача миқдорда жарима солишга сабаб бўлади.
> (46²-модда Ўзбекистон Республикасининг 2026 йил 21 январдаги ЎРҚ-1115-сонли Қонунига асосан иккинчи қисм билан тўлдирилган — Қонунчилик маълумотлари миллий базаси, 21.01.2026 й., 03/26/1115/0063-сон)

> **ru (LexUZ translation; part 2 marked «Неофициальный перевод»):**
> **Статья 46². Нарушение законодательства о персональных данных**
> Незаконный сбор, систематизация, хранение, изменение, дополнение, использование, предоставление, распространение, передача, обезличивание и уничтожение персональных данных, а равно несоблюдение при обработке персональных данных граждан Республики Узбекистан с использованием информационных технологий, в том числе во всемирной информационной сети Интернет, требований по сбору, систематизации и хранению персональных данных на технических средствах, физически размещенных на территории Республики Узбекистан, и в базах персональных данных, зарегистрированных в установленном порядке в Государственном реестре баз персональных данных, —
> влечет наложение штрафа на граждан в сумме семи, а на должностных лиц — пятидесяти базовых расчетных величин.
> Незаконная обработка персональных данных с использованием технологий искусственного интеллекта, их распространение в средствах массовой информации, сетях телекоммуникаций или всемирной информационной сети Интернет, —
> влечет наложение штрафа в размере от пятидесяти до ста базовых расчетных величин с конфискацией предметов административного правонарушения.

Breakdown:

| Part | Elements (composition) | Subject | Fine | Repeat |
|---|---|---|---|---|
| 1, clause A | **Unlawful** collection, systematization, storage, change, supplementing, use, provision, dissemination, transfer, de-identification, destruction of PD | citizens; officials | **7 BCA** (citizens) / **50 BCA** (officials) — fixed amounts, not a range | no repeat part in the Code; repeat after a penalty → Criminal Code art. 141² |
| 1, clause B | Failure, when processing citizens' PD with IT incl. the Internet, to meet the requirements to collect, systematize and store PD **on technical means physically in Uzbekistan** and **in databases registered in the State Register** (old localization wording — see section 8) | citizens; officials | same | same |
| 2 (since 21.01.2026) | Unlawful processing of PD **using AI technologies**, their dissemination in mass media, telecom networks or the Internet | not split by subject (anyone liable under the Code) | **50–100 BCA** + confiscation of the instruments (uz: «ҳуқуқбузарликни содир этиш қуролларини»; the ru text says "предметов") | Criminal art. 141² does not mention AI — its disposition repeats only part 1 |

Note: ZRU-1115 entered into force on official publication («Ушбу Қонун расмий эълон қилинган кундан эътиборан
кучга киради», https://lex.uz/docs/8008401), i.e. 21.01.2026. The Ministry of Digital Technologies' news item
(https://gov.uz/en/digital/news/view/122739, 21.01.2026) wrongly calls the unit "minimum wage" — the Code says
BCA.

### 2. History of art. 46² and art. 141²

| Date (in force) | Act | What changed | Source |
|---|---|---|---|
| 01.10.2019 | ZRU-548 of 08.07.2019 | Art. 46² added: "Violation of legislation (қонун ҳужжатлари) on personal data" — only clause A; fine **3–5 minimum wages** (citizens), **5–10** (officials). Art. 141² added: after an administrative penalty — up to **50 minimum wages**; part 2 — 50–100 | edition 09.07.2019: https://lex.uz/docs/97664?ONDATE=09.07.2019%2000 ; https://lex.uz/docs/111453?ONDATE=09.07.2019%2000 ; ZRU-548: https://lex.uz/docs/4407820 |
| 2019–2021 | (units) | The "previous edition" link of the current text points straight to 09.07.2019; how "minimum wage" became BCA in 2019–2021 was not traced article by article — **NOT VERIFIED** | — |
| 21.04.2021 | ZRU-683 of 21.04.2021 | Title of 46² and 141²: «қонун ҳужжатлари» → «қонунчилик»; ZRU-547 art. 33 re-worded | https://lex.uz/docs/5388561 |
| 31.01.2022 | ZRU-726 of 29.10.2021 | Text of 46² and 141² re-written: **localization clause B added** (mirrors art. 27¹ of 2021); 46²: 7 / 50 BCA; 141²: 100–150 BCA; part 2: 150–200 BCA | https://lex.uz/docs/5701569 (uz) ; https://lex.uz/ru/docs/5701571 (ru) |
| 21.01.2026 | ZRU-1115 of 21.01.2026 | 46² **part 2 (AI)** added | https://lex.uz/docs/8008401 |
| 27.03.2026 | ZRU-1125 of 26.03.2026 | New art. 27¹ of ZRU-547 — **the codes were not touched** | R-10; codes checked in editions 12.09.2026 and 05.02.2027 |
| up to 05.02.2027 | — | No further change to 46² or 141² in the editions lex.uz already lists (11.12.2026, 30.12.2026, 05.02.2027) | https://lex.uz/docs/97664?ONDATE=05.02.2027 ; https://lex.uz/docs/111453?ONDATE=05.02.2027 |

### 3. Criminal Code art. 141² — full text

Source: official Uzbek https://lex.uz/docs/111453 ; Russian https://lex.uz/ru/docs/111457 (current edition; text
unchanged since 31.01.2022, also in the edition dated 05.02.2027).

> **uz (official):**
> **141²-модда. Шахсга доир маълумотлар тўғрисидаги қонунчиликни бузиш**
> Шахсга доир маълумотларни қонунга хилоф равишда йиғиш, тизимлаштириш, сақлаш, ўзгартириш, тўлдириш, улардан фойдаланиш, уларни бериш, тарқатиш, узатиш, эгасизлантириш ва йўқ қилиш, худди шунингдек ахборот технологияларидан фойдаланган ҳолда, шу жумладан Интернет жаҳон ахборот тармоғида Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ишлов берилаётганда жисман Ўзбекистон Республикаси ҳудудида жойлашган техник воситаларда ҳамда Шахсга доир маълумотлар базаларининг давлат реестрида белгиланган тартибда рўйхатдан ўтказилган шахсга доир маълумотлар базаларида шахсга доир маълумотларни йиғишга, тизимлаштиришга ва сақлашга оид талабларга риоя этмаслик, ўша ҳаракатлар учун маъмурий жазо қўлланилганидан кейин содир этилган бўлса, —
> базавий ҳисоблаш миқдорининг юз бараваридан бир юз эллик бараваригача миқдорда жарима ёки уч йилгача муайян ҳуқуқдан маҳрум қилиш ёхуд икки йилгача ахлоқ тузатиш ишлари билан жазоланади.
> Ўша ҳаракатлар:
> а) бир гуруҳ шахслар томонидан олдиндан тил бириктириб;
> б) такроран ёки хавфли рецидивист томонидан;
> в) ғаразли ёки бошқа паст ниятларда;
> г) хизмат мавқеидан фойдаланган ҳолда содир этилган бўлса;
> д) оғир оқибатларга сабаб бўлса, —
> базавий ҳисоблаш миқдорининг бир юз эллик бараваридан икки юз бараваригача миқдорда жарима ёки икки йилдан уч йилгача ахлоқ тузатиш ишлари ёки бир йилдан уч йилгача озодликни чеклаш ёхуд уч йилгача озодликдан маҳрум қилиш билан жазоланади.
> (141²-модданинг матни Ўзбекистон Республикасининг 2021 йил 29 октябрдаги ЎРҚ-726-сонли Қонуни таҳририда — Қонунчилик маълумотлари миллий базаси, 30.10.2021 й., 03/21/726/1001-сон — 2022 йил 31 январдан кучга киради)

> **ru:**
> **Статья 141². Нарушение законодательства о персональных данных**
> Незаконный сбор, систематизация, хранение, изменение, дополнение, использование, предоставление, распространение, передача, обезличивание и уничтожение персональных данных, а равно несоблюдение при обработке персональных данных граждан Республики Узбекистан с использованием информационных технологий, в том числе во всемирной информационной сети Интернет, требований по сбору, систематизации и хранению персональных данных на технических средствах, физически размещенных на территории Республики Узбекистан, и в базах персональных данных, зарегистрированных в установленном порядке в Государственном реестре баз персональных данных, совершенное после применения административного взыскания за такие же действия, —
> наказывается штрафом от ста до ста пятидесяти базовых расчетных величин или лишением определенного права до трех лет либо исправительными работами до двух лет.
> Те же действия: а) совершенные по предварительному сговору группой лиц; б) совершенные повторно или опасным рецидивистом; в) совершенные из корыстных или иных низменных побуждений; г) совершенные с использованием служебного положения; д) повлекшие тяжкие последствия, —
> наказываются штрафом от ста пятидесяти до двухсот базовых расчетных величин или исправительными работами от двух до трех лет или ограничением свободы от одного года до трех лет либо лишением свободы до трех лет.

- **Prejudice:** part 1 requires that the same acts were committed «ўша ҳаракатлар учун маъмурий жазо
  қўлланилганидан кейин» / «после применения административного взыскания за такие же действия».
- **Subject:** natural persons only — Criminal Code art. 17: «Жиноят содир этгунга қадар ўн олти ёшга тўлган, ақли
  расо жисмоний шахслар жавобгарликка тортиладилар» / «Ответственности подлежат физические, вменяемые лица, которым до
  совершения преступления исполнилось шестнадцать лет» (part 2 repealed by ZRU-735 of 07.12.2021).
- Criminal fines in general: 5 to 600 BCA (art. 44 part 2: «Жарима базавий ҳисоблаш миқдорининг беш бараваридан олти
  юз бараваригача миқдорда белгиланади»).

### 4. ZRU-547 art. 33 and the authorized body's power to give binding instructions

Source: https://lex.uz/docs/4396419 (uz) · https://lex.uz/ru/docs/4396428 (ru), current edition, read 21.11.2026.

> **uz:** **33-модда. Шахсга доир маълумотлар тўғрисидаги қонунчиликни бузганлик учун жавобгарлик**
> Шахсга доир маълумотлар тўғрисидаги қонунчиликни бузганликда айбдор шахслар белгиланган тартибда жавобгар бўлади.
> (33-модда Ўзбекистон Республикасининг 2021 йил 21 апрелдаги ЎРҚ-683-сонли Қонуни таҳририда — Қонунчилик маълумотлари миллий базаси, 21.04.2021 й., 03/21/683/0375-сон)
> (LexUZ comment) «Қаранг: Ўзбекистон Республикасининг Маъмурий жавобгарлик тўғрисидаги кодексининг 46²-моддаси, Жиноят кодексининг 141²-моддаси.»
>
> **ru:** **Статья 33. Ответственность за нарушение законодательства о персональных данных**
> Лица, виновные в нарушении законодательства о персональных данных, несут ответственность в установленном порядке.

Art. 8 (powers of the authorized body), two items relevant to enforcement:

> **uz:** «шахсга доир маълумотлар тўғрисидаги қонунчилик талабларига риоя этилиши устидан ўз ваколатлари доирасида давлат назоратини амалга оширади;» … «шахсга доир маълумотлар тўғрисидаги қонунчиликнинг бузилишларини бартараф қилиш ҳақида юридик ва жисмоний шахслар томонидан ижро этилиши мажбурий бўлган кўрсатмалар киритади;»
> **ru:** «осуществляет в пределах своих полномочий государственный контроль за соблюдением требований законодательства о персональных данных;» … «вносит обязательные для исполнения юридическими и физическими лицами предписания об устранении нарушений законодательства о персональных данных;»

→ Against a **company**, the law's tool is the **binding instruction (prescription)**; the fine goes to the
official. Whether failure to obey a prescription is itself an administrative offence (e.g. a general article on
non-compliance with lawful demands of a control body) was **not checked — NOT VERIFIED**.

### 5. Liability matrix (BCA = 440,000 UZS since 01.09.2026; USD at CBU 12,004.48 UZS, 21.11.2026)

| Violation | Article / part | Subject | Fine in BCA | Fine in UZS (min–max) | ≈ USD | Repeat / criminal |
|---|---|---|---|---|---|---|
| Unlawful collection / use / transfer / dissemination of PD (e.g. form without legal basis, PD to third parties) | Adm. 46² p.1 (A) | citizen | 7 | 3,080,000 | 257 | after penalty, within the 1-year window (art. 37) → Crim. 141² p.1 |
| same | Adm. 46² p.1 (A) | official (director, responsible person) | 50 | 22,000,000 | 1,833 | same |
| Not storing citizens' PD on servers in Uzbekistan / not in a registered DB (old wording; for 3 categories clearly applicable — see section 8) | Adm. 46² p.1 (B) | citizen / official | 7 / 50 | 3,080,000 / 22,000,000 | 257 / 1,833 | same |
| Unlawful processing of PD with AI, dissemination in media / telecom / Internet | Adm. 46² p.2 | any person liable under the Code | 50–100 + confiscation | 22,000,000 – 44,000,000 | 1,833–3,665 | 141² does not cover the AI wording |
| Same acts as p.1 after an administrative penalty | Crim. 141² p.1 | natural person ≥16 | 100–150, or deprivation of a right ≤3 y, or correctional work ≤2 y | 44,000,000 – 66,000,000 | 3,665–5,498 | — |
| Aggravated (group, repeat, mercenary motive, **official position**, grave consequences) | Crim. 141² p.2 | natural person | 150–200, or correctional work 2–3 y, or restriction of liberty 1–3 y, or imprisonment ≤3 y | 66,000,000 – 88,000,000 | 5,498–7,331 | — |
| Legal entity | — | **not named** in art. 46² (only citizens and officials) and not a subject of the Criminal Code (art. 17: natural persons) | — | — | — | company gets a binding instruction (ZRU-547 art. 8) and, for localization, may be listed in the register and blocked (section 9) |

Amounts for offences committed **before 01.09.2026** (BCA 412,000): 2,884,000 / 20,600,000 / 20,600,000–41,200,000
UZS. For a continuing offence (e.g. a tracker still running) the BCA on the day of detection applies (art. 25).

### 6. Procedure — Administrative Code (uz official / ru)

| Topic | Article | Quote | 
|---|---|---|
| Who hears the case | **245** (part 1 in the edition of ZRU-1185 of 02.11.2026; next edition ZRU-1186 from 05.02.2027 keeps 46²) | uz: «Жиноят ишлари бўйича судлар ушбу Кодекснинг … 46, 46¹, 46²-моддаларида … назарда тутилган маъмурий ҳуқуқбузарликлар ҳақидаги ишларни кўриб чиқади.» ru: «Суды по уголовным делам рассматривают дела об административных правонарушениях, предусмотренных статьями … 46, 46¹, 46² …» |
| Who draws up the protocol | **280** | uz: «Бузилиши маъмурий жавобгарликни келтириб чиқарадиган қоидаларга риоя этилишини текшириш ва (ёки) назорат қилиш қонунчилик билан зиммасига юклатилган тегишли органнинг ваколатли мансабдор шахси маъмурий ҳуқуқбузарлик тўғрисидаги баённомани тузади.» ru: «Протокол об административном правонарушении составляется уполномоченным должностным лицом соответствующего органа, на который законодательством возложен контроль и (или) надзор за соблюдением правил, нарушение которых влечет административную ответственность.» (uz note: ZRU-683 edition; ru note cites ZRU-436 of 2017 — notes differ, wording identical in substance) |
| Protocol power for localization | CMR No. 707, annex 3, item 5 | uz: «…Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ишлов беришнинг алоҳида шартларини бузганликлари юзасидан маъмурий ҳуқуқбузарлик тўғрисида баённомаларни тузади ва кўриб чиқиш учун судга юборади;» ru: «составляет и направляет в суд для рассмотрения протоколы об административных правонарушениях в отношении собственников и (или) операторов … о нарушении особых условий обработки персональных данных граждан Республики Узбекистан;» |
| Planned (not adopted) | PP-14 of 19.01.2026, annex 2, item 1 | uz: «Миграция ва персоналлаштириш департаменти … ва унинг ҳудудий бўлинмаларига Ўзбекистон Республикасининг «Шахсга доир маълумотлар тўғрисида»ги Қонуни талабларини бузган шахсларга нисбатан маъмурий баённома расмийлаштириш ваколатини бериш.» Mechanism: draft law amending the Administrative Code; deadline «2026 йил май»; responsible: MoI, MoJ. **Status 21.11.2026: no such amendment in the Code (art. 46², 245, 280 unchanged) or in the RSS 21.10–19.11.2026.** |
| Limitation period | **36** part 1 | uz: «Маъмурий жазо ҳуқуқбузарлик содир этилган кундан бошлаб, давом этаётган ҳуқуқбузарликлар учун эса, ҳуқуқбузарлик аниқланган кундан бошлаб бир йилдан кечиктирмай қўлланилиши мумкин.» ru: «Административное взыскание может быть применено не позднее одного года со дня совершения правонарушения, а при длящемся правонарушении — одного года со дня его обнаружения.» |
| "Penalized" status (window for 141²) | **37** | uz: «Башарти маъмурий жазога тортилган шахс шу жазони ўташ муддати тугаган кундан бошлаб бир йил мобайнида янги маъмурий ҳуқуқбузарлик содир этмаган бўлса, мазкур шахс маъмурий жазога тортилмаган деб ҳисобланади.» ru: «…в течение года со дня окончания исполнения взыскания не совершило нового административного правонарушения, то оно считается не подвергавшимся административному взысканию.» |
| Which BCA | **25** part 2 | uz: «Жариманинг миқдори маъмурий ҳуқуқбузарлик содир этилган вақтдаги, давом этаётган маъмурий ҳуқуқбузарлик учун эса бу ҳуқуқбузарлик аниқланган вақтдаги белгилаб қўйилган базавий ҳисоблаш миқдоридан келиб чиққан ҳолда белгиланади.» ru: «Размер штрафа определяется исходя из базовой расчетной величины, установленной на момент совершения административного правонарушения, а при длящемся правонарушении — на момент его обнаружения.» |
| Subjects | **13**, **15** | art. 13 uz: «…ўн олти ёшга тўлган шахслар … маъмурий жавобгарликка тортилади»; art. 15 part 2 ru: «Должностным лицом признается лицо, … осуществляющее организационно-распорядительные, административно-хозяйственные функции в государственных органах, органах самоуправления граждан, на предприятиях, учреждениях, организациях, независимо от форм собственности…» |
| Softer law is retroactive | **9** part 4 | uz: «Маъмурий ҳуқуқбузарлик учун жавобгарликни енгиллаштирувчи ёки бекор қилувчи ҳужжатлар орқага қайтиш кучига эгадир…» ru: «Акты, смягчающие или устраняющие ответственность за административные правонарушения, имеют обратную силу…» |
| Special legal regime (TIFC) | **9** part 6 (ZRU-1158, from 25.07.2026) | Lets the Constitutional Law replace administrative liability with other measures for currency, customs, tax, securities, competition, crypto-assets and trade/services rules — **personal data is not in the list** (relevant to F-32 of R-10) |

### 7. Base calculation amount (V-11)

| Period | BCA, UZS | Act | Source |
|---|---|---|---|
| from **01.09.2026** | **440,000** | Presidential Decree **PF-115 of 23.06.2026** "On increasing wages, pensions, stipends and allowances", item 3(b)(ii); decree in force 23.06.2026, published 23.06.2026 No. 06/26/115/0619 | uz: https://lex.uz/docs/8283656 · ru: https://lex.uz/ru/docs/8283680 |
| until 31.08.2026 | 412,000 | previous decree — number and date **NOT VERIFIED on lex.uz** (Spot: last raised in August 2025) | https://www.spot.uz/ru/2026/06/23/indexation/ |

> **uz:** «3. Қуйидагилар: … (б) 2026 йил 1 сентябрдан бошлаб: (i) меҳнатга ҳақ тўлашнинг энг кам миқдори — ойига 1 360 000 сўм; (ii) базавий ҳисоблаш миқдори — 440 000 сўм этиб белгилансин.»
> **ru:** «3. Установить: … (б) с 1 сентября 2026 года: (i) минимальный размер оплаты труда — 1 360 000 сумов в месяц; (ii) базовую расчетную величину — 440 000 сумов.»

Do not confuse: the **minimum wage** (МРОТ / меҳнатга ҳақ тўлашнинг энг кам миқдори) is 1,360,000 UZS from the same
date; the **pension base** is 504,000 UZS from 01.07.2026. Only the BCA is used for these fines. No newer change of
the BCA in the lex.uz RSS 21.10–19.11.2026.

### 8. Q14 — the codes vs the new art. 27¹

| Text | Wording on localization (verbatim, ru for comparison; uz official in sections 1, 3 and R-10) |
|---|---|
| **Old art. 27¹** (ZRU-666 of 14.01.2021, in force 16.04.2021 – 26.03.2026; edition https://lex.uz/ru/docs/4396428?ONDATE=29.11.2023%2001) | «Собственник и (или) оператор при обработке персональных данных граждан Республики Узбекистан с использованием информационных технологий, в том числе во всемирной информационной сети Интернет, обязан обеспечить их сбор, систематизацию и хранение в базах персональных данных на технических средствах, физически размещенных на территории Республики Узбекистан и зарегистрированных в установленном порядке в Государственном реестре баз персональных данных.» |
| **Adm. 46² p.1 / Crim. 141² p.1** (ZRU-726, since 31.01.2022, unchanged to 05.02.2027) | «…несоблюдение при обработке персональных данных граждан Республики Узбекистан с использованием информационных технологий, в том числе во всемирной информационной сети Интернет, требований по сбору, систематизации и хранению персональных данных на технических средствах, физически размещенных на территории Республики Узбекистан, и в базах персональных данных, зарегистрированных в установленном порядке в Государственном реестре баз персональных данных…» |
| **New art. 27¹** (ZRU-1125, since 27.03.2026) | «Обязательному хранению на территории Республики Узбекистан подлежат следующие персональные данные: биометрические…; генетические…; данные физических лиц — пользователей услуг операторов телекоммуникаций…» Other data «могут храниться и обрабатываться за пределами территории Республики Узбекистан при выполнении одного из следующих условий…» |
| **New art. 20 part 1** (ZRU-1125) | Only databases that must be stored in Uzbekistan under art. 27¹ part 2 are registered (R-10, section 2). |

Old art. 27¹ — official Uzbek text (edition 29.11.2023, https://lex.uz/docs/4396419?ONDATE=29.11.2023%2001; this
also answers the "old wording of art. 27¹" request in `research/legal-27-1-2026-v2.md`):

> **27¹-модда. Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ишлов беришнинг алоҳида шартлари**
> Мулкдор ва (ёки) оператор Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ахборот технологияларидан фойдаланган ҳолда ишлов беришда, шу жумладан Интернет жаҳон ахборот тармоғида ишлов беришда уларнинг жисман Ўзбекистон Республикаси ҳудудида жойлашган техник воситаларда ҳамда белгиланган тартибда Шахсга доир маълумотлар базаларининг давлат реестрида рўйхатдан ўтказилган шахсга доир маълумотлар базаларида йиғилишини, тизимлаштирилишини ва сақланишини таъминлаши шарт.
> (27¹-модда Ўзбекистон Республикасининг 2021 йил 14 январдаги ЎРҚ-666-сонли Қонунига асосан киритилган — Қонун ҳужжатлари маълумотлари миллий базаси, 15.01.2021 й., 03/21/666/0032-сон — 2021 йил 16 апрелдан кучга киради)

Findings:
1. **Divergence confirmed (Juris was right).** The codes copy the 2021 rule word for word — "all citizens' data
   processed with IT, on local servers, in registered databases". The law now requires this only for three
   categories, and registration only for those databases.
2. **How a court would read it — interpretation, NOT VERIFIED by a lawyer.** Clause B punishes non-compliance with
   «требований» / «талабларга» (the requirements). Those requirements come from ZRU-547, and since 27.03.2026
   ZRU-547 contains no such requirement for other data. Art. 9 part 4 of the Code makes softer rules retroactive.
   Our reading: for non-mandatory data stored abroad on a lawful basis, clause B has nothing to attach to. The
   residual risk is a literal application by a control body that has not caught up — the same kind of lag as art. 8
   naming the old authority (R-10, V-03).
3. **For PD-LOC levels:** no change to passport §5. 🔴 (with art. 46² p.1 B as sanction) for biometric, genetic
   and telecom-user data abroad; 🟡 for other data sent to non-listed countries (basis not visible, art. 27¹ part 3);
   no finding for listed countries. Add the uncertainty note (F-42) and do **not** write "fine for storing data
   abroad" for ordinary data.
4. Clause A (unlawful processing / transfer) is unaffected and remains the main basis for consent and leak
   findings.

### 9. The 2021 restrictions (V-07)

#### 9.1 Legal basis — CMR No. 707 of 05.09.2018, annex 3 (added by CMR No. 255 of 29.04.2021)

Source: official Uzbek https://lex.uz/docs/3893085 (Latin version https://lex.uz/docs/-3893085), Russian
https://lex.uz/ru/docs/3893082. Annex 3 is still in force (the 2025 changes — CMR 135 of 01.03.2025 renamed the
authorized body in item 2, CMR 791 of 15.12.2025 cancelled an item of a different annex). Title: «Ўзбекистон
Республикаси фуқароларининг шахсга доир маълумотларига ишлов беришнинг алоҳида шартларига риоя этилиши устидан давлат
назоратини амалга ошириш тартиби тўғрисида низом».

| Item | uz (official) | ru |
|---|---|---|
| 2 (definition) | «Шахсга доир маълумотлар субъектлари ҳуқуқларини бузувчилар реестри — Ўзбекистон Республикаси фуқароларининг шахсга доир маълумотларига ишлов беришнинг алоҳида шартларига риоя этмаган шахсга доир маълумотлар базасининг мулкдорлари ва (ёки) операторларининг рўйхати;» | «Реестр нарушителей прав субъектов персональных данных — перечень собственников и (или) операторов базы персональных данных, не соблюдающих особые условия обработки персональных данных граждан Республики Узбекистан;» |
| 2 (definition) | «фойдаланишни чеклаш — мулкдор ва (ёки) операторларнинг Ўзбекистон Республикаси ҳудудида Интернет жаҳон ахборот тармоғидаги ресурсдан фойдаланишини тўхтатишга ёки тезликни камайтиришга доир ташкилий ва дастурий-техник чора-тадбирлар мажмуаси;» | «ограничение доступа — комплекс организационных и программно-технических мер по прекращению или снижению скорости доступа …» |
| 3 | «…давлат назорати Шахсга доир маълумотлар субъектлари ҳуқуқларини бузувчилар реестрини … юритиш орқали амалга оширилади.» | «Государственный контроль … осуществляется путем ведения Реестра нарушителей прав субъектов персональных данных» |
| 13 | «…кўрсатмасида белгиланган муддат ичида … қонун бузилиши ҳолатлари бартараф этилмаган тақдирда, мулкдор ва (ёки) оператор тўғрисидаги маълумотлар Реестрга киритилади.» | «В случае неустранения в течение срока, установленного в предписании … сведения о собственнике и (или) операторе вносятся в Реестр.» |
| 18 | «Вазирлик Реестрга киритилгандан сўнг 12 соат давомида … Интернет жаҳон ахборот тармоғи ресурсларидан фойдаланишини чеклашни амалга оширади.» | «Министерство в течение 12 часов после внесения в Реестр осуществляет ограничение доступа…» |

Flow (annex 3, items 7–23 and the scheme): Center for Mass Communications monitors → within 24 h passes data to
the authorized body → within 24 h the authorized body gives a conclusion to Uzkomnazorat → within 1 day
Uzkomnazorat issues an **instruction with a deadline** → not fixed in time → **listed in the register** → within
12 h submission to the IT ministry → within 12 h **access restricted** (stop or slow down). Exit: conclusion that
the deficiencies are fixed, or a court decision cancelling the conclusion (item 19); the operator may appeal the
conclusion to court (item 14). Note: the scope is "special conditions of processing" = the old art. 27¹
(localization) — the regulation was written for it.

Bodies named in annex 3 are partly outdated (the IT ministry is now the Ministry of Digital Technologies; the
authorized body is now the MoI Department per R-10). The live register page in 2026 (Latin script) names
«Migratsiya va personallashtirish departamenti» of the Ministry of Internal Affairs and «Raqamli texnologiyalar
vazirligi huzuridagi Axborotlashtirish va telekommunikatsiyalar sohasida nazorat inspeksiyasi» (snapshot
26.09.2026). Uzkomnazorat still exists
and took over the media-oversight functions of the dissolved AIMC in July 2025 (kun.uz, 16.07.2025).

#### 9.2 Timeline (primary: Uzkomnazorat release and register snapshots; secondary in brackets)

| Date | Event | Source |
|---|---|---|
| 16.04.2021 | Old art. 27¹ in force (ZRU-666 of 14.01.2021) | lex.uz edition note |
| May 2021 | State Personalization Center sends letters to Facebook, Google, Mail.ru, Microsoft, Telegram, Tencent, TikTok, Twitter, Yandex (director U. Tashkhodjaev) | [Spot, 12.05.2021] |
| 07.06.2021 | Uzkomnazorat instructions: Twitter No. 01-20/1250, WeChat 01-20/1249, VKontakte 01-20/1248 | register snapshots 26.07.2021 |
| 16.06.2021 | Instructions: Skype 01-20/1302, TikTok 01-20/1303 | same |
| **02.07.2021** | Submissions 01-20/1454 – 01-20/1458; **restriction set 02.07.2021** for Skype, Twitter, WeChat, VKontakte, TikTok | register; Uzkomnazorat release 02.07.2021: «…соответствующие социальные сети со 2 июля 2021 года внесены в «Реестр нарушителей прав субъектов персональных данных» и использование соответствующих ресурсов в сети Интернет на территории Республики Узбекистан ограничено в установленном порядке до устранения выявленных недостатков.» |
| 26.07.2021 | Register published at pd.gov.uz/spoiler (5 entries, «Cheklov mavjud») | snapshot 26.07.2021; [Spot, 26.07.2021] |
| **03.11.2021** | 7 more entries: Facebook, Instagram, Telegram, YouTube, LinkedIn, Odnoklassniki, Moi Mir — instructions 01-20/1489 – 01-20/1495 dated 02.07.2021, submissions 370–376 of 02.11.2021, restriction 03.11.2021 | snapshot 03.11.2021 15:19 UTC; [kun.uz, 03.11.2021] |
| 03.11.2021 (evening) | The 7 entries **removed the same day** (gone in the 17:39 UTC snapshot). President's press secretary: the President was informed about «односторонних, не продуманных до конца действиях „Узкомназората“, принятых по указанию правительства»; head of Uzkomnazorat G. Ziyaev dismissed «за ошибочные и несогласованные действия» | snapshots; [Spot, 03.11.2021]; [anhor.uz] |
| 05.11.2021 | The minister of IT and communications and the PM's IT adviser also lose their posts | [Spot, 05.11.2021] |
| 17.03 – 14.05.2022 | **Skype** removed from the register | snapshots 17.03.2022 (listed) and 14.05.2022 (not listed) |
| **01.08.2022** | AIMC: Twitter, VKontakte, WeChat fully available again («Restrictions affect development negatively»); talks with TikTok continue; Spot counts **366 days** of restriction | [Spot, 01.08.2022]; [kun.uz, 01.08.2022]; snapshot 08.08.2022 shows only TikTok |
| 2022–2026 | **TikTok** stays listed, status «Cheklov mavjud» (restriction in place) | snapshots 07.12.2022, 05.08.2025, 09.05.2026, **26.09.2026** |

Answers to the prompt's questions: **who decided** — Uzkomnazorat (State Inspectorate for Control in the Sphere of
Informatization and Telecommunications) on the conclusion of the State Personalization Center; technical
restriction by the IT ministry. **Basis** — ZRU-547 art. 27¹ (2021 wording) + CMR 707 annex 3. **Register of
violators** — exists, kept under annex 3, **public** at https://pd.gov.uz/spoiler (entries show the order and
submission numbers, dates and status). Only global services have ever been listed (by the archived snapshots).
Whether the November 2021 reversal had its own legal act — **NOT VERIFIED** (only press statements found).

### 10. Other practice

| Date | What | Article | Outcome | Source (level) |
|---|---|---|---|---|
| reported 23.12.2024 | Two employees of two mobile operators gave subscribers' full names and addresses (by phone number) to a third person; court case No. 1-1006-2407/980, verdict in force | Crim. **141² part 2** (group by prior agreement) | both found guilty; sentence not reported | anhor.uz, citing a lawyers' Telegram channel (secondary) |
| 04.02.2026 | Cybersecurity Center reviews claims that data of up to 15 M citizens from state systems leaked | — | outcome not published (not found) | kun.uz (secondary) |
| 2021–2026 | Administrative fines under art. 46² | Adm. 46² | **no published case found** | searched: Google (ru/uz/en), kun.uz, spot.uz, anhor.uz, gov.uz, regulator pages; **not searched**: the courts' decision database (public.sud.uz) and Supreme Court statistics |

### 11. Global context (for the pitch; amounts at CBU rates of 21.11.2026)

| Jurisdiction | Maximum | Turnover-based? | Who pays | Localization / transfer | Source |
|---|---|---|---|---|---|
| **Uzbekistan** | Adm.: 100 BCA = **44 M UZS (≈ $3.7k)** (AI part); general part 50 BCA = 22 M UZS for officials. Crim.: 200 BCA = 88 M UZS or up to 3 y prison | no | natural persons and officials only | art. 46² p.1 (old wording) + **blocking via the register** | lex.uz (sections 1–3) |
| **EU (GDPR art. 83(5))** | **€20 M or 4 % of worldwide annual turnover**, whichever is higher (≈ 263 bn UZS / $21.9 M for the fixed cap); transfers to third countries are in 83(5)(c) | yes | undertakings and others | yes (arts. 44–49) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 |
| **Russia (KoAP art. 13.11, ed. 04.08.2026)** | Localization p.8: legal entities 1–6 M RUB; repeat p.9: **6–18 M RUB** (≈ 2.6 bn UZS). Leaks p.14: 10–15 M RUB; repeat leak p.15: **1–3 % of revenue, min 20 M, max 500 M RUB** (≈ 73 bn UZS / $6.1 M); biometric repeat p.18: 1–3 %, min 25 M | yes (p.15, p.18) | citizens, officials, sole traders, legal entities | yes (p.8–9) | https://www.consultant.ru/document/cons_doc_LAW_34661/1f421640c6775ff67079ebde06a7d2f6d17b96db/ |
| **Kazakhstan (Adm. Code arts. 79, 640)** | **30–2,000 MRP**; MRP 2026 = 4,325 KZT → up to 8.65 M KZT (≈ 228 M UZS / $19k); criminal art. 147 for grave cases | no | natural persons, officials, businesses by size | not checked | regulator: https://www.gov.kz/memleket/entities/infsecurity/press/press-releases/details/16593?lang=ru ; MRP: https://tengrinews.kz/kazakhstan_news/utverjden-novyiy-mrp-na-2026-god-v-kazahstane-586608/ (secondary) |

Pitch line (draft): Uzbekistan's fines are among the lowest in the region and hit people, not companies — but
Uzbekistan is the only one of the four where **a regulator listed and blocked global platforms within weeks**, and
one of them is still listed five years later.

## Proposed `sanction:` texts (for Role 1 — proposal only, `backend/` not changed)

Templates (the field is one string per passport §11.2; amounts at BCA 440,000 from 01.09.2026):

```yaml
# T1 — unlawful processing / transfer (clause A)
sanction: "Administrative Code art. 46² part 1 — fine 7 BCA (3,080,000 UZS) for citizens, 50 BCA (22,000,000 UZS) for officials; after a penalty, within 1 year — Criminal Code art. 141² (100–150 BCA). BCA 440,000 UZS from 01.09.2026 (PF-115)."
# T2 — localization of the three mandatory categories (clause B)
sanction: "Administrative Code art. 46² part 1 (storage on technical means in Uzbekistan) — 7 BCA citizens / 50 BCA officials; repeat after a penalty — Criminal Code art. 141²; risk of listing in the register of violators and access restriction (CMR No. 707, annex 3)."
# T3 — localization of other data (🟡)
sanction: "Uncertain: Administrative Code art. 46² part 1 still uses the pre-2026 localization wording (not aligned with art. 27¹ as amended by ZRU-1125); no sanction if one of the art. 27¹ part 3 bases exists."
# T4 — AI processing
sanction: "Administrative Code art. 46² part 2 — fine 50–100 BCA (22–44 M UZS) with confiscation."
```

UI one-liners for the report's "possible consequences" line (our drafts, not quotes; uz in Latin script,
MJtK = Ma’muriy javobgarlik to‘g‘risidagi kodeks, JK = Jinoyat kodeksi, BHM = bazaviy hisoblash miqdori):
- T1 ru: КоАО ст. 46² ч. 1: штраф гражданам 7 БРВ (3 080 000 сум), должностным лицам 50 БРВ (22 000 000 сум). Повторно в течение года после взыскания — УК ст. 141².
  uz: MJtK 46²-moddasi 1-qismi: fuqarolarga 7 BHM (3 080 000 so‘m), mansabdor shaxslarga 50 BHM (22 000 000 so‘m) jarima. Jazodan keyin bir yil ichida takrorlansa — JK 141²-moddasi.
- T2 ru: КоАО ст. 46² ч. 1 + риск внесения в Реестр нарушителей и ограничения доступа к сайту.
  uz: MJtK 46²-moddasi 1-qismi + buzuvchilar reyestriga kiritilish va saytga kirish cheklanishi xavfi.
- T4 ru: КоАО ст. 46² ч. 2: штраф 50–100 БРВ (22–44 млн сум) с конфискацией. uz: MJtK 46²-moddasi 2-qismi: 50–100 BHM (22–44 mln so‘m) jarima, musodara bilan.

| Rule | Proposed `sanction:` | Why |
|---|---|---|
| PD-CNS-01 (form without consent) | T1 | collection without a legal basis = «қонунга хилоф равишда йиғиш» (clause A); consent article itself — R-01 |
| PD-LEAK-01 (PD to third parties) | T1 | «бериш, тарқатиш, узатиш» (provision, dissemination, transfer) |
| PD-REC-01 (session replay records inputs) | T1 | collection and transfer of typed PD to a third party |
| PD-TRK-01 (trackers before consent) | T1 **only if** IP / cookie ID are PD (V-08 open); else `null` | depends on R-01 / V-08 |
| PD-PII-01 (excessive data) | T1 marked "possible" | unlawful collection only if beyond the purpose — legal call (R-01) |
| PD-BIO-01 (biometrics abroad) | T2 | biometrics is a mandatory-localization category |
| PD-LOC-01 / PD-LOC-02 | T2 for telecom-operator sites (V-18) and biometric/genetic data; **T3** otherwise | section 8 |
| PD-DB-01, PD-HOST-01, PD-MAIL-01 | T2 if the data is in a mandatory category, else T3 | same |
| PD-MIS-01 (policy vs behaviour) | the sanction of the underlying behaviour (T1/T2/T3) | the contradiction itself has no separate article in these codes |
| PD-POL-01 / PD-POL-02 | `null` | no separate offence for a missing/incomplete policy in art. 46² (whether the law requires a public policy — R-01) |
| SEC-01 / SEC-02 | `null` | no article for missing HTTPS/headers; a resulting leak → T1 |
| (future) AI SDK receives form PD | T4 | needs a detector — not proposed without Role 1 |

## Fact check (passport §11.4)

| ID | Claim | Status | Correct wording | Source |
|---|---|---|---|---|
| V-05 | The Administrative Code has an article on violating PD legislation; fine amount | **CONFIRMED** | Art. 46² "Violation of legislation on personal data": part 1 — **7 BCA (citizens), 50 BCA (officials)**, fixed; part 2 (AI, since 21.01.2026) — 50–100 BCA + confiscation. No liability of legal entities. Heard by criminal courts (art. 245). | https://lex.uz/docs/97664 ; https://lex.uz/ru/docs/97661 |
| V-06 | The Criminal Code has an article on violating PD legislation | **CONFIRMED** | Art. 141²: only after an administrative penalty for the same acts — 100–150 BCA or deprivation of a right ≤3 y or correctional work ≤2 y; part 2 (group, repeat, motive, official position, grave consequences) — 150–200 BCA … or imprisonment ≤3 y | https://lex.uz/docs/111453 ; https://lex.uz/ru/docs/111457 |
| V-07 | In 2021 Uzbekistan restricted several social networks for violating localization | **CONFIRMED** | 02.07.2021: Twitter, TikTok, VKontakte, Skype, WeChat (Uzkomnazorat, register of violators, CMR 707 annex 3); 03.11.2021: 7 more, reversed the same day; Twitter/VK/WeChat unblocked 01.08.2022; TikTok still listed (snapshot 26.09.2026) | Uzkomnazorat release (archived): https://web.archive.org/web/20210702150703/https://gis.uz/ru/news/997 ; register: https://web.archive.org/web/20210726115936/https://pd.gov.uz/spoiler/ ; https://lex.uz/docs/3893085 |
| V-11 | BCA value for 2026 | **CONFIRMED** | **440,000 UZS from 01.09.2026** (PF-115 of 23.06.2026, item 3(b)(ii)); 412,000 before (previous act NOT VERIFIED) | https://lex.uz/docs/8283656 ; https://lex.uz/ru/docs/8283680 |
| Q14 | Arts. 46² and 141² still use the old, broad localization wording after ZRU-1125 | **CONFIRMED** | Both carry the ZRU-726 (2021) text mirroring old art. 27¹; unchanged in the edition dated 05.02.2027. Interpretation for levels — section 8 (not verified by a lawyer) | sections 1, 3, 8 |
| V-01 (part) | Liability — art. 33 | **CONFIRMED** | Art. 33 is a reference norm («белгиланган тартибда жавобгар бўлади»), edition ZRU-683 | https://lex.uz/docs/4396419 |
| new | Protocols for PD violations are drawn up by the MoI Migration and Personalization Department | **NOT VERIFIED (planned only)** | PP-14 annex 2 item 1 plans it (draft law, May 2026); not in the Code as of 21.11.2026. Current: the control body's official (art. 280); for localization Uzkomnazorat (CMR 707 annex 3 item 5) | https://lex.uz/docs/8003859 ; https://lex.uz/docs/97664 |
| new | A public register of PD violators exists | **CONFIRMED** | pd.gov.uz/spoiler; one entry (TikTok) on 26.09.2026 | https://web.archive.org/web/20260926041426/https://pd.gov.uz/spoiler/?type=spoiler |
| new | Published administrative fines under art. 46² | **NOT FOUND** | none found in news/regulator pages; court database not searched | section 10 |

## Feature ideas (passport §10 format)

Numbering continues after passport 0.13 (it already uses F-35…F-38 for other features).

- **F-20 / F-31 (already accepted in passport 0.13, D-025: "mechanism now, numbers only after V-05")** — this file
  supplies the numbers: "officials: 22,000,000 UZS (50 BCA × 440,000, PF-115, from 01.09.2026)". Keep the BCA value
  in one config entry with source URL and date, and print that date in the report · no new ID
- F-39 · "Who pays" note: the fine under art. 46² is personal (director / responsible person, art. 15), the company
  gets a prescription and, for localization, a blocking risk · strongest argument for the person who signs the
  contract · S · R-02 · Final (pitch + report text)
- F-40 · Repeat-risk flag: onboarding question "was anyone in your company fined under art. 46² in the last
  12 months?" → the report warns that the same finding now falls under Criminal Code art. 141² · S · R-02 · Roadmap
- F-41 · Register-of-violators watch: check pd.gov.uz/spoiler on a schedule; if a site embeds a listed service
  (today: TikTok pixel/SDK), show ⚪ "this service is restricted in Uzbekistan — part of your audience may not load it"
  and alert on new listings · S · R-02 · Final (uses existing tracker detection; no new detector)
- F-42 · "Legal uncertainty" badge on PD-LOC 🟡 findings: "the Administrative Code still has the 2021 localization
  wording (Q14); this is not a violation if a basis under art. 27¹ part 3 exists" · honest, lawyer-friendly · S ·
  R-02 · MVP (text only)
- F-43 · Early warning from future editions: lex.uz lists editions that take effect later (we saw 11.12.2026,
  30.12.2026, 05.02.2027); diff articles 46², 141², 245 and ZRU-547 on each new future edition → "the law will change
  on <date>" alert · S · R-02 · Final (fits F-16)
- F-44 · AI-processing finding (art. 46² part 2, 50–100 BCA): when the AI-services catalog (passport F-32) sees a
  form's PD going to an AI API, attach the part 2 sanction · reuses F-32 data, no new detector without Role 1 · M ·
  R-02 · Roadmap

## Questions for the team / contradictions with the passport

- **Q-L6 (Role 2 / lawyer, Q14).** Do we accept the reading in section 8 (old localization wording of art. 46²
  cannot apply to data that art. 27¹ allows abroad)? Until confirmed, PD-LOC stays 🟡 for non-mandatory data with the
  uncertainty note (F-42).
- **Q-L7 (Role 1).** `sanction:` is one string. To print amounts per subject and the BCA date (F-20) a structured
  field (article, part, subject, bca_min, bca_max) would be cleaner — a schema change, Role 1 decides.
- **Q-L8 (Role 3, pitch).** Passport §2 says "Consequences: fines… blocking". Correction for the pitch: fines are
  small and personal (max 44 M UZS administrative, 88 M criminal); **companies are not fined**; the real business risk is
  listing and blocking (2021 precedent, TikTok still listed). Do not say "a company can be fined X".
- **Q-L9 (Role 2).** Whom do we name as the enforcer in reports? Today: criminal courts decide; protocols — the
  control body's official; for localization — Uzkomnazorat (CMR 707 annex 3); the MoI Department's own protocol
  power is planned (PP-14) but not adopted. Proposed wording: "authorized state bodies (MoI Migration and
  Personalization Department; Uzkomnazorat for localization); cases are heard by criminal courts".
- **Q-L10 (Role 2).** CMR 707 annex 3 still names the "Ministry for Development of IT and Communications" and (since
  2025) the "Personalization Agency under the MoJ"; the live register page names the MoI Department and the
  Ministry of Digital Technologies' inspection. Same lag as art. 8 (R-10 Q-L1) — confirm we cite the annex as in force.
- **Q-L11 (Role 2, next step).** Search the courts' decision database (public.sud.uz) for art. 46² / 141² cases to
  replace "practice not found" with numbers before the final.

## Sources

Laws (lex.uz, read 21.11.2026):
- Administrative Code, official Uzbek (current; editions list up to 05.02.2027): https://lex.uz/docs/97664 · Russian: https://lex.uz/ru/docs/97661
- Editions used for history: https://lex.uz/docs/97664?ONDATE=09.07.2019%2000 · https://lex.uz/docs/97664?ONDATE=01.12.2021 · https://lex.uz/docs/97664?ONDATE=12.09.2026%2002 · https://lex.uz/docs/97664?ONDATE=05.02.2027
- Criminal Code, official Uzbek: https://lex.uz/docs/111453 · Russian: https://lex.uz/ru/docs/111457 · editions: https://lex.uz/docs/111453?ONDATE=09.07.2019%2000 · https://lex.uz/docs/111453?ONDATE=05.02.2027
- ZRU-547 (current): https://lex.uz/docs/4396419 · https://lex.uz/ru/docs/4396428 · old art. 27¹ (edition 29.11.2023): https://lex.uz/docs/4396419?ONDATE=29.11.2023%2001 · https://lex.uz/ru/docs/4396428?ONDATE=29.11.2023%2001
- Amending laws: ZRU-548 of 08.07.2019: https://lex.uz/docs/4407820 · ZRU-683 of 21.04.2021: https://lex.uz/docs/5388561 · ZRU-726 of 29.10.2021: https://lex.uz/docs/5701569 · https://lex.uz/ru/docs/5701571 · ZRU-1115 of 21.01.2026: https://lex.uz/docs/8008401
- PF-115 of 23.06.2026 (BCA): https://lex.uz/docs/8283656 · https://lex.uz/ru/docs/8283680
- CMR No. 707 of 05.09.2018 with annex 3 (CMR No. 255 of 29.04.2021): https://lex.uz/docs/3893085 · https://lex.uz/docs/-3893085 · https://lex.uz/ru/docs/3893082
- PP-14 of 19.01.2026: https://lex.uz/docs/8003859
- lex.uz RSS (checked 21.11.2026): https://lex.uz/rss · https://lex.uz/ru/rss

Regulator pages (Internet Archive):
- Uzkomnazorat release 02.07.2021: https://web.archive.org/web/20210702150703/https://gis.uz/ru/news/997
- Register of violators: https://web.archive.org/web/20210726115936/https://pd.gov.uz/spoiler/ · https://web.archive.org/web/20211103151921/https://pd.gov.uz/spoiler/ · https://web.archive.org/web/20211103173905/https://pd.gov.uz/spoiler/ · https://web.archive.org/web/20220317000458/https://pd.gov.uz/spoiler/ · https://web.archive.org/web/20220514094333/https://pd.gov.uz/spoiler/?type=spoiler · https://web.archive.org/web/20220808060004/https://pd.gov.uz/spoiler/?type=spoiler · https://web.archive.org/web/20260926041426/https://pd.gov.uz/spoiler/?type=spoiler

News and secondary (each fact above marks which one it rests on):
- Spot: https://www.spot.uz/ru/2021/05/12/personal-data/ · https://www.spot.uz/ru/2021/06/28/tiktok/ · https://www.spot.uz/ru/2021/07/02/blocks/ · https://www.spot.uz/ru/2021/07/26/personal-data · https://www.spot.uz/ru/2021/11/03/limitation/ · https://www.spot.uz/ru/2021/11/03/restore/ · https://www.spot.uz/ru/2021/11/05/dismissed/ · https://www.spot.uz/ru/2022/08/01/unblocked/ · https://www.spot.uz/ru/2026/06/23/indexation/
- kun.uz: https://kun.uz/ru/news/2021/11/04/v-uzbekistane-ogranichili-rabotu-telegram-facebook-youtube-instagram-i-odnoklassniki · https://kun.uz/en/news/2022/08/01/uzbekistan-unblocks-twitter-wechat-and-vkontakte · https://kun.uz/en/news/2025/07/16/uzkomnazorat-takes-over-media-oversight-duties-from-dissolved-aimc · https://kun.uz/en/news/2026/02/04/cybersecurity-center-investigates-claims-of-personal-data-leak-from-state-systems
- anhor.uz: https://anhor.uz/ru/news/access · https://anhor.uz/uzl/news/2-ta-aloqa-kompaniyasi-mutaxassislari-jinoiy-javobgarlikka-tortildi/
- Freedom House, Freedom on the Net 2022 — Uzbekistan: https://freedomhouse.org/country/uzbekistan/freedom-net/2022
- Ministry of Digital Technologies on ZRU-1115: https://gov.uz/en/digital/news/view/122739
- Central Bank of Uzbekistan rates 21.11.2026: https://cbu.uz/ru/arkhiv-kursov-valyut/json/
- GDPR: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 · Russia KoAP 13.11: https://www.consultant.ru/document/cons_doc_LAW_34661/1f421640c6775ff67079ebde06a7d2f6d17b96db/ · Kazakhstan: https://www.gov.kz/memleket/entities/infsecurity/press/press-releases/details/16593?lang=ru · https://tengrinews.kz/kazakhstan_news/utverjden-novyiy-mrp-na-2026-god-v-kazahstane-586608/
- Q14 origin: `research/competitors.md` (Juris row and Q14)
