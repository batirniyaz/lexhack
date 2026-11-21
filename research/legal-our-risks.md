# Probo's own legal risks (R-08)
- Author: Alii, Role 2 (legal research), prepared with Claude Code
- Date/time: 21.11.2026, 05:40
- Based on passport version: 0.14
- Method:
  - **Finding the norms.** I searched the local lex.uz corpus (77,047 acts, crawled 9–10.11.2026) for the articles.
  - **Live check.** Each quote below was then re-read on **live lex.uz on 21.11.2026** (Python/httpx; official Uzbek
    text in Cyrillic plus the LexUZ Russian text). Acts checked: the Constitution, the Criminal Code, the Administrative
    Code, ZRU-764 (cybersecurity), ZRU-701 (licensing), CMR No. 675 (legal consulting), Law 400-I (access to
    information), Law 560-II (informatization), the Civil Code, ZRU-42 (copyright) and ZRU-547.
  - **lex.uz terms.** I read the lex.uz terms pages (`/ru/axborot`, `/uz/axborot`).
  - **DPF list.** I searched the EU-US DPF list in a browser. The search works (Cloudflare is found). Anthropic is not
    found.
  - **Our code.** I checked what Probo actually does: `backend/qalqon/scanner/crawler.py` (user agent),
    `config.py` (20 pages), `llm/client.py` (Anthropic API), `deploy/README.md` (Cloudflare tunnel) and passport D-024.
- Confidence: **high** for the texts, lists and amounts. **Medium** for the reading of how they apply to Probo. This is a
  researcher's reading, not a lawyer's opinion.

## Conclusions

1. **A passive scan of public pages is lawful and needs no consent from the site owner.** But the active mode on a site
   that is not our client would be a risk, so **D-009 stays**.
   - *Why it is lawful.* Everyone has the right to "seek, receive and disseminate any information" (Constitution art. 33).
     Public information resources are "intended for an unlimited circle of users", and their owners "must ensure equal
     access" to them (Law 560-II art. 11).
   - *What the offences require.* Both offences require **unauthorized** access:
     - Administrative Code art. 155: access "for the purpose of using" a system.
     - Criminal Code art. 278²: unauthorized access that causes destruction, blocking, modification, copying or
       interception of information, or disrupts the system.
     A page that its owner published for everyone is not unauthorized access.
   - *Why the active mode is different.* Sending canary data through someone else's form or logging into their
     accounts is not what a public page offers.
2. **New risk — security findings may not be published (ZRU-764 art. 24).** Information about **vulnerabilities**
   found in information systems and resources "may be disclosed **with the permission of the cybersecurity subject**",
   and only after protective measures are taken. It may be used **only to eliminate them**.
   - *What this covers.* SEC-01 (no HTTPS on a PD form) and SEC-02 (missing security headers) are such information.
     PD-DB-01 (a cloud database visible in the page code) is close to it.
   - *What to do.* On scans of sites the user does not own — the public demo, share links and statistics — the details
     of these findings must be hidden (F-47).
3. **New risk — legal consulting is a notified activity.** A commercial company that provides **legal consulting
   services** must:
   - have at least one **legal consultant on staff** (higher legal education, or retraining plus 2 years of legal
     work; a citizen of Uzbekistan if there is only one — CMR No. 675 items 2 and 8);
   - **notify the justice body** before it starts (ZRU-701 annex 3, item 31).
   Working without notification costs the legal entity **25 BCA = 11,000,000 UZS** (ZRU-701 art. 52, annex 4 section
   III item 24; BCA 440,000 UZS from R-02).
   - *Where the line is.* An automated scan report (facts plus references to the law) is a software service.
     Drafting a privacy policy, a consent text or "fixed documents" (business-model-v2 category IV), and a lawyer's
     review (M12), are services named in CMR No. 675 item 4.
   - *What to do.* Sell those services only through a partner legal-consulting firm or an advocate (as M12 already
     plans). Otherwise hire a legal consultant and file the notification first.
4. **No license is needed (V-15 closed).**
   - *The list.* Licensed activities are exactly those in annex 1 of ZRU-701 (art. 13). The only IT entries there are
     cryptographic protection tools and telecom networks. Website checks, compliance audits and vulnerability scanning
     are not in it.
   - *Mandatory cybersecurity examinations.* They apply only to **state bodies' resources and systems and to critical
     information infrastructure** (ZRU-764 art. 18), under the State Security Service.
   - *What this changes for D-008.* The reason for D-008 is **not** a license. The real reasons are art. 24 (disclosure)
     and Criminal Code art. 278² / Administrative Code art. 155 (active probing without permission).
5. **Probo itself is a personal data operator, and its LLM step has a cross-border gap.**
   - *What we process.* IP addresses (rate limits), accounts, and scan artefacts. Screenshots, HTML and HAR of public
     pages can contain names and phone numbers.
   - *Grounds (art. 18).* A contract for clients. For scans: data "obtained from publicly available sources", and
     statistics "with mandatory anonymization".
   - *No registration or localization duty.* Since 27.03.2026 only the art. 27¹ part 2 databases are registered (art.
     20). Our data is not in those three categories.
   - *The gap.* The LLM provider is in the US. The US counts only for EU-US DPF participants (CMR No. 415, R-10), and
     **Anthropic is not on the DPF list** (checked 21.11.2026). Personal data inside policy texts sent to the LLM is
     therefore a transfer to a non-listed recipient.
   - *Why it matters.* Unlawful processing of personal data **with AI technologies** is a separate offence: 50–100 BCA
     with confiscation (Administrative Code art. 46² part 2, R-02).
   - *What to do.* Redact personal data before the LLM call (F-48), and send no account data to the LLM.
