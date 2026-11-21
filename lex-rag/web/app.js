"use strict";

const TEXT = {
  uz: {
    brand: "Qonun savollari",
    langLabel: "Interfeys tili",
    title: "Oʻzbekiston qonunlari haqida soʻrang",
    examples: "Masalan",
    label: "Savolingiz",
    send: "Soʻrash",
    holding: (texts, inForce, date) => `Bazada hujjat matnlari: ${texts}, amaldagilari: ${inForce}. Baza sanasi: ${date}.`,
    note: "Oʻquv loyihasi, lex.uz bilan bogʻliq emas. Javob yuridik maslahat oʻrnini bosmaydi.",
    about: "Bu qanday ishlaydi",
    empty: "Avval savol yozing",
    long: "Savol 500 belgidan uzun",
    found: "Javob",
    none: "Bazada javob yoʻq",
    down: "Javob olinmadi",
    basis: "Javob nimaga asoslangan",
    edition: (date) => `Tahrir: ${date}`,
    state: (status) => `Hujjat holati: ${status}`,
    seconds: (s) => `${String(s).replace(".", ",")} s`,
    months: ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"],
    date: (day, month, year) => `${year}-yil ${day}-${month}`,
    steps: { read: "Savolni oʻqiyapman", search: "Qonunlardan qidiryapman", answer: "Javobni yozyapman", correct: "Javobni tekshiryapman" },
    errorNet: "Server javob bermadi. Aloqani tekshirib, savolni qayta yuboring.",
    errorRate: "Bir daqiqada savollar juda koʻp. Bir daqiqa kutib, qayta yuboring.",
    errorDay: "Bugungi savollar soni tugadi. Ertaga qayta yuboring.",
    errorModel: "Javob yozilmadi. Savolni qayta yuboring.",
    retry: "Qayta yuborish",
    list: [
      ["Yillik asosiy mehnat ta'tilining eng kam muddati qancha?", "Mehnat"],
      ["Erkaklar va ayollar necha yoshdan oila qurishi mumkin?", "Oila"],
      ["Qo'shilgan qiymat solig'i stavkasi necha foiz?", "Soliq"],
      ["Otam vafot etdi, uyiga kimlar da'vo qila oladi?", "Meros"],
      ["Жиноий жавобгарлик неча ёшдан бошланади?", "Jinoyat"],
      ["Palovni qanday pishirish kerak?", "Qonunda yoʻq"],
    ],
  },
  ru: {
    brand: "Вопросы по законам",
    langLabel: "Язык интерфейса",
    title: "Спросите про законы Узбекистана",
    examples: "Например",
    label: "Ваш вопрос",
    send: "Спросить",
    holding: (texts, inForce, date) => `Текстов актов в базе: ${texts}, действующих: ${inForce}. База на ${date}.`,
    note: "Учебный проект, с lex.uz не связан. Ответ не заменяет консультацию юриста.",
    about: "Как это устроено",
    empty: "Сначала напишите вопрос",
    long: "Вопрос длиннее 500 символов",
    found: "Ответ",
    none: "В базе ответа нет",
    down: "Ответ не получен",
    basis: "На чём основан ответ",
    edition: (date) => `Редакция: ${date}`,
    state: (status) => `Статус акта: ${status}`,
    seconds: (s) => `${String(s).replace(".", ",")} с`,
    months: ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    date: (day, month, year) => `${day} ${month} ${year}`,
    steps: { read: "Читаю вопрос", search: "Ищу в законах", answer: "Пишу ответ", correct: "Перепроверяю ответ" },
    errorNet: "Сервер не ответил. Проверьте соединение и задайте вопрос ещё раз.",
    errorRate: "Слишком много вопросов за минуту. Подождите минуту и задайте вопрос ещё раз.",
    errorDay: "Вопросы на сегодня закончились. Задайте вопрос завтра.",
    errorModel: "Ответ не написан. Задайте вопрос ещё раз.",
    retry: "Спросить ещё раз",
    list: [
      ["Какой срок исковой давности установлен Гражданским кодексом?", "Гражданское право"],
      ["Сколько дней составляет минимальный ежегодный трудовой отпуск?", "Труд"],
      ["С какого возраста разрешён брак в Узбекистане?", "Семья"],
      ["Какова ставка налога на добавленную стоимость?", "Налоги"],
      ["Как приготовить плов?", "Не про закон"],
    ],
  },
};

