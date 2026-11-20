import { BrowserRouter, Route, Routes } from 'react-router'
import { Theme } from '@astryxdesign/core/theme'
import { neutralTheme } from '@astryxdesign/theme-neutral/built'
import { SettingsProvider } from './i18n'
import { Header } from './components/Header'
import { Home } from './pages/Home'
import { ScanPage } from './pages/ScanPage'
import { History } from './pages/History'
import { SitePage } from './pages/SitePage'
import { SharedPage } from './pages/SharedPage'

export default function App() {
  return (
    <Theme theme={neutralTheme}>
      <SettingsProvider>
        <BrowserRouter>
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/scan/*" element={<ScanPage />} />
              <Route path="/history" element={<History />} />
              <Route path="/sites/:domain" element={<SitePage />} />
              <Route path="/r/:token" element={<SharedPage />} />
              <Route path="*" element={<Home />} />
            </Routes>
          </main>
        </BrowserRouter>
      </SettingsProvider>
    </Theme>
  )
}
