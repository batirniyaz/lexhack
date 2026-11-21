# Pitch v1: 3 min pitch + 2 min demo + 2 min Q&A (uz / ru) (R-07)
- Author: Alii (research), prepared with Claude Code
- Date/time: 21.11.2026, 09:00
- Based on passport version: 0.14
- Inputs:
  - research files R-01, R-02, R-04, R-05, R-08, R-09, R-10, the e-commerce norms and `business-model-v2.md`;
  - live `GET /api/stats` on https://probo.aicenterkk.tech (read 21.11.2026 08:30: batch of 20.11 23:19, **n = 8**
    anonymized reference sites).
- Confidence: **high** for the legal facts and counts (sourced in the files above). **Low** for prices and market
  shares (hypotheses; R-06 interviews not done yet). Every number below has a source line in §5.

## 1. Timing and slides (3:00)

| # | Time | Slide | One message | Criteria |
|---|---|---|---|---|
| 1 | 0:00–0:25 | Problem | The lawyer reads documents; the data leaks through the site's code | B1, S1 |
| 2 | 0:25–0:50 | Proof | 8 of 8 sites load trackers before consent; the law changed twice this year | B1, S5 |
| 3 | 0:50–1:20 | Solution | Probo: a URL → in 1–2 min, where visitors' data goes + the article of the law + how to fix | T1, S3 |
| 4 | 1:20–1:45 | Why we can be trusted | Rules written by lawyers, verbatim lex.uz quotes, signed evidence, passive and legal (R-08) | S2, S4 |
| 5 | 1:45–2:10 | Business model | Free first audit → tokens per audit: 100,000 / 250,000 UZS per site per month | B2, B4 |
| 6 | 2:10–2:30 | Market and competitors | 182,338 .uz domains; no website scanner for Uzbek law; the Center does ≈25 security examinations a month | B3, B5 |
| 7 | 2:30–2:45 | Growth | Law firms, Ministry of Justice legal service centres (21,292 organizations), mobile apps, Central Asia | B5 |
| 8 | 2:45–3:00 | Team and ask | Who we are; pilot with the Ministry of Justice centres + 10 online stores | — |

## 2. Pitch text

### O‘zbekcha (≈390 so‘z)

**[1]** Har bir onlayn do‘kon, klinika va bankning saytida mijoz ma’lumotlari to‘planadi: ism, telefon, manzil. Yurist
shartnoma va siyosatni tekshiradi. Lekin ma’lumot hujjat orqali emas, sayt kodi orqali chiqib ketadi: reklama piksellari,
analitika, chat va CRM. Ularni marketolog o‘rnatadi, yurist esa bundan bexabar bo‘ladi.

**[2]** Biz turli sohalardagi 8 ta o‘zbek saytini tekshirdik. 8 tasining 8 tasida trekerlar rozilik so‘ralmasdan yuklanadi. 6 tasida
sessiya yozib olinadi, ya’ni tashrif buyuruvchi nima yozgani va qayerni bosgani qayd etiladi. 2 tasida siyosat saytning
amalda qilayotgan ishiga zid. Bu yil qoidalar ikki marta o‘zgardi: mart oyida qonundagi lokalizatsiya talabi
yangilandi, avgustda hukumat 49 davlatdan iborat ro‘yxatni tasdiqladi. Kecha qonuniy bo‘lgan narsa bugun buzilish bo‘lishi mumkin, yoki aksincha.

**[3]** Probo — saytlarni shaxsga doir ma’lumotlar to‘g‘risidagi qonun bo‘yicha avtomatik tekshiruvchi xizmat. Sayt
manzilini kiritasiz, 1–2 daqiqada hisobot olasiz. Hisobotda ma’lumot qaysi xizmatlarga va qaysi davlatlarga ketayotgani,
qonunning qaysi moddasi buzilgani va uni qanday tuzatish ko‘rsatiladi.

**[4]** Qoidalar huquqiy tadqiqot asosida yozilgan, va yurist ularni dasturchisiz o‘zgartira oladi. Iqtiboslar
so‘zma-so‘z lex.uz dan olinadi. Har bir dalil imzolanadi va xeshlanadi.
Biz faqat ochiq sahifalarni oddiy tashrif buyuruvchi kabi ochamiz: hech narsani buzmaymiz, buning uchun litsenziya ham
kerak emas.

**[5]** Birinchi tekshiruv bepul. Keyin tokenlar bilan ishlaysiz: tezkor tekshiruv oyiga 100 ming so‘m, to‘liq huquqiy
audit 250 ming so‘m. Qonun o‘zgarsa, saqlangan tekshiruvlar bepul qayta ko‘rib chiqiladi.