6. **Two smaller risks: reputation and lex.uz content.**
   - *Reputation.* The Civil Code protects a legal entity's business reputation, and **the publisher must prove that the
     information is true** (art. 100). Three things are our defence:
     - the evidence package (hashes, signature, time, vantage point);
     - the wording "signs of violation" (D-004);
     - no names in public (D-003).
   - *Law texts.* Official documents and their official translations are not copyright objects (ZRU-42 art. 8), so we
     may quote them.
   - *lex.uz terms.* They allow personal use only. Copying or distributing the site's data for profit needs the
     Center's **written permission**. Other use of information **"except the text of normative legal acts"** is allowed
     with a link.
   - *What follows.* Short quotes of official texts with a link are fine. The LexUZ Russian translation is marked
     "unofficial" and should be labelled as such. Bulk use of the lex.uz database in a paid service needs the
     Center's written permission (Q-L19).

## Data

### 1. What Probo does, and how the law sees it

| What Probo does (from the code / passport) | Whose data | Norm | Assessment |
|---|---|---|---|
| Opens up to 20 public pages in Chromium with a normal Chrome user agent; DNS, certificates | site owner's public resource | Constitution 33; Law 560-II art. 11; Law 400-I art. 3 | lawful; no consent needed |
| Records requests, cookies, screenshots, HTML, HAR of those pages | public content; may contain names, phones, e-mails published on the site | ZRU-547 art. 18 (public sources), art. 10 part 3 (retention by purpose) | lawful if kept only as long as needed (F-50) |
| Active mode: fills forms with canary data, logs in (D-009) | the site's systems | Adm. Code 155; Criminal Code 278², 278⁴ | **only on client sites with written consent** |
| Shows SEC-01/02, PD-DB-01 in reports and share links | the site's weaknesses | ZRU-764 art. 24 | **owner only** (F-47) |
| Sends policy text to the LLM (Anthropic API, US) | PD inside the text, if any | ZRU-547 art. 15, 27¹ part 3; CMR 415 (US = DPF only); Adm. Code 46² part 2 | redact first (F-48) |
| Public demo, 6 scans/hour per IP, 100/day (D-024) | visitors' IP addresses | ZRU-547 art. 4, 18 (legitimate interest); V-08 | operator duties apply (§5) |
| Anonymized statistics (`/api/stats`) | none after anonymization | ZRU-547 art. 18 (statistics with anonymization) | lawful |
| Quotes the law from lex.uz  | — | ZRU-42 art. 8; lex.uz terms | quotes OK; bulk database use needs permission |
| "Fixed documents", consent and policy generators, lawyer review (business model, F-45, M12) | client | ZRU-701 annex 3 item 31; CMR No. 675 | legal consulting → partner or notify |

### 2. Verbatim norms (live lex.uz, 21.11.2026)

**Constitution, art. 33 part 2 — right to information** · https://lex.uz/docs/6445145 · https://lex.uz/ru/docs/6445147
> **uz:** Ҳар ким исталган ахборотни излаш, олиш ва тарқатиш ҳуқуқига эга.
> **ru:** Каждый имеет право искать, получать и распространять любую информацию.

**Constitution, art. 31 part 3 — personal data** (the right Probo itself must respect)
> **uz:** Ҳар ким ўз шахсига доир маълумотларнинг ҳимоя қилиниши ҳуқуқига, шунингдек нотўғри маълумотларнинг тузатилишини, ўзи тўғрисида қонунга хилоф йўл билан тўпланган ёки ҳуқуқий асосларга эга бўлмай қолган маълумотларнинг йўқ қилинишини талаб қилиш ҳуқуқига эга.
> **ru:** Каждый имеет право на защиту своих персональных данных, а также требовать исправления недостоверных данных, уничтожения данных, собранных о нем незаконным путем или более не имеющих правовых оснований.

**Law 400-I "On guarantees and freedom of access to information", art. 3** · https://lex.uz/docs/1319 · https://lex.uz/ru/docs/2118
> **uz:** Ҳар кимнинг ахборотни излаш, олиш, тадқиқ этиш, узатиш ва тарқатиш ҳуқуқи давлат томонидан ҳимоя қилинади.
> **ru:** Государство защищает права каждого на поиск, получение, исследование, передачу и распространение информации.

**Law 560-II "On informatization", art. 11 parts 2 and 4 — public information resources** · https://lex.uz/docs/83472 · https://lex.uz/ru/docs/82956
> **uz:** Чекланмаган доирадаги фойдаланувчилар учун мўлжалланган ахборот ресурслари ҳамма эркин фойдаланиши мумкин бўлган ахборот ресурсларидир. … Ахборот ресурсларининг мулкдорлари ва эгалари ҳамма эркин фойдаланиши мумкин бўлган ахборот ресурсларидан юридик ҳамда жисмоний шахсларнинг тенг ҳуқуқ асосида эркин тарзда фойдаланишини таъминлаши керак.
> **ru:** Общедоступными информационными ресурсами являются информационные ресурсы, предназначенные для неограниченного круга пользователей. … Собственники и владельцы информационных ресурсов должны обеспечить равноправный доступ юридических и физических лиц к общедоступным информационным ресурсам.

