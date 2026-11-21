"use strict";

const $ = (sel, root = document) => root.querySelector(sel);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined && text !== null) n.textContent = text;
  return n;
};
const svg = (tag, attrs, text) => {
  const n = document.createElementNS("http://www.w3.org/2000/svg", tag);
  Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
  if (text !== undefined) n.textContent = text;
  return n;
};

const PAGE = 100;
const HALF_MS = 5000;     /* the spec: half of the answers within 5 s */
const MOST_MS = 12000;    /* and 95 % within 12 s */
const params = new URLSearchParams(location.search);
const filters = $("#filters");
const rowsBox = $("#rows");
const state = $("#state");
const more = $("#more");
const tip = $("#tip");
const chartBox = $("#chart");
let offset = 0;
let groups = [];

const seconds = (ms) => (ms === null || ms === undefined ? "—" : `${(ms / 1000).toFixed(1).replace(".", ",")} с`);
const whole = (n) => (n === null || n === undefined ? "—" : Math.round(n).toLocaleString("ru-RU"));
const dollars = (usd) => (usd === null || usd === undefined ? "—" : `$${usd.toFixed(4).replace(".", ",")}`);
const when = (iso) => (iso ? new Date(iso).toLocaleString("ru-RU", { timeZone: "Asia/Tashkent", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "—");

const SOURCE = { web: "С сайта", api: "Запрос API", batch: "Прогон", app: "Приложение" };
const STATUS = { ok: "Ответ", no_answer: "Нет ответа", error: "Сбой", timeout: "Таймаут" };
const ICON_OK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5"/></svg>';
const ICON_FAIL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>';

async function get(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(String(res.status));
  return res.json();
}

const groupKey = (g) => [g.source, g.run_id].filter(Boolean).join(":");
const groupName = (g) => [SOURCE[g.source] || g.source, g.run_id].filter(Boolean).join(" ");
const chosen = () => groups.find((g) => groupKey(g) === filters.elements.view.value) || groups.find((g) => g.source === "batch" && g.times.length >= 3) || groups.find((g) => g.times.length >= 3) || groups[0];

function showTip(html, x, y) {
  tip.replaceChildren(...html);
  tip.hidden = false;
  tip.style.left = `${Math.min(x + 12, innerWidth - tip.offsetWidth - 8)}px`;
  tip.style.top = `${y + 14}px`;
}

/* Every answer of one run, fastest first: where the curve crosses the two targets is the whole story of the latency. */
function drawChart() {
  const group = chosen();
  chartBox.replaceChildren();
  chartBox.removeAttribute("tabindex");
  if (!group || group.times.length < 3) {
    $("#h-time").textContent = "Время ответов";
    chartBox.append(el("p", "empty", "График появится, когда в журнале будет хотя бы три ответа, написанных моделью."));
    return;
  }
  const times = group.times;
  const n = times.length;
  const width = Math.max(chartBox.clientWidth, 280);
  const height = 260;
  const pad = { left: 46, right: 10, top: 14, bottom: 28 };
  const top = Math.max(15000, Math.ceil(times[n - 1] / 5000) * 5000);
  const x = (i) => pad.left + (i / (n - 1)) * (width - pad.left - pad.right);
  const y = (ms) => height - pad.bottom - (ms / top) * (height - pad.top - pad.bottom);
  const half = Math.floor((n - 1) / 2);
  const most = Math.min(Math.floor(n * 0.95), n - 1);

  $("#h-time").textContent = `Время ответов: ${groupName(group)}`;
  const plot = svg("svg", { viewBox: `0 0 ${width} ${height}`, height, role: "img",
    "aria-label": `${n} ответов от самого быстрого к самому медленному. Середина ${seconds(group.median_ms)}, 95 % ${seconds(group.p95_ms)}. Цели 5 и 12 секунд.` });
  [0, top].forEach((ms) => {
    plot.append(svg("line", { class: "grid", x1: pad.left, x2: width - pad.right, y1: y(ms), y2: y(ms) }));
    plot.append(svg("text", { class: "tick", x: pad.left - 8, y: y(ms) + 4, "text-anchor": "end" }, `${ms / 1000} с`));
  });
  [[HALF_MS, "цель для половины ответов"], [MOST_MS, "цель для 95 %"]].forEach(([ms, label]) => {
    plot.append(svg("line", { class: "target", x1: pad.left, x2: width - pad.right, y1: y(ms), y2: y(ms) }));
    plot.append(svg("text", { class: "tick", x: pad.left - 8, y: y(ms) + 4, "text-anchor": "end" }, `${ms / 1000} с`));
    plot.append(svg("text", { x: pad.left + 6, y: y(ms) - 5 }, label));
  });
  plot.append(svg("polyline", { class: "series", points: times.map((ms, i) => `${x(i).toFixed(1)},${y(ms).toFixed(1)}`).join(" ") }));
  [[half, `середина ${seconds(group.median_ms)}`, "end", -8, -8], [most, `95 %: ${seconds(group.p95_ms)}`, "end", -8, -8]].forEach(([i, label, anchor, dx, dy]) => {
    plot.append(svg("circle", { class: "point", cx: x(i), cy: y(times[i]), r: 5 }));
    plot.append(svg("text", { class: "named", x: x(i) + dx, y: y(times[i]) + dy, "text-anchor": anchor }, label));
  });
  plot.append(svg("text", { x: pad.left, y: height - 8 }, "самый быстрый"));
  plot.append(svg("text", { x: width - pad.right, y: height - 8, "text-anchor": "end" }, "самый медленный"));
  const cross = svg("line", { class: "cross", y1: pad.top, y2: height - pad.bottom, visibility: "hidden" });
  const dot = svg("circle", { class: "point", r: 5, visibility: "hidden" });
  plot.append(cross, dot);

  let current = half;
  const show = (i, cx, cy) => {
    current = i;
    [["x1", x(i)], ["x2", x(i)], ["visibility", "visible"]].forEach(([k, v]) => cross.setAttribute(k, v));
    [["cx", x(i)], ["cy", y(times[i])], ["visibility", "visible"]].forEach(([k, v]) => dot.setAttribute(k, v));
    showTip([el("strong", "", seconds(times[i])), ` ${i + 1}-й из ${n}`], cx, cy);
  };
  const hide = () => {
    tip.hidden = true;
    cross.setAttribute("visibility", "hidden");
    dot.setAttribute("visibility", "hidden");
  };
  plot.addEventListener("pointermove", (e) => {
    const box = plot.getBoundingClientRect();
    const i = Math.round(((e.clientX - box.left - pad.left) / (width - pad.left - pad.right)) * (n - 1));
    show(Math.min(Math.max(i, 0), n - 1), e.clientX, e.clientY);
  });
  plot.addEventListener("pointerleave", hide);
  chartBox.tabIndex = 0;
  chartBox.onblur = hide;
  chartBox.onkeydown = (e) => {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    e.preventDefault();
    const box = plot.getBoundingClientRect();
    const i = Math.min(Math.max(current + (e.key === "ArrowRight" ? 1 : -1), 0), n - 1);
    show(i, box.left + x(i), box.top + y(times[i]));
  };
  chartBox.append(plot);
}

function choose(group) {
  filters.elements.view.value = groupKey(group);
  filters.elements.source.value = group.source;
  filters.elements.run_id.value = group.run_id || "";
  syncUrl();
  renderStats();
  loadRuns(true);
}

function showAll() {
  ["view", "source", "run_id"].forEach((name) => { filters.elements[name].value = ""; });
  syncUrl();
  renderStats();
  loadRuns(true);
}

function renderStats() {
  const box = $("#stats");
  box.replaceChildren();
  drawChart();
  if (!groups.length) {
    box.append(el("p", "empty", "Ответов пока нет. Задайте вопрос на главной странице или запустите контрольный прогон."));
    return;
  }
  const wrap = el("div", "scroll");
  wrap.tabIndex = 0;
  const t = el("table");
  const heads = ["Откуда", "Вопросов", "Ответ", "Нет ответа", "Сбои", "Из кэша", "Верно", "Середина", "95 %", "Максимум", "Чтение", "Поиск", "Письмо", "Потрачено"];
  const head = el("thead");
  const hr = el("tr");
  heads.forEach((h, i) => { const th = el("th", i ? "num" : "", h); th.scope = "col"; hr.append(th); });
  head.append(hr);
  const body = el("tbody");
  const current = chosen();
  groups.forEach((g) => {
    const tr = el("tr");
    const name = el("td");
    const pick = el("button", "pick", groupName(g));
    pick.type = "button";
    pick.setAttribute("aria-pressed", String(g === current));
    pick.addEventListener("click", () => choose(g));
    name.append(pick);
    tr.append(name);
    [whole(g.questions), whole(g.answered), whole(g.no_answer), whole(g.errors), whole(g.cached), g.judged ? `${g.correct} из ${g.judged}` : "—",
      seconds(g.median_ms), seconds(g.p95_ms), seconds(g.max_ms), seconds(g.read_ms), seconds(g.search_ms), seconds(g.answer_ms), dollars(g.cost_usd)]
      .forEach((value) => tr.append(el("td", "num", value)));
    body.append(tr);
  });
  t.append(head, body);
  wrap.append(t);
  box.append(wrap);
}

function verdict(r) {
  const box = el("span", `verdict${r.ok === 0 ? " verdict--fail" : ""}`);
  if (r.ok === 1) box.innerHTML = ICON_OK;
  if (r.ok === 0) box.innerHTML = ICON_FAIL;
  box.append(r.ok === 0 ? "Ошибка" : STATUS[r.status] || r.status);
  return box;
}

function source(c) {
  const li = el("li", "source");
  li.append(el("span", "source__no", c.ref));
  const body = el("div");
  const link = el("a", "source__place");
  if (/^https:\/\/lex\.uz\//.test(c.url)) {
    link.href = c.url;
    link.target = "_blank";
    link.rel = "noopener";
  }
  const place = [c.article, c.part].filter(Boolean).join(", ");
  if (place) link.append(el("strong", "", place), " ");
  link.append(c.doc_title);
  body.append(link, el("blockquote", "source__quote", c.quote));
  li.append(body);
  return li;
}

function wrote(r) {
  return r.answer_ms === null && r.correct_ms === null ? null : (r.answer_ms || 0) + (r.correct_ms || 0);
}

function facts(r) {
  const dl = el("dl", "plan");
  const add = (name, value, figure) => { if (value) dl.append(el("dt", "", name), el("dd", figure ? "figure" : "", value)); };
  const plan = r.plan || {};
  const known = (r.read_ms || 0) + (r.search_ms || 0) + (r.answer_ms || 0) + (r.correct_ms || 0);
  add("Запрос к поиску", plan.query);
  add("Слова", (plan.terms || []).join(", "));
  add("Акты", (plan.acts || []).join(", "));
  add("Найдено", r.found ? whole(r.found) : "", true);
  add("Почему нет ответа", r.reason);
  if (!r.cached) {
    add("Чтение", r.read_ms ? seconds(r.read_ms) : "", true);
    add("Поиск", r.search_ms ? seconds(r.search_ms) : "", true);
    add("Письмо", r.answer_ms ? seconds(r.answer_ms) : "", true);
    add("Вторая попытка", r.correct_ms ? seconds(r.correct_ms) : "", true);
    add("Очередь и прочее", r.total_ms - known >= 50 ? seconds(r.total_ms - known) : "", true);
  }
  add("Модель", r.model);
  add("Токены", r.tokens_in ? `${whole(r.tokens_in)} + ${whole(r.tokens_out)}` : "", true);
  add("Цена", r.cost_usd ? dollars(r.cost_usd) : "", true);
  add("Категория", r.category);
  return dl;
}

function opened(r) {
  const pair = el("div", "pair");
  const left = el("div");
  left.append(el("h3", "pair__head", "Ответ"), el("p", "detail__text", r.answer || r.error || "Текста ответа нет."));
  if (r.citations.length) {
    const list = el("ol", "detail__sources");
    list.append(...r.citations.map(source));
    left.append(list);
  }
  const right = el("div");
  right.append(el("h3", "pair__head", "Эталон"), el("p", "detail__text", r.expected || "Эталона нет: вопрос задан не в контрольном прогоне."));
  if (r.ok === 1) right.append(el("p", "pair__verdict", r.why ? `Совпало, но ${r.why}` : "Совпало"));
  if (r.ok === 0) right.append(el("p", "pair__verdict", `Не совпало: ${r.why}`));
  right.append(facts(r));
  pair.append(left, right);
  return pair;
}

async function openRow(tr, r, button) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains("detail")) {
    next.remove();
    button.setAttribute("aria-expanded", "false");
    return;
  }
  button.setAttribute("aria-expanded", "true");
  const row = el("tr", "detail");
  const cell = el("td");
  cell.colSpan = 8;
  const inner = el("div", "detail__in");
  inner.append(el("div", "skel skel--row"));
  cell.append(inner);
  row.append(cell);
  tr.after(row);
  try {
    const d = await get(`api/logs/runs/${r.id}`);
    inner.replaceChildren(el("p", "detail__q", d.question), opened(d));
  } catch (e) {
    inner.replaceChildren(el("p", "bad", "Не удалось загрузить ответ. Нажмите «Обновить»."));
  }
}

