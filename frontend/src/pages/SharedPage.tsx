// /r/:token — read-only shared report (no history or share buttons; PDF still works).
import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { EmptyState } from '@astryxdesign/core/EmptyState'
import { Spinner } from '@astryxdesign/core/Spinner'
import { api, siteDomain, type ScanResult } from '../api'
import { useSettings } from '../i18n'
import { ReportView } from '../components/Report'

export function SharedPage() {
  const { t, anon } = useSettings()
  const { token = '' } = useParams()
  const [data, setData] = useState<ScanResult | null | 'missing'>(null)

  useEffect(() => { api.shared(token, anon).then(setData).catch(() => setData('missing')) }, [token, anon])

  if (data === null) return <div className="q-page" style={{ paddingTop: 80 }}><Spinner label={t.loading} /></div>
  if (data === 'missing' || !data.report) {
    return <div className="q-page" style={{ paddingTop: 80 }}><EmptyState title={t.link_not_found} /></div>
  }
  const report = data.report
  const hidden = anon || data.domain === null  // null: the public demo anonymized it on the server
  const displaySite = hidden ? (data.label ?? report.label ?? t.site_word) : siteDomain(report.site)
  return (
    <div className="q-page">
      <p className="q-muted q-noprint" style={{ margin: '24px 0 0' }}>{t.shared_note}</p>
      <ReportView report={report} facts={data.facts} displaySite={displaySite} scanId={data.scan_id ?? undefined} readonly owner={!data.security_hidden} />
    </div>
  )
}
