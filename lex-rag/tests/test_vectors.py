"""Packing vectors and searching them, on a handful of made-up ones: this path must work before hours go into it."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag import vectors  # noqa: E402


class FakeEncoder:
    def __init__(self, query):
        self.query = query

    def encode(self, texts, prefix):
        assert prefix == "query: "
        return self.query[None, :]


@pytest.fixture
def packed(tmp_path, monkeypatch):
    monkeypatch.setattr(vectors, "VECTORS", tmp_path / "v.f16")
    monkeypatch.setattr(vectors, "IDS", tmp_path / "i.i32")
    monkeypatch.setattr(vectors, "FAISS", tmp_path / "v.faiss")
    rng = np.random.default_rng(1)
    matrix = rng.normal(size=(400, vectors.DIMENSIONS)).astype(np.float32)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)
    ids = np.arange(1000, 1400, dtype=np.int32)
    matrix.astype(np.float16).tofile(vectors.VECTORS)
    ids.tofile(vectors.IDS)
    assert vectors.build_faiss() == 400
    return matrix


def test_nearest_comes_first(packed):
    found = vectors.Vectors(encoder=FakeEncoder(packed[7])).search("savol", limit=3)
    assert found[0][0] == 1007
    assert found[0][1] > found[1][1]


def test_span_stays_inside_one_act(packed):
    found = vectors.Vectors(encoder=FakeEncoder(packed[7])).search("savol", limit=5, span=(1100, 1110))
    assert found and all(1100 <= i <= 1110 for i, _ in found)
    assert 1007 not in [i for i, _ in found]


def test_same_query_same_answer(packed):
    meaning = vectors.Vectors(encoder=FakeEncoder(packed[3]))
    assert meaning.search("savol") == meaning.search("savol")


def test_passage_says_where_the_text_stands():
    text = vectors.passage("Soliq kodeksi", "MAXSUS QISM / X BOʻLIM. QOʻSHILGAN QIYMAT SOLIGʻI / 35-bob. Soliq stavkalari", "Soliq stavkalari", "12 foiz.")
    assert "QOʻSHILGAN QIYMAT SOLIGʻI" in text and "Soliq kodeksi" in text and text.endswith("12 foiz.")
    assert "MAXSUS QISM" not in text


def test_passage_without_names():
    assert vectors.passage("Akt", None, None, "Matn.") == "Akt. Matn."
