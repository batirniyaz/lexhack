// The report screen: header with score, tabs (overview, findings, data flows, policy). PRODUCT.md §4.3.
import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { useNavigate } from 'react-router'
import { Badge } from '@astryxdesign/core/Badge'
import { Banner } from '@astryxdesign/core/Banner'
import { Button } from '@astryxdesign/core/Button'
import { Collapsible } from '@astryxdesign/core/Collapsible'
import { Link } from '@astryxdesign/core/Link'
import { Table, proportional } from '@astryxdesign/core/Table'
import { TabList, Tab } from '@astryxdesign/core/TabList'
import { api, authQuery, type Localized, type LawChange, type Seal, type Facts, type Finding, type Host, type Level, type Report } from '../api'
import { CATEGORY, CLAIM, ELEMENT, PD_TYPE, countryName, formatDate, useSettings } from '../i18n'
import { FlowMap, statusKey, type MapCountry } from './FlowMap'

const LEVEL_BADGE: Record<Level, 'error' | 'warning' | 'neutral'> = {
  violation: 'error', risk: 'warning', recommendation: 'neutral',
}
const LEVEL_ORDER: Level[] = ['violation', 'risk', 'recommendation']
const COVERAGE_BADGE = { named: 'success', company: 'info', kind: 'neutral', none: 'warning' } as const

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
  // "ZRU-547 «…»" → "ZRU-547"; acts without a short code keep their title (e-commerce pilot laws).
  const code = /^(ZRU|ЗРУ|CMR|VMQ|ПКМ)[-\s]/i.test(act) ? act.split(' ')[0] : act
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
                  <div style={{ fontSize: 14, marginBottom: 6 }}>{lawRef((lang === 'ru' && b.act_ru) || b.act, b.article, lang)}</div>
                  {b.quote_uz && <blockquote className="q-quote">{b.quote_uz}</blockquote>}
                  {b.quote_uz && <div className="q-quote-meta">{t.official}</div>}
                  {lang === 'ru' && b.quote_ru && <blockquote className="q-quote" style={{ marginTop: 8 }}>{b.quote_ru}</blockquote>}
                  {lang === 'ru' && b.quote_ru && <div className="q-quote-meta">{t.unofficial}</div>}
                  {!b.quote_uz && b.citations?.map((c) => (
                    <div key={c.article} style={{ marginTop: 8 }}>
                      <blockquote className="q-quote">
                        {c.heading && <span className="q-quote-heading">{c.heading}</span>}
                        {c.parts.map((p, j) => <span key={j} className="q-quote-part">{p.text}</span>)}
                      </blockquote>
                      <div className="q-quote-meta">
                        {t.cite_meta(c.edition_date ? c.edition_date.split('-').reverse().join('.') : '—')}
                        {c.url && <> · <Link href={c.url}>{t.open_lex}</Link></>}
                      </div>
                    </div>
                  ))}
                  {!b.citations?.length && (b.url || b.url_ru) && (
                    <div className="q-quote-meta"><Link href={(lang === 'ru' && b.url_ru) || b.url || ''}>{t.open_lex}</Link></div>
                  )}
                </div>
              ))}
            </div>
          )}
          {finding.sanction_local?.[lang] && (
            <div>
              <h4>{t.consequences}</h4>
              <p style={{ margin: '0 0 6px' }}>{finding.sanction_local[lang]}</p>
              <p className="q-muted" style={{ margin: 0, fontSize: 13 }}>{t.who_pays} {t.sanction_meta}</p>
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

export function FindingList({ findings, openFirst = false, openAll = false }: { findings: Finding[]; openFirst?: boolean; openAll?: boolean }) {
  const { t } = useSettings()
  if (findings.length === 0) return <p className="q-muted">{t.no_findings}</p>
  const sorted = [...findings].sort((a, b) => LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level))
  return <div>{sorted.map((f, i) => <FindingItem key={`${f.rule_id}-${openAll}`} finding={f} open={openAll || (openFirst && i === 0)} />)}</div>
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
      {report.policy_coverage && report.policy_coverage.length > 0 ? (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 6px' }}>{t.cov_title}</h3>
          <p className="q-muted" style={{ margin: '0 0 12px', fontSize: 14 }}>{t.cov_text}</p>
          <ul className="q-checklist q-cov">
            {report.policy_coverage.map((c) => (
              <li key={c.entity}>
                <Badge variant={COVERAGE_BADGE[c.level]} label={t[`cov_${c.level}`]} />
                <div>
                  <div>{c.entity} <span className="q-muted">· {countryName(c.country, lang)} · {c.categories.map((k) => CATEGORY[lang][k] ?? k).join(', ')}</span></div>
                  <div className="q-mono q-muted" style={{ fontSize: 12.5 }}>{c.hosts.join(', ')}</div>
                </div>
              </li>
            ))}
          </ul>
        </section>
      ) : undisclosed && undisclosed.length > 0 && (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.undisclosed}</h3>
          <p style={{ margin: 0 }}>{undisclosed.map((u) => `${u.entity} (${countryName(u.country, lang)})`).join(', ')}</p>
        </section>
      )}
    </div>
  )
}

