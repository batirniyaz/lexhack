// World geometry for the data-flow map: ISO-2 codes (backend) -> ISO 3166-1 numeric ids (world-atlas).
import { feature } from 'topojson-client'
import type { FeatureCollection, Geometry } from 'geojson'
import type { Topology, GeometryCollection } from 'topojson-specification'
import world from 'world-atlas/countries-110m.json'

// Countries we see in scans (trackers, CDNs, hosting) — extend when a new one shows up as "?" on the map.
export const ISO2_TO_NUMERIC: Record<string, string> = {
  UZ: '860', US: '840', RU: '643', DE: '276', NL: '528', FI: '246', FR: '250', GB: '826', IE: '372', SE: '752',
  PL: '616', IL: '376', CA: '124', KR: '410', JP: '392', CN: '156', SG: '702', AE: '784', TR: '792', KZ: '398',
  KG: '417', TJ: '762', TM: '795', AZ: '031', GE: '268', AM: '051', BY: '112', UA: '804', LT: '440', LV: '428',
  EE: '233', CZ: '203', AT: '040', CH: '756', IT: '380', ES: '724', PT: '620', BE: '056', DK: '208', NO: '578',
  IN: '356', HK: '344', TW: '158', AU: '036', BR: '076', MT: '470', LU: '442', RO: '642', BG: '100', HU: '348',
  GR: '300', CY: '196', SK: '703', SI: '705', HR: '191', IS: '352', MX: '484', ZA: '710', SA: '682', QA: '634',
}

export type CountryFeature = FeatureCollection<Geometry, { name: string }>['features'][number]

let cache: CountryFeature[] | null = null

export function countries(): CountryFeature[] {
  if (!cache) {
    const topology = world as unknown as Topology<{ countries: GeometryCollection<{ name: string }> }>
    const collection = feature(topology, topology.objects.countries) as FeatureCollection<Geometry, { name: string }>
    // Antarctica takes space and carries no data for us.
    cache = collection.features.filter((f) => f.id !== '010')
  }
  return cache
}
