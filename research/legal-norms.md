# Norms of the personal data law for website checks (R-01)
- Author: Role 2 (legal research), prepared with Claude Code
- Date/time: 21.11.2026, 04:30
- Based on passport version: 0.13
- Method: ZRU-547 (current edition, last change 12.09.2026 by ZRU-1174) downloaded from **live lex.uz on 21.11.2026**
  in three versions — the official Uzbek Cyrillic text (https://lex.uz/docs/4396419), lex.uz's Latin-script version
  of the same text (https://lex.uz/docs/-4396419, used for the Latin quotes in `rules/*.yaml`) and the Russian
  translation (https://lex.uz/ru/docs/4396428). By-laws read the same way: the Minister of Justice's model procedure
  of processing (order No. 20-mh, reg. No. 3478 of 15.11.2023), the model procedure for the responsible person
  (order No. 19-mh, reg. No. 3477) and CMR No. 71 (State Register). Every quote below was checked by script
  against the downloaded text. Art. 27¹ and CMR No. 415 are in `research/legal-27-1-2026.md` (R-10), liability in
  `research/legal-liability.md` (R-02); not repeated here.
- Confidence: **high** for the texts; **medium** for the reading of what a website must show (section 4) and for
  V-08 (no act names IP addresses or cookies — section 5).

## Conclusions

1. **"Personal data" is defined broadly and by identifiability** (art. 4): information "relating to a certain
   natural person **or enabling his identification**", in any recorded form. No act read (ZRU-547, model procedures,
   CMR No. 71, CMR No. 570) mentions IP addresses, cookies or online identifiers. **V-08 stays an interpretation:**
   an IP address or cookie ID that is linked to a visitor, a session or an account "enables identification" and is
   personal data in that context; a bare technical log entry is arguable. This is why PD-TRK-01 and PD-LOC-02
   stay 🟡.
2. **Consent is one of seven legal grounds, not the only one** (art. 18). Processing is also lawful when needed to
   perform a contract with the subject **"or to take steps at the subject's request before such a contract"**,
   to meet the operator's legal duties, for legitimate interests that do not breach the subject's rights, etc. The
   Minister of Justice's model procedure adds: **accepting a public offer that clearly states the purposes, or
   agreeing to the service's terms, counts as consent** (item 9). → A lead or order form without a checkbox is
   **not by itself a violation**; PD-CNS-01 should be 🟡 "consent / ground and notice not visible", not 🔴.
3. **What the website must tell the visitor comes from arts. 22 and 23, not from a "privacy policy" article.**
   No norm read says "publish a policy on the website". The law requires (a) written notice of the **purposes and
   the subject's rights** when data enters a database (art. 23 part 1), (b) written notice **within 3 days** when
   data is given to a third party (art. 23 part 2), and (c) on request, information on grounds, purposes, methods,
   operator name and address, recipients, data, retention, how to use the rights, and **cross-border transfer**
   (art. 22). The model procedure requires an **internal** policy document (item 30, point 12). A public policy is
   the usual way to meet (a) and (c) → PD-POL-01 and PD-POL-02 are 🟡, and the policy checklist in
   `backend/qalqon/llm/policy.py` matches the law except for two items (section 4).
4. **Purpose limitation and data minimisation are explicit** (art. 10 part 1, art. 12 part 2, art. 19 parts 2 and
   5, art. 31): data must be "necessary and sufficient", used "only for the purposes declared earlier", and its
   volume must match the purposes → a firm basis for PD-PII-01 (excessive data) and PD-MIS-01 (behaviour beyond the
   declared purposes).
5. **Third parties and transfers:** confidentiality forbids disclosure to third parties without consent or another
   legal ground (art. 28); handing processing to a third party needs written consent, a contract with the subject,
   or law (art. 31 part 3); cross-border transfer goes to adequate countries, otherwise only with the subject's
   consent, for public-order reasons or under a treaty (art. 15, read with art. 27¹ part 3 — R-10). **V-09 closed.**
6. **The State Register is open (V-04 closed):** CMR No. 71 item 19 — the register's data are open to legal and
   natural persons, and registration status is obtained by entering the database's **registration number** into
   the register's information system. Registration is free and takes 5 working days (items 9–10); since
   27.03.2026 only databases of the three mandatory-localization categories must be registered (art. 20, R-10).

## Data

### 1. Map of ZRU-547 for a website scanner

| Art. | Topic | What it gives the scanner | Rules |
|---|---|---|---|
| 3 | Scope (part 3: special legal regime — TIFC, R-10) | which sites are out of scope | — |
| 4 | Definitions | what is personal data, operator, third party, processing | all |
| 5 | Principles (lawfulness of purposes and methods, confidentiality) | general basis | PD-PII-01, PD-MIS-01 |
| 10 | Collection: "necessary and sufficient"; retention until the purpose is reached | minimisation, retention | PD-PII-01, PD-POL-02 |
| 12 | Use only for purposes declared at collection | purpose limitation | PD-MIS-01, PD-REC-01 |
| 13 / 14 | Provision (to a specific person) / dissemination (to an indefinite circle, incl. the Internet) | what "transfer" means | PD-LEAK-01 |
| 15 | Cross-border transfer | transfer abroad | PD-LOC-01/02, PD-DB-01 |
| 18 | Grounds for processing (consent + six others) | when consent is needed | PD-CNS-01, PD-TRK-01 |
| 19 | Purposes, volume matches purposes, term ≤ consent term | minimisation | PD-PII-01 |
| 20 | Registration (only the art. 27¹ part 2 databases) | registration | — (R-10) |
| 21 | Form of consent ("any form allowing to confirm it"; written for special data); withdrawal | consent | PD-CNS-01 |
| 22 | Information the subject may obtain | policy content | PD-POL-01/02, PD-MIS-01 |
| 23 | Written notice of purposes and rights; notice within 3 days of a transfer to a third party | notice | PD-POL-01, PD-LEAK-01 |
| 25 | Special data (health, beliefs, private life, criminal record): prohibited unless an exception, e.g. written consent | special data forms | PD-PII-01 (note) |
| 26 | Biometric and genetic data: only with consent (or listed exceptions) | biometrics | PD-BIO-01 |
| 27 | Legal, organisational and technical protection measures | security | SEC-01, SEC-02 |
| 27¹ | Localization (three categories) and conditions for storage abroad | localization | PD-LOC-01/02, PD-BIO-01, PD-DB-01 (R-10) |
| 28 | Confidentiality: no disclosure to third parties without consent or another legal ground | third parties | PD-LEAK-01, PD-REC-01 |
| 30 | Subject's rights | policy content | PD-POL-02 |
| 31 | Operator's duties; entrusting processing to a third party; responsible person | processors | PD-REC-01, PD-LEAK-01 |
| 33 | Liability — reference to the Codes | sanction | R-02 |

### 2. Verbatim norms of ZRU-547

Official Uzbek: https://lex.uz/docs/4396419 · Russian: https://lex.uz/ru/docs/4396428 · edition in force on
21.11.2026 (latest change 12.09.2026). Notes in brackets are lex.uz's own edition notes.

**Art. 4 — definitions**
> **uz:** шахсга доир маълумотлар — муайян жисмоний шахсга тааллуқли бўлган ёки уни идентификация қилиш имконини берадиган, электрон тарзда, қоғозда ва (ёки) бошқа моддий жисмда қайд этилган ахборот;
> шахсга доир маълумотларга ишлов бериш — шахсга доир маълумотларни йиғиш, тизимлаштириш, сақлаш, ўзгартириш, тўлдириш, улардан фойдаланиш, уларни бериш, тарқатиш, узатиш, эгасизлантириш ва йўқ қилиш бўйича бир ҳаракатни ёки ҳаракатлар мажмуини амалга ошириш;
> шахсга доир маълумотлар базасининг оператори (оператор) — шахсга доир маълумотларга ишлов беришни амалга оширувчи давлат органи, жисмоний ва (ёки) юридик шахс;
> учинчи шахс — субъект, мулкдор ва (ёки) оператор бўлмаган, аммо шахсга доир маълумотларга ишлов бериш бўйича ҳолатлар ёки муносабатлар орқали улар билан боғлиқ бўлган ҳар қандай шахс.
>
> **ru:** персональные данные — зафиксированная на электронном, бумажном и (или) ином материальном носителе информация, относящаяся к определенному физическому лицу или дающая возможность его идентификации;
> обработка персональных данных — реализация одного или совокупности действий по сбору, систематизации, хранению, изменению, дополнению, использованию, предоставлению, распространению, передаче, обезличиванию и уничтожению персональных данных;
> оператор базы персональных данных (оператор) — государственный орган, физическое и (или) юридическое лицо, осуществляющее обработку персональных данных;
> третье лицо — любое лицо, не являющееся субъектом, собственником и (или) оператором, но связанное с ними обстоятельствами или отношениями по обработке персональных данных.

**Art. 5 — principles**
> **uz:** шахсга доир маълумотларга ишлов бериш мақсадлари ва усулларининг қонунийлиги; шахсга доир маълумотларнинг аниқлиги ва ишончлилиги; шахсга доир маълумотларнинг махфийлиги ва ҳимоя қилинганлиги;
> **ru:** законность целей и способов обработки персональных данных; точность и достоверность персональных данных; конфиденциальность и защищенность персональных данных;

**Art. 10 — collection (parts 1 and 3)**
> **uz:** Шахсга доир маълумотлар базаси мулкдор ва (ёки) оператор, шунингдек учинчи шахс томонидан амалга ошириладиган вазифаларни бажариш учун зарур ҳамда етарли бўлган шахсга доир маълумотларни йиғиш йўли билан шакллантирилади. … Шахсга доир маълумотларни сақлаш муддати уларни йиғиш ва уларга ишлов бериш мақсадига эришиш санаси билан белгиланади.
> **ru:** База персональных данных формируется путем сбора персональных данных, необходимых и достаточных для выполнения задач, осуществляемых собственником и (или) оператором, а также третьим лицом. … Срок хранения персональных данных определяется датой достижения целей их сбора и обработки.

**Art. 12 part 2 — use only for declared purposes**
> **uz:** Мулкдор, оператор ва учинчи шахс томонидан шахсга доир маълумотлардан фойдаланиш бу маълумотларнинг зарур даражада ҳимоя қилинишини таъминлаш шарти билан фақат ушбу шахсга доир маълумотларни йиғиш бўйича илгари билдирилган мақсадлар учун амалга оширилади.
> **ru:** Использование персональных данных собственником, оператором и третьим лицом осуществляется только для ранее заявленных целей их сбора, при условии обеспечения необходимого уровня защищенности персональных данных.

**Arts. 13 and 14 — provision and dissemination**
> **uz:** Шахсга доир маълумотларни муайян шахсга ошкор этишга қаратилган ҳаракатлар шахсга доир маълумотларни бериш ҳисобланади. … Шахсга доир маълумотларни номуайян доирадаги шахсларга ошкор этишга, шу жумладан шахсга доир маълумотларни оммавий ахборот воситаларида ҳаммага маълум қилишга, Интернет жаҳон ахборот тармоғига жойлаштиришга ёки шахсга доир маълумотлардан бирор-бир бошқа усул билан фойдаланиш имконини беришга қаратилган ҳаракатлар шахсга доир маълумотларни тарқатишдир.
> **ru:** Предоставлением персональных данных являются действия, направленные на раскрытие персональных данных конкретному лицу. … Распространением персональных данных являются действия, направленные на раскрытие персональных данных неопределенному кругу лиц, в том числе обнародование персональных данных в средствах массовой информации, размещение во Всемирной информационной сети Интернет или предоставление доступа к персональным данным каким-либо иным способом.

**Art. 15 — cross-border transfer (V-09)**
> **uz:** Шахсга доир маълумотларни мулкдор ва (ёки) оператор томонидан Ўзбекистон Республикаси ҳудудидан ташқарига узатиш шахсга доир маълумотларни трансчегаравий узатишдир.
> Шахсга доир маълумотларни трансчегаравий узатиш шахсга доир маълумотлар субъектларининг ҳуқуқлари бир хилда ҳимоя қилинишини таъминловчи чет давлатлар ҳудудига амалга оширилади.
> Шахсга доир маълумотларнинг бир хилда ҳимоя қилинишини таъминламайдиган чет давлатлар ҳудудига шахсга доир маълумотларни трансчегаравий узатиш қуйидаги ҳолларда амалга оширилиши мумкин:
> субъектнинг ўз шахсга доир маълумотларини трансчегаравий узатиш бўйича розилиги мавжуд бўлганда;
> Ўзбекистон Республикасининг конституциявий тузумини ҳимоя қилиш, жамоат тартибини сақлаш, фуқароларнинг ҳуқуқлари ва эркинликларини, аҳолининг соғлиғи ва маънавиятини муҳофаза қилиш зарур бўлганда;
> Ўзбекистон Республикасининг халқаро шартномаларида назарда тутилган ҳолларда.
>
> **ru:** Трансграничной передачей персональных данных является передача персональных данных собственником и (или) оператором за пределы территории Республики Узбекистан.
> Трансграничная передача персональных данных осуществляется на территорию иностранных государств, обеспечивающих адекватную защиту прав субъектов персональных данных.
> Трансграничная передача персональных данных на территорию иностранных государств, не обеспечивающих адекватную защиту персональных данных, может осуществляться в случаях:
> наличия согласия субъекта на трансграничную передачу его персональных данных;
> необходимости защиты конституционного строя Республики Узбекистан, охраны общественного порядка, прав и свобод граждан, здоровья и нравственности населения;
> предусмотренных международными договорами Республики Узбекистан.

(Part 4: transfer may be prohibited or restricted for constitutional order, morals, health, rights, defence and
state security. The list of adequate states is CMR No. 415 — R-10.)

**Art. 18 — grounds for processing**
> **uz:** Шахсга доир маълумотларга ишлов бериш қуйидаги ҳолларда амалга оширилади:
> субъект бу маълумотларга ишлов беришга розилик берганда;
> субъект тараф бўлган шартномани бажариш учун бу маълумотларга ишлов бериш ёки шундай шартнома тузилгунига қадар субъектнинг сўровига биноан чоралар кўриш зарур бўлганда;
> мулкдор ва (ёки) операторнинг қонунчиликда белгиланган мажбуриятларини бажариш учун бу маълумотларга ишлов бериш зарур бўлганда;
> субъектнинг ёки бошқа шахснинг қонуний манфаатларини ҳимоя қилиш учун бу маълумотларга ишлов бериш зарур бўлганда;
> мулкдор ва (ёки) операторнинг ёки учинчи шахснинг ҳуқуқлари ва қонуний манфаатларини амалга ошириш учун ёхуд шахсга доир маълумотлар субъектларининг ҳуқуқлари ва қонуний манфаатлари бузилмаслиги шарти билан ижтимоий аҳамиятга молик мақсадларга эришиш учун бу маълумотларга ишлов бериш зарур бўлганда;
> шахсга доир маълумотларга уларни мажбурий равишда эгасизлантириш шарти билан статистик ёки бошқа тадқиқот мақсадларида ишлов берилганда;
> агар бу маълумотлар ҳамма фойдаланиши мумкин бўлган манбалардан олинган бўлса.
>
> **ru:** Обработка персональных данных осуществляется в следующих случаях:
> согласия субъекта на обработку этих данных;
> необходимости обработки этих данных для выполнения договора, стороной которого является субъект, или принятия мер по запросу субъекта до заключения такого договора;
> необходимости обработки этих данных для исполнения обязательств собственника и (или) оператора, определенных законодательством;
> необходимости обработки этих данных для защиты законных интересов субъекта или другого лица;
> необходимости обработки этих данных для осуществления прав и законных интересов собственника и (или) оператора или третьего лица либо для достижения общественно значимых целей при условии, что при этом не нарушаются права и законные интересы субъектов персональных данных;
> обработки этих данных в статистических или иных исследовательских целях при условии обязательного обезличивания персональных данных;
> если эти данные получены из общедоступных источников.

**Art. 19 — purposes and volume (parts 2, 3, 5, 7)**
> **uz:** Шахсга доир маълумотларга ишлов беришнинг мақсадлари уларни йиғиш чоғида илгари билдирилган мақсадларга, шунингдек мулкдорнинг ва (ёки) операторнинг ҳуқуқ ва мажбуриятларига мувофиқ бўлиши керак.
> Шахсга доир маълумотларга ишлов беришнинг мақсади ўзгарган тақдирда, мулкдор ва (ёки) оператор субъектнинг ўз маълумотларига ўзгарган мақсадга мувофиқ ишлов берилиши учун розилигини олиши керак.
> Шахсга доир маълумотлар базасига киритилиши мумкин бўлган шахсга доир маълумотларнинг ҳажми субъект томонидан ушбу Қонунга мувофиқ белгиланади. Ишлов бериладиган шахсга доир маълумотларнинг ҳажми ва хусусияти уларга ишлов бериш мақсадлари ва усулларига мувофиқ бўлиши керак.
> Шахсга доир маълумотларга ишлов бериш муддати субъектнинг ўз шахсга доир маълумотларига ишлов беришга розилиги амал қиладиган муддатдан ошиб кетмаслиги керак.
>
> **ru:** Цели обработки персональных данных должны соответствовать целям, ранее заявленным при их сборе, а также правам и обязанностям собственника и (или) оператора.
> В случае изменения цели обработки персональных данных собственник и (или) оператор должны получить согласие субъекта на обработку его данных в соответствии с измененной целью.
> Объем персональных данных, который может быть включен в базу персональных данных, определяется субъектом в соответствии с настоящим Законом. Объем и характер обрабатываемых персональных данных должны соответствовать целям и способам их обработки.
> Срок обработки персональных данных не должен превышать срок, в течение которого действует согласие субъекта на обработку его персональных данных.

**Art. 21 — consent (parts 1, 2 and 7)**
> **uz:** Субъект шахсга доир маълумотларга ишлов бериш учун розиликни унинг олинганлиги фактини тасдиқлаш имконини берувчи ҳар қандай шаклда беради.
> Шахсга доир махсус маълумотларга ишлов бериш учун субъектнинг ёзма шаклдаги, шу жумладан электрон ҳужжат тарзидаги розилиги талаб этилади.
> Субъект шахсга доир маълумотларга ишлов бериш учун берилган розиликни ушбу розилик қандай шаклда берилган бўлса, шундай шаклда ёхуд ёзма шаклда, шу жумладан электрон ҳужжат тарзида чақириб олади.
>
> **ru:** Субъект дает согласие на обработку персональных данных в любой форме, позволяющей подтвердить факт его получения.
> Для обработки специальных персональных данных требуется согласие субъекта в письменной форме, в том числе в виде электронного документа.
> Субъект отзывает согласие на обработку персональных данных в той форме, в какой данное согласие было дано, либо в письменной форме, в том числе в виде электронного документа.

(Parts 3–6: consent for minors and incapable persons — by parents, guardians or the legal representative, in
writing.)

**Art. 22 part 1 — information the subject is entitled to**
> **uz:** Субъект ўзининг шахсга доир маълумотларига ишлов беришга тааллуқли бўлган, қуйидагилар кўрсатилган ахборотни олиш ҳуқуқига эга:
> шахсга доир маълумотларга ишлов берилганлиги фактининг тасдиғи;
> шахсга доир маълумотларга ишлов бериш асослари ва мақсадлари;
> шахсга доир маълумотларга ишлов беришда қўлланиладиган усуллар;
> мулкдорнинг ва (ёки) операторнинг номи ҳамда уларнинг (унинг) жойлашган ери (почта манзили), шахсга доир маълумотлардан фойдаланиш имкониятига эга бўлган ёхуд мулкдор ва (ёки) оператор билан тузилган шартнома асосида ёки қонун асосида шахсга доир маълумотлар ўзига ошкор қилиниши мумкин бўлган шахслар ҳақидаги маълумотлар;
> тегишли субъектга тааллуқли бўлган, ишлов бериладиган шахсга доир маълумотларнинг таркиби, уларни олиш манбаи, агар ушбу Қонунда бундай маълумотларни тақдим этишнинг бошқача тартиби назарда тутилган бўлмаса;
> шахсга доир маълумотларга ишлов бериш муддатлари, шу жумладан уларни сақлаш муддатлари;
> ушбу Қонуннинг 30-моддасида назарда тутилган ҳуқуқларнинг субъект томонидан амалга оширилиш тартиби;
> шахсга доир маълумотларнинг амалга оширилган ёки мўлжалланилаётган трансчегаравий узатилиши тўғрисидаги ахборот.
>
> **ru:** Субъект имеет право на получение информации, касающейся обработки его персональных данных, содержащей:
> подтверждение факта обработки персональных данных;
> основания и цели обработки персональных данных;
> применяемые способы обработки персональных данных;
> наименование собственника и (или) оператора и место их (его) нахождения (почтовый адрес), сведения о лицах, которые имеют доступ к персональным данным или которым могут быть раскрыты персональные данные на основании договора, заключенного с собственником и (или) оператором, или на основании закона;
> состав обрабатываемых персональных данных, относящихся к соответствующему субъекту, источник их получения, если иной порядок предоставления таких данных не предусмотрен настоящим Законом;
> сроки обработки персональных данных, в том числе сроки их хранения;
> порядок осуществления субъектом прав, предусмотренных статьей 30 настоящего Закона;
> информацию об осуществленной или предполагаемой трансграничной передаче персональных данных.

(The operator is released from this duty if the subject "was notified earlier" — part 4; a refusal must be sent
in writing within 10 days — part 5.)

**Art. 23 — notice (parts 1 and 2)**
> **uz:** Субъект ўзининг шахсга доир маълумотлари шахсга доир маълумотлар базасига киритилаётганда шахсга доир маълумотларга ишлов бериш мақсадлари, ушбу Қонуннинг 30-моддасида белгиланган ўз ҳуқуқлари ҳақида ёзма шаклда хабардор қилиниши керак.
> Шахсга доир маълумотлар учинчи шахсга берилган тақдирда, мулкдор ва (ёки) оператор бу ҳақда субъектни уч кун ичида ёзма шаклда хабардор қилади.
>
> **ru:** Субъект при включении его персональных данных в базу персональных данных должен быть уведомлен в письменной форме о целях обработки персональных данных, его правах, определенных статьей 30 настоящего Закона.
> В случае передачи персональных данных третьему лицу собственник и (или) оператор в течение трех дней уведомляет в письменной форме об этом субъекта.

**Art. 25 parts 1–2 — special data**
> **uz:** Ирқий ёки ижтимоий келиб чиқишга оид маълумотлар, сиёсий, диний ёки дунёқарашга оид эътиқодлар, сиёсий партиялар ва касаба уюшмаларига аъзолик тўғрисидаги маълумотлар, шунингдек жисмоний ёки руҳий (психик) саломатликка тааллуқли маълумотлар, шахсий ҳаёт ва судланганлик тўғрисидаги маълумотлар шахсга доир махсус маълумотлардир.
> Шахсга доир махсус маълумотларга ишлов бериш тақиқланади, бундан ушбу модданинг учинчи қисмида назарда тутилган ҳоллар мустасно.
> **ru:** Специальными персональными данными являются данные о расовом или социальном происхождении, политических, религиозных или мировоззренческих убеждениях, членстве в политических партиях и профессиональных союзах, а также данные, касающиеся физического или душевного (психического) здоровья, сведения о частной жизни и судимости.
> Обработка специальных персональных данных запрещается, за исключением случаев, предусмотренных частью третьей настоящей статьи.

(Part 3 lists exceptions, incl. written consent and medical services by a health worker bound to protect the data.)

**Art. 26 — biometric and genetic data (parts 1 and 3)**
> **uz:** Субъектнинг анатомик ва физиологик ўзига хос хусусиятларини тавсифловчи шахсга доир маълумотлар биометрик маълумотлардир.
> Субъектнинг шахсини аниқлаш учун фойдаланиладиган биометрик ва генетик маълумотларга фақат мазкур субъектнинг розилиги мавжуд бўлган тақдирда, бундан Ўзбекистон Республикасининг халқаро шартномаларини рўёбга чиқариш, одил судловни амалга ошириш, ижро ишини юритиш билан боғлиқ ҳоллар мустасно, шунингдек қонунчиликда назарда тутилган бошқа ҳолларда ишлов берилиши мумкин.
> **ru:** Биометрическими данными являются персональные данные, характеризующие анатомические и физиологические особенности субъекта.
> Биометрические и генетические данные, которые используются для установления личности субъекта, могут обрабатываться только при наличии согласия данного субъекта, за исключением случаев, связанных с реализацией международных договоров Республики Узбекистан, осуществлением правосудия, исполнительным производством, а также в иных случаях, предусмотренных законодательством.

**Art. 27 part 2 — protection measures**
> **uz:** Мулкдор ва (ёки) оператор, шунингдек учинчи шахс шахсга доир маълумотларни ҳимоя қилиш бўйича қуйидагиларни таъминлайдиган ҳуқуқий, ташкилий ва техник чораларни кўради:
> субъектнинг ўз шахсий ҳаётига аралашувдан ҳимоя қилиниш ҳуқуқи амалга оширилишини;
> шахсга доир маълумотларнинг яхлитлигини ва бут сақланишини;
> шахсга доир маълумотларнинг махфийлигига риоя этилишини;
> шахсга доир маълумотларга қонунга хилоф равишда ишлов берилишининг олди олинишини.
> **ru:** Собственник и (или) оператор, а также третье лицо принимают правовые, организационные и технические меры по защите персональных данных, обеспечивающие:
> реализацию права субъекта на защиту от вмешательства в его частную жизнь;
> целостность и сохранность персональных данных;
> соблюдение конфиденциальности персональных данных;
> предотвращение незаконной обработки персональных данных.

**Art. 28 — confidentiality**
> **uz:** Мулкдор ва (ёки) оператор ҳамда шахсга доир маълумотлардан фойдаланишга рухсат олган бошқа шахслар субъектнинг розилигисиз шахсга доир маълумотларни учинчи шахсларга ошкор этмаслиги ва тарқатмаслиги шарт.
> **ru:** Собственник и (или) оператор и иные лица, получившие доступ к персональным данным, обязаны не раскрывать и не распространять персональные данные без согласия субъекта.

(Part 1 defines confidentiality as the duty not to disclose «без согласия субъекта или наличия иного законного
основания» — "without the subject's consent or another legal ground".)

**Art. 30 part 1 — subject's rights (selected)**
> **uz:** ўз шахсга доир маълумотларига ишлов бериш учун розилик бериш ва бундай розиликни чақириб олиш, бундан ушбу Қонунда назарда тутилган ҳоллар мустасно;
> агар шахсга доир маълумотлар тўлиқ бўлмаса, эскирган, ноаниқ бўлса, қонунга хилоф равишда олинган бўлса ёки ишлов бериш мақсадлари учун зарур бўлмаса, мулкдордан ва (ёки) оператордан ўзининг шахсга доир маълумотларига ишлов беришни вақтинча тўхтатиб туришни талаб қилиш ҳуқуқига эга.
> **ru:** дать согласие на обработку своих персональных данных и отозвать такое согласие, кроме случаев, предусмотренных настоящим Законом;
> требовать от собственника и (или) оператора временного приостановления обработки своих персональных данных, в случае, если персональные данные являются неполными, устаревшими, неточными, незаконно полученными или не являются необходимыми для целей обработки.

(Also: to know whether the operator holds their data, to get information on processing on request, to complain
to the authorized body or court.)

**Art. 31 — operator's duties and processors (selected)**
> **uz:** ўзи вазифаларини бажариш учун зарур ва етарли бўлган шахсга доир маълумотлар таркибини тасдиқлаши;
> қонунчиликда назарда тутилган ҳолларда субъектнинг ўз шахсга доир маълумотларига ишлов бериш учун розилиги олинганлиги далилини тақдим этиши;
> субъектнинг шахсга доир маълумотларига ишлов беришни вақтинча тўхтатиш ва (ёки) уларни йўқ қилиш учун субъект томонидан ҳужжатларни электрон тарзда бериш имкониятини таъминлаши;
> Мулкдор ва (ёки) оператор шахсга доир маълумотларга ишлов беришни қуйидаги ҳолларда учинчи шахсга топширишга ҳақли:
> субъектнинг ёзма шаклдаги, шу жумладан электрон ҳужжат тарзидаги розилиги мавжуд бўлган тақдирда;
> **ru:** утверждать состав персональных данных, необходимый и достаточный для выполнения ими задач;
> представлять доказательство получения согласия субъекта на обработку его персональных данных в случаях, предусмотренных законодательством;
> обеспечить возможность подачи субъектом документов в электронном виде на временное приостановление обработки и (или) уничтожение его персональных данных;
> Собственник и (или) оператор вправе поручить обработку персональных данных третьему лицу в случаях:
> наличия согласия субъекта в письменной форме, в том числе в виде электронного документа;

(The other two cases: performance of a contract between the owner and the subject; cases provided by law. Last
part: the operator appoints a responsible unit or official.)

### 3. By-laws

#### 3.1 Model procedure of processing personal data (Minister of Justice order No. 20-mh of 15.11.2023, reg. No. 3478)

Official text in Uzbek only («Текст акта приводится на узбекском языке» on the Russian page).
https://lex.uz/docs/6663967 (Cyrillic) · https://lex.uz/docs/-6663967 (Latin) · https://lex.uz/ru/docs/6668412
(Russian page, no translation). In force on official publication.

| Item | Uzbek (verbatim) | Meaning (our translation) |
|---|---|---|
| 1 (definition) | «— субъектнинг анатомик ва физиологик ўзига хос хусусиятларини тавсифловчи шахсга доир маълумотлар (бармоқ излари, юз кўриниши, кўз гавҳари, овоз хусусиятлари ва бошқалар);» | Biometric data includes **fingerprints, face image, iris, voice** — a selfie is a face image |
| 8 | «Шахсга доир маълумотларга ишлов бериш мулкдор ва (ёки) оператор, шунингдек учинчи шахс томонидан субъект ёки унинг қонуний вакилининг розилиги билан амалга оширилади, ушбу Намунавий тартибнинг 4-банди» (… «учинчи — саккизинчи хатбошларида» … «назарда тутилган ҳоллар бундан мустасно») | Consent is the default; the other grounds of item 4 (= art. 18) are exceptions |
| 9 part 2 | «Офертада (оммавий шартномада) шахсга доир маълумотларга ишлов беришнинг мақсадлари аниқ кўрсатилган тақдирда, офертани (оммавий шартномани) қабул қилиш (тасдиқлаш) субъектнинг шахсга доир маълумотларга ишлов беришга розилиги деб ҳисобланади.» | Accepting a public offer that clearly states the purposes **is consent** |
| 9 part 3 | «Субъектнинг мулкдор ва (ёки) операторнинг хизматларидан фойдаланиш учун белгиланган талаб ва шартларга розилик бериши мулкдор ва (ёки) оператор томонидан субъектнинг шахсга доир маълумотларига ишловга беришга розилиги ҳисобланади.» | Agreeing to the service's terms of use **is consent** |
| 11 | «Шахсга доир маълумотларга ишлов бериш учун субъектнинг розилигида қуйидаги маълумотлар кўрсатилиши лозим:» — 1) operator's name and TIN; 2) subject's name and ID document; 3) purposes; 4) list of data; 5) term of consent; 6) «шахсга доир маълумотларни учинчи шахсларга бериш ва (ёки) ушбу маълумотларни трансчегаравий узатишга розилиги;» 7) publication in public sources; 8) other | What a consent must contain — a model for a consent text on a form |
| 10 | «Субъект ёки унинг қонуний вакили шахсга доир маълумотларга ишлов бериш тўғрисидаги розилигини исталган вақтда қайтариб олиш ҳуқуқига эга.» | Consent can be withdrawn at any time (data destroyed by the next working day — part 2) |
| 30, point 8 | «субъектнинг розилиги мавжуд бўлганда ҳамма фойдаланиши мумкин бўлмаган шахсга доир маълумотларни хавфсиз алоқа каналлари ва (ёки) шифрлаш воситалари орқали бошқа шахсларга бериши, бундан қонунчилик ҳужжатлари билан назарда тутилган ҳоллар мустасно;» | Non-public PD is passed to others only over **secure channels and/or encryption** |
| 30, point 12 | «шахсга доир маълумотларга ишлов бериш ва уларни ҳимоя қилиш бўйича мулкдор ва (ёки) оператор сиёсатини белгилайдиган ички ҳужжатларни тасдиқлаши;» | The operator approves **internal** documents setting its policy (not a public-policy duty) |