function FormsView({ facts }: { facts?: Facts }) {
  const { t, lang } = useSettings()
  const forms = (facts?.forms ?? []).filter((f) => f.collects_pd)
  if (forms.length === 0) return <p className="q-muted">{t.forms_none}</p>
  return (
    <div>
      {forms.map((form, i) => (
        <div key={i} className="q-promise">
          <div style={{ display: 'flex', gap: 10, alignItems: 'baseline', flexWrap: 'wrap' }}>
            <span className="q-mono">{form.pages[0]}</span>
            <Badge variant={form.has_consent ? 'success' : 'error'} label={form.has_consent ? t.with_consent : t.no_consent} />
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {form.fields.filter((f) => f.pd).map((f, j) => (
              <Badge key={j} variant="neutral" label={`${PD_TYPE[lang][f.pd ?? ''] ?? f.pd}: ${f.label || f.name || '—'}`} />
            ))}
          </div>
          {form.pages.length > 1 && <div className="q-muted" style={{ fontSize: 13 }}>{t.form_also_on(form.pages.length - 1)}</div>}
        </div>
      ))}
    </div>
  )
}

interface PageRow extends Record<string, unknown> { url: string; status: string; title: string }
interface CookieRow extends Record<string, unknown> { key: string; name: string; domain: string; third: string; landing: string }

/** "The law changed → the status changed": the same saved facts under the old and the new wording (F-16). */
function LawChangeCard({ change }: { change: LawChange }) {
  const { t, lang } = useSettings()
  const levelLabel = useLevelLabel()
  const label = (l: Localized) => l[lang] || l.en || ''
  const date = (d: string | null) => (d ? d.split('-').reverse().join('.') : '…')
  const quote = lang === 'ru' ? change.previous.basis?.quote_ru : change.previous.basis?.quote_uz
  const link = (lang === 'ru' && change.previous.basis?.url_ru) || change.previous.basis?.url
  return (
    <section className="q-lawchange" aria-label={t.lc_title}>
      <h2 style={{ fontSize: 18, margin: '0 0 6px' }}>{t.lc_title}</h2>
      <p className="q-muted" style={{ margin: '0 0 16px', fontSize: 14 }}>{t.lc_text}</p>
      <div className="q-lc-grid">
        {[change.previous, change.current].map((v, i) => (
          <div key={v.id} className="q-lc-col">
            <div className="q-muted" style={{ fontSize: 13 }}>{i === 0 ? t.lc_before : t.lc_now} · {date(v.in_force.from)} – {v.in_force.to ? date(v.in_force.to) : t.lc_today}</div>
            <div className="q-lc-score">{v.score ?? '—'}<span>/100</span></div>
            <div style={{ fontSize: 14 }}>{label(v.label)}</div>
          </div>
        ))}
      </div>
      {change.changes.length > 0 && (
        <ul className="q-lc-changes">
          {change.changes.map((c) => (
            <li key={c.rule_id}>
              <span className="q-mono q-muted">{c.rule_id}</span>{' '}
              <span>{c.title ? label(c.title) : ''}</span>{': '}
              <b>{c.before ? levelLabel(c.before) : t.lc_none}</b> → <b>{c.after ? levelLabel(c.after) : t.lc_none}</b>
            </li>
          ))}
        </ul>
      )}
      {quote && (
        <details className="q-lc-quote">
          <summary>{t.lc_old_text}</summary>
          <blockquote className="q-quote">{quote}</blockquote>
          {link && <div className="q-quote-meta"><Link href={link}>{t.open_lex}</Link> · {t.lc_unverified}</div>}
        </details>
      )}
    </section>
  )
}

