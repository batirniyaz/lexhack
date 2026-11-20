// The report screen: header with score, tabs (overview, findings, data flows, policy). PRODUCT.md §4.3.
import { useMemo, useState } from 'react'
import { Badge } from '@astryxdesign/core/Badge'
import { Banner } from '@astryxdesign/core/Banner'
import { Button } from '@astryxdesign/core/Button'
import { Collapsible } from '@astryxdesign/core/Collapsible'
import { Link } from '@astryxdesign/core/Link'
import { Table, proportional } from '@astryxdesign/core/Table'
import { TabList, Tab } from '@astryxdesign/core/TabList'
import type { Facts, Finding, Host, Level, Report } from '../api'
import { CATEGORY, CLAIM, ELEMENT, countryName, formatDate, useSettings } from '../i18n'
import { FlowMap, statusKey, type MapCountry } from './FlowMap'

const LEVEL_BADGE: Record<Level, 'error' | 'warning' | 'neutral'> = {
  violation: 'error', risk: 'warning', recommendation: 'neutral',
}
const LEVEL_ORDER: Level[] = ['violation', 'risk', 'recommendation']

function useLevelLabel() {
  const { t } = useSettings()
  return (level: Level) => ({ violation: t.lvl_violation, risk: t.lvl_risk, recommendation: t.lvl_recommendation }[level])
}

function title(finding: Finding, lang: 'uz' | 'ru'): string {
  return finding.title[lang] || finding.title.en || finding.rule_id
}

export function ScoreScale({ report }: { report: Report }) {
  const { t } = useSettings()
  const levelLabel = useLevelLabel()
  const score = report.score ?? 0
  return (
    <div className="q-scale" aria-label={`${t.score}: ${score} ${t.of100}`}>
      <div className="q-scale-top">
        <span className="q-scale-num">{score}</span>
        <span className="q-muted">{t.of100}</span>
      </div>
      <div className="q-scale-track"><div className="q-scale-fill" style={{ width: `${score}%` }} /></div>
      <div className="q-scale-levels">
        {LEVEL_ORDER.map((level) => (
          <Badge key={level} variant={LEVEL_BADGE[level]} label={`${report.levels?.[level] ?? 0} ${levelLabel(level)}`} />
        ))}
      </div>
    </div>
  )
}

/** The memorable element: the policy's own words next to the network evidence that contradicts them. */
export function SaysDoes({ finding, facts }: { finding: Finding; facts?: Facts }) {
  const { t, lang } = useSettings()
  const data = (finding.evidence[0]?.data ?? {}) as { quote?: string; observed?: { entity: string; country: string }[] }
  const observed = data.observed ?? []
  const hosts = facts?.hosts ?? []
  const trace = observed.flatMap((o) =>
    hosts.filter((h) => h.third_party && h.entity === o.entity).slice(0, 2).map((h) => ({ host: h, country: o.country })),
  ).slice(0, 7)
  const doc = facts?.policy?.documents?.[0]
  const law = finding.legal_basis[0]
  const allOnLanding = trace.length > 0 && trace.every(({ host }) => host.on_landing)
  return (
    <section className="q-sd" aria-label={`${t.says} / ${t.does}`}>
      <div className="q-sd-says">
        <p className="q-sd-head">{t.says}</p>
        <blockquote className="q-sd-quote">«{data.quote}»</blockquote>
        {doc && <p className="q-sd-source">{doc.url}</p>}
      </div>
      <div className="q-sd-does">
        <p className="q-sd-head">{t.does}{allOnLanding ? `: ${t.first_visit_all}` : ''}</p>
        <ul className="q-sd-trace">
          {trace.length > 0 ? trace.map(({ host, country }) => (
            <li key={host.host}>
              <span>{host.host}</span>
              <span className="q-c">{host.entity}</span>
              <span>{country}</span>
            </li>
          )) : observed.map((o) => (
            <li key={o.entity}><span>{o.entity}</span><span className="q-c" /><span>{o.country}</span></li>
          ))}
        </ul>
      </div>
      {law && (
        <div className="q-sd-law">
          {lawRef(law.act, law.article, lang)}. {capitalize(finding.verified ? t.rule_verified : t.rule_unverified)}.
          {finding.downgraded ? ` ${t.downgraded}` : ''}
        </div>
      )}
    </section>
  )
}

function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1)
}

/** "ZRU-547 «…»", "22 (truthful…) — NOT VERIFIED" -> "ZRU-547, 22-modda" / "ЗРУ-547, ст. 22" (English notes dropped). */
export function lawRef(act: string, article: string | null, lang: 'uz' | 'ru'): string {
  const code = act.split(' ')[0]
  if (!article) return code
  const clean = article.replace(/\s*—\s*NOT VERIFIED.*$/i, '').replace(/\s*\([^)]*\)/g, '').trim()
  const main = clean.split(/[;]/)[0]
  const [num, ...rest] = main.split(',').map((s) => s.trim())
  const part = rest.join(', ').replace(/part\s+(\d+)/i, lang === 'uz' ? '$1-qism' : 'ч. $1').replace(/ed\.\s*/i, '')
  const article_ = lang === 'uz' ? `${num}-modda` : `ст. ${num}`
  return [lang === 'uz' ? code : code.replace('ZRU', 'ЗРУ'), article_, part].filter(Boolean).join(', ')
}

