# Market for Probo in Uzbekistan (R-05)

- Author: [name], research team; prepared with Claude Code
- Date/time: 20.11 21:00; v2 21.11 00:30 (formula prices); v3 21.11 00:50 (sector packs from `service-catalog.md`)
- Passport version: 0.10 (the task brief named 0.5; the repo was at 0.10 when this file was written, see Questions)
- Confidence: **high** for the counts (official registries and statistics, opened on 20.11.2026); **low** for the shares and prices used in TAM/SAM/SOM (explicit assumptions, to be tested in R-06 interviews and with our own scan data)

> Product name: **Probo** (the working name in the passport is Qalqon, D-014). Repo documents are not renamed here.
> All USD figures use the Central Bank of Uzbekistan official rate for 20.11.2026: **1 USD = 11,971.64 UZS** ([cbu.uz](https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/)).
> Prices used in the TAM/SAM/SOM come from the price formula in `research/business-model.md` (price = 4 × our cost, per module and per unit of scale) and are hypotheses.

## Conclusions

1. **V-10 is closed: the .uz zone has 182,338 active domains** (registry statistics, 20.11.2026), up 37,639 (+26%) since 1 January 2026. Registered is not the same as live: Hurricane Electric's DNS dataset sees 90,261 .uz domains, and 40,784 of them have an A record. **Live .uz websites: about 41,000–90,000.**
2. **The paying base is organizations, and the regulated segments can be counted:** 660,392 operating businesses and organizations (1 Nov 2026), 35 commercial banks, 237 non-bank credit organizations (136 of them microfinance), 8,912 outpatient clinics (5,929 owned by small businesses), 115 e-commerce platforms, 4,200+ IT Park residents. No official count was found for telecom operators, delivery services, online schools, online shops or mobile apps: `NOT VERIFIED`.
3. **Online activity is growing fast:** e-commerce sales reached 22.7 trillion UZS in 2025 (×1.5 year on year), the number of e-commerce platforms grew from 36 to 115, and the government wants the online share of retail raised from 4.6% to 11%. Every new online shop, form or app is a new data flow to check.
4. **TAM / SAM / SOM (base case, per year), by client size, sector packs and the price formula:** TAM **429.8 bn UZS ($35.9M)**, SAM **115.1 bn UZS ($9.6M)**, SOM in year 3 **4.52 bn UZS ($378k)**, of which 2.82 bn UZS ($236k) is recurring (2.5% of SAM, about 1,020 monitored domains). Small sites are 78% of SAM by money; 35 banks, 352 regulated mid-size companies and 6,577 private clinics and schools are the other 22% because they pay for their scale and for the checks their sector's law requires.
5. **B2G channel:** the Ministry of Justice legal service centers serve **21,292 organizations, including schools, kindergartens and polyclinics** (LexHackathon 2026 Ministry of Justice infographic). That is a ready-made list of organizations and a lawyer network to deliver our reports through. At the formula price (26,031 UZS per organization per month) it is worth 1.3–4.0 bn UZS ($111k–$333k) a year, on top of the commercial SAM.

## Data

### 1. Domains and websites (closes V-10)

