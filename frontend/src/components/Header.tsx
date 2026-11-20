import { Link, useNavigate } from 'react-router'
import { Button } from '@astryxdesign/core/Button'
import { useSettings } from '../i18n'

export function Header() {
  const { t, lang, setLang, anon, setAnon } = useSettings()
  const navigate = useNavigate()
  return (
    <>
      <header className="q-header">
        <Link to="/" className="q-logo">Probo</Link>
        <nav className="q-nav" aria-label="Main">
          <Button variant="ghost" size="sm" label={t.nav_new} onClick={() => navigate('/')} />
          <Button variant="ghost" size="sm" label={t.nav_history} onClick={() => navigate('/history')} />
          <Button variant="ghost" size="sm" label={lang === 'uz' ? 'Русский' : 'Oʻzbekcha'}
            onClick={() => setLang(lang === 'uz' ? 'ru' : 'uz')} />
          <span className={anon ? 'q-anon-on' : undefined}>
            <Button variant="ghost" size="sm" label={t.nav_present} tooltip={t.nav_present_hint}
              aria-pressed={anon} onClick={() => setAnon(!anon)} />
          </span>
        </nav>
      </header>
      <hr className="q-header-rule" />
    </>
  )
}