function CopyButton({ text }: { text: string }) {
  const { t } = useSettings()
  const [done, setDone] = useState(false)
  return (
    <Button size="sm" variant="secondary" label={done ? t.copied : t.copy}
      onClick={() => { void navigator.clipboard?.writeText(text); setDone(true); setTimeout(() => setDone(false), 1600) }} />
  )
}

function FindingItem({ finding, open }: { finding: Finding; open: boolean }) {
  const { t, lang } = useSettings()
  const levelLabel = useLevelLabel()
  const fix = finding.fix[lang] || finding.fix.en || ''
  const law = finding.legal_basis.filter((b) => b.article || b.quote_uz || b.quote_ru)
  const trigger = (
    <div className="q-finding-head">
      <span><Badge variant={LEVEL_BADGE[finding.level]} label={levelLabel(finding.level)} /></span>
      <span className="q-finding-title">{title(finding, lang)}</span>
      <span className="q-muted q-mono">{finding.rule_id}</span>
    </div>
  )
  return (
    <div className="q-finding">
      <Collapsible trigger={trigger} defaultIsOpen={open}>
        <div className="q-finding-body">
          <div>
            <h4>{t.evidence}</h4>
            <ul className="q-evidence">
              {finding.evidence.map((e, i) => <li key={i}>{e.summary}</li>)}
            </ul>
            {finding.downgraded && <p className="q-muted" style={{ fontSize: 13 }}>{t.downgraded}</p>}
          </div>
          {law.length > 0 && (
            <div>
              <h4>{t.law}</h4>
              {law.map((b, i) => (
                <div key={i} style={{ marginBottom: 12 }}>
                  <div style={{ fontSize: 14, marginBottom: 6 }}>{lawRef(b.act, b.article, lang)}</div>
                  {b.quote_uz && <blockquote className="q-quote">{b.quote_uz}</blockquote>}
                  {b.quote_uz && <div className="q-quote-meta">{t.official}</div>}
                  {lang === 'ru' && b.quote_ru && <blockquote className="q-quote" style={{ marginTop: 8 }}>{b.quote_ru}</blockquote>}
                  {lang === 'ru' && b.quote_ru && <div className="q-quote-meta">{t.unofficial}</div>}
                  {(b.url || b.url_ru) && (
                    <div className="q-quote-meta"><Link href={(lang === 'ru' && b.url_ru) || b.url || ''}>{t.open_lex}</Link></div>
                  )}
                </div>
              ))}
            </div>
          )}
          {fix && (
            <div>
              <h4>{t.fix}</h4>
              <div className="q-fix"><span style={{ flex: 1 }}>{fix}</span><CopyButton text={fix} /></div>
            </div>
          )}
          <div className="q-muted" style={{ fontSize: 13 }}>{finding.verified ? t.rule_verified : t.rule_unverified}</div>
        </div>
      </Collapsible>
    </div>
  )
}

export function FindingList({ findings, openFirst = false }: { findings: Finding[]; openFirst?: boolean }) {
  const { t } = useSettings()
  if (findings.length === 0) return <p className="q-muted">{t.no_findings}</p>
  const sorted = [...findings].sort((a, b) => LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level))
  return <div>{sorted.map((f, i) => <FindingItem key={f.rule_id} finding={f} open={openFirst && i === 0} />)}</div>
}

interface HostRow extends Record<string, unknown> {
  host: string
  entity: string
  company: string
  server: string
  category: string
  first: string
  requests: number
}

export function HostTable({ hosts }: { hosts: Host[] }) {
  const { t, lang } = useSettings()
  const rows: HostRow[] = hosts.filter((h) => h.third_party).map((h) => ({
    host: h.host,
    entity: h.entity ?? '—',
    company: countryName(h.company_country, lang),
    server: h.is_cdn ? 'CDN' : countryName(h.server_country, lang),
    category: h.category ? (CATEGORY[lang][h.category] ?? h.category) : '—',
    first: h.on_landing ? t.yes : t.no,
    requests: h.requests,
  }))
  return (
    <Table<HostRow>
      data={rows}
      idKey="host"
      density="compact"
      columns={[
        { key: 'host', header: t.host, width: proportional(2.4, { minWidth: 220 }), renderCell: (r) => <span className="q-mono">{r.host}</span> },
        { key: 'entity', header: t.owner },
        { key: 'company', header: t.company_country },
        { key: 'server', header: t.server_country },
        { key: 'category', header: t.category },
        { key: 'first', header: t.first },
        { key: 'requests', header: t.requests, align: 'end' },
      ]}
    />
  )
}

function mapData(report: Report): MapCountry[] {
  return report.flows
    .filter((f) => f.country && f.country !== '?' && f.country !== 'UZ')
    .map((f) => ({ code: f.country, status: statusKey(f.status), hosts: f.hosts, entities: f.entities }))
}

