import { useEffect, useState, type ChangeEvent } from 'react'
import { Badge } from '@astryxdesign/core/Badge'
import { Button } from '@astryxdesign/core/Button'
import { api, type VerifyResult } from '../api'
import { formatDate, useSettings } from '../i18n'

/** /verify — anyone can check a Probo evidence file: signature, our key, and a report this server issued (F-19). */
export function VerifyPage() {
  const { t } = useSettings()
  const [text, setText] = useState('')
  const [result, setResult] = useState<VerifyResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [key, setKey] = useState<{ public_key: string; key_id: string } | null>(null)

  useEffect(() => { api.verifyKey().then(setKey).catch(() => setKey(null)) }, [])

  const check = async () => {
    setResult(null)
    setError(null)
    let seal: unknown
    try {
      seal = JSON.parse(text)
    } catch {
      setError(t.verify_bad_json)
      return
    }
    try {
      setResult(await api.verify(seal))
    } catch {
      setError(t.verify_error)
    }
  }

  const load = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) void file.text().then(setText)
  }

  const statement = result?.statement
  return (
    <div className="q-page" style={{ maxWidth: 760 }}>
      <h1 style={{ fontSize: 26, fontWeight: 600, margin: '24px 0 8px' }}>{t.verify_title}</h1>
      <p className="q-muted" style={{ margin: '0 0 18px' }}>{t.verify_text}</p>
      <textarea className="q-textarea q-mono" rows={10} value={text} onChange={(e) => setText(e.target.value)}
        aria-label="evidence.json" spellCheck={false} />
      <div style={{ display: 'flex', gap: 12, alignItems: 'center', margin: '12px 0 24px', flexWrap: 'wrap' }}>
        <Button variant="primary" label={t.verify_button} onClick={() => void check()} isDisabled={!text.trim()} />
        <label className="q-file">
          <input type="file" accept="application/json,.json" onChange={load} />
          <span>{t.verify_file}</span>
        </label>
      </div>
      {error && <p role="alert" style={{ color: 'var(--q-violation)' }}>{error}</p>}
      {result && (
        <section aria-live="polite" style={{ display: 'grid', gap: 10 }}>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <Badge variant={result.valid_signature ? 'success' : 'error'} label={result.valid_signature ? t.verify_valid : t.verify_invalid} />
            {result.valid_signature && (
              <Badge variant={result.our_key ? 'success' : 'warning'} label={result.our_key ? t.verify_our_key : t.verify_other_key} />
            )}
            {result.valid_signature && (
              <Badge variant={result.known_report ? 'success' : 'warning'} label={result.known_report ? t.verify_known : t.verify_unknown} />
            )}
          </div>
          {statement && (
            <dl className="q-dl">
              <div><dt>URL</dt><dd className="q-mono">{statement.site}</dd></div>
              <div><dt>{t.seal_when}</dt><dd>{formatDate(statement.scanned_at)}</dd></div>
              <div><dt>{t.score}</dt><dd>{statement.score ?? '—'}</dd></div>
              <div><dt>SHA-256 · report</dt><dd className="q-mono q-hash">{statement.sha256.report}</dd></div>
              <div><dt>{t.seal_signature}</dt><dd className="q-mono">{statement.key_id} · {formatDate(statement.sealed_at)}</dd></div>
            </dl>
          )}
        </section>
      )}
      {key && (
        <p className="q-muted" style={{ fontSize: 13, marginTop: 32 }}>
          {t.verify_key} (Ed25519, {key.key_id}): <span className="q-mono q-hash">{key.public_key}</span>
        </p>
      )}
    </div>
  )
}
