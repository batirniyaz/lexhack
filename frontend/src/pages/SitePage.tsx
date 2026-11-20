// /sites/:domain — one site over time: score trend + what changed since the previous scan (PRODUCT.md §4.5).
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import { Badge } from '@astryxdesign/core/Badge'
import { Button } from '@astryxdesign/core/Button'
import { EmptyState } from '@astryxdesign/core/EmptyState'
import { Spinner } from '@astryxdesign/core/Spinner'
import { api, type DiffItem, type Level, type SiteHistory } from '../api'
import { formatDate, useSettings } from '../i18n'

const LEVEL_BADGE: Record<Level, 'error' | 'warning' | 'neutral'> = { violation: 'error', risk: 'warning', recommendation: 'neutral' }

/** Single-series line: 2 px line, 9 px markers, recessive grid, direct label on the last point, tooltip per marker. */
function Trend({ points }: { points: { date: string; score: number }[] }) {
  const { t } = useSettings()
  const [hover, setHover] = useState<number | null>(null)
  const W = 640, H = 200, L = 34, R = 40, T = 16, B = 30
  const x = (i: number) => (points.length === 1 ? (L + W - R) / 2 : L + (i * (W - L - R)) / (points.length - 1))
  const y = (v: number) => T + ((100 - v) * (H - T - B)) / 100
  const path = points.map((p, i) => `${i ? 'L' : 'M'}${x(i)},${y(p.score)}`).join(' ')
  const last = points[points.length - 1]
  return (
    <div style={{ position: 'relative', maxWidth: 720 }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="img"
        aria-label={`${t.site_trend}: ${points.map((p) => `${p.date} ${p.score}`).join(', ')}`}>
        {[0, 50, 100].map((v) => (
          <g key={v}>
            <line x1={L} x2={W - R} y1={y(v)} y2={y(v)} stroke="var(--q-rule)" strokeWidth={1} />
            <text x={L - 8} y={y(v) + 4} textAnchor="end" fontSize={11} fill="var(--q-muted)">{v}</text>
          </g>
        ))}
        <path d={path} fill="none" stroke="var(--q-origin)" strokeWidth={2} strokeLinejoin="round" />
        {points.map((p, i) => (
          <g key={i} onMouseEnter={() => setHover(i)} onMouseLeave={() => setHover(null)}>
            <circle cx={x(i)} cy={y(p.score)} r={14} fill="transparent" />
            <circle cx={x(i)} cy={y(p.score)} r={4.5} fill="var(--q-paper)" stroke="var(--q-origin)" strokeWidth={2} />
          </g>
        ))}
        {last && (
          <text x={x(points.length - 1) + 10} y={y(last.score) + 4} fontSize={13} fontWeight={600} fill="var(--q-ink)">{last.score}</text>
        )}
        {points.length > 1 && (
          <>
            <text x={x(0)} y={H - 8} fontSize={11} fill="var(--q-muted)" textAnchor="start">{points[0].date.split(',')[0]}</text>
            <text x={x(points.length - 1)} y={H - 8} fontSize={11} fill="var(--q-muted)" textAnchor="end">{last.date.split(',')[0]}</text>
          </>
        )}
      </svg>
      {hover !== null && (
        <div className="q-map-tip" style={{ left: `${(x(hover) / W) * 100}%`, top: `${(y(points[hover].score) / H) * 100}%`, transform: 'translate(10px, -110%)' }}>
          <b>{points[hover].score}</b> <span className="q-muted">{points[hover].date}</span>
        </div>
      )}
    </div>
  )
}

function DiffList({ title, items, variant }: { title: string; items: DiffItem[]; variant: 'new' | 'fixed' | 'same' }) {
  const { t, lang } = useSettings()
  return (
    <section>
      <h3 style={{ fontSize: 15, margin: '0 0 10px' }}>{title} <span className="q-muted">{items.length}</span></h3>
      {items.length === 0 ? <p className="q-muted" style={{ margin: 0 }}>{t.diff_empty}</p> : (
        <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'grid', gap: 8 }}>
          {items.map((item) => (
            <li key={item.rule_id} style={{ display: 'flex', gap: 10, alignItems: 'baseline', textDecoration: variant === 'fixed' ? 'line-through' : undefined }}>
              <span style={{ flexShrink: 0 }}><Badge variant={variant === 'fixed' ? 'success' : LEVEL_BADGE[item.level]} label={item.rule_id} /></span>
              <span>{item.title[lang] || item.title.en}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export function SitePage() {
  const { t, anon } = useSettings()
  const { domain = '' } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState<SiteHistory | null | 'missing'>(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => { api.site(domain, anon).then(setData).catch(() => setData('missing')) }, [domain, anon])

  if (data === null) return <div className="q-page" style={{ paddingTop: 80 }}><Spinner label={t.loading} /></div>
  if (data === 'missing') return <div className="q-page" style={{ paddingTop: 80 }}><EmptyState title={t.not_found} /></div>

  const ok = data.scans.filter((s) => s.status === 'ok' && s.score !== null)
  const points = ok.map((s) => ({ date: formatDate(s.scanned_at), score: s.score as number }))
  const rescan = async () => {
    setBusy(true)
    try {
      const { scan_id } = await api.startScan(domain)
      navigate(`/scan/${scan_id}?url=${encodeURIComponent(domain)}`)
    } catch {
      setBusy(false)
    }
  }

  return (
    <div className="q-page">
      <div className="q-history-head">
        <div>
          <h1 style={{ fontSize: 26, fontWeight: 600, margin: '0 0 4px' }}>{anon ? data.label : data.domain}</h1>
          <div className="q-muted">{t.site_title}</div>
        </div>
        <Button variant="primary" label={t.rescan} isLoading={busy} onClick={rescan} />
      </div>

      <section className="q-section" style={{ paddingTop: 8 }}>
        <h2>{t.site_trend}</h2>
        {points.length > 0 && <Trend points={points} />}
      </section>

      <section className="q-section">
        <h2>{t.site_diff}</h2>
        {data.diff ? (
          <div style={{ display: 'grid', gap: 24, gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))' }}>
            <DiffList title={t.diff_new} items={data.diff.new} variant="new" />
            <DiffList title={t.diff_fixed} items={data.diff.fixed} variant="fixed" />
            <DiffList title={t.diff_unchanged} items={data.diff.unchanged} variant="same" />
          </div>
        ) : <p className="q-muted">{t.diff_need_two}</p>}
      </section>

      <section className="q-section">
        <h2>{t.site_scans}</h2>
        <div style={{ display: 'grid', gap: 6 }}>
          {[...data.scans].reverse().map((s) => (
            <div key={s.scan_id} style={{ display: 'flex', gap: 14, alignItems: 'baseline', flexWrap: 'wrap' }}>
              <span style={{ minWidth: 150 }}>{formatDate(s.scanned_at)}</span>
              <b style={{ minWidth: 36, fontVariantNumeric: 'tabular-nums' }}>{s.score ?? '—'}</b>
              <Button size="sm" variant="ghost" label={t.open} onClick={() => navigate(`/scan/${s.scan_id}`)} />
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
