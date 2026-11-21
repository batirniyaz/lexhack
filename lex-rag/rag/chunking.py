"""Paragraphs into the pieces that get searched and cited.

The unit is what a lawyer would cite: a part of an article, or a numbered point in acts without articles. That keeps
`article` and `part` in every answer exact. A piece grows only inside one such unit, and only long ones are cut.
"""
import re

MAX_CHARS = 1400    # a longer unit is cut; about 400 words, and more than the embedding model reads
TINY = 200          # neighbouring points shorter than this travel together, otherwise the index fills with one-liners
SENTENCE = re.compile(r"(?<=[.;:])\s+|\n+")

# The form of an act is the last word of its requisites before the date: "Vazirlar Mahkamasining qarori, 17.12.2019 ..."
FORMS = {
    "qonuni": "qonun", "farmoni": "farmon", "qarori": "qaror", "qaror": "qaror", "(resheniye)": "qaror", "farmoyishi": "qaror", "buyrugʻi": "buyruq",
    "nizomi": "nizom", "yoʻriqnomasi": "nizom", "tartibi": "nizom", "qoidalari": "nizom", "meʼyorlari": "nizom", "normativlari": "nizom", "standarti": "nizom",
    "bitim": "shartnoma", "konvensiya": "shartnoma", "konvensiyasi": "shartnoma", "shartnoma": "shartnoma", "bayonnoma": "shartnoma", "protokol": "shartnoma",
    "memorandum": "shartnoma", "memorandumi": "shartnoma",
}
REQUISITES = re.compile(r"(.*?),\s*\d\d\.\d\d\.\d{4}")
AMENDING = re.compile(r"o.zgartirish|qo.shimcha|o.z kuchini yo.qotgan deb|kuchini yo.qotgan deb|изменени|дополнени", re.I)
# Lower is stronger. Written from how the Uzbek system ranks acts; a question that names no act should land on the highest one.
RANK = {"konstitutsiya": 0, "kodeks": 1, "qonun": 2, "farmon": 3, "qaror": 4, "nizom": 5, "buyruq": 5, "shartnoma": 5, "boshqa": 6}


def doc_type(title, meta):
    """What kind of act it is. A code or the constitution says so in its title, everything else in its requisites."""
    head = title or ""
    if not AMENDING.search(head):
        if re.search(r"kodeksi?\s*$|^.{0,60}kodeksi\b(?!\w)", head, re.I):
            return "kodeks"
        if re.search(r"respublikasi(ning)?\s+konstitutsiyasi\s*$", head, re.I):
            return "konstitutsiya"
    found = REQUISITES.match(meta or "")
    words = (found.group(1) if found else meta or "").lower().split()
    return FORMS.get(words[-1], "boshqa") if words else "boshqa"


def rank_of(kind, meta, section):
    """Lower is stronger. A resolution of the President stands with his decrees, and local acts stand below everything of their kind."""
    value = RANK[kind]
    if kind == "qaror" and re.search(r"prezident", meta or "", re.I):
        value = RANK["farmon"]
    return value + (3 if section == "loc" else 0)


def number_of(doc_id):
    return str(doc_id).lstrip("-")


def _unit(element):
    """Which citation a paragraph belongs to."""
    if element["article"]:
        return element["appendix"], "art", element["article"], element["part"] or "1-qism"
    if element["band"]:
        return element["appendix"], "band", element["band"].split(".")[0], None
    return element["appendix"], "free", None, None


def _cut(text):
    """Long text into pieces at sentence or row ends."""
    pieces, current = [], ""
    for sentence in SENTENCE.split(text):
        while len(sentence) > MAX_CHARS:   # one huge table cell
            head, sentence = sentence[:MAX_CHARS], sentence[MAX_CHARS:]
            if current:
                pieces.append(current)
                current = ""
            pieces.append(head)
        if current and len(current) + len(sentence) + 1 > MAX_CHARS:
            pieces.append(current)
            current = ""
        current = f"{current} {sentence}" if current else sentence
    if current:
        pieces.append(current)
    return pieces


def _chunk_id(number, unit, element):
    appendix, kind, label, part = unit
    place = f"#ilova-{appendix.split('-')[0]}" if appendix else ""
    if kind == "art":
        return f"lex:{number}{place}#art-{label.split('-')[0]}#p{part.split('-')[0]}"
    if kind == "band":
        return f"lex:{number}{place}#band-{label}"
    return f"lex:{number}{place}#el-{element['element_id'].lstrip('-')}"


def chunks_of(doc_id, elements):
    """Yields one record per piece, in reading order. `elements` is one document, sorted by seq."""
    number = number_of(doc_id)
    groups = []
    for element in elements:
        if not element["is_body"] or element["kind"] == "FOOTNOTE":
            continue
        unit = _unit(element)
        last = groups[-1] if groups else None
        joins = last and last["unit"] == unit and unit[1] != "free"
        tiny = last and unit[1] != "art" and last["unit"][1] != "art" and last["unit"][0] == unit[0] and len(last["text"]) + len(element["text"]) < TINY
        if joins or tiny:
            last["text"] += "\n" + element["text"]
            last["elements"].append(element["element_id"])
        else:
            groups.append({"unit": unit, "first": element, "text": element["text"], "elements": [element["element_id"]]})

    seen = {}
    for group in groups:
        unit, first = group["unit"], group["first"]
        base = _chunk_id(number, unit, first)
        pieces = _cut(group["text"]) if len(group["text"]) > MAX_CHARS else [group["text"]]
        for n, piece in enumerate(pieces, 1):
            chunk_id = base if n == 1 else f"{base}#c{n}"
            seen[chunk_id] = seen.get(chunk_id, 0) + 1
            if seen[chunk_id] > 1:   # an amending law can repeat a number
                chunk_id = f"{chunk_id}#k{seen[chunk_id]}"
            yield {
                "chunk_id": chunk_id, "doc_id": str(doc_id), "seq": first["seq"], "piece": n, "text": piece,
                "article": unit[2] if unit[1] == "art" else (f"{unit[2]}-band" if unit[1] == "band" else None),
                "part": unit[3], "article_title": first["article_title"], "appendix": unit[0], "headers": first["headers"],
                "element_ids": ",".join(group["elements"]), "is_table": first["kind"].startswith(("TABLE", "BY_DEFAULT")),
            }
