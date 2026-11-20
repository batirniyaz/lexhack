// Live scan screen (PRODUCT.md §4.2): stages, a monospace event log, counters, a map that lights up.
// Driven by the SSE feed; in presentation mode the site's domain is hidden in every line.
import { useEffect, useMemo, useReducer, useRef } from 'react'
import { Banner } from '@astryxdesign/core/Banner'
import { ProgressBar } from '@astryxdesign/core/ProgressBar'
import { subscribe, siteDomain, type Localized, type ScanEvent } from '../api'
import { CATEGORY, countryName, useSettings } from '../i18n'
import { FlowMap, type MapCountry } from './FlowMap'

interface LogLine { id: number; t: number; kind: string; text: string; level?: string }
interface LiveState {
  started: number
  url: string
  stage: number            // 1..5
  page: { n: number; max: number; url: string } | null
  hosts: Map<string, { country: string | null; entity: string | null }>
  forms: number
  documents: number
  log: LogLine[]
  challenge: boolean
  blocked: boolean
  finished: 'done' | 'error' | null
}

type Action = { event: ScanEvent; labels: Record<string, string> }

function reducer(state: LiveState, { event, labels }: Action): LiveState {
  const now = (Date.now() - state.started) / 1000
  const add = (kind: string, text: string, level?: string): LogLine[] =>
    [...state.log, { id: state.log.length, t: now, kind, text, level }].slice(-400)
  switch (event.type) {
    case 'start':
      return { ...state, url: String(event.url ?? state.url) }
    case 'page': {
      const page = { n: Number(event.n), max: Number(event.max), url: String(event.url) }
      return { ...state, page, stage: Math.max(state.stage, 1), log: add(labels.page, `${page.url}`) }
    }
    case 'host': {
      if (!event.third_party) return state
      const host = String(event.host)
      if (state.hosts.has(host)) return state
      const hosts = new Map(state.hosts)
      hosts.set(host, { country: (event.country as string) ?? null, entity: (event.entity as string) ?? null })
      const parts = [host, event.entity ?? '', event.country ?? '?', event.category ? (labels[`cat_${event.category}`] ?? event.category) : '']
      if (event.phase === 'landing') parts.push(labels.first)
      return { ...state, hosts, stage: Math.max(state.stage, 2), log: add(labels.host, parts.filter(Boolean).join('   ')) }
    }
    case 'challenge':
      return { ...state, challenge: true, log: add(labels.wait, labels.challenge) }
    case 'blocked':
      return { ...state, blocked: true }
    case 'form': {
      const pd = (event.pd as string[]).join(', ')
      const consent = event.consent ? labels.consent_yes : labels.consent_no
      return { ...state, forms: state.forms + 1, stage: Math.max(state.stage, 3),
        log: add(labels.form, `${String(event.page)}   ${pd}   ${consent}`, event.consent ? undefined : 'risk') }
    }
    case 'document':
      return { ...state, documents: state.documents + 1, stage: Math.max(state.stage, 3),
        log: add(labels.doc, `${String(event.kind)}   ${String(event.url)}`) }
    case 'policy_start':
      return { ...state, stage: 4, log: add(labels.policy, labels.policy_reading) }
    case 'policy':
      return { ...state, stage: 5, log: add(labels.policy, event.status === 'ok'
        ? labels.policy_done.replace('{n}', String(event.claims ?? 0)) : String(event.reason ?? event.status)) }
    case 'finding': {
      const title = event.title as Localized
      return { ...state, stage: 5, log: add(labels.finding, `${String(event.rule_id)}   ${title[labels.lang as 'uz' | 'ru'] ?? title.en ?? ''}`, String(event.level)) }
    }
    case 'done':
      return { ...state, stage: 5 }
    case 'end':
      return { ...state, finished: event.status === 'done' ? 'done' : 'error' }
    case 'error':
      return state.finished ? state : { ...state, finished: 'error' }
    default:
      return state
  }
}