function clip(text, size) {
  return text && text.length > size ? `${text.slice(0, size - 1)}…` : text;
}

function addRow(r) {
  const tr = el("tr");
  const q = el("button", "runs__q", r.question);
  q.type = "button";
  q.title = r.question;
  q.setAttribute("aria-expanded", "false");
  q.addEventListener("click", () => openRow(tr, r, q));
  const asked = el("td");
  asked.append(q);
  if (r.answer) asked.append(el("p", "runs__line", `Ответ: ${clip(r.answer, 130)}`));
  if (r.expected) asked.append(el("p", "runs__line", `Эталон: ${clip(r.expected, 130)}`));
  const outcome = el("td");
  outcome.append(verdict(r));
  const part = (ms) => el("td", "num", r.cached ? "" : seconds(ms));
  const total = el("td", `num${!r.cached && r.total_ms > MOST_MS ? " is-slow" : ""}`, r.cached ? "кэш" : seconds(r.total_ms));
  tr.append(asked, outcome, part(r.read_ms), part(r.search_ms), part(wrote(r)), total, el("td", "runs__from", SOURCE[r.source] || r.source), el("td", "num", when(r.started_at)));
  rowsBox.append(tr);
}

function query() {
  const data = new URLSearchParams();
  new FormData(filters).forEach((v, k) => { if (v) data.set(k, v); });
  return data;
}

