"""lex.uz pages into plain records. Nothing here touches the network.

A document page keeps every paragraph in `<div name=ID id=ID>` inside a block whose class says what the
paragraph is. The ID is permanent and is what citations point at. In a Latin page the IDs are negative.
"""
import re

from selectolax.lexbor import LexborHTMLParser as HTMLParser

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# Requisites and editorial notes. Every other kind counts as the text of the law, so that a block type
# nobody has seen yet ends up in the search instead of silently disappearing from it.
META = {"ACT_FORM", "ACT_TITLE", "ACT_ESSENTIAL_ELEMENTS", "ACT_ESSENTIAL_ELEMENTS_NUM", "ACCEPTING_BODY", "SIGNATURE",
        "SIGNATURE_WITH_BOLD", "SIGNATURE_STAMP_TEXT", "signCont", "APPL_BANNER_LANDSCAPE_TITLE", "APPL_BANNER_PORTRAIT_TITLE",
        "PUBLICATION_ORIGIN", "DEPARTMENTAL", "OFFICIAL_SOUR_TEXT", "GRIF_PARLAMENT", "UNOFFIAL", "NEW_EDITION", "EXTRACT"}
NOTES = {"COMMENT", "CHANGES_ORIGINS", "COMMENT_FOR_WARNING"}

ARTICLE = re.compile(r"^\s*(?:(\d[\d⁰¹²³⁴⁵⁶⁷⁸⁹.]*)\s*[-–—]?\s*modda\b|(?:modda|статья)\s+(\d[\d⁰¹²³⁴⁵⁶⁷⁸⁹]*)\b)\.?\s*(.*)", re.I | re.S)
# the dot tells it from "5-modda talablari"
ARTICLE_IN_TEXT = re.compile(r"^\s*(?:(\d[\d⁰¹²³⁴⁵⁶⁷⁸⁹.]*)\s*[-–—]\s*modda|статья\s+(\d[\d⁰¹²³⁴⁵⁶⁷⁸⁹]*))\.\s+\S", re.I)
HEADING_KINDS = {"CLAUSE_DEFAULT", "TEXT_HEADER_DEFAULT", "TEXT_HEADER_AFTER_SRC", "TEXT_BOLD_CENTER", "TEXT_CENTER", "TEXT_BOLD"}   # treaties use the last four
BAND = re.compile(r"^\s*(\d{1,3}(?:\.\d{1,3})*)[.)]\s+\S")
APPENDIX = re.compile(r"(\d+)\s*[-–—]?\s*ilova|приложение\s*(?:№|N)?\s*(\d+)", re.I)
HEADER_LEVELS = (
    (0, re.compile(r"^(umumiy|maxsus)\s+qism\b", re.I)),
    (1, re.compile(r"^([IVXLC]+|\d+)\s*[-–—]?\s*bo.lim\b|^раздел\s", re.I)),
    (2, re.compile(r"^([IVXLC]+|\d+)\s*[-–—]?\s*bob\b|^глава\s", re.I)),
    (3, re.compile(r"^([IVXLC]+|\d+)\s*[-–—]?\s*(paragraf|§)|^§", re.I)),
)
OTHER_HEADER_LEVEL = 2
PDF_ONLY = re.compile(r"matni\s+pdf", re.I)
RUSSIAN_ONLY = re.compile(r"matni\s+rus\s+tilida", re.I)
NEARLY_EMPTY = 3000   # characters: a real body next to such a notice is not "only in PDF"
OKOZ_CODE = re.compile(r"\b\d\d\.\d\d\.\d\d\.\d\d\b")
LINK = re.compile(r"/docs/(-?\d+)(?:\?[^#]*)?(?:#(-?\d+))?")
SPACES = re.compile(r"[ \t\xa0\r]+")


