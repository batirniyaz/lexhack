// World map of where a site's data goes: arcs from Uzbekistan to receiving countries, colored by legal status.
// Colors are a validated status palette (DESIGN.md); identity is never color-alone: legend + tooltip + host table.
import { useMemo, useRef, useState } from 'react'
import { geoNaturalEarth1, geoPath, geoCentroid } from 'd3-geo'
import { countries, ISO2_TO_NUMERIC } from '../geo'
import { countryName, useSettings } from '../i18n'

export type StatusKey = 'allowed' | 'conditional' | 'not_listed' | 'undetermined' | 'local'

export function statusKey(status: string | null | undefined): StatusKey {
  switch (status) {
    case 'local': return 'local'
    case 'adequate': return 'allowed'
    case 'conditional_met':
    case 'conditional_unknown': return 'conditional'
    case 'not_listed':
    case 'not_in_known_list': return 'not_listed'
    default: return 'undetermined'
  }
}

export const STATUS_COLOR: Record<StatusKey, string> = {
  allowed: 'var(--q-allowed)',
  conditional: 'var(--q-conditional)',
  not_listed: 'var(--q-not-listed)',
  undetermined: 'var(--q-undetermined)',
  local: 'var(--q-origin)',
}

export interface MapCountry { code: string; status: StatusKey; hosts: number; entities?: string[] }

const WIDTH = 960
const HEIGHT = 470

export function FlowMap({ data, live = false }: { data: MapCountry[]; live?: boolean }) {
  const { t, lang } = useSettings()
  const wrapRef = useRef<HTMLDivElement>(null)
  const [tip, setTip] = useState<{ x: number; y: number; item: MapCountry } | null>(null)

  const { features, path, origin, centroids } = useMemo(() => {
    const features = countries()
    const projection = geoNaturalEarth1().fitExtent([[8, 8], [WIDTH - 8, HEIGHT - 8]], {
      type: 'FeatureCollection',
      features,
    })
    const path = geoPath(projection)
    const centroids = new Map<string, [number, number]>()
    for (const f of features) {
      const point = projection(geoCentroid(f))
      if (point && f.id !== undefined) centroids.set(String(f.id), point as [number, number])
    }
    return { features, path, origin: centroids.get(ISO2_TO_NUMERIC.UZ) ?? [WIDTH * 0.65, HEIGHT * 0.32], centroids }
  }, [])

  const byNumeric = useMemo(() => {
    const map = new Map<string, MapCountry>()
    for (const item of data) {
      const id = ISO2_TO_NUMERIC[item.code]
      if (id) map.set(id, item)
    }
    return map
  }, [data])

  const statusLabel: Record<StatusKey, string> = {
    allowed: t.st_allowed, conditional: t.st_conditional, not_listed: t.st_not_listed,
    undetermined: t.st_undetermined, local: t.st_local,
  }

  const onMove = (event: React.MouseEvent, item: MapCountry) => {
    const box = wrapRef.current?.getBoundingClientRect()
    if (!box) return
    setTip({ x: event.clientX - box.left + 12, y: event.clientY - box.top + 12, item })
  }

  const unmapped = data.filter((d) => !ISO2_TO_NUMERIC[d.code] && d.code !== 'UZ')

  return (
    <div ref={wrapRef} style={{ position: 'relative' }}>
      <svg className="q-map" viewBox={`0 0 ${WIDTH} ${HEIGHT}`} role="img"
        aria-label={data.map((d) => `${countryName(d.code, lang)}: ${statusLabel[d.status]}`).join('; ')}>
        {features.map((f) => {
          const id = String(f.id)
          const item = byNumeric.get(id)
          const isOrigin = id === ISO2_TO_NUMERIC.UZ
          const fill = isOrigin ? STATUS_COLOR.local
            : item ? (live && item.status === 'undetermined' ? 'var(--q-origin)' : STATUS_COLOR[item.status])
            : 'var(--q-land)'
          return (
            <path key={id} className="q-country" d={path(f) ?? undefined} fill={fill} opacity={item || isOrigin ? 1 : 0.9}
              onMouseMove={item ? (e) => onMove(e, item) : undefined} onMouseLeave={() => setTip(null)} />
          )
        })}
        {data.filter((d) => d.code !== 'UZ').map((d) => {
          const target = centroids.get(ISO2_TO_NUMERIC[d.code] ?? '')
          if (!target) return null
          const [x1, y1] = origin
          const [x2, y2] = target
          const lift = Math.min(120, Math.hypot(x2 - x1, y2 - y1) * 0.25)
          const cx = (x1 + x2) / 2
          const cy = Math.min(y1, y2) - lift
          return (
            <path key={`arc-${d.code}`} d={`M${x1},${y1} Q${cx},${cy} ${x2},${y2}`} fill="none"
              stroke={live ? 'var(--q-origin)' : STATUS_COLOR[d.status]} strokeWidth={2} strokeLinecap="round"
              opacity={0.85} />
          )
        })}
        <circle cx={origin[0]} cy={origin[1]} r={4.5} fill="var(--q-origin)" stroke="#fff" strokeWidth={2} />
      </svg>
      {tip && (
        <div className="q-map-tip" style={{ left: tip.x, top: tip.y }}>
          <b>{countryName(tip.item.code, lang)}</b> {live ? '' : statusLabel[tip.item.status]}
          <div className="q-muted">{t.hosts_n(tip.item.hosts)}{tip.item.entities?.length ? `: ${tip.item.entities.join(', ')}` : ''}</div>
        </div>
      )}
      {!live && (
        <div className="q-legend" aria-hidden="true">
          {(['allowed', 'conditional', 'not_listed', 'undetermined'] as StatusKey[]).map((key) => (
            <span key={key}><i className="q-swatch" style={{ background: STATUS_COLOR[key] }} />{statusLabel[key]}</span>
          ))}
        </div>
      )}
      {unmapped.length > 0 && (
        <div className="q-legend q-muted">
          {unmapped.map((d) => <span key={d.code}>{countryName(d.code, lang)}: {statusLabel[d.status]}</span>)}
        </div>
      )}
    </div>
  )
}