**Administrative Code, art. 155 — use of information** (parts 1 and 3; sanctions as amended by ZRU-586 of 03.12.2019) · https://lex.uz/docs/97664 · https://lex.uz/ru/docs/97661
> **uz:** Ахборот тизимидан фойдаланиш мақсадида унга рухсатсиз кириб олишда ифодаланган ахборот ва ахборот тизимларидан фойдаланиш қоидаларини бузиш — фуқароларга базавий ҳисоблаш миқдорининг учдан бир қисмидан бир бараваригача, мансабдор шахсларга эса — бир бараваридан уч бараваригача миқдорда жарима солишга сабаб бўлади. … Юридик ва жисмоний шахсларнинг ахборот тизимларини халқаро ахборот тармоқларига қонунга хилоф равишда улаш, бу тармоқларга тегишли ҳимоя чораларини кўрмасдан уланиш, худди шунингдек улардан маълумотларни қонунга хилоф равишда олиш — фуқароларга базавий ҳисоблаш миқдорининг икки бараваридан беш бараваригача, мансабдор шахсларга эса — беш бараваридан етти бараваригача миқдорда жарима солишга сабаб бўлади.
> **ru:** Нарушение правил пользования информацией и информационными системами, выразившееся в несанкционированном доступе в информационную систему с целью ее использования, — влечет наложение штрафа на граждан от одной третьей до одной, а на должностных лиц — от одной до трех базовых расчетных величин. … Незаконное включение информационных систем юридических и физических лиц в международные информационные сети, включение в них без принятия необходимых мер защиты, а равно незаконное получение от них информации — влечет наложение штрафа на граждан от двух до пяти, а на должностных лиц — от пяти до семи базовых расчетных величин.

**Criminal Code, art. 278² — unauthorized access to computer information** (part 1) · https://lex.uz/docs/111453 · https://lex.uz/ru/docs/111457
> **uz:** Компьютер ахборотидан, яъни ахборот-ҳисоблаш тизимлари, тармоқлари ва уларнинг таркибий қисмларидаги ахборотлардан қонунга хилоф равишда (рухсатсиз) фойдаланиш, агар ушбу ҳаракат ахборотнинг йўқ қилиб юборилиши, тўсиб қўйилиши, модификациялаштирилиши, ундан нусха кўчирилиши ёхуд унинг қўлга киритилишига, электрон ҳисоблаш машиналари, электрон ҳисоблаш машиналари тизими ёки уларнинг тармоқлари ишининг бузилишига сабаб бўлса, — базавий ҳисоблаш миқдорининг юз бараваригача миқдорда жарима ёки уч йилгача муайян ҳуқуқдан маҳрум қилиш ёхуд бир йилгача ахлоқ тузатиш ишлари билан жазоланади.
> **ru:** Незаконный (несанкционированный) доступ к компьютерной информации, то есть информации в информационно-вычислительных системах, сетях и их составных частях, если это действие повлекло уничтожение, блокирование, модификацию, копирование либо перехват информации, нарушение работы электронно-вычислительных машин, системы электронно-вычислительных машин или их сети, — наказывается штрафом до ста базовых расчетных величин или лишением определенного права до трех лет либо исправительными работами до одного года.

(Art. 278⁵ "computer sabotage" needs the **intentional** disabling of equipment or destruction of a system, so it is
far from 20 pages at a slow pace. Art. 278⁴ covers entering knowingly false information into a computer system that
causes large damage: one more reason why canary data goes only into client sites.)

**ZRU-764 "On cybersecurity" of 15.04.2022, art. 24 — disclosure of vulnerabilities** · https://lex.uz/docs/5960604 · https://lex.uz/ru/docs/5960609
> **uz:** Ахборот тизимлари ва ресурсларида аниқланган заифликлар, кибертаҳдидлар, киберҳужумлар ҳамда бошқа бузғунчилик ҳаракатлари тўғрисидаги, шунингдек ахборотлаштириш объектлари ҳақидаги ахборот уларни ҳимоя қилиш бўйича тегишли чоралар кўрилганидан кейин киберхавфсизлик субъектининг рухсати билан ошкор қилиниши мумкин.
> Аниқланган кибертаҳдидлар ва заифликлар тўғрисидаги ахборотдан фақат уларни бартараф этиш ҳамда қонунга хилоф ҳаракатларнинг олдини олиш учун фойдаланилиши керак.
> **ru:** Информация о выявленных в информационных системах и ресурсах уязвимостях, киберугрозах, кибератаках и других подрывных действиях, а также об объектах информатизации может быть раскрыта с разрешения субъекта кибербезопасности после принятия соответствующих мер по их защите.
> Информация о выявленных киберугрозах и уязвимостях должна быть использована исключительно для их устранения и предотвращения незаконных действий.

**ZRU-764, art. 18 part 2 — who must pass a cybersecurity examination**
> **uz:** Қуйидагилар киберхавфсизлик талабларига мувофиқлик юзасидан мажбурий тартибда экспертизадан ўтказилиши лозим: давлат органларининг ахборот ресурслари; давлат органларининг ахборот тизимлари; муҳим ахборот инфратузилмаси объектлари тоифасига киритилган ахборот тизимлари.
> **ru:** Экспертизе на соответствие требованиям кибербезопасности в обязательном порядке подлежат: информационные ресурсы государственных органов; информационные системы государственных органов; информационные системы, включенные в категорию объектов критической информационной инфраструктуры.

**ZRU-701 "On licensing, permitting and notification procedures", art. 13 part 1** · https://lex.uz/docs/5511879 · https://lex.uz/ru/docs/5511900
> **uz:** Ушбу Қонуннинг 1-иловасида кўрсатилган фаолият турлари фаолиятнинг лицензияланадиган турларидир.
> **ru:** Лицензируемыми видами деятельности являются виды деятельности, указанные в приложении № 1 к настоящему Закону.

Annex 1, the only IT-related licenses (full search of the live text for кибер / криптограф / защиты информации /
информационной безопасности / аудит / программн / интернет):
- «Лицензия для деятельности по разработке, производству и реализации средств криптографической защиты информации»
- «Лицензия на проектирование, строительство, эксплуатацию и оказание услуг сетей телекоммуникаций»