function syncUrl() {
  const data = query();
  history.replaceState(null, "", data.toString() ? `?${data}` : location.pathname);
}

async function loadRuns(reset) {
  if (reset) {
    offset = 0;
    rowsBox.replaceChildren();
    state.textContent = "Загружаю ответы";
  }
  try {
    const data = query();
    const filtered = [...data.keys()].some((k) => k !== "view");
    const run = data.get("run_id");
    $("#all").hidden = !filtered;
    data.delete("view");
    data.set("limit", PAGE);
    data.set("offset", offset);
    const res = await get(`api/logs/runs?${data}`);
    res.rows.forEach(addRow);
    offset += res.rows.length;
    const slow = rowsBox.querySelector(".is-slow") ? " Выделено всё, что дольше 12 с." : "";
    const only = run ? `Прогон ${run}. ` : "";
    state.textContent = res.total ? `${only}Показано ${whole(offset)} из ${whole(res.total)}.${slow}` : filtered ? "По этим условиям ответов нет. Снимите часть фильтров." : "Ответов пока нет.";
    more.hidden = offset >= res.total;
  } catch (e) {
    state.textContent = "Не удалось загрузить журнал. Проверьте соединение и нажмите «Обновить».";
    more.hidden = true;
  }
}

async function loadTop() {
  try {
    groups = (await get("api/logs/summary")).groups;
    renderStats();
    $("#updated").textContent = `Обновлено ${new Date().toLocaleTimeString("ru-RU", { timeZone: "Asia/Tashkent" })}`;
  } catch (e) {
    $("#stats").replaceChildren(el("p", "bad", "Не удалось загрузить итоги. Проверьте соединение и нажмите «Обновить»."));
    chartBox.replaceChildren(el("p", "bad", "Не удалось загрузить график."));
  }
}

function refresh() {
  loadTop();
  loadRuns(true);
}

["source", "outcome", "verdict", "q", "view", "run_id"].forEach((k) => { if (params.get(k) && filters.elements[k]) filters.elements[k].value = params.get(k); });
let typing;
filters.addEventListener("input", (e) => {
  if (e.target.name === "source") filters.elements.run_id.value = "";   /* another source leaves the chosen run behind */
  clearTimeout(typing);
  typing = setTimeout(() => {
    syncUrl();
    loadRuns(true);
  }, 250);
});
filters.addEventListener("submit", (e) => e.preventDefault());
$("#refresh").addEventListener("click", refresh);
more.addEventListener("click", () => loadRuns(false));
$("#all").addEventListener("click", showAll);
let resizing;
new ResizeObserver(() => {
  clearTimeout(resizing);
  resizing = setTimeout(() => { if (groups.length) drawChart(); }, 120);
}).observe(chartBox);
refresh();