#### 3.2 CMR No. 71 of 08.02.2020 — State Register (V-04)

Source: https://lex.uz/docs/4729730 (uz) · https://lex.uz/ru/docs/4732190 (ru); title re-worded by CMR No. 821 of
24.12.2025 ("administrative regulation of the public service of keeping the State Register").

| Item | uz | ru |
|---|---|---|
| 9 | «Ушбу Регламентда назарда тутилган давлат хизмати бепул кўрсатилади.» | «Государственная услуга, предусмотренная настоящим Регламентом, оказывается бесплатно.» |
| 10 | «Ваколатли орган сўровнома келиб тушган кундан кейин беш иш куни мобайнида шахсга доир маълумотлар базасини Давлат реестрида рўйхатдан ўтказади ёки рўйхатдан ўтказишни рад этади.» | «Уполномоченный орган в течение пяти рабочих дней со дня поступления анкеты регистрирует базу персональных данных в Государственном реестре или отказывает в регистрации.» |
| 19 | «Давлат реестри маълумотлари юридик ва жисмоний шахсларнинг улар билан танишиши учун очиқ ҳисобланади.» «Мулкдор ва (ёки) операторнинг Давлат реестри рўйхатидан ўтказилгани ҳақидаги маълумотлар ушбу маълумотлар базасининг қайд рақамини Давлат реестрини юритиш ахборот тизимига киритиш орқали автоматик тарзда олинади.» | «Сведения Государственного реестра являются открытыми для ознакомления юридических и физических лиц.» «Сведения о регистрации собственника и (или) оператора в Государственном реестре получаются автоматически путем ввода регистрационного номера базы данных в информационную систему ведения Государственного реестра.» |