**ZRU-701 annex 3, item 31 — notification** (columns: notification · activity · authority)
> **uz:** Юридик маслаҳат хизматларини кўрсатувчи тижорат ташкилоти фаолиятини бошлаганлиги ёки тугатганлиги ҳақида хабарнома | Юридик маслаҳат хизматларини кўрсатиш. | Қорақалпоғистон Республикаси Адлия вазирлиги, вилоятлар ва Тошкент шаҳар адлия бошқармалари
> **ru:** Уведомление о начале или прекращении деятельности коммерческой организации, оказывающей юридические консультационные услуги | Оказание юридических консультационных услуг. | Министерство юстиции Республики Каракалпакстан, управления юстиции областей и города Ташкента

**ZRU-701 annex 4, section III, item 24 — fine for working without notification** (heading: «Занятие деятельностью без
уведомления уполномоченного органа…», amounts «в базовых расчетных величинах»)
> **uz:** Юридик маслаҳат хизматларини кўрсатувчи тижорат ташкилоти фаолиятини бошлаганлик ёки тугатганлик ҳақида хабарнома | 25
> **ru:** Уведомление о начале или прекращении деятельности коммерческой организации, оказывающей юридические консультационные услуги | 25

**ZRU-701 art. 52 part 2 — who is fined** (paragraph 2 as amended by ZRU-878, in force 17.02.2024)
> **uz:** Лицензиялаш, рухсат бериш ва хабардор қилиш тартиб-таомиллари соҳасидаги қуйидаги ҳуқуқбузарликларни содир этганлик учун юридик шахсларга жарималар солинади: фаолият билан лицензиясиз, рухсат этиш хусусиятига эга ҳужжатсиз ва ваколатли органни хабардор этмасдан шуғулланиш…
> **ru:** За совершение следующих правонарушений в области лицензирования, разрешительных и уведомительных процедур на юридических лиц налагаются штрафы: занятие деятельностью без лицензии, документа разрешительного характера и без уведомления уполномоченного органа…

**CMR No. 675 of 17.08.2018 — Regulation on legal consulting services of commercial organizations** (last change CMR
No. 350 of 30.06.2026) · https://lex.uz/docs/3908401 · https://lex.uz/ru/docs/3908803
> **uz (item 2):** юридик маслаҳат хизмати — тижорат ташкилотларининг юридик ва жисмоний шахсларга (кейинги ўринларда мижоз деб аталади) шартнома асосида юридик маслаҳат хизматлари кўрсатиш борасидаги фаолияти;
> юридик маслаҳатчи — олий юридик маълумотга ёки юридик мутахассислик бўйича қайта тайёрлаш курсларини тугатиб белгиланган намунадаги дипломга ва юридик мутахассислик бўйича камида икки йиллик иш стажига эга бўлган ва юридик маслаҳатчилар ташкилоти штатида турган жисмоний шахс.
> **uz (item 4, selected):** бизнесга юридик кўмаклашиш (хизмат кўрсатиш), шу жумладан ташкилотнинг жорий масалалари бўйича маслаҳат бериш; … шартномалар, контрактлар, келишувлар, аризалар, шикоятлар ва бошқа ҳуқуқий ҳужжатлар лойиҳаларини тайёрлаш ва экспертизадан ўтказиш;
> **uz (item 8):** Юридик маслаҳатчилар ташкилотларини ташкил этиш ва фаолият кўрсатишининг мажбурий шарти штатда камида битта юридик маслаҳатчи бўлиши ҳисобланади. Агар штатда фақат битта юридик маслаҳатчи бўлса, у ҳолда у Ўзбекистон Республикаси фуқароси бўлиши лозим.
> **ru (item 2):** юридическое консультирование — деятельность коммерческих организаций по оказанию на договорной основе физическим и юридическим лицам (далее — клиент) юридических консультационных услуг;
> **ru (item 4, selected):** составление и экспертиза проектов договоров, контрактов, соглашений, а также заявлений, жалоб и других документов правового характера;
> **ru (item 8):** Обязательным условием создания и деятельности организаций юридических консультантов является наличие в штате юридического консультанта. В случаях, если в штате имеется только один юридический консультант, то он должен быть гражданином Республики Узбекистан.

(LexUZ marks the Russian of item 2 paragraph 4 "unofficial translation" after CMR No. 350. Annex 2 item 3 still says the
organization starts work after a written notice of entry into the register. The register is kept by the justice bodies
— the same bodies that receive the ZRU-701 notification.)

**Civil Code, art. 100 parts 1 and last — business reputation** · https://lex.uz/docs/111189 · https://lex.uz/ru/docs/111181
> **uz:** Фуқаро ўзининг шаъни, қадр-қиммати ёки ишчанлик обрўсига путур етказувчи маълумотлар юзасидан, башарти бундай маълумотларни тарқатган шахс уларнинг ҳақиқатга тўғри келишини исботлай олмаса, суд йўли билан раддия талаб қилишга ҳақли. … Ушбу моддадаги фуқаронинг ишчанлик обрўсини ҳимоя қилиш тўғрисидаги қоидаси юридик шахснинг ишчанлик обрўсини ҳимоя этишга нисбатан ҳам тегишли йўсинда татбиқ этилади.
> **ru:** Гражданин вправе требовать по суду опровержение порочащих его честь, достоинство или деловую репутацию сведений, если распространивший такие сведения не докажет, что они соответствуют действительности. … Правила настоящей статьи о защите деловой репутации гражданина соответственно применяются к защите деловой репутации юридического лица.

