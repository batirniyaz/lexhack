# Customer interviews: script (uz / ru), answer table, how to read the results (R-06)
- Author: Alii (research; Alii runs the interviews), prepared with Claude Code
- Date/time: 21.11.2026, 08:55
- Based on passport version: 0.14; prices from `research/business-model-v2.md` (D-026)
- Method:
  - The script asks about **past behaviour, not opinions** ("when did you last…", not "would you…"). The product
    comes only at the end, so answers are not shaped by our pitch.
  - Price is asked after showing the **anonymized sample report** (`GET /api/sample`). It uses four short
    price-sensitivity questions (Van Westendorp).
  - 10–12 minutes per call. Goal from passport §9: **5–10 companies before 13:00 on 21.11.**
- Confidence: this file is a tool. The results table is empty until the calls are made. **No numbers from it may go
  into the pitch until it is filled.**

## Conclusions (what the interviews must answer)

1. **Is the problem real?** Do businesses collect personal data on the site without knowing which third parties
   receive it? (Q1–Q2)
2. **Do they know the law, and did the 2026 changes reach them?** (Q3)
3. **What do they do today, and what does it cost?** Nothing, an internal lawyer, a law firm, IT? (Q4–Q5)
4. **Who decides and pays?** Lawyer, marketing, IT or the owner. This decides our sales channel. (Q6)
5. **Price:** are 100,000 UZS (Express) and 250,000 UZS (Full audit) per site per month below, at or above what they
   would pay? (Q7 and the price block)

## Who to call (10 slots, one per sector; names are never written in this repo — D-003)

| # | Sector | Who to ask | Why this sector |
|---|---|---|---|
| 1 | Online store (electronics / clothes) | owner or marketer | forms, payment, many trackers; e-commerce pilot (EC-01…03) |
| 2 | Private clinic / laboratory | manager | health data = special data (art. 25) |
| 3 | Microfinance or lending service | compliance / lawyer | ID and phone forms; regulated |
| 4 | Delivery / taxi / food service | product or marketing | apps, location |
| 5 | Online school / courses | owner | minors' data (art. 21) |
| 6 | Real estate developer | marketing | lead forms to CRM and Telegram bots (V-16) |
| 7 | Travel agency | owner | passports, cross-border transfer |
| 8 | Car dealer / leasing | marketing | lead forms, call tracking |
| 9 | Bank (compliance department) | compliance officer | many domains, critical infrastructure |
| 10 | Law firm | partner | channel partner, not a buyer (business model §10) |

Where to find them: personal contacts, the team's Telegram contacts, LinkedIn, mentors at the hackathon, the company's
phone or Telegram from its own website (a phone call is fine; **no cold e-mails about their site's findings** —
`competitors-v2.md`, D-009).

## Rules for the interviewer

- Ask permission to take notes. **Do not record** without a clear "yes". Write down only the sector, size and role.
  The person's name or company goes into the table **only if they agree**, and never into the repo (ZRU-547 art. 18
  and art. 23; D-003).
- Do not show their own site's findings unless they ask. If they ask, scan only in passive mode and send the result
  **only to them** (R-08, ZRU-764 art. 24).
- Do not argue, and do not sell before Q7. Note exact words for the strongest sentence ("quote" column).

## Script

**Opening (30 s)**
- **uz:** Assalomu alaykum! Men Alii, Probo jamoasidanman — biz LexHackathon’da saytlar shaxsga doir ma’lumotlarni
  qanday yig‘ishi va kimga uzatishi bo‘yicha yechim qilyapmiz. 10 daqiqa vaqtingizni olsam bo‘ladimi? Hech narsa
  sotmayman, sizning tajribangiz qiziq. Qisqa yozib olsam maylimi? Ismingiz va kompaniya nomi hech qayerda chiqmaydi.
