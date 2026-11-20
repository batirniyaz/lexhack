// UI strings (Uzbek Latin default, Russian) + app-wide settings: language and presentation mode.
// Uzbek copy was written by Role 1 — teammates, please review the wording.
import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'

export type Lang = 'uz' | 'ru'

const uz = {
  nav_new: 'Yangi tekshiruv',
  nav_history: 'Tarix',
  nav_present: 'Taqdimot rejimi',
  nav_present_hint: 'Sayt nomlari yashiriladi',
  hero_title: 'Saytingiz shaxsiy maʼlumotlarni aslida qayerga yuboryapti?',
  hero_text: 'Probo saytni oddiy tashrif buyuruvchi kabi ochadi, maxfiylik siyosatini oʻqiydi va ikkalasini Oʻzbekiston qonuni bilan solishtiradi.',
  url_label: 'Sayt manzili',
  url_placeholder: 'masalan, misol.uz',
  check: 'Tekshirish',
  fineprint: 'Faqat ochiq sahifalar, 1–2 daqiqa. Natija — qonunbuzarlik belgilari, yuridik xulosa emas.',
  sample_title: 'Hisobotdan namuna',
  sample_open: 'Namuna hisobotni ochish',
  facts_title: 'Mashhur saytlarda nima topdik',
  fact_trackers: (k: number, n: number) => `${n} ta mashhur saytdan ${k} tasida trekerlar birinchi tashrifdayoq, roziliksiz yuklanadi.`,
  fact_webvisor: (k: number, _n: number) => `${k} tasida Yandex Webvisor tashrif buyuruvchi shaklga nima yozayotganini yozib oladi.`,
  fact_policy: (k: number, _n: number) => `${k} tasining maxfiylik siyosati sayt aslida foydalanadigan xizmatlarni tilga olmaydi.`,
  fact_note: 'Saytlar nomi koʻrsatilmaydi. Passiv tekshiruv natijalari.',
  says: 'Siyosatda yozilgan',
  does: 'Sayt aslida nima qiladi',
  scanning: (site: string) => `${site} tekshirilmoqda`,
  stage_pages: 'Sahifalar',
  stage_network: 'Tarmoq soʻrovlari',
  stage_forms: 'Shakllar va hujjatlar',
  stage_policy: 'Siyosatni oʻqish',
  stage_law: 'Qonun bilan solishtirish',
  c_hosts: 'uchinchi tomon xostlari',
  c_countries: 'davlat',
  c_forms: 'shaxsiy maʼlumot shakli',
  c_docs: 'huquqiy hujjat',
  log_page: 'sahifa',
  log_host: 'xost',
  log_form: 'shakl',
  log_doc: 'hujjat',
  log_policy: 'siyosat',
  log_finding: 'topilma',
  log_wait: 'kutilmoqda',
  first_visit: 'birinchi tashrifda',
  first_visit_all: 'birinchi tashrifdayoq, roziliksiz',
  no_consent: 'rozilik yoʻq',
  with_consent: 'rozilik bor',
  policy_reading: 'AI siyosatni oʻqimoqda…',
  policy_done: (n: number) => `${n} ta vaʼda topildi, iqtiboslar matn bilan tekshirildi`,
  challenge: 'Sayt botlarni tekshirmoqda, kutamiz…',
  blocked_title: 'Sayt tekshiruvga yopiq',
  blocked_text: 'Sayt botlardan himoya sahifasini koʻrsatdi. Bunday sahifadagi maʼlumot sayt haqida emas, shuning uchun hech qanday topilma chiqarilmadi.',
  error_title: 'Tekshiruv yakunlanmadi',
  retry: 'Qayta tekshirish',
  score: 'Ball',
  of100: '100 dan',
  lvl_violation: 'jiddiy',
  lvl_risk: 'xavf',
  lvl_recommendation: 'tavsiya',
  scanned: (pages: number, req: number) => `${pages} sahifa, ${req} soʻrov`,
  not_verified: 'Qoidalar hali yurist tomonidan tekshirilmagan. Bu qonunbuzarlik belgilari, yuridik xulosa emas.',
  tab_overview: 'Umumiy',
  tab_findings: 'Topilmalar',
  tab_flows: 'Maʼlumot oqimi',
  tab_policy: 'Siyosat',
  top_findings: 'Asosiy topilmalar',
  all_findings: 'Barcha topilmalar',
  flows_sentence: (n: number) => `Maʼlumotlar ${n} ta davlatdagi kompaniyalarga yuboriladi.`,
  evidence: 'Dalillar',
  law: 'Qonun',
  fix: 'Qanday tuzatish',
  copy: 'Nusxa olish',
  copied: 'Nusxa olindi',
  unofficial: 'rasmiy boʻlmagan tarjima',
  official: 'rasmiy matn',
  open_lex: 'lex.uz da ochish',
  downgraded: 'Vaʼdada istisnolar bor, shuning uchun daraja pasaytirildi. Yurist baholashi kerak.',
  rule_unverified: 'yurist tekshirmagan',
  rule_verified: 'yurist tekshirgan',
  no_findings: 'Belgilangan tekshiruvlar boʻyicha topilma yoʻq',
  limits: 'Biz faqat brauzer koʻradigan narsani koʻramiz: maʼlumotlar bazasi qayerdaligi va server maʼlumotni keyin qayerga yuborishi tashqaridan koʻrinmaydi.',
  host: 'Xost',
  owner: 'Kompaniya',
  company_country: 'Kompaniya davlati',
  server_country: 'Server',
  category: 'Turi',
  first: 'Birinchi tashrif',
  requests: 'Soʻrovlar',
  yes: 'ha',
  no: 'yoʻq',
  st_local: 'Oʻzbekiston',
  st_allowed: 'Roʻyxatdagi davlat',
  st_conditional: 'Shart bilan',
  st_not_listed: 'Roʻyxatda yoʻq',
  st_undetermined: 'Aniqlanmagan',
  hosts_n: (n: number) => `${n} ta xost`,
  docs_read: 'Oʻqilgan hujjatlar',
  elements: 'Siyosatning majburiy bandlari',
  present: 'bor',
  missing: 'yoʻq',
  promises: 'Saytning vaʼdalari',
  promise_contradicted: 'Skaner natijasiga zid',
  promise_unchecked: 'Skaner bunga zid narsa topmadi',
  undisclosed: 'Siyosat tilga olmagan xizmatlar',
  no_policy: 'Siyosat matni topilmadi yoki tahlil qilinmadi.',
  history_title: 'Tekshiruvlar tarixi',
  history_empty: 'Hali tekshiruv yoʻq',
  history_empty_text: 'Sayt manzilini kiriting — natija shu yerda saqlanadi.',
  col_site: 'Sayt',
  col_date: 'Sana',
  col_score: 'Ball',
  col_findings: 'Topilmalar',
  col_status: 'Holat',
  status_ok: 'tayyor',
  status_blocked: 'yopiq',
  open: 'Ochish',
  replay: 'Jonli tasmani qayta koʻrsatish',
  loading: 'Yuklanmoqda…',
  not_found: 'Bunday tekshiruv topilmadi',
  bad_url: 'Manzilni tekshiring: masalan, misol.uz',
}

