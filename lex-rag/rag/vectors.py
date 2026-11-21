"""Meaning search: ONNX on the CPU, no GPU and no service to keep running.

Vectors are built in priority order and appended to two plain files, so a stopped run continues and a half-finished index
already works for the acts that matter most. `build_faiss` packs them into the index the API reads.
"""
import functools
import os

import numpy as np

from lexuz import store

OUT = store.DATA / "index"
MODELS_DIR = store.DATA / "models"
MODEL = ("intfloat/multilingual-e5-small", "onnx/model_qint8_avx512_vnni.onnx")
DIMENSIONS = 384
MAX_TOKENS = 192
VECTORS, IDS, FAISS = OUT / "vectors.f16", OUT / "vector_ids.i32", OUT / "vectors.faiss"


class Encoder:
    def __init__(self, model=MODEL, threads=8):
        import onnxruntime
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer

        repo, file = model
        self.name = repo
        self.tokenizer = Tokenizer.from_file(hf_hub_download(repo, "tokenizer.json", cache_dir=MODELS_DIR))
        self.tokenizer.enable_truncation(max_length=MAX_TOKENS)
        self.tokenizer.enable_padding()
        options = onnxruntime.SessionOptions()
        options.intra_op_num_threads = threads
        self.session = onnxruntime.InferenceSession(hf_hub_download(repo, file, cache_dir=MODELS_DIR), options, providers=["CPUExecutionProvider"])
        self.inputs = {i.name for i in self.session.get_inputs()}

    def encode(self, texts, prefix):
        """e5 was trained with these prefixes, and works worse without them. Vectors come out with length 1, ready for dot products."""
        encoded = self.tokenizer.encode_batch([prefix + t for t in texts])
        ids = np.array([e.ids for e in encoded], dtype=np.int64)
        mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)
        feed = {"input_ids": ids, "attention_mask": mask}
        if "token_type_ids" in self.inputs:
            feed["token_type_ids"] = np.zeros_like(ids)
        hidden = self.session.run(None, feed)[0]
        weights = mask[..., None].astype(np.float32)
        pooled = (hidden * weights).sum(1) / np.maximum(weights.sum(1), 1e-9)
        return pooled / np.maximum(np.linalg.norm(pooled, axis=1, keepdims=True), 1e-9)


def passage(title, headers, article_title, text):
    """What gets embedded: the names around a paragraph say what it does not. "Soliq stavkalari" means VAT only through its section."""
    section = " ".join((headers or "").split(" / ")[-2:])[:120]
    head = ". ".join(filter(None, (title[:90], section, article_title)))
    return f"{head}. {text}"


def build_faiss():
    """Exact search over 8-bit vectors: 1 million of them take about 400 MB, and the same query always gives the same answer."""
    import faiss

    ids = np.fromfile(IDS, dtype=np.int32).astype(np.int64)
    matrix = np.memmap(VECTORS, dtype=np.float16, mode="r", shape=(len(ids), DIMENSIONS))
    inner = faiss.IndexScalarQuantizer(DIMENSIONS, faiss.ScalarQuantizer.QT_8bit, faiss.METRIC_INNER_PRODUCT)
    index = faiss.IndexIDMap2(inner)
    sample = np.asarray(matrix[:: max(1, len(ids) // 100000)], dtype=np.float32)
    inner.train(sample)
    for start in range(0, len(ids), 50000):
        index.add_with_ids(np.asarray(matrix[start:start + 50000], dtype=np.float32), ids[start:start + 50000])
    temp = FAISS.with_suffix(".building")
    faiss.write_index(index, str(temp))
    temp.replace(FAISS)
    return len(ids)


class Vectors:
    def __init__(self, encoder=None):
        import faiss

        self.faiss = faiss
        self.index = faiss.read_index(str(FAISS))
        self.encoder = encoder or Encoder(threads=min(4, os.cpu_count() or 1))
        self.embedded = functools.lru_cache(maxsize=64)(lambda text: self.encoder.encode([text], "query: ").astype(np.float32))   # one question searches several acts

    def search(self, question, limit=150, span=None):
        """Chunk ids with similarity, best first. A span keeps it inside one act."""
        query = self.embedded(question)
        params = None
        if span:
            params = self.faiss.SearchParameters(sel=self.faiss.IDSelectorRange(span[0], span[1] + 1))
        scores, ids = self.index.search(query, limit, params=params)
        return [(int(i), float(s)) for i, s in zip(ids[0], scores[0]) if i >= 0]
