import { Link } from '@astryxdesign/core/Link'
import { useNavigate } from 'react-router'
import { useSettings } from '../i18n'

/** Links every page needs: our own privacy notice (we must pass our own check) and the report verifier. */
export function Footer() {
  const { t } = useSettings()
  const navigate = useNavigate()
  const go = (path: string) => (e: React.MouseEvent) => { e.preventDefault(); navigate(path) }
  return (
    <footer className="q-footer">
      <span>© 2026 Probo · {t.footer_note}</span>
      <span style={{ display: 'flex', gap: 18 }}>
        <Link href="/privacy" onClick={go('/privacy')}>{t.footer_privacy}</Link>
        <Link href="/verify" onClick={go('/verify')}>{t.footer_verify}</Link>
      </span>
    </footer>
  )
}