**[6]** O‘zbekistonda 182 mingdan ortiq .uz domen bor. Dunyo bo‘yicha 27 ta vositani o‘rgandik: hech biri saytni O‘zbekiston
qonuni bo‘yicha tekshirmaydi. Mahalliy yuridik firmalar faqat hujjatlarni tekshiradi. Kiberxavfsizlik markazi esa zaifliklarni
izlaydi va oyiga 25 ga yaqin ekspertiza o‘tkazadi.

**[7]** Bizning yo‘limiz — yuridik firmalar, Adliya vazirligining yuridik xizmat markazlari (21 mingdan ortiq tashkilot),
keyin mobil ilovalar va Markaziy Osiyo.

**[8]** Jamoamiz: dasturchi va ikki tadqiqotchi — huquq va biznes. So‘rovimiz: Adliya vazirligi markazlari bilan pilot
va 10 ta onlayn do‘kon bilan tanishuv. Rahmat!

### Русский (≈390 слов)

**[1]** На сайте каждого интернет-магазина, клиники и банка собираются данные клиентов: имя, телефон, адрес. Юрист
проверяет договоры и политику. Но данные уходят не через документы, а через код сайта: рекламные пиксели, аналитику,
чаты и CRM. Ставит их маркетолог, а юрист об этом не знает.

**[2]** Мы проверили 8 узбекских сайтов из разных отраслей. На 8 из 8 трекеры загружаются до какого-либо согласия. На 6 ведётся
запись сессий: записывается, что посетитель вводит и куда нажимает. На 2 политика противоречит тому, что сайт делает на
самом деле. В этом году правила менялись дважды: в марте изменилось требование закона о локализации, в августе
правительство утвердило список из 49 государств. То, что вчера было законно, сегодня может быть нарушением, и наоборот.

**[3]** Probo — автоматическая проверка сайтов на соответствие закону о персональных данных. Вводите адрес сайта и через
1–2 минуты получаете отчёт: в какие сервисы и страны уходят данные, какая статья закона нарушена и как это исправить.

**[4]** Правила написаны на основе правового исследования, и юрист может менять их без программиста. Цитаты
берутся дословно из lex.uz. Каждое доказательство подписано и хешировано. Мы открываем
только публичные страницы, как обычный посетитель: ничего не взламываем, и лицензия для этого не нужна.

**[5]** Первая проверка бесплатная. Дальше — токены: экспресс-проверка 100 тысяч сумов в месяц, полный юридический аудит
250 тысяч. Когда меняется закон, сохранённые проверки пересматриваются бесплатно.

**[6]** В Узбекистане больше 182 тысяч доменов .uz. Мы изучили 27 инструментов в мире: ни один не проверяет сайт по
узбекскому закону. Местные юрфирмы проверяют только документы. Центр кибербезопасности ищет уязвимости и проводит около 25
экспертиз в месяц.

**[7]** Наш путь — юрфирмы, центры правовых услуг Минюста (больше 21 тысячи организаций), затем мобильные приложения и
Центральная Азия.

**[8]** Наша команда — разработчик и два исследователя: право и бизнес. Наша просьба — пилот с центрами Минюста и
знакомство с 10 интернет-магазинами. Спасибо!

## 3. Demo (2:00) — what to click

| Time | Action | What to say (uz / ru, one line) |
|---|---|---|
| 0:00–0:20 | Home page → paste a URL of **our demo site** (`demo-site/bad`), or a pre-scanned reference site shown anonymized (D-003, D-017) | «Har qanday ochiq saytni oddiy tashrif buyuruvchi kabi ochamiz» / «Открываем любой публичный сайт как обычный посетитель» |
| 0:20–0:50 | Live feed: requests, countries, trackers appear | «Mana, ma’lumot qaysi davlatlarga ketyapti» / «Вот куда уходят данные» |
| 0:50–1:20 | Report → one 🟡 finding: verbatim article (uz/ru) + lex.uz link + "how to fix" | «Har bir topilma — qonun moddasi va tuzatish yo‘li» / «Каждая находка — статья закона и способ исправить» |
| 1:20–1:40 | Policy tab: "the policy says X, the site does Y" (PD-MIS-01) | «Siyosat bir narsani aytadi, sayt boshqasini qiladi» / «Политика говорит одно, сайт делает другое» |
| 1:40–2:00 | Law change: the same scan under the pre-27.03.2026 art. 27¹ vs today (F-16); mention EC-02 becomes stricter on 12.12.2026 | «Qonun o‘zgardi — holat ham o‘zgardi» / «Закон изменился — статус тоже» |

Backup: if the live scan hangs (bot protection, D-018), open the cached report of the same site.

## 4. Ten likely questions — short answers (uz / ru)

