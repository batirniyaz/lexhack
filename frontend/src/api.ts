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
  articles?: string[]
  citations?: Citation[]
  act_ru?: string
}
/** Verbatim article text from lex.uz via lex-rag (backend/qalqon/legal/citations.py); not verified by a lawyer. */
export interface Citation {
  act: string
  article: string
  heading: string
  parts: { part: string | null; text: string }[]
  url: string | null
  edition_date: string | null
  source: string
  verified_by_lawyer: boolean
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
  sanction_local?: { uz: string | null; ru: string | null; source: string | null } | null
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
  scope?: Scope
  policy_coverage?: Coverage[] | null
  law_change?: LawChange | null
}
/** The same saved facts evaluated under the previous wording of the law (F-16). */
export interface LawVersionSummary {
  id: string
  label: Localized
  in_force: { from: string; to: string | null }
  score: number | null
  levels: Record<Level, number>
  findings: Record<string, Level>
  basis?: LegalBasis
}
export interface LawChange {
  previous: LawVersionSummary
  current: LawVersionSummary
  changes: { rule_id: string; before: Level | null; after: Level | null; title: Localized | null }[]
  note: string
}
/** How the policy names each tracking or AI service (F-17): product named / only company / only kind / not named. */
export interface Coverage {
  entity: string
  country: string | null
  categories: string[]
  level: 'named' | 'company' | 'kind' | 'none'
  hosts: string[]
}
/** What was checked, when, from where, with which rules and model (backend/qalqon/evidence.py). */
export interface Scope {
  mode: string
  pages: string[]
  pages_count: number | null
  requests: number | null
  scanned_at: string | null
  vantage: string | null
  scanner_version: string
  rules_version: string
  llm: { model: string | null; prompt_version: string | null } | null
}
export interface Seal {
  statement: {
    issuer: string
    scan_id: string | null
    site: string
    scanned_at: string
    score: number | null
    sha256: { report: string; facts: string | null; har: string | null }
    sealed_at: string
    key_id: string
  }
  algorithm: string
  public_key: string
  signature: string
}
export interface VerifyResult {
  valid_signature: boolean
  our_key: boolean
  known_report: boolean
  statement?: Seal['statement']
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
  domain?: string | null
  scan_id?: string | null
  seal?: Seal | null
  viewer_is_owner?: boolean
  security_hidden?: boolean
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

// Public demo (backend guard.py): the owner key unlocks everything; a per-scan token unlocks the scans this
// browser started. Both live in localStorage and are sent with every request.
const TOKENS_KEY = 'q-scan-tokens'

function scanTokens(): Record<string, string> {
  try {
    return JSON.parse(localStorage.getItem(TOKENS_KEY) || '{}') as Record<string, string>
  } catch {
    return {}
  }
}

function rememberToken(scanId: string, token: string) {
  const entries = Object.entries({ ...scanTokens(), [scanId]: token }).slice(-100)
  localStorage.setItem(TOKENS_KEY, JSON.stringify(Object.fromEntries(entries)))
}

function authHeaders(scanId?: string): Record<string, string> {
  const headers: Record<string, string> = {}
  const key = localStorage.getItem('q-key')
  if (key) headers['X-Probo-Key'] = key
  const token = scanId ? scanTokens()[scanId] : undefined
  if (token) headers['X-Scan-Token'] = token
  return headers
}

/** Query string with the same credentials, for plain links and EventSource (they cannot send headers). */
export function authQuery(scanId?: string): string {
  const params = new URLSearchParams()
  const key = localStorage.getItem('q-key')
  if (key) params.set('key', key)
  const token = scanId ? scanTokens()[scanId] : undefined
  if (token) params.set('t', token)
  return params.toString()
}

async function getJson<T>(path: string, scanId?: string): Promise<T> {
  const response = await fetch(path, { headers: authHeaders(scanId) })
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
    const headers: Record<string, string> = { 'Content-Type': 'application/json', ...authHeaders() }
    const response = await fetch('/api/scans', {
      method: 'POST',
      headers,
      body: JSON.stringify({ url, max_pages: maxPages }),
    })
    const body = await response.json().catch(() => ({}))
    if (!response.ok) throw new ApiError(response.status, typeof body.detail === 'string' ? body.detail : 'error')
    if (body.token) rememberToken(body.scan_id, body.token)
    return body
  },
  result: (scanId: string, anon: boolean) =>
    getJson<ScanResult>(`/api/scans/${scanId}?facts=1${anon ? '&anon=1' : ''}`, scanId),
  health: () => getJson<{ public_mode: boolean; owner: boolean }>('/api/health'),
  sample: () => getJson<{ token: string; result: ScanResult }>('/api/sample'),
  verify: async (seal: unknown): Promise<VerifyResult> => {
    const response = await fetch('/api/verify', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(seal),
    })
    if (!response.ok) throw new ApiError(response.status, 'verify failed')
    return response.json()
  },
  verifyKey: () => getJson<{ algorithm: string; public_key: string; key_id: string }>('/api/verify/key'),
  list: () => getJson<ScanListItem[]>('/api/scans?limit=100'),
  stats: () => getJson<MarketStats>('/api/stats'),
  site: (domain: string, anon: boolean) => getJson<SiteHistory>(`/api/sites/${encodeURIComponent(domain)}${anon ? '?anon=1' : ''}`),
  share: async (scanId: string): Promise<{ token: string; path: string }> => {
    const response = await fetch(`/api/scans/${scanId}/share`, { method: 'POST', headers: authHeaders(scanId) })
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
  const query = [replay ? 'replay=1' : '', authQuery(scanId)].filter(Boolean).join('&')
  const source = new EventSource(`/api/scans/${scanId}/events${query ? `?${query}` : ''}`)
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