**ZRU-42 "On copyright and related rights", art. 8 — what is not protected** · https://lex.uz/docs/1022944 · https://lex.uz/ru/docs/1023494
> **uz:** Қуйидагилар муаллифлик ҳуқуқи объектлари бўлмайди: расмий ҳужжатлар (қонунлар, қарорлар, тўхтамлар ва шу кабилар), шунингдек уларнинг расмий таржималари;
> **ru:** Не являются объектами авторского права: официальные документы (законы, постановления, решения и т. п.), а также их официальные переводы;

**lex.uz — "Conditions of providing information"** · https://lex.uz/ru/axborot · https://lex.uz/uz/axborot (site terms, not a legal act)
> **ru:** Вы можете использовать информацию, полученную на данном информационном ресурсе только для персональных целей. Любое копирование, распространение, продажа, передача полученных данных в целях получения прибыли не допускается без письменного разрешения владельца. Использование информации (за исключением текста нормативно-правовых актов) на других ресурсах допускается с указанием ссылки на источник.

**ZRU-547 — Probo as an operator** · https://lex.uz/docs/4396419 · https://lex.uz/ru/docs/4396428
> **Art. 18, grounds (selected), uz:** субъект тараф бўлган шартномани бажариш учун бу маълумотларга ишлов бериш ёки шундай шартнома тузилгунига қадар субъектнинг сўровига биноан чоралар кўриш зарур бўлганда; … шахсга доир маълумотларга уларни мажбурий равишда эгасизлантириш шарти билан статистик ёки бошқа тадқиқот мақсадларида ишлов берилганда; агар бу маълумотлар ҳамма фойдаланиши мумкин бўлган манбалардан олинган бўлса.
> **ru:** необходимости обработки этих данных для выполнения договора, стороной которого является субъект, или принятия мер по запросу субъекта до заключения такого договора; … обработки этих данных в статистических или иных исследовательских целях при условии обязательного обезличивания персональных данных; если эти данные получены из общедоступных источников.
>
> **Art. 20 part 1 (ZRU-1125), uz:** Ушбу Қонун 27¹-моддасининг иккинчи қисмига мувофиқ Ўзбекистон Республикаси ҳудудида сақланиши шарт бўлган шахсга доир маълумотлар базалари Шахсга доир маълумотлар базаларининг давлат реестрида рўйхатдан ўтказилиши лозим.
>
> **Art. 31, last part, ru:** Собственник и (или) оператор определяет структурное подразделение или должностное лицо, ответственное за работу, связанную с обработкой и защитой персональных данных, и обеспечивает его работу в соответствии с Типовым порядком обработки персональных данных.

**Administrative Code, art. 46² part 2 — AI** (added by ZRU-1115 of 21.01.2026; full text and history in R-02)
> **uz:** Сунъий интеллект технологияларидан фойдаланган холда шахсга доир маълумотларга қонунга хилоф равишда ишлов бериш, уларни оммавий ахборот воситаларида, телекоммуникация тармоқларида ёки Интернет жаҳон ахборот тармоғида тарқатиш, — маъмурий ҳуқуқбузарликни содир этиш қуролларини мусодара қилиб, базавий ҳисоблаш миқдорининг эллик бараваридан юз бараваригача миқдорда жарима солишга сабаб бўлади.

### 3. Risk register

The BCA is 440,000 UZS (R-02, PF-115, from 01.09.2026).

| # | Risk | Norm | Likelihood now | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Claim that a passive scan is "unauthorized access" | Adm. Code 155; Criminal Code 278² | low | low: 155 fines are ⅓–3 BCA | Public pages only. Respect logins and paywalls. Scanner info page with an opt-out contact (F-49) | Role 1 |
| 2 | Active mode used on a site that is not our client | Adm. Code 155; Criminal Code 278², 278⁴ | low (D-009) | high | Written consent plus proof that the client controls the domain (DNS TXT or file, as in F-47) before canaries or logins | Role 1 |
| 3 | Publishing security weaknesses of other people's sites | ZRU-764 art. 24 | **medium** (the public demo scans any URL; share links) | medium | Hide SEC-01/02 and PD-DB-01 details unless the viewer is the verified owner; statistics as counts only (F-47) | Role 1 |
| 4 | A named company says a finding is false | Civil Code 100 | low to medium | medium | Evidence package, "signs of violation", date and vantage in every report, no names in public (D-003, D-004) | all |
| 5 | Selling documents or lawyer review without notification | ZRU-701 annex 3 item 31, annex 4 III-24; CMR 675 | **medium** (once category IV is sold) | 25 BCA = 11 M UZS plus a ban | Partner firm or advocate for M11/M12 and generators; or hire a legal consultant and notify first | team |
| 6 | PD in texts sent to the LLM (US, not DPF) | ZRU-547 art. 15, 27¹; CMR 415; Adm. Code 46² part 2 | medium | 50–100 BCA (22–44 M UZS) | Redact e-mails, phones and names before the LLM (F-48); no account data to the LLM; or a model hosted in a listed country | Role 1 |
| 7 | Our own data handling (IP logs, accounts, scan artefacts) | ZRU-547 arts. 10, 18, 23, 27, 31; Adm. Code 46² part 1 | medium | 7 BCA (citizen) or 50 BCA (official) | Policy (§5), retention timers (F-50), responsible person, internal policy | team |
| 8 | Bulk use of lex.uz content in a paid product | lex.uz terms; ZRU-42 art. 8 | low to medium | the Center may object or block | Quote official texts with links; label LexUZ Russian as a translation; ask the Center for written permission (Q-L19) | Alii |
| 9 | Load on scanned sites | Criminal Code 278⁵ (intentional) | very low | — | 20 pages, a fixed window, per-IP limits; stop on challenge pages (D-018) | Role 1 |
| 10 | Our own site breaks the rules we check | ZRU-547; ZRU-792 | medium | reputation in front of the jury | Probo's site: no trackers before consent, a policy with all art. 22 elements, seller details (EC-01) | Role 1 |

