// /scan/:id — live feed while the scan runs, then the report on the same URL (PRODUCT.md §4.2–4.3).
import { useCallback, useEffect, useState } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router'
import { Button } from '@astryxdesign/core/Button'
import { EmptyState } from '@astryxdesign/core/EmptyState'
import { Spinner } from '@astryxdesign/core/Spinner'
import { api, ApiError, siteDomain, type ScanResult } from '../api'
import { useSettings } from '../i18n'
import { LiveScan } from '../components/LiveScan'
import { ReportView } from '../components/Report'

type Mode = 'loading' | 'live' | 'report' | 'notfound' | 'error'

export function ScanPage() {
  const { t, anon } = useSettings()
  const params = useParams()
  const [search] = useSearchParams()
  const navigate = useNavigate()
  const scanId = params['*'] ?? ''
  const replay = search.get('replay') === '1'
  const [mode, setMode] = useState<Mode>('loading')
  const [result, setResult] = useState<ScanResult | null>(null)

  const load = useCallback(async () => {
    try {
      const data = await api.result(scanId, anon)
      setResult(data)
      if (data.report) setMode('report')
      else if (data.status === 'error') setMode('error')
      else setMode('live')
    } catch (e) {
      setMode(e instanceof ApiError && e.status === 404 ? 'notfound' : 'error')
    }
  }, [scanId, anon])

  useEffect(() => {
    if (replay) setMode('live')
    else void load()
  }, [load, replay])

  const onFinished = useCallback((status: 'done' | 'error') => {
    if (replay) navigate(`/scan/${scanId}`, { replace: true })
    if (status === 'done') void load()
    else setMode('error')
  }, [load, navigate, replay, scanId])

  if (mode === 'loading') return <div className="q-page" style={{ paddingTop: 80 }}><Spinner label={t.loading} /></div>
  if (mode === 'live') {
    return (
      <div className="q-page">
        <LiveScan scanId={scanId} initialUrl={search.get('url') ?? result?.report?.site ?? ''} replay={replay}
          onFinished={onFinished} />
      </div>
    )
  }
  if (mode === 'notfound') {
    return <div className="q-page" style={{ paddingTop: 80 }}><EmptyState title={t.not_found} /></div>
  }
  const report = result?.report
  if (mode === 'error' || !report) {
    return (
      <div className="q-page" style={{ paddingTop: 80 }}>
        <EmptyState title={t.error_title} description={result?.error ?? undefined}
          actions={<Button variant="primary" label={t.retry} onClick={() => navigate('/')} />} />
      </div>
    )
  }
  if (report.status === 'blocked') {
    return (
      <div className="q-page" style={{ paddingTop: 80 }}>
        <EmptyState title={t.blocked_title} description={t.blocked_text}
          actions={<Button label={t.nav_new} onClick={() => navigate('/')} />} />
      </div>
    )
  }
  const displaySite = anon ? (result?.label ?? report.label ?? t.site_word) : siteDomain(report.site)
  return (
    <div className="q-page">
      <ReportView report={report} facts={result?.facts} displaySite={displaySite} scanId={scanId} domain={result?.domain ?? undefined} />
      {anon && (
        <div style={{ marginTop: 40 }}>
          <Button variant="ghost" size="sm" label={t.replay} onClick={() => navigate(`/scan/${scanId}?replay=1`)} />
        </div>
      )}
    </div>
  )
}
