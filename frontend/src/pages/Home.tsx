// Home (PRODUCT.md §4.1): one URL field, a real excerpt of the core idea, anonymized market facts.
import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router'
import { Button } from '@astryxdesign/core/Button'
import { Link } from '@astryxdesign/core/Link'
import { TextInput } from '@astryxdesign/core/TextInput'
import { api, ApiError, type MarketStats, type ScanResult } from '../api'
import { useSettings } from '../i18n'
import { SaysDoes } from '../components/Report'

export function Home() {
  const { t } = useSettings()
  const navigate = useNavigate()
  const [url, setUrl] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState<MarketStats | null>(null)
  const [sample, setSample] = useState<{ id: string; result: ScanResult } | null>(null)

  useEffect(() => {
    api.stats().then(setStats).catch(() => setStats(null))
    // Sample: a finished, anonymized report that shows a "policy vs behaviour" finding.
    api.list().then(async (scans) => {
      for (const scan of scans.filter((s) => s.status === 'ok').slice(0, 20)) {
        const result = await api.result(scan.scan_id, true)
        if (result.report?.findings.some((f) => f.rule_id === 'PD-MIS-01')) {
          setSample({ id: scan.scan_id, result })
          return
        }
      }
    }).catch(() => undefined)
  }, [])

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    const value = url.trim()
    if (!/^[^\s]+\.[a-z]{2,}/i.test(value.replace(/^https?:\/\//, ''))) {
      setError(t.bad_url)
      return
    }
    setBusy(true)
    setError(null)
    try {
      const { scan_id } = await api.startScan(value)
      navigate(`/scan/${scan_id}?url=${encodeURIComponent(value)}`)
    } catch (e) {
      setError(e instanceof ApiError && e.status === 429 ? t.rate_limited
        : e instanceof ApiError && e.status === 403 ? t.key_required
        : e instanceof Error ? e.message : String(e))
      setBusy(false)
    }
  }

  const n = stats?.sites ?? 0
  const rule = (id: string) => stats?.sites_with_rule[id] ?? 0
  const mismatch = sample?.result.report?.findings.find((f) => f.rule_id === 'PD-MIS-01')

  return (
    <div className="q-page">
      <section className="q-hero">
        <h1>{t.hero_title}</h1>
        <p>{t.hero_text}</p>
        <form className="q-scan-form" onSubmit={submit} noValidate>
          <TextInput label={t.url_label} value={url} onChange={(v) => setUrl(v)} placeholder={t.url_placeholder}
            type="url" size="lg" width="100%"
            status={error ? { type: 'error', message: error } : undefined} />
          <Button type="submit" variant="primary" size="lg" label={t.check} isLoading={busy} />
        </form>
        <div className="q-fineprint">{t.fineprint}</div>
      </section>

      {mismatch && sample && (
        <section className="q-section">
          <h2>{t.sample_title}</h2>
          <SaysDoes finding={mismatch} facts={sample.result.facts} />
          <div style={{ marginTop: 12 }}>
            <Link href={`/scan/${sample.id}`} onClick={(e) => { e.preventDefault(); navigate(`/scan/${sample.id}`) }}>
              {t.sample_open}
            </Link>
          </div>
        </section>
      )}

      {stats && n > 0 && (
        <section className="q-section">
          <h2>{t.facts_title}</h2>
          <div className="q-facts">
            <p>{t.fact_trackers(rule('PD-TRK-01'), n)}</p>
            {rule('PD-REC-01') > 0 && <p>{t.fact_webvisor(rule('PD-REC-01'), n)}</p>}
            {rule('PD-POL-02') > 0 && <p>{t.fact_policy(rule('PD-POL-02'), n)}</p>}
            <p className="q-muted" style={{ fontSize: 14 }}>{t.fact_note}</p>
          </div>
        </section>
      )}
    </div>
  )
}