### 4. Disclaimer for the report (UZ / RU)

**Full version (end of every report):**

> **UZ:** Ushbu hisobot Probo xizmati tomonidan avtomatik tarzda tayyorlandi. U saytning ochiq sahifalarini oddiy
> tashrif buyuruvchi sifatida {sana va vaqt} da {mamlakat / tarmoq} dan kuzatish natijalariga asoslanadi. Hisobotdagi
> topilmalar qonunbuzarlik **alomatlari** bo‘lib, rasmiy yuridik xulosa, davlat organining qarori yoki huquqiy
> maslahat hisoblanmaydi. Probo saytning ichki tizimlari, shartnomalari va ma’lumotlar bazalarini ko‘rmaydi; yakuniy
> baholashni yurist amalga oshiradi. Qonun normalari lex.uz dagi rasmiy matnlardan iqtibos qilingan; rus tilidagi
> matnlar LexUZ tarjimasidir. Xavfsizlikka oid topilmalar faqat sayt egasi uchun mo‘ljallangan va ularni bartaraf
> etishdan boshqa maqsadda oshkor qilinmasligi lozim («Kiberxavfsizlik to‘g‘risida»gi Qonunning 24-moddasi).
>
> **RU:** Настоящий отчёт подготовлен сервисом Probo автоматически. Он основан на наблюдении открытых страниц сайта в
> роли обычного посетителя {дата и время} из {страна / сеть}. Выводы отчёта — **признаки** нарушения, а не официальное
> юридическое заключение, решение государственного органа или юридическая консультация. Probo не видит внутренних
> систем, договоров и баз данных сайта; окончательную оценку даёт юрист. Нормы процитированы по официальным текстам
> lex.uz; тексты на русском языке — перевод LexUZ. Сведения о безопасности предназначены только владельцу сайта и не
> подлежат раскрытию иначе как для их устранения (статья 24 Закона «О кибербезопасности»).

**Short version (footer, share pages):**

> **UZ:** Avtomatik tekshiruv: ochiq sahifalar, {sana}. Qonunbuzarlik alomatlari, yuridik xulosa emas.
> **RU:** Автоматическая проверка открытых страниц, {дата}. Признаки нарушения, не юридическое заключение.

The UI already says «признаки нарушения, а не юридическое заключение» (`frontend/src/i18n.tsx`). The full version adds
the date and vantage point, what we cannot see, the source of the norms and the art. 24 line.

### 5. Probo's own privacy policy — main points (art. 22 elements, R-01 §4)

1. **Operator:** the Probo legal entity, its TIN, postal address and contact e-mail (art. 22; model procedure item 11).
2. **Purposes and grounds:**
   - Accounts and payments: contract (art. 18, 2nd ground).
   - Rate limits and security logs: legitimate interest (art. 18, 5th ground).
   - Scans of public pages: publicly available sources (last ground).
   - Statistics: anonymization (6th ground).
   - Marketing e-mails: consent only.
3. **Data:**
   - account: name, e-mail, company, role;
   - technical: IP address, time, user agent;
   - scan artefacts: URLs, requests, cookies set by the scanned site, screenshots and HTML of public pages;
   - for active scans: the client's test account and canary data.
   - We do not collect visitors' data of the scanned sites.
