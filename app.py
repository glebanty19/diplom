from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from functools import lru_cache

from flask import Flask, jsonify, render_template_string, request
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

try:
    from flask_cors import CORS
except ImportError:
    CORS = None

try:
    from rapidfuzz import process as fuzz_process
except ImportError:
    fuzz_process = None

from dataset import apple_products
from ml_ranker import SyntheticProductRanker


TYPO_DICT = {
    "еелфон": "телефон",
    "елефон": "телефон",
    "теефон": "телефон",
    "тлефон": "телефон",
    "телефн": "телефон",
    "телифон": "телефон",
    "телефооон": "телефон",
    "смарфтон": "смартфон",
    "смратфон": "смартфон",
    "айфн": "айфон",
    "айфоон": "айфон",
    "камра": "камера",
    "камерва": "камера",
    "ноутбк": "ноутбук",
    "ноутбукк": "ноутбук",
    "макбукк": "макбук",
    "планшетт": "планшет",
    "батарайка": "батарея",
    "ігрии": "ігри",
    "процесорр": "процесор",
}

SAFE_VOCAB = [
    "iphone",
    "айфон",
    "телефон",
    "смартфон",
    "macbook",
    "макбук",
    "ноутбук",
    "ipad",
    "айпад",
    "планшет",
    "камера",
    "батарея",
    "ігри",
    "навчання",
    "потужний",
    "бюджетний",
]

CATEGORY_ALIASES = {
    "iphone": "iPhone",
    "phone": "iPhone",
    "айфон": "iPhone",
    "телефон": "iPhone",
    "смартфон": "iPhone",
    "macbook": "MacBook",
    "макбук": "MacBook",
    "ноутбук": "MacBook",
    "ноут": "MacBook",
    "laptop": "MacBook",
    "ipad": "iPad",
    "айпад": "iPad",
    "планшет": "iPad",
    "tablet": "iPad",
    "imac": "iMac",
}

TOKEN_SYNONYMS = {
    "айфон": "iphone",
    "телефон": "iphone",
    "смартфон": "iphone",
    "айпад": "ipad",
    "планшет": "ipad",
    "макбук": "macbook",
    "ноутбук": "macbook",
    "ноут": "macbook",
    "дешевий": "budget",
    "недорогий": "budget",
    "бюджетний": "budget",
    "доступний": "budget",
    "дорогий": "premium",
    "преміум": "premium",
    "флагман": "premium",
    "камера": "camera",
    "фото": "camera",
    "зйомка": "camera",
    "батарея": "battery",
    "автономність": "battery",
    "заряд": "battery",
    "компактний": "small",
    "малий": "small",
    "маленький": "small",
    "великий": "large",
    "навчання": "study",
    "студент": "study",
    "школа": "study",
    "ігри": "gaming",
    "ігровий": "gaming",
    "малювання": "drawing",
    "дизайн": "drawing",
    "стилус": "drawing",
    "програмування": "coding",
    "розробка": "coding",
    "код": "coding",
    "потужний": "performance",
    "процесор": "performance",
    "швидкий": "performance",
    "новий": "new",
    "свіжий": "new",
    "старий": "old",
    "старіший": "old",
}