1. **"Is scanning other people's sites legal?"**
   - **uz:** Ha. Faqat hamma uchun ochiq sahifalarni oddiy brauzer kabi ochamiz. Konstitutsiyaning 33-moddasi axborot olish
     huquqini beradi, JK 278² va MJtK 155 esa faqat ruxsatsiz kirishni jazolaydi. Faol rejim (forma va akkaunt) faqat
     mijoz saytida, yozma rozilik bilan.
   - **ru:** Да. Мы открываем только публичные страницы, как браузер. Статья 33 Конституции даёт право на получение
     информации, а УК 278² и КоАО 155 наказывают только несанкционированный доступ. Активный режим — только на сайтах
     клиентов, с письменного согласия.
2. **"What is the fine?"**
   - **uz:** MJtK 46²: fuqaroga 7 BHM (3,08 mln so‘m), mansabdorga 50 BHM (22 mln so‘m). Sun’iy intellekt bilan qilinsa,
     50–100 BHM. Takror sodir etilsa, JK 141². Kompaniyaga emas, mas’ul shaxsga jarima solinadi.
   - **ru:** КоАО 46²: 7 БРВ гражданину (3,08 млн сумов) и 50 БРВ должностному лицу (22 млн). С использованием ИИ —
     50–100 БРВ. При повторе — УК 141². Штраф платит ответственное лицо, а не компания.
3. **"Doesn't the Cybersecurity Center already do this?"**
   - **uz:** Yo‘q. Markaz zaifliklarni qidiradi: «saytni buzish mumkinmi?». Biz «ma’lumot qonuniy uzatilyaptimi?» degan
     savolga javob beramiz. Bir-birimizni to‘ldiramiz.
   - **ru:** Нет. Центр ищет уязвимости: «можно ли взломать сайт». Мы отвечаем на вопрос «законно ли передаются данные».
     Мы дополняем друг друга.
4. **"Is a finding a violation?"**
   - **uz:** Yo‘q, bu «alomat». Biz serverning ichini ko‘rmaymiz. Yakuniy xulosani yurist beradi, ko‘p topilmalar shuning
     uchun 🟡 darajada.
   - **ru:** Нет, это «признак». Мы не видим сервер изнутри. Окончательный вывод даёт юрист, поэтому большинство находок
     имеют уровень 🟡.
5. **"Data goes to Russia — is that a violation?"**
   - **uz:** Yo‘q. Rossiya VMQ 415 ro‘yxatida bor. AQSh esa faqat DPF qatnashchilari uchun ruxsat etilgan, buni
     kompaniya bo‘yicha tekshiramiz.
   - **ru:** Нет. Россия есть в списке ПКМ № 415. США — только для участников DPF, это мы проверяем по каждой компании.
6. **"Who pays, and why monthly?"**
   - **uz:** Sayt va qonun o‘zgarib turadi: marketolog yangi piksel qo‘shadi, qonun yangilanadi. Oylik tekshiruv shuni
     ushlaydi. To‘lovchi — marketing yoki yuridik bo‘lim, buni intervyularda tekshiryapmiz.
   - **ru:** Сайты и законы меняются: маркетолог добавляет пиксель, закон обновляется. Ежемесячная проверка это ловит.
     Платит маркетинг или юристы — это мы проверяем в интервью.
7. **"Your unit economics?"**
   - **uz:** To‘liq audit narxi 250 ming so‘m (~$21). Bizning xarajat — LLM va brauzer, taxminan $0,2. Yurist mehnati
     faqat III–IV toifalarda.
   - **ru:** Полный аудит стоит 250 тысяч сумов (~$21). Наша себестоимость — LLM и браузер, около $0,2. Труд юриста —
     только в категориях III–IV.
8. **"Do you need a license?"**
   - **uz:** Avtomatik tekshiruvga litsenziya kerak emas, chunki ZRU-701 ro‘yxatida bunday faoliyat yo‘q. Hujjat
     tayyorlash va yurist xulosasini hamkor yuridik firma beradi, yoki biz Adliyani xabardor qilamiz.
   - **ru:** На автоматическую проверку лицензия не нужна: в перечне ЗРУ-701 такого вида нет. Документы и заключение юриста
     даёт партнёрская юрфирма, либо мы уведомляем Минюст.
9. **"What if the law changes again?"**
   - **uz:** Biz uchun bu yaxshi. Qoidalar sozlama sifatida saqlanadi, mijozning saqlangan tekshiruvlari bepul qayta
     ko‘rib chiqiladi. Masalan, 12 dekabrdan ofertada qaytarish shartlari majburiy bo‘ladi.
   - **ru:** Для нас это плюс. Правила хранятся как настройки, сохранённые проверки клиента пересматриваются бесплатно.
     Например, с 12 декабря условия возврата в оферте станут обязательными.
10. **"Do you depend on Claude / foreign AI? Where does the data go?"**
    - **uz:** Asosiy tekshiruvlar qoidalar bilan ishlaydi. LLM faqat siyosat matnini o‘qiydi. Matnni LLMga yuborishdan
      oldin shaxsiy ma’lumotlarni o‘chiramiz (F-48), model esa almashtirilishi mumkin.
    - **ru:** Основные проверки работают на правилах. LLM только читает текст политики. Перед отправкой мы удаляем
      персональные данные (F-48), а модель можно заменить.