4. **Recipients:**
   - hosting (Role 1's server; country to confirm, Q-L16);
   - Cloudflare (tunnel; US, DPF active);
   - the LLM provider (Anthropic, US): **only redacted public text, no account data**;
   - the payment provider;
   - a partner lawyer, only at the client's request.
5. **Cross-border transfer:** state the countries. The US counts only for DPF companies (CMR No. 415). For any other
   recipient, state the basis (art. 15: consent).
6. **Retention:**
   - accounts: contract plus 1 year;
   - IP and security logs: 30 days;
   - scans of non-client sites: 30 days, then delete the artefacts and keep anonymized counts;
   - client scans: contract term plus 1 year (evidence).
   - Basis: art. 10 part 3 — until the purpose is reached.
7. **Subject's rights (art. 30)** and how to use them:
   - by e-mail, with an electronic request to stop processing or delete (art. 31);
   - an answer within the legal terms;
   - a complaint to the authorized body (in practice the MoI Migration and Personalization Department, R-10) or to court.
8. **Responsible person** (art. 31, last part) and protection measures (art. 27): TLS, access control, hashed tokens.
9. **Cookies:** only the ones the service needs. **No third-party trackers on Probo's own site** — we must pass our own
   scan.
10. **Changes** to the policy, with a date and version.

### 6. Terms of service — main points

1. **Form:** a public offer (Civil Code art. 369). It is accepted by registering or paying (art. 370: performing the
   offer's conditions counts as acceptance).
2. **Service:** an automated passive check of public pages and a report of signs of violation with law references.
   It is **not** legal consulting. Documents and lawyer review come from a registered partner (or from Probo after its
   notification, §1 conclusion 3).
3. **Active mode** (forms, logins, canaries): only for domains the client owns or controls. Needed: a written request,
   domain verification, and the client's warranty and responsibility for the authority given.
4. **Prohibited use:**
   - scanning to attack, overload or harass;
   - bypassing limits;
   - publishing other people's security findings (ZRU-764 art. 24);
   - using reports to discredit a competitor (ZRU-850 art. 21).
5. **Confidentiality:** security findings go only to the verified owner. Share links show no security details.
6. **Limits of the result:** a scan from one vantage point at one time; sites change; CDN and server country may be
   inaccurate (D-004, "undetermined"). Liability is limited to the fee paid, within the law.
7. **Evidence:** reports carry hashes and a signature. Probo keeps the evidence for the retention period.
8. **Content:** the law texts are official documents (ZRU-42 art. 8), and Russian texts are LexUZ translations. The
   report's own text is licensed to the client for internal use and for showing to regulators.
9. **Personal data:** see the policy (§5).
10. **Law and disputes:** the law of Uzbekistan; negotiation first, then the courts of Uzbekistan.

### 7. V-15 and V-17 in one line each

- **V-15:** no license, permit or notification is needed to check websites or to scan for vulnerabilities (ZRU-701 art.
  13, annexes 1–3). Active testing of someone else's system without permission is an offence risk (Adm. Code 155,
  Criminal Code 278²), and publishing found weaknesses needs the owner's permission (ZRU-764 art. 24). **D-008 stays,
  with this reason instead of "licensed activity".**
- **V-17:** quotes of laws with a link — yes (ZRU-42 art. 8; the lex.uz terms say «за исключением текста нормативно-правовых актов»).
  Bulk, for-profit use of the lex.uz database — only with the Center's written permission.

### 8. Answers for the legal mentor (short, uz / ru)

- **"Is scanning legal?"**
  - **uz:** Biz faqat hamma uchun ochiq sahifalarni oddiy brauzer kabi ochamiz. Konstitutsiyaning 33-moddasi har kimga
    axborotni izlash va olish huquqini beradi. JK 278² va MJtK 155 esa faqat ruxsatsiz kirishni jazolaydi. Formalarni
    to‘ldirish va akkauntga kirish faqat mijoz saytida, yozma rozilik bilan amalga oshiriladi.
  - **ru:** Мы открываем только общедоступные страницы, как обычный браузер. Статья 33 Конституции даёт каждому право
    искать и получать информацию, а УК 278² и КоАО 155 наказывают только несанкционированный доступ. Формы и личные
    кабинеты — только на сайтах клиентов, с письменного согласия.
- **"Do you need a license?"**
  - **uz:** Yo‘q. ZRU-701 ning 1-ilovasida bunday faoliyat yo‘q. Hujjat tayyorlash va yurist xulosasi yuridik maslahat
    xizmati hisoblanadi: uni ro‘yxatdagi hamkor tashkilot beradi, yoki biz Adliya organini xabardor qilib, shtatga
    yurist olamiz.
  - **ru:** Нет: в приложении № 1 к ЗРУ-701 такого вида нет. Подготовка документов и заключение юриста — это
    юридические консультационные услуги: их оказывает партнёр из реестра, либо мы уведомляем органы юстиции и берём
    юриста в штат.
- **"Do you publish weaknesses of sites?"**
  - **uz:** Yo‘q. Kiberxavfsizlik to‘g‘risidagi qonunning 24-moddasiga ko‘ra, zaifliklar faqat egasiga ko‘rsatiladi.
    Ochiq statistika anonim.
  - **ru:** Нет. По статье 24 Закона «О кибербезопасности» уязвимости показываются только владельцу, а публичная
    статистика анонимна.

## Fact check (passport §11.4)

| ID | Claim | Status | Correct wording | Source |
|---|---|---|---|---|
| V-15 | Checking websites for vulnerabilities requires a license or permit | **REFUTED** | Not in ZRU-701 annexes 1–3 (licenses, permits, notifications). The only IT licenses are for cryptographic tools and telecom networks. Mandatory examinations cover only state bodies and critical infrastructure (ZRU-764 art. 18). The real limits are art. 24 (disclosure) and Adm. Code 155 / Criminal Code 278² (access without permission) | https://lex.uz/ru/docs/5511900 ; https://lex.uz/ru/docs/5960609 |
| V-17 | lex.uz: personal use only; for-profit copying needs written permission | **CONFIRMED, with an exception** | The terms exempt the text of legal acts from the link rule («за исключением текста нормативно-правовых актов»), and laws are not copyright objects (ZRU-42 art. 8). Bulk commercial use of the database still needs the Center's permission | https://lex.uz/ru/axborot ; https://lex.uz/ru/docs/1023494 |
| new | A passive scan of public pages is lawful without the owner's consent | **CONFIRMED (interpretation)** | No norm forbids it. The offences require unauthorized access. Constitution 33 and Law 560-II art. 11 support access to public resources | §2 |
| new | Commercial legal consulting needs a notification and a staff legal consultant | **CONFIRMED** | ZRU-701 annex 3 item 31; CMR No. 675 items 2, 4, 8; fine 25 BCA for the legal entity (annex 4 III-24, art. 52) | https://lex.uz/ru/docs/5511900 ; https://lex.uz/ru/docs/3908803 |
| new | Information about found vulnerabilities may be disclosed only with the owner's permission | **CONFIRMED** | ZRU-764 art. 24 | https://lex.uz/ru/docs/5960609 |
| new | Anthropic is an EU-US DPF participant | **NOT FOUND** on the list on 21.11.2026 (search checked with Cloudflare, which is found) | Treat the US recipient as "not listed" for PD | https://www.dataprivacyframework.gov/list |
| passport §13 | "We don't store other people's personal data" | **INACCURATE** | Screenshots, HTML and HAR of public pages may contain names, phones and e-mails, and we log IP addresses. Say instead: "only public pages, kept for a limited time, never sold" | §1 |

## Feature ideas (passport §10 format)

- F-47 · **Owner-only security details.** SEC-01/02 and PD-DB-01 details are shown only to a viewer who verified the
  domain (DNS TXT record or a file at `/.well-known/`). Public scans and share links show "security: N findings, details
  for the owner". The same verification unlocks the active mode · ZRU-764 art. 24; D-009 · M · R-08 · Final (the hiding
  part is S and fits before the checkpoint)
