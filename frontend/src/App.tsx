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
import { VerifyPage } from './pages/VerifyPage'
import { PrivacyPage } from './pages/PrivacyPage'
import { Footer } from './components/Footer'

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
              <Route path="/verify" element={<VerifyPage />} />
              <Route path="/privacy" element={<PrivacyPage />} />
              <Route path="*" element={<Home />} />
            </Routes>
          </main>
          <Footer />
        </BrowserRouter>
      </SettingsProvider>
    </Theme>
  )
}