const $ = (sel, root = document) => root.querySelector(sel);
const form = $("#ask");
const input = $("#q");
const send = $("#send");
const hint = $("#hint");
const thread = $("#thread");

const params = new URLSearchParams(location.search);
let lang = ["uz", "ru"].includes(params.get("lang")) ? params.get("lang") : (navigator.language || "").startsWith("ru") ? "ru" : "uz";
let about = null;
let busy = false;
let count = 0;

function day(iso) {
  if (!iso) return "";
  const t = TEXT[lang];
  const [year, month, date] = iso.split("-").map(Number);
  return t.date(date, t.months[month - 1], year);
}

function paintHolding() {
  if (!about) return;
  $("#holding").textContent = TEXT[lang].holding(about.with_text.toLocaleString("ru-RU"), about.in_force.toLocaleString("ru-RU"), day(about.snapshot));
}

function paintLanguage() {
  const t = TEXT[lang];
  document.documentElement.lang = lang;
  document.title = t.brand;
  document.querySelectorAll("[data-t]").forEach((el) => { el.textContent = t[el.dataset.t]; });
  document.querySelectorAll("[data-t-aria]").forEach((el) => { el.setAttribute("aria-label", t[el.dataset.tAria]); });
  document.querySelectorAll("[data-lang]").forEach((b) => { b.setAttribute("aria-pressed", String(b.dataset.lang === lang)); });
  $("#examples").replaceChildren(...t.list.map(([q, topic]) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.className = "example";
    a.href = `?q=${encodeURIComponent(q)}`;
    a.setAttribute("aria-disabled", String(busy));
    const text = document.createElement("span");
    text.textContent = q;
    const branch = document.createElement("span");
    branch.className = "example__topic";
    branch.textContent = topic;
    a.append(text, branch);
    a.addEventListener("click", (e) => { e.preventDefault(); ask(q); });
    li.append(a);
    return li;
  }));
  paintHolding();
}

document.querySelectorAll("[data-lang]").forEach((b) => b.addEventListener("click", () => {
  lang = b.dataset.lang;
  params.set("lang", lang);
  history.replaceState(null, "", `?${params}`);
  paintLanguage();
}));

function setHint(message) {
  hint.textContent = message || "";
  hint.classList.toggle("is-error", Boolean(message));
  input.setAttribute("aria-invalid", message ? "true" : "false");
}

function fitBox() {
  input.style.height = "auto";
  input.style.height = `${input.scrollHeight + 2}px`;
}

/* On a phone focus opens the keyboard over the answer, so only a real pointer gets it. */
function focusBox() {
  if (matchMedia("(hover: hover)").matches) input.focus({ preventScroll: true });
}

function setBusy(value) {
  busy = value;
  send.disabled = value;
  document.querySelectorAll(".example").forEach((a) => { a.setAttribute("aria-disabled", String(value)); });
}

input.addEventListener("input", () => { setHint(); fitBox(); });
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    form.requestSubmit();
  }
});
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) { setHint(TEXT[lang].empty); input.focus(); return; }
  if (q.length > 500) { setHint(TEXT[lang].long); return; }
  ask(q);
});

/* The answer carries marks like [2]. Each becomes a link to its article beside it. Text only goes in through text nodes. */
function fillAnswer(el, text, no) {
  el.replaceChildren();
  let last = 0;
  for (const m of text.matchAll(/\s*\[(\d+)\]/g)) {
    el.append(text.slice(last, m.index));
    const a = document.createElement("a");
    a.className = "mark";
    a.href = `#a${no}-s${m[1]}`;
    a.textContent = m[1];
    el.append(a);
    last = m.index + m[0].length;
  }
  el.append(text.slice(last));
}