- **ru:** Здравствуйте! Меня зовут Алий, я из команды Probo — на LexHackathon мы делаем решение о том, как сайты
  собирают персональные данные и кому их передают. Можно 10 минут вашего времени? Я ничего не продаю, мне важен ваш
  опыт. Можно я буду коротко записывать? Ваше имя и название компании нигде не появятся.

**Q1 — what data**
- **uz:** Saytingiz yoki ilovangiz orqali mijozlardan qanday ma’lumotlar olasiz? (ism, telefon, manzil, pasport,
  to‘lov, joylashuv…) Ular keyin qayerga tushadi — CRM, Telegram, Excel?
- **ru:** Какие данные клиентов вы получаете через сайт или приложение (имя, телефон, адрес, паспорт, оплата,
  геолокация…)? Куда они потом попадают — CRM, Telegram, Excel?

**Q2 — who installed what**
- **uz:** Saytga analitika, reklama pikseli (Meta, Google, Yandex), onlayn-chat yoki qo‘ng‘iroq tracking’ini kim
  o‘rnatgan? Oxirgi marta qachon yangi narsa qo‘shildi va buni kim tasdiqladi?
- **ru:** Кто ставил на сайт аналитику, рекламные пиксели (Meta, Google, Яндекс), онлайн-чат или коллтрекинг? Когда
  в последний раз что-то добавляли и кто это согласовывал?

**Q3 — awareness**
- **uz:** «Shaxsga doir ma’lumotlar to‘g‘risida»gi qonun sizning saytingizga qanday talablar qo‘yadi deb
  bilasiz? 2026-yilda bu qonunda o‘zgarishlar bo‘lganini eshitganmisiz — qaysilarini?
- **ru:** Какие требования, по-вашему, закон «О персональных данных» предъявляет к вашему сайту? Слышали ли вы об
  изменениях 2026 года — каких именно?

**Q4 — last check (past behaviour)**
- **uz:** Oxirgi marta qachon saytingiz yoki hujjatlaringiz shu qonun bo‘yicha tekshirilgan? Kim tekshirgan
  (o‘z yuristingiz, yuridik firma, IT bo‘limi) va bu qancha turgan?
- **ru:** Когда в последний раз ваш сайт или документы проверяли на соответствие этому закону? Кто проверял (свой
  юрист, юрфирма, IT-отдел) и сколько это стоило?

**Q5 — trigger events**
- **uz:** Shu mavzuda biror holat bo‘lganmi: davlat organi tekshiruvi, mijoz shikoyati, bank, hamkor yoki investor
  talabi, ma’lumot sizib chiqishi? Nima qildingiz?
- **ru:** Были ли случаи по этой теме: проверка госоргана, жалоба клиента, требование банка, партнёра или
  инвестора, утечка данных? Что вы тогда сделали?

**Q6 — who decides, which budget**
- **uz:** Agar bunday tekshiruv kerak bo‘lsa, qarorni kim qabul qiladi va pul qaysi byudjetdan chiqadi —
  yuridik, marketing, IT yoki rahbar?
- **ru:** Если такая проверка понадобится, кто принимает решение и из какого бюджета платят — юристы, маркетинг, IT
  или руководитель?

**Show the sample report (1–2 min)** — the anonymized example on the home page. Say only what it shows: which
services receive visitors' data, in which countries, what the law says (with the article), and how to fix it.

**Q7 — value and price**
- **uz:** Shu hisobotdan sizga eng foydali qism qaysi, qaysi biri keraksiz? Bitta saytni bir marta shunday tekshirish
  uchun qancha to‘lagan bo‘lardingiz? Har oy qayta tekshirish va qonun o‘zgarsa xabar berish uchun-chi?
- **ru:** Какая часть отчёта для вас самая полезная, а какая лишняя? Сколько вы заплатили бы за разовую такую
  проверку одного сайта? А за ежемесячную перепроверку с уведомлением, когда меняется закон?

**Price block (4 short questions, monthly price for one site, in UZS)**