/** Scope + integrity: what was checked, from where, with which rules; hashes and the Ed25519 signature (F-19). */
function SealView({ report, seal, scanId }: { report: Report; seal?: Seal | null; scanId?: string }) {
  const { t } = useSettings()
  const scope = report.scope
  if (!scope) return null
  const rows: [string, React.ReactNode][] = [
    [t.seal_mode, t.seal_passive],
    [t.seal_vantage, scope.vantage ?? t.seal_vantage_unknown],
    [t.seal_when, scope.scanned_at ? formatDate(scope.scanned_at) : '—'],
    [t.seal_pages, t.scanned(scope.pages_count ?? 0, scope.requests ?? 0)],
    [t.seal_rules, <span className="q-mono">{scope.rules_version}</span>],
  ]
  if (scope.llm?.model) rows.push([t.seal_model, <span className="q-mono">{scope.llm.model} · {scope.llm.prompt_version}</span>])
  if (seal) {
    rows.push(['SHA-256 · report', <span className="q-mono q-hash">{seal.statement.sha256.report}</span>])
    if (seal.statement.sha256.facts) rows.push(['SHA-256 · facts', <span className="q-mono q-hash">{seal.statement.sha256.facts}</span>])
    if (seal.statement.sha256.har) rows.push(['SHA-256 · HAR', <span className="q-mono q-hash">{seal.statement.sha256.har}</span>])
    rows.push([t.seal_signature, <span>{seal.algorithm} · <span className="q-mono">{seal.statement.key_id}</span> · {formatDate(seal.statement.sealed_at)}</span>])
  }
  return (
    <section>
      <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.seal_title}</h3>
      <dl className="q-dl">
        {rows.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}
      </dl>
      <p className="q-muted" style={{ fontSize: 13, margin: '10px 0 0' }}>{t.seal_note}</p>
      {seal && scanId && (
        <div style={{ display: 'flex', gap: 16, marginTop: 10, flexWrap: 'wrap' }}>
          <Link href={`/api/scans/${scanId}/evidence?${authQuery(scanId)}`}>{t.seal_download}</Link>
          <Link href="/verify">{t.seal_verify}</Link>
        </div>
      )}
    </section>
  )
}

function EvidenceView({ facts, scanId, report, seal }: { facts?: Facts; scanId?: string; report: Report; seal?: Seal | null }) {
  const { t } = useSettings()
  if (!facts) return null
  const pages: PageRow[] = facts.pages.map((p) => ({ url: p.final_url, status: String(p.status ?? '—'), title: p.title ?? '' }))
  const cookies: CookieRow[] = (facts.cookies ?? []).map((c, i) => ({
    key: `${c.name}-${c.domain}-${i}`, name: c.name, domain: c.domain,
    third: c.third_party ? t.yes : t.no, landing: c.set_on_landing ? t.yes : t.no,
  }))
  return (
    <div style={{ display: 'grid', gap: 36 }}>
      <SealView report={report} seal={seal} scanId={scanId} />
      {scanId && <div><Link href={`/api/scans/${scanId}/har?${authQuery(scanId)}`}>{t.ev_har}</Link></div>}
      <section>
        <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.ev_pages}</h3>
        <Table<PageRow> data={pages} idKey="url" density="compact" columns={[
          { key: 'url', header: 'URL', width: proportional(3, { minWidth: 260 }), renderCell: (r) => <span className="q-mono">{r.url}</span> },
          { key: 'status', header: t.ev_status, align: 'end' },
          { key: 'title', header: t.ev_title, width: proportional(2) },
        ]} />
      </section>
      <section>
        <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.ev_cookies} ({cookies.length})</h3>
        <Table<CookieRow> data={cookies} idKey="key" density="compact" columns={[
          { key: 'name', header: t.ev_cookie_name, renderCell: (r) => <span className="q-mono">{r.name}</span> },
          { key: 'domain', header: t.ev_cookie_domain, renderCell: (r) => <span className="q-mono">{r.domain}</span> },
          { key: 'third', header: t.ev_third },
          { key: 'landing', header: t.first },
        ]} />
      </section>
      {(facts.backends ?? []).length > 0 && (
        <section>
          <h3 style={{ fontSize: 16, margin: '0 0 10px' }}>{t.ev_backends}</h3>
          {(facts.backends ?? []).map((b, i) => (
            <div key={i} className="q-mono" style={{ marginBottom: 6 }}>
              {b.kind}{b.region ? ` (${b.region})` : ''} <span className="q-muted">{b.source}</span>
            </div>
          ))}
        </section>
      )}
    </div>
  )
}

type TabKey = 'overview' | 'findings' | 'flows' | 'policy' | 'forms' | 'evidence'
const TAB_ORDER: TabKey[] = ['overview', 'findings', 'flows', 'policy', 'forms', 'evidence']

interface ReportViewProps {
  report: Report
  facts?: Facts
  displaySite: string
  scanId?: string
  domain?: string
  readonly?: boolean
  seal?: Seal | null
}