IPHONE_YEAR = {
    7: 2016,
    8: 2017,
    10: 2018,
    11: 2019,
    12: 2020,
    13: 2021,
    14: 2022,
    15: 2023,
    16: 2024,
    17: 2025,
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apple AI Помічник</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f7; min-height: 100vh; padding: 40px 16px; }
    .wrap { max-width: 760px; margin: 0 auto; }
    h1 { text-align: center; font-size: 2rem; font-weight: 700; color: #1d1d1f; margin-bottom: 8px; }
    .sub { text-align: center; color: #6e6e73; margin-bottom: 28px; font-size: .98rem; }
    .card { background: #fff; border-radius: 18px; padding: 24px; box-shadow: 0 2px 16px rgba(0,0,0,.08); margin-bottom: 20px; }
    .row { display: flex; gap: 10px; }
    input[type=text] { flex: 1; padding: 14px 16px; border-radius: 12px; border: 1px solid #d2d2d7; font-size: 15px; }
    .go { padding: 14px 22px; background: #007aff; color: #fff; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
    .hints { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .hint { background: #f3f4f6; border: none; padding: 6px 12px; border-radius: 999px; font-size: .8rem; cursor: pointer; }
    .intent-row, .reason-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
    .intent-tag, .reason-tag { background: #e8f0fe; color: #1a56db; border-radius: 999px; padding: 4px 10px; font-size: .76rem; }
    .corrected { background: #fff8e1; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 8px 12px; margin-bottom: 10px; font-size: .85rem; }
    .info { color: #6e6e73; font-size: .9rem; margin-bottom: 12px; }
    .item { background: #fff; border-radius: 16px; padding: 18px; margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,.06); }
    .top { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 6px; }
    .name { font-weight: 700; color: #1d1d1f; }
    .pct { font-weight: 700; color: #007aff; }
    .meta { color: #6e6e73; font-size: .82rem; margin-bottom: 6px; }
    .bar-wrap { height: 6px; background: #e5e7eb; border-radius: 999px; margin-bottom: 10px; }
    .bar { height: 6px; background: linear-gradient(90deg, #34c759, #007aff); border-radius: 999px; }
    .desc { color: #4b5563; font-size: .9rem; line-height: 1.45; }
    .msg { text-align: center; color: #6e6e73; padding: 28px; }
    .err { color: #dc2626; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Apple AI Помічник</h1>
    <p class="sub">Опишіть, що вам потрібно, і система підбере найкращі варіанти.</p>
    <div class="card">
      <div class="row">
        <input type="text" id="q" placeholder="Наприклад: недорогий телефон з хорошою камерою">
        <button class="go" id="btn">Знайти</button>
      </div>
      <div class="hints" id="hints">
        <button class="hint">недорогий телефон з хорошою камерою</button>
        <button class="hint">ноутбук для програмування</button>
        <button class="hint">планшет для малювання</button>
        <button class="hint">компактний планшет для читання</button>
        <button class="hint">великий ноутбук для монтажу</button>
      </div>
    </div>
    <div id="results"></div>
  </div>
  <script>
    const hints = document.getElementById('hints');
    const input = document.getElementById('q');
    const button = document.getElementById('btn');
    const results = document.getElementById('results');

    hints.addEventListener('click', (e) => {
      if (!e.target.classList.contains('hint')) return;
      input.value = e.target.textContent.trim();
      doSearch();
    });

    button.addEventListener('click', doSearch);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') doSearch();
    });

    function renderTags(intent) {
      const tags = [];
      if (intent.category) tags.push(`📦 ${intent.category}`);
      if (intent.size === 'small') tags.push('👌 компактний');
      if (intent.size === 'large') tags.push('⬛ великий');
      if (intent.budget) tags.push('💸 бюджетний');
      if (intent.premium) tags.push('💎 дорогий');
      if (intent.camera) tags.push(intent.best_camera ? '📷 топ камера' : '📷 камера');
      if (intent.battery) tags.push('🔋 батарея');
      if (intent.performance) tags.push('⚡ потужність');
      if (intent.study) tags.push('🎓 навчання');
      if (intent.gaming) tags.push('🎮 ігри');
      if (intent.drawing) tags.push('✏️ малювання');
      return tags.map((tag) => `<span class="intent-tag">${tag}</span>`).join('');
    }

    function doSearch() {
      const q = input.value.trim();
      if (!q) return;
      results.innerHTML = '<div class="msg">Аналізую запит...</div>';

      fetch('/recommend?query=' + encodeURIComponent(q))
        .then((r) => r.json())
        .then((data) => {
          if (!data.results || !data.results.length) {
            results.innerHTML = '<div class="msg err">Нічого не знайдено.</div>';
            return;
          }

          let html = '';
          if (data.corrected) {
            html += `<div class="corrected">Автовиправлення: <strong>${data.query}</strong></div>`;
          }
          html += `<div class="intent-row">${renderTags(data.intent || {})}</div>`;
          html += `<div class="info">Топ ${data.results.length} результатів. Режим: ${data.engine}</div>`;

          data.results.forEach((item) => {
            const pct = Math.round(item.confidence * 100);
            const reasons = (item.reasons || []).map((r) => `<span class="reason-tag">${r}</span>`).join('');
            html += `
              <div class="item">
                <div class="top">
                  <div class="name">${item.name}</div>
                  <div class="pct">${pct}%</div>
                </div>
                <div class="meta">${item.category} · $${item.price} · ${item.year} · ${item.size}"</div>
                <div class="bar-wrap"><div class="bar" style="width:${pct}%"></div></div>
                <div class="reason-row">${reasons}</div>
                <div class="desc">${item.description}</div>
              </div>
            `;
          });

          results.innerHTML = html;
        })
        .catch(() => {
          results.innerHTML = `<div class="msg err">Помилка з'єднання.</div>`;
        });
    }
  </script>
</body>
</html>"""


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text.lower())
    text = text.replace("’", "'").replace("`", "'")
    text = re.sub(r"([а-яіїєґa-z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([а-яіїєґa-z])", r"\1 \2", text)
    text = re.sub(r"[^a-zа-яіїєґ0-9$+\-/'\s.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_merged_tokens(token: str) -> list[str]:
    markers = ["телеф", "смартф", "айфон", "iphone", "ipad", "планш", "ноут", "макбук", "macbook"]
    for marker in markers:
        idx = token.find(marker)
        if idx > 0:
            left = token[:idx]
            right = token[idx:]
            if left and right:
                return [left, right]
    return [token]


def fix_typos(text: str) -> str:
    tokens = normalize_text(text).split()
    corrected = []
    changed = False
    for token in tokens:
        for part in split_merged_tokens(token):
            if part in TYPO_DICT:
                corrected.append(TYPO_DICT[part])
                changed = True
                continue
            if fuzz_process and len(part) > 4:
                match = fuzz_process.extractOne(part, SAFE_VOCAB)
                if match and match[1] >= 90 and match[0] != part:
                    corrected.append(match[0])
                    changed = True
                    continue
            corrected.append(part)
    result = " ".join(corrected)
    return result if changed else normalize_text(text)


def canonicalize_token(token: str) -> str:
    if token in TOKEN_SYNONYMS:
        return TOKEN_SYNONYMS[token]
    if token.endswith("ефон") or token.endswith("лефон") or token.endswith("елфон"):
        return "iphone"
    if token.startswith(("камер", "фото", "зйом")):
        return "camera"
    if token.startswith(("батар", "автоном", "заряд")):
        return "battery"
    if token.startswith(("компакт", "мален", "мали")) or token == "mini":
        return "small"
    if token.startswith("велик"):
        return "large"
    if token.startswith(("дешев", "недорог", "бюдж", "доступ")):
        return "budget"
    if token.startswith(("дорог", "премі", "флагман")):
        return "premium"
    if token.startswith(("навч", "студ", "школ")):
        return "study"
    if token.startswith(("ігр", "game")):
        return "gaming"
    if token.startswith(("малю", "дизайн", "стилус", "pencil")):
        return "drawing"
    if token.startswith(("програм", "розроб", "код")):
        return "coding"
    if token.startswith(("потуж", "процес", "швидк", "продуктив")):
        return "performance"
    if token.startswith(("нов", "свіж", "остан")):
        return "new"
    if token.startswith(("стар", "б/у")):
        return "old"
    if token.startswith(("кращ", "найкращ", "топ")):
        return "best"
    return token


def canonicalize_tokens(tokens: list[str]) -> list[str]:
    return [canonicalize_token(token) for token in tokens]


def parse_price_limit(text: str) -> int | None:
    match = re.search(r"\bдо\s*(\d{2,5})\b", text)
    if not match:
        match = re.search(r"\b(\d{2,5})\s*(?:\$|usd|дол|грн)\b", text)
    return int(match.group(1)) if match else None


def get_year(product: dict) -> int:
    if "year" in product:
        return int(product["year"])
    if product.get("category") == "iPhone":
        return IPHONE_YEAR.get(int(product.get("series", 12)), 2020)
    return int(product.get("series", 2024))


CURRENT_YEAR = max(get_year(product) for product in apple_products)


def infer_flags(product: dict) -> set[str]:
    name = product["name"].lower()
    category = product["category"]
    size = float(product["size"])
    flags = set()

    if category == "iPhone":
        if size <= 5.8:
            flags.add("small")
        if size >= 6.7:
            flags.add("large")
    elif category == "MacBook":
        if size <= 13.6:
            flags.add("small")
        if size >= 15.0:
            flags.add("large")
    elif category == "iPad":
        if size <= 8.3:
            flags.add("small")
        if size >= 12.9:
            flags.add("large")

    if product["performance"] >= 7:
        flags.add("performance")
    if product["camera"] >= 7:
        flags.add("camera")
    if product["battery"] >= 8:
        flags.add("battery")

    if category == "MacBook":
        flags.update({"study"})
        if any(term in name for term in ["pro", "m1", "m2", "m3", "m4"]):
            flags.update({"coding"})
        if "max" in name or "pro" in name:
            flags.update({"gaming"})

    if category == "iPad":
        flags.update({"study"})
        if any(term in name for term in ["pro", "air"]):
            flags.update({"drawing"})
        if any(term in name for term in ["pro", "m1", "m2", "m3", "m4", "a17"]):
            flags.update({"gaming"})

    if category == "iPhone":
        flags.update({"camera"})
        if product["performance"] >= 8:
            flags.add("gaming")

    return flags


def build_search_text(product: dict) -> str:
    category = product["category"]
    year = get_year(product)
    name = product["name"].lower()
    tokens = []

    if category == "iPhone":
        tokens.extend(["iphone", "айфон", "телефон", "смартфон"])
    elif category == "MacBook":
        tokens.extend(["macbook", "макбук", "ноутбук", "laptop"])
    elif category == "iPad":
        tokens.extend(["ipad", "айпад", "планшет", "tablet"])

    flags = infer_flags(product)
    if "small" in flags:
        tokens.extend(["компактний", "малий"])
    if "large" in flags:
        tokens.extend(["великий", "великий екран"])
    if "study" in flags:
        tokens.extend(["навчання", "студент"])
    if "drawing" in flags:
        tokens.extend(["малювання", "дизайн", "стилус"])
    if "coding" in flags:
        tokens.extend(["програмування", "розробка", "код"])
    if "gaming" in flags:
        tokens.extend(["ігри", "монтаж", "3d"])
    if "camera" in flags:
        tokens.extend(["камера", "фото"])
    if "battery" in flags:
        tokens.extend(["батарея", "автономність"])
    if "performance" in flags:
        tokens.extend(["потужний", "процесор", "продуктивність"])

    price = product["price"]
    if category == "iPhone":
        if price <= 350:
            tokens.extend(["дешевий", "бюджетний"])
        elif price <= 750:
            tokens.extend(["недорогий", "середній"])
        else:
            tokens.extend(["дорогий", "флагман"])
    elif category == "MacBook":
        if price <= 700:
            tokens.extend(["дешевий", "бюджетний"])
        elif price <= 1300:
            tokens.extend(["середній"])
        else:
            tokens.extend(["дорогий", "професійний"])
    elif category == "iPad":
        if price <= 350:
            tokens.extend(["дешевий", "бюджетний"])
        elif price <= 800:
            tokens.extend(["недорогий", "середній"])
        else:
            tokens.extend(["дорогий", "преміум"])

    tokens.extend(name.replace('"', " ").replace("(", " ").replace(")", " ").split())
    tokens.extend([str(year), str(product.get("series", year))])
    return " ".join(canonicalize_tokens(normalize_text(" ".join(tokens)).split()))


def build_catalog() -> list[dict]:
    catalog = []
    for product in apple_products:
        enriched = dict(product)
        enriched["year"] = get_year(product)
        enriched["flags"] = infer_flags(product)
        enriched["freshness"] = max(0.0, 1.0 - (CURRENT_YEAR - enriched["year"]) / 8.0)
        enriched["search_text"] = build_search_text(product)
        enriched["token_counts"] = Counter(enriched["search_text"].split())
        catalog.append(enriched)
    return catalog


CATALOG = build_catalog()
DOC_FREQ = Counter()
for product in CATALOG:
    DOC_FREQ.update(set(product["token_counts"]))

IDF = {token: math.log((1 + len(CATALOG)) / (1 + freq)) + 1.0 for token, freq in DOC_FREQ.items()}

LEARNED_RANKER = SyntheticProductRanker(
    normalize=normalize_text,
    canonicalize_tokens=canonicalize_tokens,
    catalog=CATALOG,
    current_year=CURRENT_YEAR,
)


def build_semantic_index() -> tuple[TruncatedSVD | None, Normalizer | None, list[list[float]]]:
    product_texts = [product["search_text"] for product in CATALOG]
    tfidf = LEARNED_RANKER.word_vectorizer.transform(product_texts)
    max_dims = min(96, tfidf.shape[0] - 1, tfidf.shape[1] - 1)
    if max_dims < 2:
        return None, None, []

    svd = TruncatedSVD(n_components=max_dims, random_state=42)
    normalizer = Normalizer(copy=False)
    product_lsa = svd.fit_transform(tfidf)
    product_lsa = normalizer.transform(product_lsa)
    return svd, normalizer, product_lsa.tolist()


SEM_SVD, SEM_NORM, PRODUCT_SEMANTIC = build_semantic_index()


def parse_intent(query: str) -> dict:
    normalized = normalize_text(query)
    tokens = canonicalize_tokens(normalized.split())

    intent = {
        "category": None,
        "budget": False,
        "premium": False,
        "camera": False,
        "best_camera": False,
        "battery": False,
        "performance": False,
        "size": None,
        "study": False,
        "gaming": False,
        "drawing": False,
        "coding": False,
        "novelty": None,
        "price_max": parse_price_limit(normalized),
    }

    for token in tokens:
        if token in CATEGORY_ALIASES:
            intent["category"] = CATEGORY_ALIASES[token]
        elif token == "budget":
            intent["budget"] = True
        elif token == "premium":
            intent["premium"] = True
        elif token == "camera":
            intent["camera"] = True
        elif token == "battery":
            intent["battery"] = True
        elif token == "performance":
            intent["performance"] = True
        elif token == "small":
            intent["size"] = "small"
        elif token == "large" and intent["size"] != "small":
            intent["size"] = "large"
        elif token == "study":
            intent["study"] = True
        elif token == "gaming":
            intent["gaming"] = True
            intent["performance"] = True
        elif token == "drawing":
            intent["drawing"] = True
        elif token == "coding":
            intent["coding"] = True
            intent["performance"] = True
        elif token == "new":
            intent["novelty"] = "new"
        elif token == "old":
            intent["novelty"] = "old"
        elif token == "best":
            intent["best_camera"] = True

    if "iphone" in tokens and intent["category"] is None:
        intent["category"] = "iPhone"
    if "macbook" in tokens and intent["category"] is None:
        intent["category"] = "MacBook"
    if "ipad" in tokens and intent["category"] is None:
        intent["category"] = "iPad"

    if intent["best_camera"]:
        intent["camera"] = True

    return intent


def weighted_overlap(query_tokens: list[str], product: dict) -> float:
    query_counts = Counter(query_tokens)
    numerator = 0.0
    denominator = 0.0
    for token, q_count in query_counts.items():
        weight = IDF.get(token, 1.0)
        denominator += q_count * weight
        numerator += min(q_count, product["token_counts"].get(token, 0)) * weight
    return numerator / denominator if denominator else 0.0


def learned_score(query: str) -> list[float]:
    return LEARNED_RANKER.score_all(query).tolist()


def semantic_score(query: str) -> list[float]:
    if SEM_SVD is None or SEM_NORM is None or not PRODUCT_SEMANTIC:
        return [0.0] * len(CATALOG)

    q_tfidf = LEARNED_RANKER.word_vectorizer.transform([query])
    q_lsa = SEM_SVD.transform(q_tfidf)
    q_lsa = SEM_NORM.transform(q_lsa)
    q_vec = q_lsa[0]

    scores: list[float] = []
    for vec in PRODUCT_SEMANTIC:
        dot = sum(a * b for a, b in zip(vec, q_vec))
        scores.append(max(0.0, min(1.0, float(dot))))
    return scores


def numeric_fit_score(intent: dict, product: dict) -> float:
    category = product["category"]
    price = product["price"]
    quality = (product["performance"] + product["camera"] + product["battery"]) / 30.0
    score = quality * 0.12 + product["freshness"] * 0.10

    if intent["category"] and category != intent["category"]:
        return -1.0

    if intent["budget"] and intent["price_max"] is None:
        caps = {"iPhone": 750, "MacBook": 1200, "iPad": 750, "iMac": 1800}
        if price > caps.get(category, 1000):
            return -1.0

    if intent["premium"]:
        floors = {"iPhone": 850, "MacBook": 1500, "iPad": 900, "iMac": 1800}
        if price < floors.get(category, 800):
            score -= 0.25

    if intent["price_max"] is not None:
        if price > intent["price_max"]:
            return -1.0
        score += min(0.18, (intent["price_max"] - price) / max(intent["price_max"], 1) * 0.25)

    if intent["size"] == "small":
        if category == "iPhone" and product["size"] > 6.1:
            return -1.0
        if category == "MacBook" and product["size"] > 14.2:
            return -1.0
        if category == "iPad" and product["size"] > 11.0:
            return -1.0
        score += 0.14

    if intent["size"] == "large":
        if "large" in product["flags"]:
            score += 0.18
        else:
            score -= 0.12

    if intent["camera"]:
        score += product["camera"] / 22.0
        if intent["best_camera"]:
            score += product["camera"] / 14.0
        if intent["budget"]:
            score += min(0.24, (product["camera"] * 120.0) / max(price, 1))

    if intent["battery"]:
        score += product["battery"] / 24.0
        if category == "iPhone" and not intent["premium"]:
            if price <= 900:
                score += 0.12
            elif price >= 1100:
                score -= 0.14

    if intent["performance"]:
        score += product["performance"] / 20.0
        if product["year"] <= CURRENT_YEAR - 5:
            score -= 0.12

    if intent["study"]:
        if "study" in product["flags"]:
            score += 0.22
        if category in {"MacBook", "iPad"} and price <= 1000:
            score += 0.12
        if category == "iPad" and price <= 800:
            score += 0.14
        if category == "iPad" and "drawing" in product["flags"] and price <= 850:
            score += 0.05
        if category == "iPad" and price > 950:
            score -= 0.16
        if category == "iPhone":
            score -= 0.10

    if intent["coding"]:
        if category != "MacBook":
            score -= 0.20
        if "coding" in product["flags"]:
            score += 0.24
        if not intent["premium"] and intent["price_max"] is None:
            if 900 <= price <= 2200:
                score += 0.16
            elif price > 2400:
                score -= 0.22

    if intent["gaming"]:
        if "gaming" in product["flags"]:
            score += 0.22
        if category == "iPhone" and product["performance"] < 7:
            score -= 0.18

    if intent["drawing"]:
        if category != "iPad":
            score -= 0.18
        if "drawing" in product["flags"]:
            score += 0.24
        if category == "iPad" and product["size"] >= 12.9:
            score += 0.08

    if intent["budget"]:
        if category == "iPhone":
            if price <= 700:
                score += 0.22
            elif price <= 800:
                score += 0.02
            else:
                score -= 0.30
        elif category == "MacBook":
            if price <= 900:
                score += 0.18
            elif price <= 1200:
                score += 0.04
            else:
                score -= 0.24
        elif category == "iPad":
            if price <= 600:
                score += 0.18
            elif price <= 750:
                score += 0.04
            else:
                score -= 0.24

    if intent["premium"]:
        score += min(0.20, price / 10000.0)

    if intent["novelty"] == "new":
        score += product["freshness"] * 0.30
    elif intent["novelty"] == "old":
        age = CURRENT_YEAR - product["year"]
        if 2 <= age <= 6:
            score += 0.18
        elif age > 7:
            score -= 0.18

    return score


def explain_match(intent: dict, product: dict) -> list[str]:
    reasons = []
    if intent["category"]:
        reasons.append(product["category"])
    if intent["budget"] and product["price"] <= {"iPhone": 700, "MacBook": 900, "iPad": 600}.get(product["category"], 700):
        reasons.append("хороша ціна")
    if intent["premium"] and product["price"] >= {"iPhone": 850, "MacBook": 1500, "iPad": 900}.get(product["category"], 850):
        reasons.append("преміум сегмент")
    if intent["camera"] and product["camera"] >= 8:
        reasons.append("сильна камера")
    if intent["battery"] and product["battery"] >= 8:
        reasons.append("добра автономність")
    if intent["performance"] and product["performance"] >= 8:
        reasons.append("висока продуктивність")
    if intent["study"] and "study" in product["flags"]:
        reasons.append("добрий для навчання")
    if intent["drawing"] and "drawing" in product["flags"]:
        reasons.append("підходить для малювання")
    if intent["coding"] and "coding" in product["flags"]:
        reasons.append("підходить для програмування")
    if intent["gaming"] and "gaming" in product["flags"]:
        reasons.append("підходить для важких задач")
    if intent["size"] == "small" and "small" in product["flags"]:
        reasons.append("компактний")
    if intent["size"] == "large" and "large" in product["flags"]:
        reasons.append("великий екран")
    if not reasons:
        reasons.append("збалансований варіант")
    return reasons[:3]


def hybrid_score(
    query: str,
    intent: dict,
    query_tokens: list[str],
    learned_scores: list[float],
    semantic_scores: list[float],
    index: int,
) -> float:
    product = CATALOG[index]
    rule = numeric_fit_score(intent, product)
    if rule < 0:
        return -1.0

    lexical = weighted_overlap(query_tokens, product)
    learned = learned_scores[index]
    semantic = semantic_scores[index]
    structured = sum(
        [
            1 if intent["category"] else 0,
            1 if intent["budget"] else 0,
            1 if intent["premium"] else 0,
            1 if intent["camera"] else 0,
            1 if intent["battery"] else 0,
            1 if intent["performance"] else 0,
            1 if intent["size"] else 0,
            1 if intent["study"] else 0,
            1 if intent["gaming"] else 0,
            1 if intent["drawing"] else 0,
            1 if intent["coding"] else 0,
            1 if intent["price_max"] is not None else 0,
        ]
    )

    if structured >= 2:
        return learned * 0.30 + lexical * 0.20 + rule * 0.40 + semantic * 0.10
    return learned * 0.40 + lexical * 0.27 + rule * 0.23 + semantic * 0.10


def confidence_from_scores(scores: list[float]) -> list[float]:
    if not scores:
        return []
    peak = max(scores)
    exps = [math.exp((score - peak) * 6.0) for score in scores]
    total = sum(exps) or 1.0
    return [round(value / total, 4) for value in exps]


app = Flask(__name__)
if CORS is not None:
    CORS(app)


@lru_cache(maxsize=512)
def prepared_query(query: str) -> str:
    return " ".join(canonicalize_tokens(normalize_text(query).split()))


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/recommend", methods=["GET"])
def recommend():
    query_raw = request.args.get("query", "").strip()
    if not query_raw:
        return jsonify({"query": "", "corrected": False, "intent": {}, "results": []})

    query_fixed = fix_typos(query_raw)
    corrected = query_fixed != normalize_text(query_raw)
    intent = parse_intent(query_fixed)
    query_norm = prepared_query(query_fixed)
    query_tokens = query_norm.split()
    learned_scores = learned_score(query_norm)
    semantic_scores = semantic_score(query_norm)

    scored = []
    for index, _ in enumerate(CATALOG):
        score = hybrid_score(query_norm, intent, query_tokens, learned_scores, semantic_scores, index)
        if score >= 0:
            scored.append((index, score))

    scored.sort(key=lambda item: item[1], reverse=True)
    top = scored[:3]
    confidences = confidence_from_scores([score for _, score in top])

    results = []
    for position, ((index, _), confidence) in enumerate(zip(top, confidences), start=1):
        product = CATALOG[index]
        results.append(
            {
                "rank": position,
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "year": product["year"],
                "size": product["size"],
                "description": product["description"],
                "confidence": confidence,
                "reasons": explain_match(intent, product),
            }
        )

    return jsonify(
        {
            "query": query_fixed,
            "corrected": corrected,
            "intent": intent,
            "engine": "trained-lexical-rule-semantic",
            "training_accuracy": round(LEARNED_RANKER.validation_accuracy, 4),
            "training_top3_accuracy": round(LEARNED_RANKER.validation_top3_accuracy, 4),
            "results": results,
        }
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