→ A check is possible **only by registration number**, not by company name (as written). The register site
pd.gov.uz has a "certificate status check" (Guvohnoma holatini tekshirish) menu item (archived page of
26.07.2021). Probo cannot check registration from a URL — at most it can ask the client for the number.

#### 3.3 Other by-laws found (not quoted in full)

- CMR No. 570 of 05.10.2022 — regulations on determining the **protection level** of PD and on storing biometric
  and genetic data outside databases (https://lex.uz/docs/6225462). Relevant to level-3 audits, not to a passive
  website scan.
- Minister of Justice order No. 19-mh (reg. No. 3477 of 15.11.2023) — model procedure for the operator's
  responsible unit or person (https://lex.uz/docs/6663969).

### 4. What a website notice must contain — law vs `ELEMENTS` in `backend/qalqon/llm/policy.py`

| `ELEMENTS` key | Norm | Status |
|---|---|---|
| `operator` | art. 22 (name and postal address); model procedure item 11, 1) | required (art. 22) |
| `purposes` | art. 22 (grounds and purposes); **art. 23 part 1** (notice of purposes) | **required at collection** |
| `data_categories` | art. 22 (composition of data, source); item 11, 4) | required (art. 22) |
| `consent` | art. 21 (form, withdrawal); art. 30 | required (how to give / withdraw) |
| `retention` | art. 22 (terms of processing and storage); art. 10 part 3 | required (art. 22) |
| `recipients` | art. 22 (persons who have access or to whom data may be disclosed); art. 23 part 2 | required (art. 22) |
| `cross_border` | art. 22 (last item: transfer done or planned); item 11, 6) | required (art. 22) |
| `subject_rights` | art. 22 (how to use the art. 30 rights); **art. 23 part 1** | **required at collection** |
| `contact` | art. 22 (postal address); art. 31 (electronic filing of requests to stop processing) | required in substance |
| `cookies` | — (no norm names cookies) | good practice only (V-08) |
| *missing:* `legal_grounds` | art. 22: «асослари ва мақсадлари» / «основания и цели» | **add** (Q-L12) |
| *missing:* `methods` | art. 22: processing methods | optional, add if cheap |

