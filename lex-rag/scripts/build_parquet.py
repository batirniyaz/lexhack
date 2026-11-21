"""Raw pages into data/parquet: acts, elements and links. Safe to run again: it only reads the raw files."""
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from lexuz import parse, store  # noqa: E402
from lexuz.translit import to_latin  # noqa: E402

OUT = store.DATA / "parquet"
STATUS = {"y": "amalda", "r": "kuchini yo'qotgan", "n": "amalda emas"}   # the icon in the search list; on cards "n" reads "Не действующий"
BATCH = 500   # documents per row group: one long code can hold thousands of paragraphs

TEXT = pa.string()
ACTS = pa.schema([
    ("doc_id", TEXT), ("section", TEXT), ("year", pa.int32()), ("list_title", TEXT), ("list_meta", TEXT), ("list_state", TEXT),
    ("title", TEXT), ("issuer_line", TEXT), ("number", TEXT), ("adopted", TEXT), ("in_force_from", TEXT), ("edition", TEXT),
    ("editions", pa.list_(TEXT)), ("ru_id", TEXT), ("en_id", TEXT), ("other_uz_id", TEXT), ("okoz", pa.list_(TEXT)),
    ("script", TEXT), ("text_chars", pa.int64()), ("pdf_only", pa.bool_()), ("ru_only", pa.bool_()), ("pdf_file", TEXT), ("warnings", TEXT),
    ("doc_status", TEXT),
    ("category", TEXT), ("form", TEXT), ("status", TEXT), ("term", TEXT), ("ended", TEXT), ("end_reason", TEXT), ("language", TEXT),
    ("raw_bytes", pa.int64()), ("text_lang", TEXT), ("text_page", TEXT),
])
ELEMENTS = pa.schema([
    ("element_id", TEXT), ("doc_id", TEXT), ("seq", pa.int32()), ("kind", TEXT), ("is_body", pa.bool_()), ("is_note", pa.bool_()),
    ("text", TEXT), ("headers", TEXT), ("appendix", TEXT), ("article", TEXT), ("article_title", TEXT), ("part", TEXT),
    ("band", TEXT), ("okoz", pa.list_(TEXT)),
])
LINKS = pa.schema([("from_element", TEXT), ("doc_id", TEXT), ("to_doc", TEXT), ("to_element", TEXT)])


def read_doc(doc_id):
    """The act and its text. The text may live on another page than the Latin one: then the elements come from there."""
    twin = doc_id[1:] if doc_id.startswith("-") else f"-{doc_id}"
    if store.raw_path("twins", doc_id).exists():   # no Latin text on the site yet: the same act in Cyrillic, spelled in Latin here
        act, elements, links = parse.parse_doc(to_latin(store.load_raw("twins", doc_id)), doc_id)
        act.update(text_lang="uz", text_page=twin, pdf_only=False, ru_only=False, ru_id=None, en_id=None, other_uz_id=twin)
        return act, elements, links
    act, elements, links = parse.parse_doc(store.load_raw("docs", doc_id), doc_id)
    act.update(text_lang="uz", text_page=doc_id)
    if act["ru_only"] and store.raw_path("ru", doc_id).exists():
        russian, ru_elements, ru_links = parse.parse_doc(store.load_raw("ru", doc_id), doc_id)
        if russian["text_chars"] > act["text_chars"]:
            act.update(text_lang="ru", text_page=act["ru_id"], text_chars=russian["text_chars"], script=russian["script"])
            elements, links = ru_elements, ru_links
    return act, elements, links


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    con = store.connect()
    rows = con.execute("SELECT doc_id, section, year, title, meta, state, card_status, doc_status FROM docs").fetchall()
    rows = [r for r in rows if r[7] == "ok" or store.raw_path("twins", r[0]).exists()]
    writers = {name: pq.ParquetWriter(OUT / f"{name}.parquet", schema, compression="zstd")
               for name, schema in (("acts", ACTS), ("elements", ELEMENTS), ("links", LINKS))}
    acts, elements, links, failed = [], [], [], []

    def flush():
        writers["acts"].write_table(pa.Table.from_pylist(acts, schema=ACTS))
        writers["elements"].write_table(pa.Table.from_pylist(elements, schema=ELEMENTS))
        writers["links"].write_table(pa.Table.from_pylist(links, schema=LINKS))
        acts.clear(), elements.clear(), links.clear()

    for n, (doc_id, section, year, title, meta, state, card_status, _) in enumerate(rows, 1):
        try:
            act, els, refs = read_doc(doc_id)
            card = parse.parse_card(store.load_raw("cards", doc_id.lstrip("-"))) if card_status == "ok" else {}
        except Exception as e:   # one broken page must be visible, not end the build
            failed.append((doc_id, f"{type(e).__name__}: {e}"))
            continue
        card_start = card.pop("in_force_from", None)
        acts.append({**act, **card, "section": section, "year": year, "list_title": title, "list_meta": meta, "list_state": state,
                     "doc_status": STATUS.get(state), "in_force_from": act["in_force_from"] or card_start, "raw_bytes": act["text_chars"]})
        elements.extend(els)
        links.extend(refs)
        if n % BATCH == 0:
            flush()
            print(n, "of", len(rows), flush=True)
    flush()
    for writer in writers.values():
        writer.close()
    print("documents", len(rows), "failed", len(failed), failed[:5])
    for name in writers:
        print(name, round((OUT / f"{name}.parquet").stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