- F-48 · **PII redaction before the LLM.** Replace e-mails, phones, Uzbek IDs (the `uz_ids.py` detectors exist) and
  person names in policy text with placeholders before the Anthropic call; never send account data · art. 15, 27¹;
  Adm. Code 46² part 2 · S · R-08 · Final
- F-49 · **"How Probo scans" page.** What we load, limits, IP ranges, an abuse and opt-out contact; sites that ask are put
  on a do-not-scan list · reduces claims under Adm. Code 155 and Civil Code 100; good faith in front of the jury · S ·
  R-08 · Final
- F-50 · **Retention timer.** Artefacts of non-client scans are deleted after 30 days; counts and hashes stay · art. 10
  part 3, art. 18 · S · R-08 · Roadmap

## Questions for the team / contradictions with the passport

- **Q-L15 (Role 1, before the checkpoint).** Hide SEC-01/02 and PD-DB-01 details on public scans and share links
  (F-47, ZRU-764 art. 24)?
- **Q-L16 (Role 1).** Where is the server physically (D-024: "Role 1's always-on machine"), and where are scan artefacts
  stored? This goes into our policy (§5 item 4).
- **Q-L17 (Role 1).** LLM: redaction (F-48), or a provider in a listed country? Anthropic is not on the DPF list.
- **Q-L18 (team, business).** Category IV ("fixed documents", M12) and F-45 are legal consulting. Is it a partner firm
  (the M12 note "billed by the partner"), or Probo's own notification plus a staff legal consultant?
- **Q-L19 (Alii).** Write to the "Adolat" National Legal Information Center for written permission to use lex.uz
  content in a commercial product (V-17). Until then, quote with links only.
- **Contradiction — D-008.** Its reason "possibly a licensed activity (V-15)" is refuted. Suggested reason: "publishing
  vulnerabilities needs the owner's permission (ZRU-764 art. 24), and active testing without permission risks Adm.
  Code 155 / Criminal Code 278²".
- **Contradiction — §13 "Is scanning legal?"** Replace "we don't store other people's personal data" with the §8 answer.

## Appendix — independent check of the team's legal quotes (21.11.2026)

I checked every Cyrillic, Latin and Russian quote by script against live lex.uz texts downloaded the same day. The
script removes page noise and normalizes apostrophes and superscripts. A negative test with a changed word is caught.

| File (author) | Quotes checked | Not found on lex.uz | Why |
|---|---|---|---|
| `rules/*.yaml`, 15 rules (R-03, Doniyor) | 62 | 0 | — |
| `backend/data/law_versions.yaml` (old art. 27¹, ed. 29.11.2023) | 2 | 0 | — |
| `research/legal-norms.md` (R-01, Doniyor) | 136 | 0 | — |
| `research/legal-liability.md` (R-02, Doniyor) | 83 | 13, none of them a law-text error | 8 are edition notes, headings or LexUZ comments; checked one by one, they are on lex.uz. 4 are quotes from news sites. 1 is a Latin phrase from PP-14 that was checked live in R-10 |
| `research/legal-our-risks.md` (this file) | 61 | 13, none of them a law-text error | All 13 are our own disclaimer and UI text, not quotes from lex.uz. One real error was found and fixed: the lex.uz terms phrase, now quoted exactly |

**Result:** no wording errors in the law quotes of R-01, R-02 or R-03. This checks the **text**, not the choice of
article or level. Those choices stay with the lawyer.

## Sources

- Constitution: https://lex.uz/docs/6445145 · https://lex.uz/ru/docs/6445147
- Criminal Code: https://lex.uz/docs/111453 · https://lex.uz/ru/docs/111457
- Administrative Code: https://lex.uz/docs/97664 · https://lex.uz/ru/docs/97661
- ZRU-764 "On cybersecurity": https://lex.uz/docs/5960604 · https://lex.uz/ru/docs/5960609
- ZRU-701 "On licensing, permitting and notification procedures": https://lex.uz/docs/5511879 · https://lex.uz/ru/docs/5511900
- CMR No. 675 of 17.08.2018 (legal consulting): https://lex.uz/docs/3908401 · https://lex.uz/ru/docs/3908803
- Law 400-I "On guarantees and freedom of access to information": https://lex.uz/docs/1319 · https://lex.uz/ru/docs/2118
- Law 560-II "On informatization": https://lex.uz/docs/83472 · https://lex.uz/ru/docs/82956
- Civil Code (part 1): https://lex.uz/docs/111189 · https://lex.uz/ru/docs/111181
- ZRU-42 "On copyright and related rights": https://lex.uz/docs/1022944 · https://lex.uz/ru/docs/1023494
- ZRU-850 "On competition", art. 21: https://lex.uz/docs/6518381 · https://lex.uz/ru/docs/6518383
- ZRU-547 "On personal data": https://lex.uz/docs/4396419 · https://lex.uz/ru/docs/4396428
- lex.uz terms: https://lex.uz/ru/axborot · https://lex.uz/uz/axborot
- EU-US Data Privacy Framework list: https://www.dataprivacyframework.gov/list
- Related: `research/legal-norms.md` (R-01), `research/legal-liability.md` (R-02, BCA and art. 46²),
  `research/legal-27-1-2026.md` (R-10, CMR No. 415), `research/business-model-v2.md`, `research/service-catalog-v2.md`
