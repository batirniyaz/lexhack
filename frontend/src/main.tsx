import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

// Self-hosted fonts (no Google Fonts at the venue). All cover Uzbek oʻ gʻ ʼ and Cyrillic.
import '@fontsource/ibm-plex-sans/400.css'
import '@fontsource/ibm-plex-sans/500.css'
import '@fontsource/ibm-plex-sans/600.css'
import '@fontsource/ibm-plex-mono/400.css'
import '@fontsource/ibm-plex-mono/500.css'
import '@fontsource/literata/400.css'
import '@fontsource/literata/400-italic.css'

import '@astryxdesign/core/reset.css'
import '@astryxdesign/core/astryx.css'
import '@astryxdesign/theme-neutral/theme.css'
import './styles.css'

import App from './App.tsx'

// Access key for starting scans on the public demo: open the site once with ?key=…, it is kept in this browser.
const params = new URLSearchParams(window.location.search)
const accessKey = params.get('key')
if (accessKey) {
  localStorage.setItem('q-key', accessKey)
  params.delete('key')
  const rest = params.toString()
  window.history.replaceState(null, '', window.location.pathname + (rest ? `?${rest}` : ''))
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