| # | uz | ru |
|---|---|---|
| P1 | Qaysi narxda bu juda arzon bo‘lib, sifatiga ishonmay qolasiz? | При какой цене это так дёшево, что вы усомнитесь в качестве? |
| P2 | Qaysi narxda arzon, ya’ni foydali xarid deb bilasiz? | При какой цене это недорого, то есть выгодная покупка? |
| P3 | Qaysi narxda qimmat, lekin baribir o‘ylab ko‘rasiz? | При какой цене это дорого, но вы ещё подумаете? |
| P4 | Qaysi narxda shunchalik qimmatki, olmaysiz? | При какой цене это так дорого, что вы не купите? |

**Close (30 s)**
- **uz:** Rahmat! Agar xohlasangiz, saytingizni oddiy tashrif buyuruvchi sifatida bepul tekshirib, natijani faqat
  sizga yuboramiz. Kimga yuborsak bo‘ladi? Yana kimni tavsiya qilasiz?
- **ru:** Спасибо! Если хотите, мы бесплатно проверим ваш сайт как обычный посетитель и пришлём результат только
  вам. Кому отправить? Кого ещё вы могли бы порекомендовать?

## Answer table (fill during the calls)

| # | Date, time | Sector | Size (staff) | Role | Q1 PD collected, where it goes | Q2 who installs tools | Q3 knows law (0 no / 1 heard / 2 details) | Q4 last check: when, who, cost | Q5 trigger event | Q6 decider / budget | Q7 one-off price | Q7 monthly price | P1 / P2 / P3 / P4 (UZS) | Pilot (yes / no) | Strongest quote |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | | | | |
| 5 | | | | | | | | | | | | | | | |
| 6 | | | | | | | | | | | | | | | |
| 7 | | | | | | | | | | | | | | | |
| 8 | | | | | | | | | | | | | | | |
| 9 | | | | | | | | | | | | | | | |
| 10 | | | | | | | | | | | | | | | |

## How to read the results (decide before the calls, so the answers are not bent afterwards)

| Question | Signal "yes" | Signal "no" | What changes if "no" |
|---|---|---|---|
| Problem is real | ≥ 3 of 5 collect PD **and** cannot name every service that receives it (Q1–Q2) | most know exactly what is installed | lead the pitch with law changes and evidence, not "hidden trackers" |
| Law awareness is low | ≥ 3 of 5 score 0–1 on Q3 | most score 2 | position as monitoring and evidence, not education |
| Nobody checks the site | ≥ 3 of 5: never checked, or only documents checked (Q4) | regular technical checks exist | find out who does them (competitor for R-04) |
| Buyer | the same Q6 role in ≥ 3 calls | spread across roles | keep two channels: marketing and law firms |
| Price 100k / 250k UZS | the median of P2–P3 brackets the price | P2 above it means we are cheap; P3 below it means we are expensive | change only the **public** numbers in `business-model-v2.md` (team decision) |
| Pilot | ≥ 2 say yes to the free check | 0 yes | the free partial audit (D-026) is not enough of a hook |

Report the result honestly in one line per row. Write the number of calls ("n = 4") next to every claim.
"3 of 4 owners…" goes into the pitch only if it is in the table.

## Questions for the team

- **Q-R6-1 (team).** Who makes calls besides Alii? 5 calls by one person by 13:00 is tight. Split by sector.
- **Q-R6-2 (Role 1).** Is `GET /api/sample` stable for showing on a phone during a call, or should we send a PDF?

## Sources

- Price hypotheses: `research/business-model-v2.md` (D-026); segments: `research/market.md`,
  `research/service-catalog-v2.md`
- Ethics and limits: `research/legal-our-risks.md` (R-08), passport D-003, D-009
- Method: "ask about past behaviour, not hypotheticals" (customer-discovery practice); Van Westendorp
  price-sensitivity meter (four price questions)
