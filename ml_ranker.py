from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split


def _price_band(category: str, price: int) -> str:
    if category == "iPhone":
        if price <= 350:
            return "дуже бюджетний"
        if price <= 650:
            return "бюджетний"
        if price <= 950:
            return "середній"
        return "преміум"
    if category == "MacBook":
        if price <= 700:
            return "бюджетний"
        if price <= 1300:
            return "середній"
        return "професійний"
    if price <= 300:
        return "бюджетний"
    if price <= 800:
        return "середній"
    return "преміум"


def _canonical_category_term(category: str) -> str:
    return {
        "iPhone": "iphone",
        "MacBook": "macbook",
        "iPad": "ipad",
        "iMac": "imac",
    }.get(category, category.lower())


def _size_terms(category: str, size: float, flags: set[str]) -> list[str]:
    terms: list[str] = []
    if "small" in flags:
        terms.extend(["компактний", "малий", "невеликий"])
    if "large" in flags:
        terms.extend(["великий", "великий екран"])
    if category == "MacBook" and size <= 13.6:
        terms.extend(["ультрапортативний", "легкий"])
    return terms


def _quality_terms(product: dict) -> list[str]:
    terms: list[str] = []
    if product["camera"] >= 9:
        terms.extend(["топ камера", "найкраща камера", "для фото"])
    elif product["camera"] >= 7:
        terms.extend(["хороша камера", "для фото"])

    if product["battery"] >= 9:
        terms.extend(["довга автономність", "потужна батарея"])
    elif product["battery"] >= 7:
        terms.append("хороша автономність")

    if product["performance"] >= 9:
        terms.extend(["дуже потужний", "флагманська продуктивність"])
    elif product["performance"] >= 7:
        terms.extend(["потужний", "висока продуктивність"])

    return terms


def _scenario_terms(product: dict) -> list[str]:
    flags = product["flags"]
    terms: list[str] = []
    if "study" in flags:
        terms.extend(["для навчання", "для студента", "для школи"])
    if "coding" in flags:
        terms.extend(["для програмування", "для розробки", "для коду"])
    if "drawing" in flags:
        terms.extend(["для малювання", "для дизайну", "зі стилусом"])
    if "gaming" in flags:
        terms.extend(["для важких задач", "для монтажу", "для 3d"])
    return terms


def _novelty_terms(current_year: int, year: int) -> list[str]:
    age = current_year - year
    if age <= 1:
        return ["новий", "свіжий", "актуальний"]
    if age <= 4:
        return ["сучасний"]
    return ["старіший", "перевірений"]


def _add_sample(samples: set[str], sample: str) -> None:
    cleaned = " ".join(sample.split()).strip().lower()
    if not cleaned:
        return
    if len(cleaned.split()) < 2:
        return
    samples.add(cleaned)