## 5. Number sheet (say only these; source for each)

| Number | Use | Source |
|---|---|---|
| 8 of 8 sites: trackers before consent; 6 of 8 session recording; 4 of 8 policy incomplete; 2 of 8 policy contradicts behaviour; average score 82.6 | slide 2 (**always say "8 sites"**) | `GET /api/stats`, batch 20.11 23:19 |
| ZRU-1125 of 26.03.2026 (localization narrowed); CMR No. 415 of 29.07.2026 (49 countries) | slide 2 | `research/legal-27-1-2026.md` |
| Fines: 7 / 50 BCA (3.08 / 22 M UZS); AI: 50–100 BCA; BCA 440,000 UZS from 01.09.2026 | Q2 | `research/legal-liability.md` |
| 182,338 active .uz domains (41–90 k live) | slide 6 | `research/market.md` (V-10) |
| 27 global tools, none covers Uzbekistan; 14+ Russian scanners for 152-FZ; no Uzbek website scanner | slide 6 | `research/competitors-global.md`, `research/competitors.md` |
| Cybersecurity Center: 225 web-resource examinations in 9 months of 2026 (≈25 a month) | slide 6, Q3 | `research/csec.md` |
| 21,292 organizations served by Ministry of Justice legal service centres | slide 7 | `research/market.md` (organizer's infographic) |
| Prices 100,000 / 250,000 UZS; free first audit | slide 5 | `research/business-model-v2.md` (hypothesis) |
| Cost of a Full audit ≈ $0.2 (LLM $0.14 + browser ≈ $0.03) | Q7 | `research/business-model.md` §7 |
| ZRU-1173: return terms in the offer from 12.12.2026 | Q9, demo | `research/legal-ecommerce.md` |

**Do not say:**
- "first in the world" (positioning is "first for Uzbek law", README-v2);
- "violation" for a 🟡 finding;
- "sending data to Russia is illegal";
- any interview result before `research/interviews.md` is filled;
- "we don't store anyone's personal data" (R-08: scan artefacts may contain it).

## 6. Market slide numbers with v2 prices (recomputed; assumptions explicit)

The counts are from `market.md`; the segment split is the v1 one. The prices are from `business-model-v2.md`. The
purchase pattern per segment is an **assumption**, as `market-v2.md` asked.

| Segment | Units (base) | Assumed monthly purchase | UZS / month per unit | UZS / year |
|---|---|---|---|---|
| Small sites | 39,910 domains (45,130 SAM domains − banks − mid-regulated − mid) | 1 × I (Express) | 100,000 | 47.9 bn |
| Mid: private clinics and schools | 3,289 (50% of 6,577) | 1 × II | 250,000 | 9.9 bn |
| Mid-regulated (non-bank lenders, e-commerce platforms) | 352 organizations | 3 × II + 1 × III | 1,975,000 | 8.3 bn |
| Banks | 35 | 10 × II + 1 × III | 2,587,500 | 1.1 bn |
| **SAM (base)** | | | | **≈ 67 bn UZS ≈ $5.6 M** |
| SAM (high: small sites on 1 × II) | | | | ≈ 139 bn UZS ≈ $11.6 M |
| **SOM, year 3** | 2.5% of SAM domains ≈ 1,100 monitored sites | | | **≈ 1.7 bn UZS ≈ $140 k** |

USD at 11,971.64 UZS (CBU, 20.11.2026). Say "SAM", not TAM: the TAM that multiplies all .uz domains is easy to attack
(`market-v2.md`).

## Questions for the team

- **Q-R7-1 (team).** Who speaks? Suggestion: Role 3 speaks slides 1–2 and 5–8, Role 1 does slides 3–4 and the demo,
  Role 2 takes the legal questions (Q1, Q2, Q4, Q5, Q8).
- **Q-R7-2 (Role 1).** Is the "law change" view (F-16) on stage, or only mentioned? It is the strongest answer to Q9.
- **Q-R7-3 (team).** Replace slide 8's "ask" with a named pilot partner if the mentors give one at the checkpoint.

## Sources

- `GET https://probo.aicenterkk.tech/api/stats` (read 21.11.2026 08:30)
- `research/legal-27-1-2026.md`, `research/legal-liability.md`, `research/legal-norms.md`, `research/legal-our-risks.md`,
  `research/legal-ecommerce.md`, `research/csec.md`, `research/market.md`, `research/market-v2.md`,
  `research/business-model.md`, `research/business-model-v2.md`, `research/competitors-global.md`,
  `research/competitors.md`, `research/interviews.md`; passport §12–§13
