# Qalqon UI — design plan

Spec of screens: `../PRODUCT.md`. This file: how it looks and why.

## Concept: "what they say vs what they do"
The product compares a site's words with its behaviour. The type system shows that difference directly:

| Role | Typeface | Used for |
|---|---|---|
| **What they say** | Literata (serif) | Only words quoted from documents: privacy policies, offers, laws |
| **What they do** | IBM Plex Mono | Only machine evidence: hosts, IPs, requests, the live log |
| **Our voice** | IBM Plex Sans | Everything we write: UI, headings, explanations |

All three are self-hosted (`@fontsource/*`, no Google Fonts at the venue) and cover Uzbek Latin `oʻ gʻ ʼ`
(U+02BB–02BC) and Cyrillic — checked in their `unicode-range`.

## Color (every color means something)
| Name | Hex | Meaning |
|---|---|---|
| Surface | Astryx neutral (white) | Page |
| Sheet | `#f4f5f7` | Evidence panes (the "machine" side) |
| Ink | Astryx neutral text | Text |
| Allowed country | `#2a78d6` | Adequate-protection list (CMR No. 415) |
| Conditional | `#d69200` | Allowed only if a condition is met (e.g. US + DPF) |
| Not on the list | `#c7332f` | Country outside the list; also 🔴 violation |
| Undetermined | `#9aa0a6` | CDN / unknown — always labelled in text |

Map statuses validated with the dataviz validator (light mode): lightness, chroma, CVD separation (worst ΔE 16.3,
deutan) and normal-vision floor (21.4) pass; amber is below 3:1 contrast, so the map always has a labelled legend,
per-country tooltips and the host table as the table view. Findings use Astryx `Badge` variants
(`error` / `warning` / `neutral`). No decorative color, no gradients, no shadows beyond the theme's.

## Layout
Left-aligned, one column up to 1120 px; the live scan and the says-vs-does card split into two columns on desktop
and stack on mobile.

```
Home                                         Report
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│ Qalqon        Tarix   UZ RU  Taqdimot │     │ site            score scale  ● ● ●   │
│                                        │     │ [Umumiy][Topilmalar][Oqim][Siyosat] │
│ Saytingiz shaxsiy maʼlumotlarni        │     │ ┌ policy says (serif) ┬ site does ─┐│
│ aslida qayerga yuboryapti?             │     │ │ «…berilmaydi…»       │ mono trace  ││
│ [ https://…            ] [Tekshirish]  │     │ └──────────────────────┴─────────────┘│
│                                        │     │ findings list …                       │
│ says-vs-does excerpt (sample report)   │     └──────────────────────────────────────┘
│ market facts as sentences              │
└──────────────────────────────────────┘
```

## Principles
1. **One memorable element:** the says-vs-does split (serif quote on white, mono trace on the sheet). Everything
   else stays quiet.
2. **Motion only where the system is working:** log lines appear and countries light up during a scan. The report
   itself does not animate. `prefers-reduced-motion` turns the live effects off.
3. **No template chrome:** no all-caps eyebrows, no "→" in buttons, no stat cards with big numbers, no middle-dot
   meta strings, no emoji icons. Numbering only where content is a real sequence (scan stages).
4. **Plain words, user's point of view:** "Tekshirish" (Check), "Topilmalar" (Findings); errors say what happened
   and what to do.
5. **Quality floor:** contrast ≥ 4.5:1 for text, visible focus, 375 / 768 / 1024 / 1440 px, reduced motion
   (UI UX Pro Max checklist).