def _core_queries(product: dict, current_year: int) -> list[str]:
    category_term = _canonical_category_term(product["category"])
    band = _price_band(product["category"], product["price"])
    size_terms = _size_terms(product["category"], product["size"], product["flags"])
    quality_terms = _quality_terms(product)
    scenario_terms = _scenario_terms(product)
    novelty_terms = _novelty_terms(current_year, product["year"])

    name = product["name"].lower()
    series = str(product.get("series", product["year"]))
    year = str(product["year"])
    samples: set[str] = set()

    _add_sample(samples, name)
    _add_sample(samples, f"{name} {year}")
    _add_sample(samples, f"{band} {name}")
    _add_sample(samples, f"{category_term} {series}")
    _add_sample(samples, f"{band} {category_term} {series}")
    _add_sample(samples, f"{category_term} до {product['price'] + 50}")
    _add_sample(samples, f"{category_term} до {product['price'] + 120}")

    for novelty in novelty_terms:
        _add_sample(samples, f"{novelty} {category_term}")
        _add_sample(samples, f"{novelty} {name}")

    for size_term in size_terms:
        _add_sample(samples, f"{size_term} {category_term}")
        _add_sample(samples, f"{size_term} {name}")
        _add_sample(samples, f"{band} {size_term} {category_term}")

    for quality in quality_terms:
        _add_sample(samples, f"{category_term} {quality}")
        _add_sample(samples, f"{name} {quality}")
        _add_sample(samples, f"{band} {category_term} {quality}")

    for scenario in scenario_terms:
        _add_sample(samples, f"{category_term} {scenario}")
        _add_sample(samples, f"{name} {scenario}")
        _add_sample(samples, f"{band} {category_term} {scenario}")
        for size_term in size_terms[:2]:
            _add_sample(samples, f"{size_term} {category_term} {scenario}")

    if product["category"] == "MacBook":
        _add_sample(samples, f"macbook {series}")
        if "coding" in product["flags"]:
            _add_sample(samples, f"macbook для програмування до {product['price'] + 100}")
        if product["size"] >= 15.0:
            _add_sample(samples, "великий macbook для роботи")
            _add_sample(samples, "великий ноутбук для монтажу")
        if product["size"] <= 13.6:
            _add_sample(samples, "легкий macbook для подорожей")
            _add_sample(samples, "компактний ноутбук для навчання")

    if product["category"] == "iPad":
        if "drawing" in product["flags"]:
            _add_sample(samples, f"ipad для малювання до {product['price'] + 120}")
        if "small" in product["flags"]:
            _add_sample(samples, "компактний ipad для читання")
            _add_sample(samples, "малий ipad")
        if "large" in product["flags"]:
            _add_sample(samples, "великий ipad для роботи")
            _add_sample(samples, "великий планшет для малювання")

    if product["category"] == "iPhone":
        if product["camera"] >= 9:
            _add_sample(samples, "iphone з найкращою камерою")
        elif product["camera"] >= 7:
            _add_sample(samples, "iphone з хорошою камерою")
        if "small" in product["flags"]:
            _add_sample(samples, "компактний iphone")
        if "large" in product["flags"]:
            _add_sample(samples, "великий iphone")

    return sorted(samples)


@dataclass
class CategoryModel:
    category: str
    class_indices: list[int]
    word_vectorizer: TfidfVectorizer
    char_vectorizer: TfidfVectorizer
    classifier: LogisticRegression