export function PolicyView({ report, facts }: { report: Report; facts?: Facts }) {
  const { t, lang } = useSettings()
  const policy = facts?.policy
  if (!policy || policy.status !== 'ok') return <p className="q-muted">{t.no_policy}</p>
  const contradicted = new Set(
    report.findings.filter((f) => f.rule_id === 'PD-MIS-01')
      .flatMap((f) => f.evidence.map((e) => String((e.data as { quote?: string } | undefined)?.quote ?? ''))),
  )
  const undisclosed = report.findings.find((f) => f.rule_id === 'PD-POL-02')?.evidence
    .flatMap((e) => ((e.data as { undisclosed?: { entity: string; country: string }[] } | undefined)?.undisclosed ?? []))
  return (
    <div style={{ display: 'grid', gap: 36 }}>
      <section>
        <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.docs_read}</h3>
        {policy.documents?.map((d) => <div key={d.url} className="q-mono q-muted">{d.url}</div>)}
      </section>
      {policy.elements && policy.is_personal_data_policy && (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 14px' }}>{t.elements}</h3>
          <ul className="q-checklist">
            {Object.entries(policy.elements).map(([key, el]) => (
              <li key={key}>
                <Badge variant={el.present ? 'success' : 'neutral'} label={el.present ? t.present : t.missing} />
                <div>
                  <div>{ELEMENT[lang][key] ?? key}</div>
                  {el.quote && <blockquote className="q-quote" style={{ marginTop: 6, fontSize: 14.5 }}>{el.quote}</blockquote>}
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}
      {policy.claims && policy.claims.length > 0 && (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 6px' }}>{t.promises}</h3>
          {policy.claims.map((c, i) => {
            const isContradicted = contradicted.has(c.quote)
            return (
              <div key={i} className="q-promise">
                <div style={{ display: 'flex', gap: 10, alignItems: 'baseline', flexWrap: 'wrap' }}>
                  <b style={{ fontWeight: 500 }}>{CLAIM[lang][c.type] ?? c.type}</b>
                  <Badge variant={isContradicted ? 'error' : 'neutral'}
                    label={isContradicted ? t.promise_contradicted : t.promise_unchecked} />
                </div>
                <blockquote className="q-quote">«{c.quote}»</blockquote>
              </div>
            )
          })}
        </section>
      )}
      {undisclosed && undisclosed.length > 0 && (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.undisclosed}</h3>
          <p style={{ margin: 0 }}>{undisclosed.map((u) => `${u.entity} (${countryName(u.country, lang)})`).join(', ')}</p>
        </section>
      )}
    </div>
  )
}

type TabKey = 'overview' | 'findings' | 'flows' | 'policy'

export function ReportView({ report, facts, displaySite }: { report: Report; facts?: Facts; displaySite: string }) {
  const { t } = useSettings()
  const [tab, setTab] = useState<TabKey>('overview')
  const map = useMemo(() => mapData(report), [report])
  const mismatch = report.findings.find((f) => f.rule_id === 'PD-MIS-01')
  const anyUnverified = report.findings.some((f) => !f.verified)
  const top = [...report.findings].sort((a, b) => LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level)).slice(0, 3)
  const date = formatDate(report.scanned_at)

  return (
    <div>
      <div className="q-report-head">
        <div>
          <h1>{displaySite}</h1>
          <div className="q-muted">{date}. {t.scanned(report.stats.pages, report.stats.requests)}</div>
        </div>
        <ScoreScale report={report} />
      </div>
      {anyUnverified && <div style={{ marginBottom: 20 }}><Banner status="info" title={t.not_verified} /></div>}
      <TabList value={tab} onChange={(v) => setTab(v as TabKey)} hasDivider role="tablist">
        <Tab value="overview" label={t.tab_overview} panelId="q-panel" />
        <Tab value="findings" label={`${t.tab_findings} ${report.findings.length}`} panelId="q-panel" />
        <Tab value="flows" label={t.tab_flows} panelId="q-panel" />
        <Tab value="policy" label={t.tab_policy} panelId="q-panel" />
      </TabList>
      <div id="q-panel" role="tabpanel" style={{ paddingTop: 28 }}>
        {tab === 'overview' && (
          <div style={{ display: 'grid', gap: 40 }}>
            {mismatch && <SaysDoes finding={mismatch} facts={facts} />}
            <section>
              <h2 style={{ fontSize: 18, margin: '0 0 6px' }}>{t.top_findings}</h2>
              <FindingList findings={top} />
            </section>
            <section>
              <p style={{ margin: '0 0 12px' }}>{t.flows_sentence(map.length)}</p>
              <FlowMap data={map} />
            </section>
            <p className="q-muted" style={{ fontSize: 14, margin: 0 }}>{t.limits}</p>
          </div>
        )}
        {tab === 'findings' && <FindingList findings={report.findings} openFirst />}
        {tab === 'flows' && (
          <div style={{ display: 'grid', gap: 28 }}>
            <FlowMap data={map} />
            {facts && <HostTable hosts={facts.hosts} />}
          </div>
        )}
        {tab === 'policy' && <PolicyView report={report} facts={facts} />}
      </div>
    </div>
  )
}