type Dict = typeof uz

const ru: Dict = {
  nav_new: 'Новая проверка',
  nav_history: 'История',
  nav_present: 'Режим презентации',
  nav_present_hint: 'Названия сайтов скрыты',
  hero_title: 'Куда ваш сайт на самом деле отправляет персональные данные?',
  hero_text: 'Probo открывает сайт как обычный посетитель, читает политику конфиденциальности и сравнивает одно с другим по закону Узбекистана.',
  url_label: 'Адрес сайта',
  url_placeholder: 'например, primer.uz',
  check: 'Проверить',
  fineprint: 'Только открытые страницы, 1–2 минуты. Результат — признаки нарушения, а не юридическое заключение.',
  sample_title: 'Пример из отчёта',
  sample_open: 'Открыть пример отчёта',
  facts_title: 'Что мы нашли на популярных сайтах',
  fact_trackers: (k, n) => `На ${k} из ${n} популярных сайтов трекеры загружаются при первом визите, без согласия.`,
  fact_webvisor: (k) => `На ${k} из них Яндекс Вебвизор записывает, что посетитель вводит в формы.`,
  fact_policy: (k) => `У ${k} из них политика не называет сервисы, которыми сайт реально пользуется.`,
  fact_note: 'Названия сайтов не показываем. Результаты пассивной проверки.',
  says: 'Что написано в политике',
  does: 'Что сайт делает на самом деле',
  scanning: (site) => `Проверяем ${site}`,
  stage_pages: 'Страницы',
  stage_network: 'Сетевые запросы',
  stage_forms: 'Формы и документы',
  stage_policy: 'Чтение политики',
  stage_law: 'Сверка с законом',
  c_hosts: 'сторонних хостов',
  c_countries: 'стран',
  c_forms: 'форм с персданными',
  c_docs: 'юридических документов',
  log_page: 'страница',
  log_host: 'хост',
  log_form: 'форма',
  log_doc: 'документ',
  log_policy: 'политика',
  log_finding: 'находка',
  log_wait: 'ожидание',
  first_visit: 'при первом визите',
  first_visit_all: 'сразу при первом визите, без согласия',
  no_consent: 'нет согласия',
  with_consent: 'согласие есть',
  policy_reading: 'ИИ читает политику…',
  policy_done: (n) => `Найдено обещаний: ${n}, цитаты сверены с текстом`,
  challenge: 'Сайт проверяет, не бот ли мы. Ждём…',
  blocked_title: 'Сайт закрыт для проверки',
  blocked_text: 'Сайт показал страницу защиты от ботов. Данные с такой страницы относятся не к сайту, поэтому находок нет.',
  error_title: 'Проверка не завершилась',
  retry: 'Проверить снова',
  score: 'Оценка',
  of100: 'из 100',
  lvl_violation: 'серьёзных',
  lvl_risk: 'рисков',
  lvl_recommendation: 'рекомендаций',
  scanned: (pages, req) => `${pages} страниц, ${req} запросов`,
  not_verified: 'Правила ещё не проверены юристом. Это признаки нарушения, а не юридическое заключение.',
  tab_overview: 'Обзор',
  tab_findings: 'Находки',
  tab_flows: 'Потоки данных',
  tab_policy: 'Политика',
  top_findings: 'Главные находки',
  all_findings: 'Все находки',
  flows_sentence: (n) => `Данные уходят компаниям из стран: ${n}.`,
  evidence: 'Доказательства',
  law: 'Закон',
  fix: 'Как исправить',
  copy: 'Скопировать',
  copied: 'Скопировано',
  unofficial: 'неофициальный перевод',
  official: 'официальный текст',
  open_lex: 'Открыть на lex.uz',
  downgraded: 'В обещании есть оговорки, поэтому уровень понижен. Нужна оценка юриста.',
  rule_unverified: 'не проверено юристом',
  rule_verified: 'проверено юристом',
  no_findings: 'По заданным проверкам находок нет',
  limits: 'Мы видим только то, что видит браузер: где стоит база данных и куда сервер передаёт данные дальше, снаружи не видно.',
  host: 'Хост',
  owner: 'Компания',
  company_country: 'Страна компании',
  server_country: 'Сервер',
  category: 'Тип',
  first: 'Первый визит',
  requests: 'Запросы',
  yes: 'да',
  no: 'нет',
  st_local: 'Узбекистан',
  st_allowed: 'Страна в перечне',
  st_conditional: 'С условием',
  st_not_listed: 'Нет в перечне',
  st_undetermined: 'Не определено',
  hosts_n: (n) => `хостов: ${n}`,
  docs_read: 'Прочитанные документы',
  elements: 'Обязательные пункты политики',
  present: 'есть',
  missing: 'нет',
  promises: 'Обещания сайта',
  promise_contradicted: 'Противоречит результату скана',
  promise_unchecked: 'Скан не нашёл противоречий',
  undisclosed: 'Сервисы, о которых политика молчит',
  no_policy: 'Текст политики не найден или не проанализирован.',
  history_title: 'История проверок',
  history_empty: 'Проверок пока нет',
  history_empty_text: 'Введите адрес сайта — результат сохранится здесь.',
  col_site: 'Сайт',
  col_date: 'Дата',
  col_score: 'Оценка',
  col_findings: 'Находки',
  col_status: 'Статус',
  status_ok: 'готово',
  status_blocked: 'закрыт',
  open: 'Открыть',
  replay: 'Показать живую ленту ещё раз',
  loading: 'Загрузка…',
  not_found: 'Такая проверка не найдена',
  bad_url: 'Проверьте адрес: например, primer.uz',
}