| Indicator | Value | As of | Source | Checked |
|---|---|---|---|---|
| Active .uz domains | **182,338** | 20.11.2026 | .uz registry, [cctld.uz](https://cctld.uz/?lang=eng) | opened 20.11 |
| Pending activation | 1,127 | 20.11.2026 | [cctld.uz](https://cctld.uz/?lang=eng) | opened |
| Base at the start of 2026 ("since beginning of year") | 143,785 | 01.01.2026 | [cctld.uz](https://cctld.uz/?lang=eng) | opened |
| Net growth in 2026 | +37,639 (69,740 new, 32,101 deleted) | 20.11.2026 | [cctld.uz](https://cctld.uz/?lang=eng) | opened |
| .uz domains in Hurricane Electric's DNS dataset | 90,261 | 18.11.2026 | [bgp.he.net](https://bgp.he.net/report/dns/uz) | opened |
| …of which with an A record (can serve a website) | 40,784 | 18.11.2026 | [bgp.he.net](https://bgp.he.net/report/dns/uz) | opened |
| Uzbek organizations' websites outside .uz (.com, .org…) | unknown | — | — | `NOT VERIFIED` |
| Share of Uzbek enterprises that have a website | no official indicator found (stat.uz publishes only Internet access and PC use) | — | [siat.stat.uz indicator 1284](https://siat.stat.uz/data/1284/?lang=en) | `NOT VERIFIED` |

How to read it: the registry counts every paid-for domain, including parked and personal ones. Hurricane Electric's crawler methodology is not published, so 90,261 and 40,784 are a **proxy** for live sites, not an official count.

### 2. Organizations: who pays

| Segment (passport §7) | Count | As of | Source | Checked |
|---|---|---|---|---|
| All operating businesses and organizations | **660,392** (+19% y/y); small and micro: 489,100 (74.1%) | 01.11.2026 | National Statistics Committee via [Daryo, 17.11.2026](https://daryo.uz/en/2026/11/17/number-of-businesses-operating-in-uzbekistan-rises-19-to-660-400/) | opened |
| Commercial banks | **35** (assets 1,044.8 trn UZS) | 01.10.2026 | Central Bank via [UzDaily, 07.11.2026](https://www.uzdaily.uz/en/uzbekistans-12-largest-banks-hold-79-of-system-assets/) | opened |
| Non-bank credit organizations | **237**: 136 microfinance, 90 pawnshops, 9 factoring, 1 mortgage refinancing, 1 guarantee | 01.07.2026 | Central Bank via [Daryo, 20.08.2026](https://daryo.uz/en/2026/08/20/uzbekistans-non-bank-credit-organizations-see-assets-rise-64-to-224bn/) | opened |
| Outpatient clinics | **8,912**, of which **5,929** owned by small businesses (our proxy for private clinics) | 01.01.2026 | National Statistics Committee via [Daryo, 26.10.2026](https://daryo.uz/en/2026/10/26/uzbekistan-counts-nearly-9-000-outpatient-clinics-tashkent-leads/) | opened |
| E-commerce platforms | **115** (36 in 2024) | 2025 | NAPP via [UzDaily, 21.02.2026](https://www.uzdaily.uz/en/online-sales-in-uzbekistan-reach-227-trillion-soums-in-2025/) | opened |
| Online shops on their own sites | no official count | — | — | `NOT VERIFIED` |
| Non-state general schools | 551 | start of 2025/26 school year | [stat.uz](https://stat.uz/en/press-center/news-of-committee/68152-zbekistonda-khususij-maktablar-soni-551-taga-etdi-4) | search summary, page not opened |
| Non-state higher education organizations | 97 | 2025/26 | [siat.stat.uz indicator 3182](https://siat.stat.uz/data/3182/?lang=en) | search summary, page not opened |
| Family non-state preschools | 29,196 | end of 2025 | [stat.uz](https://stat.uz/en/press-center/news-of-committee/70678-zbekistonda-oilavij-nodavlat-bo-chalar-soni-29-2-mingtaga-etdi-4) | search summary, page not opened |
| Online schools and training centers | no official count | — | — | `NOT VERIFIED` |
| Delivery services | no official count | — | — | `NOT VERIFIED` |
| Telecom operators (mobile, fixed, ISPs) | no official count of licensed operators | — | — | `NOT VERIFIED` |
| IT Park residents | **4,200+** companies, 60,000+ employees | undated (page read 20.11.2026) | [gov.uz IT Park page](https://gov.uz/en/digital/activity_page/it-park-uzbekistan) | opened |
| IT Park: foreign-capital residents / exporting residents | 1,095 / 1,050 (exports to 102 countries) | H1 2026, published 06.08.2026 | [it-park.uz](https://www.it-park.uz/uz/itpark/news/it-park-rezidentlarining-eksport-geografiyasi-102-ta-mamlakatga-yetdi) | opened |
| IT Park participants' service exports | $392.5M in Jan–Jun 2026 (+$90.3M y/y) | H1 2026 | [stat.uz](https://stat.uz/oz/matbuot-markazi-2/qo-mita-yangiliklar-2/69842-it-park-ishtirokchilarining-khizmatlar-eksporti-392-5-mln-dollarga-etdi) | search summary, page not opened |
| Mobile apps published by Uzbek companies | no dataset found (would need AppBrain / Sensor Tower developer-country data) | — | — | `NOT VERIFIED` |
| Advocates | ~4,000 (a **2019** figure, stale) | 25.12.2019 | [Tashkent Times](https://www.tashkenttimes.uz/national/4797-there-are-4-000-advocates-in-uzbekistan-with-its-population-of-33-million) | opened; `NOT VERIFIED` for 2026 |

### 3. Ministry of Justice: legal service centers (B2G channel)

Source: LexHackathon 2026 Ministry of Justice infographic "Yuridik xizmatlar faoliyatini muvofiqlashtirish sohasida amalga oshirilgan ishlar", repo file `files/taqdimot.pdf` (read 20.11.2026).

| Indicator | Value | Quote (Uzbek, from the infographic) |
|---|---|---|
| Organizations served by the legal service centers | **21,292**, including schools, kindergartens and polyclinics | "21 292 ta tashkilotga, shu jumladan maktab, bog'cha va poliklinikalarga yuridik xizmat ko'rsatilmoqda" |
| Legal basis of the centers | Presidential resolutions PQ-5168 of 29.06.2021 and PQ-173 of 18.03.2022 | "PQ 5168 29.06.2021 Prezident qarori", "PQ 173 18.03.2022 Prezident qarori" |
| Draft documents reviewed since 2021 | 37 million | "37 mln hujjat loyihasi huquqiy ekspertizadan o'tkazildi" |
| Legal service staff in state bodies and organizations | 2,012 people | "2 012 nafar yuridik xizmat xodimi bugungi kunda faoliyat olib bormoqda" |
| Existing system | "E-huquqshunos" electronic system, mobile app | "'E-huquqshunos' elektron tizimi joriy qilinib…" |

Why it matters: these lawyers already review documents for 21,292 organizations but have no tool to check what those organizations' websites and apps do with personal data. The prize "pilot in Ministry of Justice systems" (passport §16) is the entry point.

### 4. Growth of the digital economy

| Indicator | Value | Source | Checked |
|---|---|---|---|
| E-commerce sales, 2025 | 22.7 trn UZS (×1.5 y/y) | NAPP via [UzDaily, 21.02.2026](https://www.uzdaily.uz/en/online-sales-in-uzbekistan-reach-227-trillion-soums-in-2025/) | opened |
| Online share of retail | 4.6% in 2025 (3.7% in 2024); total retail 492.8 trn UZS | same | opened |
| Government target | raise the domestic e-commerce share of retail to 11% (no year stated) | [Kun.uz, 10.04.2026](https://kun.uz/en/news/2026/04/10/president-mirziyoyev-sets-targets-to-triple-e-commerce-share-of-retail-trade) | opened |
| .uz domains in 2026 | +26% (143,785 → 182,338) | computed from [cctld.uz](https://cctld.uz/?lang=eng) | opened |
| Operating businesses | +19% y/y | [Daryo, 17.11.2026](https://daryo.uz/en/2026/11/17/number-of-businesses-operating-in-uzbekistan-rises-19-to-660-400/) | opened |

### 5. TAM / SAM / SOM (v3: by client size, sector packs, formula prices)

Prices come from the formula in `business-model.md` §5 (**price = 4 × our cost**, summed over modules and scale) with the **sector packs** from `service-catalog.md` §2 and §7, which pre-tick the services each sector's law requires. "Full" includes roadmap modules (mobile apps M8, inside scans M9); "available" uses only modules that need no new scanning technology.

| Segment | Who | Domains each | Price full, UZS/month | Price available, UZS/month |
|---|---|---|---|---|
| **Large** | 35 commercial banks (telecom operators would belong here, but their count is `NOT VERIFIED`, so they are left out) | 25 | 10,643,634 ($889) | 8,663,209 ($724) |
| **Mid-regulated** | 237 non-bank credit organizations + 115 e-commerce platforms = 352 (microfinance pack) | 3 | 2,109,998 ($176) | 2,052,590 ($171) |
| **Mid** | 5,929 private outpatient clinics + 551 private schools + 97 private universities = 6,577 (clinic pack) | 1 | 334,642 ($28) | 334,642 ($28) |
| **Small sites** | every other .uz site | 1 | 186,966 ($15.6) | 186,966 ($15.6) |
| B2G (separate) | organizations served by the Ministry of Justice legal service centers | 1 | 26,031 ($2.2) per organization | same |

#### TAM: every organization in the segment on its full module set

**TAM = 12 × (N_small × P_small + N_mid × P_mid + 352 × P_midreg + 35 × P_large)**, full prices.

| Case | N_small | Why | TAM, UZS/year | TAM, USD/year |
|---|---|---|---|---|
| Low | 81,753 | .uz domains seen in DNS (90,261) minus the 8,508 domains of the other segments | 223.2 bn | $18.6M |
| **Base** | **173,830** | all active .uz domains (182,338) minus 8,508 | **429.8 bn** | **$35.9M** |
| High | 653,428 | every operating organization (660,392) minus the 6,964 counted in the other segments | 1,505.8 bn | $125.8M |

Base TAM by segment: small sites 390.0 bn, mid 26.4 bn, mid-regulated 8.9 bn, large 4.5 bn UZS. N_mid = 6,577 in all three cases.

#### SAM: live sites that collect personal data, on the modules available without new technology

**SAM = 12 × (N_small × P_small + N_mid × P_mid + 352 × P_midreg + 35 × P_large)**, available prices.

- The total number of SAM domains is the same as in v1: live .uz sites × the share that collects personal data = 16,314 / **45,130** / 91,169 (low / base / high; 40% or 50% of 40,784, 90,261 or 182,338, **assumption**).
- `N_mid` = 6,577 × share of private clinics and schools with a site that collects personal data: 30% / **50%** / 70% (**assumption**).
- `N_small` = SAM domains − 875 (banks) − 1,056 (mid-regulated) − N_mid.

| Case | N_small | N_mid | SAM, UZS/year | SAM, USD/year |
|---|---|---|---|---|
| Low | 12,410 | 1,973 | 48.1 bn | $4.0M |
| **Base** | **39,911** | **3,288** | **115.1 bn** | **$9.6M** |
| High | 84,634 | 4,604 | 220.7 bn | $18.4M |

Base SAM by segment: small sites 89.5 bn (78%), mid 13.2 bn, mid-regulated 8.7 bn, large 3.6 bn UZS. History: v1 (fixed plans) 97.5 bn → v2 (formula) 109.2 bn → v3 (sector packs) 115.1 bn, because regulated sectors now pay for the checks their law requires.

**B2G layer, counted separately:** 21,292 organizations × share with a website or app (20% / 40% / 60%, **assumption**) × 26,031 UZS × 12.

| Case | Organizations | UZS/year | USD/year |
|---|---|---|---|
| Low | 4,258 | 1.33 bn | $111k |
| Base | 8,517 | 2.66 bn | $222k |
| High | 12,775 | 3.99 bn | $333k |

#### SOM: what we can win by the end of year 3 (2029), bottom-up

| Line | Price (available), UZS/month | Low | **Base** | High |
|---|---|---|---|---|
| Small sites | 186,966 | 300 → 673M | **800 → 1,795M** | 1,500 → 3,365M |
| Clinics / schools | 334,642 | 25 → 100M | **60 → 241M** | 120 → 482M |
| MFO / e-commerce | 2,052,590 | 8 → 197M | **20 → 493M** | 40 → 985M |
| Banks | 8,663,209 | 2 → 208M | **4 → 416M** | 8 → 832M |
| Law-firm partner discount (30% of small and mid revenue at −20%, assumption) | | −46M | **−122M** | −231M |
| **Recurring revenue (ARR)** | | **1,132M ($94.6k)** | **2,822M ($235.7k)** | **5,433M ($453.9k)** |
| One-off: onboarding of a third of the mid-size and larger accounts in year 3 + Fix packs (150 / 400 / 800 at 559,830 UZS) | | 146M ($12.2k) | **367M ($30.7k)** | 735M ($61.4k) |
| B2G | 26,031 per organization | 0 | **1 contract, 4,258 organizations → 1,330M ($111.1k)** | 8,517 organizations → 2,660M ($222.2k) |
| **Total revenue, year 3** | | **1,278M UZS ($106.7k)** | **4,520M UZS ($377.5k)** | **8,829M UZS ($737.5k)** |
| Monitored domains | | ~400 | **~1,020** | ~1,940 |
| Recurring as a share of base SAM | | 1.0% | **2.5%** | 4.7% |

All amounts in UZS per year. Sanity checks for the base case: 800 small sites are 0.9% of the .uz domains seen in DNS; 4 of 35 banks; 20 of 352 regulated mid-size companies; 60 of about 3,300 private clinics and schools with a site.

**Beachhead list (countable, regulated, handle sensitive data):** 35 banks + 237 non-bank credit organizations + 115 e-commerce platforms + 5,929 private outpatient clinics + 551 private schools + 97 private universities = **6,964 named organizations**, plus 4,200+ IT Park residents who build sites and apps for others (the Launch check, M13, is made for them).

## Features for the product (§10 format)

IDs start at P-F20 to avoid a clash with P-F3…P-F7 in `scope-extension-proposal.md`. Role 1 assigns real F-IDs.

| ID | Feature | What it gives | Complexity | Who proposed | Status |
|---|---|---|---|---|---|
| P-F20 | **SAM calibrator:** from the F-03 batch scan, report the anonymized share of .uz sites with PD forms, trackers before consent and foreign transfers | Replaces the 50% `s_PD` assumption with our own measured number; also a B1 headline | S | Research (Role 3) | Proposal (Final) |
| P-F21 | **Sector tag** for every scanned domain (bank, MFO, clinic, e-commerce, education, government) from a list plus page keywords | Per-segment statistics for the pitch and per-segment SAM | S | Research | Proposal (Roadmap) |
| P-F22 | **Private teaser report:** send a site owner its own passive-scan summary (never public) as a sales opener | Turns the free scan into outbound sales; needs R-08 legal check first | S | Research | Proposal (Roadmap, after R-08) |

## Questions for the team / contradictions with the passport

1. **Passport version.** The task brief said v0.5; the repo was at v0.10 when this file was written, so this file follows v0.10 (including D-020: Opus 5.5 as the LLM).
2. **Name.** The brief and the team now call the product **Probo**; passport D-014 says the final name is still to be chosen. A decision-log entry would settle it.
3. **Mobile apps.** The brief says Probo checks apps too; passport §4 and F-09 keep the mobile scanner on the roadmap. Apps are left out of TAM/SAM/SOM until F-09 is in scope.
4. **IT Park numbers don't agree.** gov.uz says 4,200+ residents (undated) and 1,200+ exporters; it-park.uz says 1,050 exporters and 1,095 foreign-capital residents (H1 2026). IT Park is an organizer, so we can ask the mentors for an official dated number at the checkpoint.
5. **For Role 1:** can the batch scan give the share of scanned sites that have forms collecting PD (P-F20)? That one number replaces the main SAM assumption.
6. **No official counts** for telecom operators, delivery services, online schools, online shops and mobile apps. If a mentor asks, say "not published" and use the beachhead list above. Telecom operators are therefore missing from the "Large" segment, which makes TAM and SAM slightly conservative.
7. **Segment sizes in v2** (domains per client, scale of each preset) are assumptions taken from the worked examples in `business-model.md` §6. Real quantities come from discovery scans (P-F23, P-F28).
8. **V-10 is ready to close** (fact-check row below). Role 1 updates §14.

| ID | Claim | Status | Correct wording | Source |
|---|---|---|---|---|
| V-10 | The number of domains in the .uz zone | CONFIRMED | 182,338 active .uz domains on 20.11.2026, +37,639 since 1 January 2026 (registry). About 41–90 thousand are live sites (DNS proxy, Hurricane Electric, 18.11.2026) | https://cctld.uz/?lang=eng ; https://bgp.he.net/report/dns/uz |

## Sources

- https://cctld.uz/?lang=eng — .uz registry statistics, 20.11.2026
- https://bgp.he.net/report/dns/uz — Hurricane Electric .uz TLD report, 18.11.2026
- https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/ — CBU official USD rate, 20.11.2026
- https://daryo.uz/en/2026/11/17/number-of-businesses-operating-in-uzbekistan-rises-19-to-660-400/
- https://www.uzdaily.uz/en/uzbekistans-12-largest-banks-hold-79-of-system-assets/
- https://daryo.uz/en/2026/08/20/uzbekistans-non-bank-credit-organizations-see-assets-rise-64-to-224bn/
- https://daryo.uz/en/2026/10/26/uzbekistan-counts-nearly-9-000-outpatient-clinics-tashkent-leads/
- https://www.uzdaily.uz/en/online-sales-in-uzbekistan-reach-227-trillion-soums-in-2025/
- https://kun.uz/en/news/2026/04/10/president-mirziyoyev-sets-targets-to-triple-e-commerce-share-of-retail-trade
- https://stat.uz/en/press-center/news-of-committee/68152-zbekistonda-khususij-maktablar-soni-551-taga-etdi-4
- https://siat.stat.uz/data/3182/?lang=en
- https://stat.uz/en/press-center/news-of-committee/70678-zbekistonda-oilavij-nodavlat-bo-chalar-soni-29-2-mingtaga-etdi-4
- https://siat.stat.uz/data/1284/?lang=en
- https://gov.uz/en/digital/activity_page/it-park-uzbekistan
- https://www.it-park.uz/uz/itpark/news/it-park-rezidentlarining-eksport-geografiyasi-102-ta-mamlakatga-yetdi
- https://stat.uz/oz/matbuot-markazi-2/qo-mita-yangiliklar-2/69842-it-park-ishtirokchilarining-khizmatlar-eksporti-392-5-mln-dollarga-etdi
- https://www.tashkenttimes.uz/national/4797-there-are-4-000-advocates-in-uzbekistan-with-its-population-of-33-million
- `files/taqdimot.pdf` — LexHackathon 2026 Ministry of Justice infographic (in the repo)
