// /history — scans stored on this server, newest first (PRODUCT.md §4.4). No login in P0.
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import { Badge } from '@astryxdesign/core/Badge'
import { Button } from '@astryxdesign/core/Button'
import { EmptyState } from '@astryxdesign/core/EmptyState'
import { Link } from '@astryxdesign/core/Link'
import { Spinner } from '@astryxdesign/core/Spinner'
import { Table } from '@astryxdesign/core/Table'
import { api, siteDomain, type Level, type ScanListItem } from '../api'
import { formatDate, useSettings } from '../i18n'

interface Row extends Record<string, unknown> {
  id: string
  site: string
  date: string
  score: string
  findings: string
  levels?: Record<Level, number>
  status: string
  domain: string
  delta: number | null
}

export function History() {
  const { t, anon } = useSettings()
  const navigate = useNavigate()
  const [items, setItems] = useState<ScanListItem[] | null>(null)

  useEffect(() => { api.list().then(setItems).catch(() => setItems([])) }, [])

  if (items === null) return <div className="q-page" style={{ paddingTop: 80 }}><Spinner label={t.loading} /></div>

  const rows: Row[] = items.map((s) => ({
    id: s.scan_id,
    site: anon ? s.label : siteDomain(s.site ?? ''),
    date: formatDate(s.scanned_at),
    score: s.score === null ? '—' : String(s.score),
    findings: '',
    levels: s.levels,
    status: s.status,
    domain: s.domain,
    delta: s.delta,
  }))

  return (
    <div className="q-page">
      <div className="q-history-head">
        <h1 style={{ fontSize: 26, fontWeight: 600, margin: 0 }}>{t.history_title}</h1>
        <Button variant="primary" label={t.nav_new} onClick={() => navigate('/')} />
      </div>
      {rows.length === 0 ? (
        <EmptyState title={t.history_empty} description={t.history_empty_text}
          actions={<Button variant="primary" label={t.nav_new} onClick={() => navigate('/')} />} />
      ) : (
        <Table<Row>
          data={rows}
          idKey="id"
          hasHover
          columns={[
            { key: 'site', header: t.col_site, renderCell: (r) => (
              <Link href={`/sites/${r.domain}`} onClick={(e) => { e.preventDefault(); navigate(`/sites/${r.domain}`) }}>
                <span className="q-mono">{r.site}</span>
              </Link>
            ) },
            { key: 'date', header: t.col_date },
            { key: 'score', header: t.col_score, align: 'end', renderCell: (r) => (
              <span style={{ fontVariantNumeric: 'tabular-nums' }}>
                {r.score}
                {r.delta ? <span className="q-muted" style={{ marginInlineStart: 6 }}>{r.delta > 0 ? `▲${r.delta}` : `▼${-r.delta}`}</span> : null}
              </span>
            ) },
            { key: 'findings', header: t.col_findings, renderCell: (r) => r.levels ? (
              <span style={{ display: 'inline-flex', gap: 6, flexWrap: 'wrap' }}>
                <Badge variant="error" label={`${r.levels.violation} ${t.lvl_violation}`} />
                <Badge variant="warning" label={`${r.levels.risk} ${t.lvl_risk}`} />
                <Badge variant="neutral" label={`${r.levels.recommendation} ${t.lvl_recommendation}`} />
              </span>
            ) : '—' },
            { key: 'status', header: t.col_status, renderCell: (r) => (
              <Badge variant={r.status === 'ok' ? 'success' : 'neutral'} label={r.status === 'ok' ? t.status_ok : t.status_blocked} />
            ) },
            { key: 'id', header: '', renderCell: (r) => (
              <Button size="sm" variant="secondary" label={t.open} onClick={() => navigate(`/scan/${r.id}`)} />
            ) },
          ]}
        />
      )}
    </div>
  )
}