const DICTS: Record<Lang, Dict> = { uz, ru }

// Labels that come from the backend as keys.
export const CATEGORY: Record<Lang, Record<string, string>> = {
  uz: {
    analytics: 'analitika', advertising: 'reklama', tag_manager: 'teg menejeri', session_replay: 'seans yozuvi',
    social: 'ijtimoiy tarmoq', marketing: 'marketing', ab_testing: 'A/B test', cdn: 'CDN', fonts: 'shriftlar',
    hosting: 'hosting', payments: 'toʻlov', crm: 'CRM', chat: 'chat', captcha: 'kapcha', maps: 'xarita',
    translation: 'tarjima', government: 'davlat xizmati', other: 'boshqa',
  },
  ru: {
    analytics: 'аналитика', advertising: 'реклама', tag_manager: 'тег-менеджер', session_replay: 'запись сессий',
    social: 'соцсеть', marketing: 'маркетинг', ab_testing: 'A/B-тест', cdn: 'CDN', fonts: 'шрифты',
    hosting: 'хостинг', payments: 'оплата', crm: 'CRM', chat: 'чат', captcha: 'капча', maps: 'карты',
    translation: 'перевод', government: 'госуслуга', other: 'другое',
  },
}

export const ELEMENT: Record<Lang, Record<string, string>> = {
  uz: {
    operator: 'Operator (kim maʼlumotlarni qayta ishlaydi)', purposes: 'Qayta ishlash maqsadlari',
    data_categories: 'Qaysi maʼlumotlar yigʻiladi', consent: 'Rozilik qanday beriladi va qaytarib olinadi',
    retention: 'Saqlash muddati', recipients: 'Maʼlumot oluvchi uchinchi shaxslar',
    cross_border: 'Chet elga uzatish va saqlash joyi', subject_rights: 'Subyekt huquqlari',
    contact: 'Murojaat uchun aloqa', cookies: 'Cookie va kuzatuv',
  },
  ru: {
    operator: 'Оператор (кто обрабатывает данные)', purposes: 'Цели обработки', data_categories: 'Какие данные собираются',
    consent: 'Как даётся и отзывается согласие', retention: 'Срок хранения', recipients: 'Третьи лица — получатели',
    cross_border: 'Передача за рубеж и место хранения', subject_rights: 'Права субъекта',
    contact: 'Контакт для обращений', cookies: 'Cookie и отслеживание',
  },
}

