// Typed client for the Qalqon API (backend/qalqon/api.py). Shapes follow ARCHITECTURE.md (API section).

export type Level = 'violation' | 'risk' | 'recommendation'
export type Localized = { en?: string; ru?: string; uz?: string }

export interface Evidence { summary: string; data?: Record<string, unknown> }
export interface LegalBasis {
  act: string
  article: string | null
  quote_uz: string | null
  quote_ru: string | null
  url: string | null
  url_ru?: string | null
  edition_date: string | null
}
export interface Finding {
  rule_id: string
  level: Level
  rule_level?: Level
  downgraded?: boolean
  title: Localized
  evidence: Evidence[]
  legal_basis: LegalBasis[]
  sanction: string | null
  fix: Localized
  verified: boolean
  counts_for_score: boolean
}
export interface Flow { country: string; status: string; hosts: number; entities: string[] }
export interface Stats {
  pages: number
  requests: number
  third_party_requests: number
  third_party_hosts: number
  cookies: number
  forms_with_pd?: number
  documents_found?: number
}
export interface Report {
  scan_id: string
  site: string
  scanned_at: string
  status: 'ok' | 'blocked'
  blocked?: string
  score: number | null
  levels?: Record<Level, number>
  findings: Finding[]
  not_evaluated: { rule_id: string; reason: string }[]
  flows: Flow[]
  stats: Stats
  label?: string
}
export interface Host {
  host: string
  third_party: boolean
  ips: string[]
  requests: number
  on_landing: boolean
  server_country: string | null
  org: string | null
  is_cdn: boolean
  entity: string | null
  company_country: string | null
  dpf: boolean | null
  category: string | null
  country: string | null
}
export interface Form {
  pages: string[]
  pd_categories: string[]
  has_consent: boolean
  collects_pd: boolean
  fields: { label: string; name: string; type: string; pd?: string | null }[]
}
export interface PolicyElement { present: boolean; quote: string | null; verified: boolean; label: string }
export interface Claim { type: string; statement_en: string; quote: string; services: string[]; countries: string[] }
export interface Policy {
  status: 'ok' | 'no_document' | 'skipped' | 'error'
  reason?: string
  documents?: { url: string; kind: string; chars: number }[]
  is_personal_data_policy?: boolean
  elements?: Record<string, PolicyElement>
  claims?: Claim[]
}
export interface Cookie { name: string; domain: string; third_party: boolean; set_on_landing: boolean }
export interface Backend { kind: string; region?: string | null; source?: string; page?: string }
export interface Facts {
  site: string
  site_domains: string[]
  pages: { url: string; final_url: string; status: number | null; title: string | null }[]
  hosts: Host[]
  forms: Form[]
  documents: { kind: string | null; url: string; title: string; visited: boolean }[]
  cookies?: Cookie[]
  backends?: Backend[]
  policy?: Policy
  stats: Stats
}
export interface ScanResult {
  report?: Report
  facts?: Facts
  status?: string
  error?: string | null
  label?: string
  domain?: string
  scan_id?: string
}
export interface ScanListItem {
  scan_id: string
  site: string
  domain: string
  label: string
  status: string
  score: number | null
  delta: number | null
  levels?: Record<Level, number>
  scanned_at: string
}
export interface DiffItem { rule_id: string; level: Level; title: Localized }
export interface SiteHistory {
  domain: string
  label: string
  scans: { scan_id: string; site: string; label: string; status: string; score: number | null; levels?: Record<Level, number>; scanned_at: string }[]
  diff: { from: string; to: string; new: DiffItem[]; fixed: DiffItem[]; unchanged: DiffItem[] } | null
}
export interface MarketStats {
  sites: number
  average_score: number | null
  sites_with_rule: Record<string, number>
  sites_sending_to_country: Record<string, number>
}

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(path)
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new ApiError(response.status, typeof body.detail === 'string' ? body.detail : response.statusText)
  }
  return response.json() as Promise<T>
}

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

export const api = {
  startScan: async (url: string, maxPages?: number): Promise<{ scan_id: string }> => {
    const response = await fetch('/api/scans', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, max_pages: maxPages }),
    })
    const body = await response.json().catch(() => ({}))
    if (!response.ok) throw new ApiError(response.status, typeof body.detail === 'string' ? body.detail : 'error')
    return body
  },
  result: (scanId: string, anon: boolean) =>
    getJson<ScanResult>(`/api/scans/${scanId}?facts=1${anon ? '&anon=1' : ''}`),
  list: () => getJson<ScanListItem[]>('/api/scans?limit=100'),
  stats: () => getJson<MarketStats>('/api/stats'),
  site: (domain: string, anon: boolean) => getJson<SiteHistory>(`/api/sites/${encodeURIComponent(domain)}${anon ? '?anon=1' : ''}`),
  share: async (scanId: string): Promise<{ token: string; path: string }> => {
    const response = await fetch(`/api/scans/${scanId}/share`, { method: 'POST' })
    if (!response.ok) throw new ApiError(response.status, 'share failed')
    return response.json()
  },
  shared: (token: string, anon: boolean) =>
    getJson<ScanResult>(`/api/shared/${encodeURIComponent(token)}${anon ? '?anon=1' : ''}`),
}

/** Every event type the backend streams (ARCHITECTURE.md). */
export const EVENT_TYPES = [
  'start', 'page', 'host', 'challenge', 'blocked', 'form', 'document',
  'policy_start', 'policy', 'finding', 'done', 'end', 'error',
] as const
export type ScanEvent = { type: (typeof EVENT_TYPES)[number]; [key: string]: unknown }

/** Subscribe to the live feed (or a replay). Returns a function that closes the stream. */
export function subscribe(scanId: string, onEvent: (event: ScanEvent) => void, replay = false): () => void {
  const source = new EventSource(`/api/scans/${scanId}/events${replay ? '?replay=1' : ''}`)
  const handler = (message: MessageEvent) => {
    try {
      onEvent(JSON.parse(message.data) as ScanEvent)
    } catch {
      /* ignore malformed lines */
    }
  }
  for (const type of EVENT_TYPES) source.addEventListener(type, handler as EventListener)
  source.addEventListener('end', () => source.close())
  source.onerror = () => {
    // The server closes the stream after 'end'; the browser reports that as an error and would reconnect.
    if (source.readyState !== EventSource.CLOSED) source.close()
    onEvent({ type: 'error', message: 'stream closed' })
  }
  return () => source.close()
}

/** Very small helper: the registrable domain of a URL, good enough to hide it in presentation mode (.uz, .com). */
export function siteDomain(url: string): string {
  try {
    const host = new URL(url.includes('://') ? url : `https://${url}`).hostname.replace(/^www\./, '')
    const parts = host.split('.')
    return parts.length > 2 && ['co', 'com', 'org', 'net'].includes(parts[parts.length - 2])
      ? parts.slice(-3).join('.')
      : parts.slice(-2).join('.')
  } catch {
    return url
  }
}