export function LiveScan({ scanId, initialUrl, replay, onFinished }: {
  scanId: string
  initialUrl: string
  replay: boolean
  onFinished: (status: 'done' | 'error') => void
}) {
  const { t, lang, anon } = useSettings()
  const labels = useMemo(() => ({
    lang, page: t.log_page, host: t.log_host, form: t.log_form, doc: t.log_doc, policy: t.log_policy,
    finding: t.log_finding, wait: t.log_wait, first: t.first_visit, challenge: t.challenge,
    consent_yes: t.with_consent, consent_no: t.no_consent, policy_reading: t.policy_reading,
    policy_done: t.policy_done(-1).replace('-1', '{n}'),
    ...Object.fromEntries(Object.entries(CATEGORY[lang]).map(([k, v]) => [`cat_${k}`, v])),
  }), [t, lang]) as Record<string, string>

  const [state, dispatch] = useReducer(reducer, null, () => ({
    started: Date.now(), url: initialUrl, stage: 1, page: null, hosts: new Map(), forms: 0, documents: 0,
    log: [], challenge: false, blocked: false, finished: null,
  }) as LiveState)

  const labelsRef = useRef(labels)
  labelsRef.current = labels
  useEffect(() => subscribe(scanId, (event) => dispatch({ event, labels: labelsRef.current }), replay), [scanId, replay])

  useEffect(() => { if (state.finished) onFinished(state.finished) }, [state.finished, onFinished])

  const logRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const el = logRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [state.log.length])

  const domain = siteDomain(state.url || initialUrl)
  const mask = (text: string) => (anon && domain ? text.split(domain).join('sayt') : text)

  const countries = useMemo(() => {
    const byCountry = new Map<string, MapCountry>()
    for (const { country, entity } of state.hosts.values()) {
      if (!country || country === 'UZ' || country === '?') continue
      const item = byCountry.get(country) ?? { code: country, status: 'undetermined' as const, hosts: 0, entities: [] }
      item.hosts += 1
      if (entity && !item.entities!.includes(entity)) item.entities!.push(entity)
      byCountry.set(country, item)
    }
    return [...byCountry.values()]
  }, [state.hosts])

  const stages = [t.stage_pages, t.stage_network, t.stage_forms, t.stage_policy, t.stage_law]
  const shownSite = anon ? 'sayt' : domain

  return (
    <div>
      <div className="q-report-head" style={{ paddingBottom: 0 }}>
        <div>
          <h1>{t.scanning(shownSite)}</h1>
          {state.page && <div className="q-muted q-mono">{state.page.n} / {state.page.max}   {mask(state.page.url)}</div>}
        </div>
      </div>
      {state.challenge && !state.blocked && <div style={{ marginTop: 16 }}><Banner status="warning" title={t.challenge} /></div>}
      <div className="q-live">
        <div>
          <ol className="q-stages">
            {stages.map((label, i) => {
              const n = i + 1
              const s = n < state.stage ? 'done' : n === state.stage ? 'active' : 'todo'
              return (
                <li key={label} className="q-stage" data-state={s}>
                  <span className="q-stage-n">{n}</span><span>{label}</span>
                </li>
              )
            })}
          </ol>
          <div style={{ marginTop: 20 }}>
            <ProgressBar label={stages[state.stage - 1]} isIndeterminate={!state.finished} value={state.finished ? 100 : 0} />
          </div>
        </div>
        <div ref={logRef} className="q-log" role="log" aria-live="polite">
          {state.log.map((line) => (
            <div key={line.id} className="q-log-line" data-level={line.level}>
              <span className="q-muted">{line.t.toFixed(1)}</span>
              <span className="q-log-kind">{line.kind}</span>
              <span title={mask(line.text)}>{mask(line.text)}</span>
            </div>
          ))}
        </div>
        <div>
          <FlowMap data={countries} live />
          <ul className="q-counters">
            <li><b>{state.hosts.size}</b> {t.c_hosts}</li>
            <li><b>{countries.length}</b> {t.c_countries}{countries.length ? `: ${countries.map((c) => countryName(c.code, lang)).join(', ')}` : ''}</li>
            <li><b>{state.forms}</b> {t.c_forms}</li>
            <li><b>{state.documents}</b> {t.c_docs}</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