def _clean(text):
    lines = [SPACES.sub(" ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def _prepare(html):
    """Keeps what plain text would lose: 13<sup>1</sup>-modda must not read as 131-modda, and table cells must not merge."""
    html = re.sub(r"<sup[^>]*>\s*(\d+)\s*</sup>", lambda m: m.group(1).translate(SUPERSCRIPT), html, flags=re.I)
    html = re.sub(r"</t[dh]>", " | </td>", html, flags=re.I)
    return re.sub(r"</tr>|<br\s*/?>", "\n", html, flags=re.I)


def _paragraphs(html):
    """Yields (class, element id, text, links) in reading order."""
    start = html.rfind("<div", 0, html.find('id="divCont"'))
    tree = HTMLParser(_prepare(html[max(start, 0):]))
    for node in tree.css("div[name][id]"):
        ident = node.attributes.get("id")
        if ident != node.attributes.get("name") or not re.fullmatch(r"(edi)?-?\d+", ident or ""):
            continue
        block = node.parent
        classes = (block.attributes.get("class") or "").split() if block else []
        links = [(m.group(1), m.group(2)) for a in node.css("a[href]") for m in LINK.finditer(a.attributes["href"])]
        yield (classes[0] if classes else "UNMARKED"), ident, _clean(node.text(separator="", strip=False)), links


def _script(text):
    sample = text[:20000]
    cyrillic = len(re.findall("[а-яёўқғҳА-ЯЁЎҚҒҲ]", sample))
    latin = len(re.findall("[a-zA-Z]", sample))
    return "cyrl" if cyrillic > latin else "latn"


class Position:
    """Where the reader is in the document while walking it from top to bottom."""

    def __init__(self):
        self.headers = {}
        self.appendix = None
        self.article = None
        self.article_title = None
        self.part = 0
        self.band = None
        self.open_list = False   # the previous paragraph ended with ":" or ";", so this one continues the same part

    def header(self, text):
        level = next((lvl for lvl, rx in HEADER_LEVELS if rx.search(text)), OTHER_HEADER_LEVEL)
        self.headers = {k: v for k, v in self.headers.items() if k < level}
        self.headers[level] = " ".join(text.split())   # "X BOʻLIM." and its name stand on two lines
        self.article = self.article_title = self.band = None
        self.part, self.open_list = 0, False

    def enter_appendix(self, text):
        found = APPENDIX.search(text)
        self.appendix = f"{found.group(1) or found.group(2)}-ilova" if found else "ilova"
        self.headers, self.article, self.article_title, self.band = {}, None, None, None
        self.part, self.open_list = 0, False

    def enter_article(self, number, title):
        self.article, self.article_title = f"{number.rstrip('.')}-modda", title.strip() or None
        self.band, self.part, self.open_list = None, 0, False

    def paragraph(self, text, continues=False):
        if continues:   # a table belongs to the part or band above it
            return
        if self.article:
            starts_part = not self.open_list and not re.match(r"[a-zа-я0-9]{1,3}\)|[—–-]\s", text)
            self.part += 1 if starts_part or self.part == 0 else 0
        else:
            found = BAND.match(text)
            if found:
                self.band = found.group(1)
        self.open_list = text.rstrip().endswith((":", ";"))


def parse_doc(html, doc_id):
    """Returns (act, elements, links). Elements keep notes too: they are flagged, not thrown away."""
    head = html[:html.find('id="divCont"')] if 'id="divCont"' in html else html
    tree = HTMLParser(head)
    label = tree.css_first(".docHeader__item-label")
    title_tag = tree.css_first("title")
    raw_title = re.sub(r"\s+", " ", title_tag.text() if title_tag else "").strip()
    named = re.match(r"^(?:(?P<number>.*?)[-\s]*(?:сон|son)\s+)?(?P<date>\d\d\.\d\d\.\d{4})\.?\s*(?P<name>.*)$", raw_title)
    others = {}
    for target, title in re.findall(r"""openUrl\('/\w+/docs/(-?\d+)'\)"\s+title="([^"]+)\"""", head):
        key = "ru_id" if "рус" in title.lower() else "en_id" if "english" in title.lower() else "other_uz_id"
        others[key] = target
    selected = re.search(r'lx_date_selected[^>]*>\s*(\d\d\.\d\d\.\d{4})', head)
    in_force = re.search(r"Kuchga kirish sanasi.*?(\d\d\.\d\d\.\d{4})", head, re.S)

    position, elements, links, okoz_by_element = Position(), [], [], {}
    for ident, code_block in re.findall(r'id="onLBC(-?\d+)">(.*?)</div>\s*</div>\s*</div>', html, re.S):
        okoz_by_element.setdefault(ident, []).extend(OKOZ_CODE.findall(code_block))

    for order, (kind, ident, text, targets) in enumerate(_paragraphs(html)):
        if not text:
            continue
        is_body = kind not in META and kind not in NOTES
        heading = ARTICLE.match(text) if kind in HEADING_KINDS else None
        inline = ARTICLE_IN_TEXT.match(text) if kind == "ACT_TEXT" else None
        if kind == "ACT_TITLE_APPL" or kind.startswith("APPL_BANNER"):
            if position.appendix is None or APPENDIX.search(text):
                position.enter_appendix(text)
        elif heading:
            position.enter_article(heading.group(1) or heading.group(2), heading.group(3))
        elif kind == "TEXT_HEADER_DEFAULT":
            position.header(text)
        elif inline:   # amending laws write the article number and its text in one paragraph
            position.enter_article(inline.group(1) or inline.group(2), "")
            position.paragraph(text)
        elif is_body and kind != "FOOTNOTE":
            position.paragraph(text, continues=kind.startswith("TABLE"))
        element_id = ident[3:] if ident.startswith("edi") else ident
        elements.append({
            "element_id": element_id, "doc_id": str(doc_id), "seq": order, "kind": kind,
            "is_body": is_body, "is_note": kind in NOTES, "text": text,
            "headers": " / ".join(position.headers[k] for k in sorted(position.headers)) or None,
            "appendix": position.appendix, "article": position.article, "article_title": position.article_title,
            "part": f"{position.part}-qism" if position.article and position.part else None,
            "band": position.band, "okoz": sorted(set(okoz_by_element.get(element_id, []))),
        })
        links += [{"from_element": element_id, "doc_id": str(doc_id), "to_doc": doc, "to_element": target}
                  for doc, target in targets]

    body = [e["text"] for e in elements if e["is_body"]]
    warnings = " ".join(e["text"] for e in elements if e["is_note"] and (PDF_ONLY.search(e["text"]) or RUSSIAN_ONLY.search(e["text"])))
    pdf = re.search(r'/uz/files/(\d+)\.zip', html)
    text_size = sum(map(len, body))
    act = {
        "doc_id": str(doc_id), "title": named.group("name") if named else raw_title,
        "issuer_line": label.text(strip=True) if label else None,
        "number": (named.group("number") or "").strip() or None if named else None,
        "adopted": named.group("date") if named else None,
        "in_force_from": in_force.group(1) if in_force else None, "edition": selected.group(1) if selected else None,
        "editions": sorted(set(re.findall(r"ONDATE=(\d\d\.\d\d\.\d{4})'\)", head))),
        "ru_id": others.get("ru_id"), "en_id": others.get("en_id"), "other_uz_id": others.get("other_uz_id"),
        "okoz": sorted(set(okoz_by_element.get(str(doc_id), []))),
        "script": _script(" ".join(body)), "text_chars": text_size,
        "pdf_only": bool(PDF_ONLY.search(warnings + " " + " ".join(body[:30]))) and text_size < NEARLY_EMPTY,
        "ru_only": bool(RUSSIAN_ONLY.search(warnings)) and text_size < NEARLY_EMPTY,
        "pdf_file": pdf.group(1) if pdf else None, "warnings": warnings or None,
    }
    return act, elements, links


def parse_card(html):
    """The legal analysis card. Labels are in Russian whatever the page language is."""
    tree = HTMLParser(html)
    fields = {}
    for label in tree.css("td.lbl"):
        cell = label.next
        while cell is not None and cell.tag != "td":
            cell = cell.next
        if cell is not None:
            fields[label.text(strip=True)] = cell.text(strip=True) or None
    return {
        "category": fields.get("Вид акта"), "form": fields.get("Форма акта"), "status": fields.get("Статус акта"),
        "in_force_from": fields.get("Дата вступления в силу"), "term": fields.get("Срок действия"),
        "ended": fields.get("Дата прекращения действия"), "end_reason": fields.get("Причины прекращения действия"),
        "language": fields.get("Язык акта"),
    }