So PD-POL-02 can treat purposes and subject rights as the core (art. 23 notice), the rest as art. 22 completeness.

### 5. V-08 — are IP addresses and cookie IDs personal data? (interpretation)

- Text: art. 4 «муайян жисмоний шахсга тааллуқли бўлган ёки уни идентификация қилиш имконини берадиган … ахборот»
  / «информация, относящаяся к определенному физическому лицу или дающая возможность его идентификации».
  The test is identifiability, in any form of record.
- No law or by-law read names IP addresses, cookies, device IDs or online identifiers (ZRU-547, model procedures
  3477 and 3478, CMR No. 71, CMR No. 570). Web search for an official explanation by the authorized body found none
  (21.11.2026).
- Practice signal only: the Ministry of Justice's own site policy (gov.uz) lists "IP addresses" among the data it
  collects from the contact form and protects under the personal data law
  (https://gov.uz/ru/mj/pages/maxfiylik-siyosati) — a website text, not a legal act.
- Reading: a cookie ID or advertising ID is designed to single out one browser/person over time; combined with
  an IP address, page history and, often, a phone or e-mail entered later, it "enables identification" → personal
  data in the hands of a tracker network. A one-off IP in a server log is weaker. **Status: NOT VERIFIED
  (interpretation)** — so tracker findings stay 🟡, with the wording "visitor identifiers that may be personal
  data".

## Fact check (passport §11.4)

| ID | Claim | Status | Correct wording | Source |
|---|---|---|---|---|
| V-01 | ZRU-547 of 02.07.2019, in force 01.10.2019; consent art. 21, cross-border art. 15, registration art. 20, biometrics art. 26, liability art. 33 | **CONFIRMED** | Same; plus: grounds art. 18, notice art. 23, information art. 22, confidentiality art. 28. Texts quoted in section 2 | https://lex.uz/docs/4396419 ; https://lex.uz/ru/docs/4396428 |
| V-04 | A State Register exists; is there a public search? | **CONFIRMED (partly)** | Register data are open; status is obtained by entering the **registration number** in the register's information system (CMR No. 71 item 19). No search by company name in the text | https://lex.uz/docs/4729730 ; https://lex.uz/ru/docs/4732190 |
| V-08 | IP address and cookie ID are personal data | **NOT VERIFIED (interpretation)** | No act names them; by art. 4 they are PD when they enable identification (typical for tracker IDs) | section 5 |
| V-09 | Cross-border transfer rules | **CONFIRMED** | Art. 15: to adequate states; to others only with the subject's consent, for constitutional order / public order / health reasons, or under a treaty; read with art. 27¹ part 3 and CMR No. 415 (R-10). Model procedure items 20–21 repeat art. 15 | https://lex.uz/docs/4396419 ; R-10 |
| new | Consent is not the only ground; accepting an offer or service terms counts as consent | **CONFIRMED** | Art. 18 (seven grounds); model procedure item 9 parts 2–3 | https://lex.uz/docs/4396419 ; https://lex.uz/docs/6663967 |
| new | The law requires a public privacy policy on the website | **REFUTED (as worded)** | No such norm; the duties are notice (art. 23) and information on request (art. 22); the model procedure requires an internal policy (item 30, point 12) | sections 2–3 |

## Feature ideas (passport §10 format)

- F-45 · Consent-text generator from model procedure item 11 (operator + TIN, purposes, data list, term, third
  parties / cross-border) in uz/ru, pre-filled from the scan (recipients and countries we saw) · turns a 🟡
  PD-CNS-01 into a concrete fix · S · R-01 · Final (fits F-04)
- F-46 · "Offer as consent" check: if the form page links to a public offer / terms that state the purposes,
  the PD-CNS-01 finding says so and drops to ⚪ (model procedure item 9) · fewer false findings (D-019) · M ·
  R-01 · Roadmap (needs the LLM to read the offer — Role 1)

## Questions for the team / contradictions with the passport

- **Q-L12 (Role 1).** Add `legal_grounds` («асослари» — art. 22) to `ELEMENTS` in `backend/qalqon/llm/policy.py`;
  `methods` is optional. `cookies` has no legal norm — keep it, but never as a 🔴/🟡 reason on its own.
- **Q-L13 (Role 1, passport §5).** PD-CNS-01 is 🔴 in the passport draft. By art. 18 and model procedure item 9 a
  form without a checkbox can be lawful (request before a contract, accepted offer or terms). `rules/PD-CNS-01.yaml`
  sets it to 🟡 with this reason. The demo story stays: "the site collects data without visible consent or notice".
- **Q-L14 (Role 2, next).** The model procedure exists only in Uzbek; if we quote it in Russian reports, mark the
  Russian as our translation.

## Sources

- ZRU-547: https://lex.uz/docs/4396419 (official, Cyrillic) · https://lex.uz/docs/-4396419 (Latin) · https://lex.uz/ru/docs/4396428 (Russian)
- Model procedure of processing (order No. 20-mh, reg. 3478): https://lex.uz/docs/6663967 · https://lex.uz/docs/-6663967 · https://lex.uz/ru/docs/6668412
- Model procedure for the responsible person (order No. 19-mh, reg. 3477): https://lex.uz/docs/6663969 · https://lex.uz/ru/docs/6663971
- CMR No. 71 of 08.02.2020: https://lex.uz/docs/4729730 · https://lex.uz/ru/docs/4732190
- CMR No. 570 of 05.10.2022: https://lex.uz/docs/6225462
- pd.gov.uz (archived 26.07.2021): https://web.archive.org/web/20210726115936/https://pd.gov.uz/spoiler/
- Ministry of Justice site policy (practice signal for V-08): https://gov.uz/ru/mj/pages/maxfiylik-siyosati
- Related: `research/legal-27-1-2026.md` (R-10), `research/legal-liability.md` (R-02), `backend/qalqon/llm/policy.py`