@dataclass
class SyntheticProductRanker:
    normalize: Callable[[str], str]
    canonicalize_tokens: Callable[[list[str]], list[str]]
    catalog: list[dict]
    current_year: int

    def __post_init__(self) -> None:
        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True,
        )
        self.classifier = LogisticRegression(
            max_iter=4000,
            C=6.0,
            solver="lbfgs",
            class_weight="balanced",
        )
        self.category_terms = {
            "iPhone": {"iphone"},
            "MacBook": {"macbook", "laptop"},
            "iPad": {"ipad", "tablet"},
            "iMac": {"imac"},
        }
        self.training_examples, self.labels = self._build_training_set()
        self._fit()

    def _prepare_text(self, text: str) -> str:
        normalized = self.normalize(text)
        return " ".join(self.canonicalize_tokens(normalized.split()))

    def _build_training_set(self) -> tuple[list[str], list[int]]:
        texts: list[str] = []
        labels: list[int] = []
        for index, product in enumerate(self.catalog):
            samples = _core_queries(product, self.current_year)
            samples.append(product["search_text"])
            prepared_samples = {self._prepare_text(sample) for sample in samples}
            for sample in sorted(prepared_samples):
                texts.append(sample)
                labels.append(index)
        return texts, labels

    def _infer_category(self, prepared_text: str) -> str | None:
        tokens = set(prepared_text.split())
        for category, terms in self.category_terms.items():
            if tokens & terms:
                return category
        return None

    def _train_category_model(self, category: str, train_idx: np.ndarray) -> CategoryModel | None:
        category_rows = [
            idx for idx in train_idx if self.catalog[int(self.labels[idx])]["category"] == category
        ]
        if len(category_rows) < 2:
            return None

        texts = [self.training_examples[idx] for idx in category_rows]
        labels = np.array([self.labels[idx] for idx in category_rows])
        unique_labels = np.unique(labels)
        if len(unique_labels) < 2:
            return None

        word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        char_vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True,
        )
        classifier = LogisticRegression(
            max_iter=4000,
            C=6.0,
            solver="lbfgs",
            class_weight="balanced",
        )

        X_word = word_vectorizer.fit_transform(texts)
        X_char = char_vectorizer.fit_transform(texts)
        X = hstack([X_word, X_char]).tocsr()
        classifier.fit(X, labels)

        return CategoryModel(
            category=category,
            class_indices=unique_labels.tolist(),
            word_vectorizer=word_vectorizer,
            char_vectorizer=char_vectorizer,
            classifier=classifier,
        )

    def _fit(self) -> None:
        X_word = self.word_vectorizer.fit_transform(self.training_examples)
        X_char = self.char_vectorizer.fit_transform(self.training_examples)
        X = hstack([X_word, X_char]).tocsr()

        train_idx, test_idx = train_test_split(
            np.arange(len(self.labels)),
            test_size=0.18,
            random_state=42,
            stratify=self.labels,
        )
        y_train = np.array(self.labels)[train_idx]
        y_test = np.array(self.labels)[test_idx]

        self.classifier.fit(X[train_idx], y_train)

        self.category_models: dict[str, CategoryModel] = {}
        for category in sorted({product["category"] for product in self.catalog}):
            model = self._train_category_model(category, train_idx)
            if model is not None:
                self.category_models[category] = model

        probability_rows: list[np.ndarray] = []
        predicted: list[int] = []
        for idx in test_idx:
            prepared = self.training_examples[idx]
            category_hint = self._infer_category(prepared)
            scores = self.score_prepared(prepared, category_hint=category_hint)
            probability_rows.append(scores)
            predicted.append(int(np.argmax(scores)))

        probabilities = np.vstack(probability_rows)
        probabilities = np.clip(probabilities, 1e-12, 1.0)
        probabilities = probabilities / probabilities.sum(axis=1, keepdims=True)

        top3_indices = np.argsort(probabilities, axis=1)[:, -3:]
        self.validation_accuracy = float(accuracy_score(y_test, predicted))
        self.validation_top3_accuracy = float(
            np.mean([y_test[i] in top3_indices[i] for i in range(len(y_test))])
        )
        self.validation_log_loss = float(
            log_loss(y_test, probabilities, labels=np.arange(len(self.catalog)))
        )
        self.validation_test_size = int(len(y_test))
        self.validation_labels = y_test.tolist()
        self.validation_predicted = list(predicted)
        self.validation_probabilities = probabilities.tolist()
        self.validation_classes = list(range(len(self.catalog)))

    def _global_scores_prepared(self, prepared: str) -> np.ndarray:
        X_word = self.word_vectorizer.transform([prepared])
        X_char = self.char_vectorizer.transform([prepared])
        X = hstack([X_word, X_char]).tocsr()
        proba = self.classifier.predict_proba(X)[0]
        scores = np.zeros(len(self.catalog), dtype=float)
        for cls_index, product_index in enumerate(self.classifier.classes_):
            scores[int(product_index)] = float(proba[cls_index])
        return scores

    def _category_scores_prepared(self, prepared: str, category_hint: str) -> np.ndarray | None:
        model = self.category_models.get(category_hint)
        if model is None:
            return None

        X_word = model.word_vectorizer.transform([prepared])
        X_char = model.char_vectorizer.transform([prepared])
        X = hstack([X_word, X_char]).tocsr()
        proba = model.classifier.predict_proba(X)[0]
        scores = np.zeros(len(self.catalog), dtype=float)
        for cls_index, product_index in enumerate(model.classifier.classes_):
            scores[int(product_index)] = float(proba[cls_index])
        return scores

    def score_prepared(self, prepared: str, category_hint: str | None = None) -> np.ndarray:
        inferred = category_hint or self._infer_category(prepared)
        if inferred:
            category_scores = self._category_scores_prepared(prepared, inferred)
            if category_scores is not None and category_scores.sum() > 0:
                return category_scores
        return self._global_scores_prepared(prepared)

    def score_all(self, query: str, category_hint: str | None = None) -> np.ndarray:
        prepared = self._prepare_text(query)
        return self.score_prepared(prepared, category_hint=category_hint)
