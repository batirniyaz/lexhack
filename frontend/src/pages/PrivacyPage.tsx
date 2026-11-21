import { useEffect, useState } from 'react'
import { api } from '../api'
import { useSettings } from '../i18n'

/**
 * Probo's own privacy notice (ZRU-547 art. 22 elements; research/legal-our-risks.md §5). It describes what the demo
 * really does today: no accounts, no own cookies, no trackers. Keep it in sync with the code.
 */
const TEXT = {
  uz: {
    title: 'Maxfiylik siyosati',
    updated: 'Tahrir: 21.11.2026',
    sections: [
      ['Operator', 'Probo — LexHackathon 2026 jamoasining demo-xizmati. Yuridik shaxs hali roʻyxatdan oʻtmagan.'],
      ['Qanday maʼlumotlarga ishlov beramiz', 'Siz haqingizda: IP-manzil, vaqt va brauzer turi — faqat suiisteʼmolni cheklash uchun (bir manzildan soatiga 6 ta tekshiruv). Akkaunt, roʻyxatdan oʻtish, oʻz cookie fayllarimiz va trekerlar yoʻq. Tekshirilgan saytlar haqida: ularning ochiq sahifalari, tarmoq soʻrovlari, sayt oʻrnatgan cookie fayllar, hujjatlar matni.'],
      ['Maqsad va asos', 'IP-manzil — xizmatni suiisteʼmoldan himoya qilish (qonuniy manfaat, Qonunning 18-moddasi). Saytlar tekshiruvi — hamma foydalanishi mumkin boʻlgan manbalardan olingan maʼlumotlar (18-modda). Statistika — faqat anonim shaklda.'],
      ['Kimga uzatiladi', 'Cloudflare (AQSh, EU-US Data Privacy Framework ishtirokchisi) — saytga xavfsiz ulanish uchun. Anthropic (AQSh) — faqat tekshirilgan saytlarning ochiq hujjatlari matni, undan e-mail, telefon, PINFL, pasport va karta raqamlari oldindan olib tashlanadi. Boshqa hech kimga berilmaydi va sotilmaydi.'],
      ['Saqlash joyi va muddati', 'Server Oʻzbekistonda (Toshkent). Server jurnallari hajm bilan cheklangan va avtomatik oʻchiriladi. Tekshiruv natijalari hakaton davomida va undan keyin 30 kungacha saqlanadi, soʻrov boʻyicha oldinroq oʻchiriladi.'],
      ['Xavfsizlik', 'HTTPS, xavfsizlik sarlavhalari, kalit bilan kirish. Tekshirilgan saytlarning xavfsizlikka oid tafsilotlari faqat sayt egasiga koʻrsatiladi (Kiberxavfsizlik toʻgʻrisidagi qonunning 24-moddasi).'],
      ['Huquqlaringiz', 'Siz oʻzingiz haqingizdagi maʼlumotlar bilan tanishish, ularni oʻchirishni talab qilish va ishlov berishga eʼtiroz bildirish huquqiga egasiz (30-modda). Shikoyat vakolatli davlat organiga yoki sudga berilishi mumkin.'],
    ],
    contact: 'Aloqa',
  },
  ru: {
    title: 'Политика конфиденциальности',
    updated: 'Редакция: 21.11.2026',
    sections: [
      ['Оператор', 'Probo — демо-сервис команды LexHackathon 2026. Юридическое лицо пока не зарегистрировано.'],
      ['Какие данные мы обрабатываем', 'О вас: IP-адрес, время и тип браузера — только для ограничения злоупотреблений (6 проверок в час с одного адреса). Аккаунтов, регистрации, собственных cookie и трекеров нет. О проверяемых сайтах: их открытые страницы, сетевые запросы, cookie, которые ставит сайт, тексты документов.'],
      ['Цели и основания', 'IP-адрес — защита сервиса от злоупотреблений (законный интерес, ст. 18 Закона). Проверка сайтов — данные из общедоступных источников (ст. 18). Статистика — только в обезличенном виде.'],
      ['Кому передаём', 'Cloudflare (США, участник EU-US Data Privacy Framework) — для защищённого подключения к сайту. Anthropic (США) — только тексты открытых документов проверяемых сайтов, из которых заранее удалены e-mail, телефоны, ПИНФЛ, номера паспортов и карт. Больше никому не передаём и не продаём.'],
      ['Где и сколько храним', 'Сервер в Узбекистане (Ташкент). Журналы сервера ограничены по объёму и удаляются автоматически. Результаты проверок хранятся во время хакатона и до 30 дней после него, по запросу удаляются раньше.'],
      ['Защита', 'HTTPS, заголовки безопасности, доступ по ключу. Сведения о безопасности проверенных сайтов показываются только владельцу сайта (ст. 24 Закона «О кибербезопасности»).'],
      ['Ваши права', 'Вы вправе узнать, какие данные о вас есть, потребовать их удаления и возразить против обработки (ст. 30). Жалобу можно подать в уполномоченный государственный орган или в суд.'],
    ],
    contact: 'Контакт',
  },
} as const

export function PrivacyPage() {
  const { lang } = useSettings()
  const text = TEXT[lang]
  const [contact, setContact] = useState<string | null>(null)
  useEffect(() => { api.health().then((h) => setContact(h.contact ?? null)).catch(() => setContact(null)) }, [])
  return (
    <div className="q-page" style={{ maxWidth: 760 }}>
      <h1 style={{ fontSize: 26, fontWeight: 600, margin: '24px 0 4px' }}>{text.title}</h1>
      <p className="q-muted" style={{ margin: '0 0 24px' }}>{text.updated}</p>
      {text.sections.map(([head, body]) => (
        <section key={head} style={{ marginBottom: 18 }}>
          <h2 style={{ fontSize: 16, margin: '0 0 6px' }}>{head}</h2>
          <p style={{ margin: 0, lineHeight: 1.6 }}>{body}</p>
        </section>
      ))}
      {contact && (
        <section>
          <h2 style={{ fontSize: 16, margin: '0 0 6px' }}>{text.contact}</h2>
          <p style={{ margin: 0 }}>{contact}</p>
        </section>
      )}
    </div>
  )
}