export const CLAIM: Record<Lang, Record<string, string>> = {
  uz: {
    data_stored_in_uzbekistan: 'Maʼlumotlar faqat Oʻzbekistonda saqlanadi', no_cross_border_transfer: 'Chet elga uzatilmaydi',
    cross_border_transfer_disclosed: 'Chet elga uzatish haqida aytilgan', no_third_party_sharing: 'Uchinchi shaxslarga berilmaydi',
    third_party_services_listed: 'Foydalaniladigan xizmatlar nomlangan', tracking_only_with_consent: 'Kuzatuv faqat rozilik bilan',
    no_biometric_data: 'Biometrik maʼlumot yigʻilmaydi', other: 'Boshqa vaʼda',
  },
  ru: {
    data_stored_in_uzbekistan: 'Данные хранятся только в Узбекистане', no_cross_border_transfer: 'За рубеж не передаются',
    cross_border_transfer_disclosed: 'Передача за рубеж раскрыта', no_third_party_sharing: 'Третьим лицам не передаются',
    third_party_services_listed: 'Названы используемые сервисы', tracking_only_with_consent: 'Отслеживание только с согласия',
    no_biometric_data: 'Биометрию не собирают', other: 'Другое обещание',
  },
}

interface Settings {
  lang: Lang
  setLang: (lang: Lang) => void
  anon: boolean
  setAnon: (anon: boolean) => void
  t: Dict
}

const SettingsContext = createContext<Settings | null>(null)