function buildSource(c, no, t) {
  const li = document.createElement("li");
  li.className = "source";
  li.id = `a${no}-s${c.ref}`;
  const number = document.createElement("span");
  number.className = "source__no";
  number.textContent = c.ref;
  const body = document.createElement("div");
  const link = document.createElement("a");
  link.className = "source__place";
  if (/^https:\/\/lex\.uz\//.test(c.url)) {
    link.href = c.url;
    link.target = "_blank";
    link.rel = "noopener";
  }
  const place = [c.article, c.part].filter(Boolean).join(", ");
  if (place) {
    const strong = document.createElement("strong");
    strong.textContent = place;
    link.append(strong, " ");
  }
  link.append(c.doc_title);
  const quote = document.createElement("blockquote");
  quote.className = "source__quote";
  quote.textContent = c.quote;
  body.append(link, quote);
  const notes = [];
  if (c.doc_status && c.doc_status !== "amalda") notes.push(t.state(c.doc_status));
  if (c.edition_date) notes.push(t.edition(day(c.edition_date)));
  if (notes.length) {
    const meta = document.createElement("p");
    meta.className = "source__meta";
    meta.textContent = notes.join(". ");
    body.append(meta);
  }
  li.append(number, body);
  return li;
}

function statusLabel(status, t) {
  if (status === "ok") return t.found;
  if (status === "no_answer") return t.none;
  return t.down;
}

function renderAnswer(q, r, no, seconds) {
  const t = TEXT[lang];
  const node = $("#answer-tpl").content.firstElementChild.cloneNode(true);
  $(".entry__status", node).textContent = statusLabel(r.status, t);
  $(".entry__time", node).textContent = t.seconds(seconds);
  $(".entry__q", node).textContent = q;
  const text = $(".entry__text", node);
  fillAnswer(text, r.answer, no);
  text.classList.toggle("entry__text--long", r.answer.length > 180);
  if (r.citations.length) {
    $(".entry__body", node).classList.remove("entry__body--plain");
    $(".basis", node).hidden = false;
    $(".basis__head", node).textContent = t.basis;
    $(".sources", node).append(...r.citations.map((c) => buildSource(c, no, t)));
  }
  return node;
}

function renderFailure(q, message) {
  const t = TEXT[lang];
  const node = $("#answer-tpl").content.firstElementChild.cloneNode(true);
  $(".entry__status", node).textContent = t.down;
  $(".entry__q", node).textContent = q;
  const text = $(".entry__text", node);
  text.textContent = message;
  text.classList.add("entry__text--long");
  const again = document.createElement("button");
  again.type = "button";
  again.className = "key key--quiet retry";
  again.textContent = t.retry;
  again.addEventListener("click", () => { node.remove(); ask(q); });
  text.after(again);
  return node;
}

async function failureOf(res) {
  if (res.status !== 429) return "errorNet";
  const body = await res.json().catch(() => null);
  return body && body.error && body.error.code === "DAILY_LIMIT" ? "errorDay" : "errorRate";
}

async function ask(q) {
  if (busy) return;
  setBusy(true);
  setHint();
  document.body.classList.add("has-answers");
  input.value = "";
  fitBox();
  const no = ++count;

  const t = TEXT[lang];
  const wait = $("#wait-tpl").content.firstElementChild.cloneNode(true);
  $(".entry__q", wait).textContent = q;
  const step = $(".wait__step", wait);
  const clock = $(".wait__time", wait);
  step.textContent = t.steps.read;
  thread.prepend(wait);
  window.scrollTo({ top: 0 });
  const began = performance.now();
  const passed = () => (performance.now() - began) / 1000;
  const timer = setInterval(() => { clock.textContent = t.seconds(Math.round(passed())); }, 1000);

  let node;
  try {
    const res = await fetch("api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q }) });
    if (!res.ok || !res.body) throw new Error(await failureOf(res));
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.trim()) continue;
        const message = JSON.parse(line);
        if (message.step && t.steps[message.step]) step.textContent = t.steps[message.step];
        if (message.answer) {
          if (!message.answer.answer) throw new Error("errorModel");
          node = renderAnswer(q, message.answer, no, passed().toFixed(1));
        }
      }
    }
    if (!node) throw new Error("errorNet");
  } catch (e) {
    node = renderFailure(q, t[e.message] || t.errorNet);
  }
  clearInterval(timer);
  wait.replaceWith(node);
  setBusy(false);
  focusBox();
}

paintLanguage();
input.value = (params.get("q") || "").slice(0, 500);   /* a link fills the box and no more: opening a page must not spend a question */
fitBox();
focusBox();
fetch("api/about").then((res) => (res.ok ? res.json() : null)).then((facts) => {
  if (facts && facts.with_text) { about = facts; paintHolding(); }
}).catch(() => {});