export function ReportView({ report, facts, displaySite, scanId, domain, readonly = false, seal }: ReportViewProps) {
  const { t } = useSettings()
  const navigate = useNavigate()
  const [tab, setTab] = useState<TabKey>('overview')
  const [printing, setPrinting] = useState(false)
  const [share, setShare] = useState<'idle' | 'busy' | 'copied' | 'error'>('idle')
  const map = useMemo(() => mapData(report), [report])
  const mismatch = report.findings.find((f) => f.rule_id === 'PD-MIS-01')
  const anyUnverified = report.findings.some((f) => !f.verified)
  const top = [...report.findings].sort((a, b) => LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level)).slice(0, 3)
  const date = formatDate(report.scanned_at)

  // PDF = the browser's "Save as PDF": render every section expanded, print, then go back.
  useEffect(() => {
    if (!printing) return
    const done = () => setPrinting(false)
    window.addEventListener('afterprint', done)
    const timer = window.setTimeout(() => window.print(), 500)
    return () => { window.clearTimeout(timer); window.removeEventListener('afterprint', done) }
  }, [printing])

  const onShare = async () => {
    if (!scanId) return
    setShare('busy')
    try {
      const { token } = await api.share(scanId)
      await navigator.clipboard?.writeText(`${window.location.origin}/r/${token}`)
      setShare('copied')
      window.setTimeout(() => setShare('idle'), 2500)
    } catch {
      setShare('error')
    }
  }

  const labels: Record<TabKey, string> = {
    overview: t.tab_overview, findings: `${t.tab_findings} ${report.findings.length}`, flows: t.tab_flows,
    policy: t.tab_policy, forms: t.tab_forms, evidence: t.tab_evidence,
  }
  const section = (key: TabKey): ReactNode => {
    switch (key) {
      case 'overview':
        return (
          <div style={{ display: 'grid', gap: 40 }}>
            {mismatch && <SaysDoes finding={mismatch} facts={facts} />}
            {report.law_change && report.law_change.changes.length > 0 && <LawChangeCard change={report.law_change} />}
            {!printing && (
              <section>
                <h2 style={{ fontSize: 18, margin: '0 0 6px' }}>{t.top_findings}</h2>
                <FindingList findings={top} />
              </section>
            )}
            <section>
              <p style={{ margin: '0 0 12px' }}>{t.flows_sentence(map.length)}</p>
              <FlowMap data={map} />
            </section>
            <p className="q-muted" style={{ fontSize: 14, margin: 0 }}>{t.limits}</p>
          </div>
        )
      case 'findings':
        return <FindingList findings={report.findings} openFirst openAll={printing} />
      case 'flows':
        return (
          <div style={{ display: 'grid', gap: 28 }}>
            {!printing && <FlowMap data={map} />}
            {facts && <HostTable hosts={facts.hosts} />}
          </div>
        )
      case 'policy':
        return <PolicyView report={report} facts={facts} />
      case 'forms':
        return <FormsView facts={facts} />
      case 'evidence':
        return <EvidenceView facts={facts} scanId={printing ? undefined : scanId} report={report} seal={seal} />
    }
  }

  return (
    <div>
      <div className="q-report-head">
        <div>
          <h1>{displaySite}</h1>
          <div className="q-muted">{date}. {t.scanned(report.stats.pages, report.stats.requests)}</div>
          <div className="q-actions q-noprint">
            {!readonly && domain && (
              <Button size="sm" variant="secondary" label={t.act_history} onClick={() => navigate(`/sites/${domain}`)} />
            )}
            {!readonly && scanId && (
              <Button size="sm" variant="secondary" isLoading={share === 'busy'} onClick={onShare}
                label={share === 'copied' ? t.act_shared : share === 'error' ? t.act_share_error : t.act_share} />
            )}
            <Button size="sm" variant="secondary" label={t.act_pdf} onClick={() => setPrinting(true)} />
          </div>
        </div>
        <ScoreScale report={report} />
      </div>
      <div style={{ marginBottom: 20 }}><Banner status="info" title={anyUnverified ? t.not_verified : t.signs_note} /></div>
      {printing ? (
        <div className="q-print-all">
          {TAB_ORDER.map((key) => (
            <section key={key} className="q-print-section">
              <h2 className="q-print-h">{labels[key]}</h2>
              {section(key)}
            </section>
          ))}
        </div>
      ) : (
        <>
          <div className="q-noprint">
            <TabList value={tab} onChange={(v) => setTab(v as TabKey)} hasDivider role="tablist">
              {TAB_ORDER.map((key) => <Tab key={key} value={key} label={labels[key]} panelId="q-panel" />)}
            </TabList>
          </div>
          <div id="q-panel" role="tabpanel" style={{ paddingTop: 28 }}>{section(tab)}</div>
        </>
      )}
    </div>
  )
}