function stored<T extends string>(key: string, fallback: T, allowed: readonly T[]): T {
  const value = typeof localStorage !== 'undefined' ? localStorage.getItem(key) : null
  return allowed.includes(value as T) ? (value as T) : fallback
}

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => stored('q-lang', 'uz', ['uz', 'ru'] as const))
  const [anon, setAnonState] = useState<boolean>(() => stored('q-anon', 'off', ['on', 'off'] as const) === 'on')
  const setLang = useCallback((value: Lang) => {
    setLangState(value)
    localStorage.setItem('q-lang', value)
    document.documentElement.lang = value
  }, [])
  const setAnon = useCallback((value: boolean) => {
    setAnonState(value)
    localStorage.setItem('q-anon', value ? 'on' : 'off')
  }, [])
  const value = useMemo(() => ({ lang, setLang, anon, setAnon, t: DICTS[lang] }), [lang, setLang, anon, setAnon])
  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>
}

export function useSettings(): Settings {
  const value = useContext(SettingsContext)
  if (!value) throw new Error('useSettings must be used inside SettingsProvider')
  return value
}

/** 20.11.2026, 20:06 — the same in both languages (the browser's "uz" date format renders as "2026 M11 20"). */
export function formatDate(iso: string | null | undefined): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const p = (n: number) => String(n).padStart(2, '0')
  return `${p(d.getDate())}.${p(d.getMonth() + 1)}.${d.getFullYear()}, ${p(d.getHours())}:${p(d.getMinutes())}`
}

const regionNames: Partial<Record<Lang, Intl.DisplayNames>> = {}

// Our own names for countries we actually see: some browsers (e.g. headless Chromium) have no Uzbek country names.
const COUNTRY_NAMES: Record<Lang, Record<string, string>> = {
  uz: {
    UZ: 'Oʻzbekiston', US: 'AQSh', RU: 'Rossiya', DE: 'Germaniya', NL: 'Niderlandiya', FI: 'Finlandiya', FR: 'Fransiya',
    GB: 'Buyuk Britaniya', IE: 'Irlandiya', SE: 'Shvetsiya', PL: 'Polsha', IL: 'Isroil', CA: 'Kanada',
    KR: 'Janubiy Koreya', JP: 'Yaponiya', CN: 'Xitoy', SG: 'Singapur', AE: 'BAA', TR: 'Turkiya', KZ: 'Qozogʻiston',
    KG: 'Qirgʻiziston', TJ: 'Tojikiston', CH: 'Shveytsariya', IT: 'Italiya', ES: 'Ispaniya', IN: 'Hindiston',
    HK: 'Gonkong', AU: 'Avstraliya', MT: 'Malta', LU: 'Lyuksemburg', AT: 'Avstriya', BE: 'Belgiya', DK: 'Daniya',
    NO: 'Norvegiya', CZ: 'Chexiya', UA: 'Ukraina', BY: 'Belarus', LT: 'Litva', LV: 'Latviya', EE: 'Estoniya',
  },
  ru: {
    UZ: 'Узбекистан', US: 'США', RU: 'Россия', DE: 'Германия', NL: 'Нидерланды', FI: 'Финляндия', FR: 'Франция',
    GB: 'Великобритания', IE: 'Ирландия', SE: 'Швеция', PL: 'Польша', IL: 'Израиль', CA: 'Канада',
    KR: 'Южная Корея', JP: 'Япония', CN: 'Китай', SG: 'Сингапур', AE: 'ОАЭ', TR: 'Турция', KZ: 'Казахстан',
    KG: 'Киргизия', TJ: 'Таджикистан', CH: 'Швейцария', IT: 'Италия', ES: 'Испания', IN: 'Индия',
    HK: 'Гонконг', AU: 'Австралия', MT: 'Мальта', LU: 'Люксембург', AT: 'Австрия', BE: 'Бельгия', DK: 'Дания',
    NO: 'Норвегия', CZ: 'Чехия', UA: 'Украина', BY: 'Беларусь', LT: 'Литва', LV: 'Латвия', EE: 'Эстония',
  },
}

/** Localized country name for an ISO-2 code: our table first, then the browser's CLDR data, then the code. */
export function countryName(code: string | null | undefined, lang: Lang): string {
  if (!code || code === '?') return '?'
  const own = COUNTRY_NAMES[lang][code]
  if (own) return own
  try {
    regionNames[lang] ??= new Intl.DisplayNames([lang], { type: 'region' })
    return regionNames[lang]!.of(code) ?? code
  } catch {
    return code
  }
}
