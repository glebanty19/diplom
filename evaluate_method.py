from __future__ import annotations

from dataclasses import dataclass

from app import app


@dataclass
class EvalCase:
    query: str
    expected_categories: set[str]
    preferred_names: set[str]
    forbidden_names: set[str]


CASES = [
    EvalCase(
        query="недорогий телефон з хорошою камерою",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 13 Pro", "iPhone 15", "iPhone 14 Plus"},
        forbidden_names={"iPhone 17 Pro Max", "iPhone 17 Pro"},
    ),
    EvalCase(
        query="дешевий телефон",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 13 Pro", "iPhone 14 Plus", "iPhone 12 Pro Max"},
        forbidden_names={"iPhone 17 Pro Max", "iPhone 17 Pro"},
    ),
    EvalCase(
        query="дорогий телефон",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 17 Pro Max", "iPhone 16 Pro Max", "iPhone 17 Pro"},
        forbidden_names={"iPhone 8", "iPhone SE (2020)"},
    ),
    EvalCase(
        query="великий телефон",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 17 Pro Max", "iPhone 16 Pro Max", "iPhone 15 Pro Max"},
        forbidden_names={"iPhone 13 Mini", "iPhone SE (2022)"},
    ),
    EvalCase(
        query="компактний телефон",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 13 Mini", "iPhone SE (2022)", "iPhone 12 Mini"},
        forbidden_names={"iPhone 17 Pro Max", "iPhone 16 Plus"},
    ),
    EvalCase(
        query="телефон для ігор",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 17 Pro", "iPhone 16 Plus", "iPhone 15 Pro Max"},
        forbidden_names={"iPhone 8", "iPhone 7"},
    ),
    EvalCase(
        query="телефон з хорошою батареєю",
        expected_categories={"iPhone"},
        preferred_names={"iPhone 17", "iPhone 16 Plus", "iPhone 16"},
        forbidden_names={"iPhone 12 Mini", "iPhone SE (2020)"},
    ),
    EvalCase(
        query="дешевий ноутбук",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 13\" M1 (2020)", "MacBook Pro 13\" Intel (2020)", "MacBook Air 13\" M1 (2020)"},
        forbidden_names={"MacBook Pro 16\" M4 Max (2024)"},
    ),
    EvalCase(
        query="дорогий ноутбук",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 16\" M4 Pro (2024)", "MacBook Pro 14\" M4 Pro (2024)", "MacBook Pro 14\" M4 Max (2024)"},
        forbidden_names={"MacBook Air 13\" Intel (2020)", "MacBook Air 13\" Retina (2018)"},
    ),
    EvalCase(
        query="великий ноутбук",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 16\" M4 Pro (2024)", "MacBook Pro 16\" M4 Max (2024)", "MacBook Pro 16\" M3 Max (2023)"},
        forbidden_names={"MacBook Air 13\" M3 (2024)"},
    ),
    EvalCase(
        query="компактний ноутбук",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Air 13\" M3 (2024)", "MacBook Pro 13\" M2 (2022)", "MacBook Air 13\" M2 (2022)"},
        forbidden_names={"MacBook Pro 16\" M4 Pro (2024)"},
    ),
    EvalCase(
        query="ноутбук для навчання",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 13\" M2 (2022)", "MacBook Air 13\" M2 (2022)", "MacBook Pro 14\" M1 Pro (2021)"},
        forbidden_names={"MacBook Pro 16\" M4 Max (2024)"},
    ),
    EvalCase(
        query="ноутбук для ігор",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 16\" M4 Pro (2024)", "MacBook Pro 16\" M4 Max (2024)", "MacBook Pro 16\" M2 Max (2023)"},
        forbidden_names={"MacBook Air 13\" Intel (2020)"},
    ),
    EvalCase(
        query="ноутбук для програмування",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 14\" M4 Pro (2024)", "MacBook Pro 14\" M2 Max (2023)", "MacBook Air 13\" M3 (2024)"},
        forbidden_names={"iPad Pro 13\" M4 (2024)", "iPhone 17 Pro Max"},
    ),
    EvalCase(
        query="великий ноутбук для монтажу",
        expected_categories={"MacBook"},
        preferred_names={"MacBook Pro 16\" M4 Max (2024)", "MacBook Pro 16\" M3 Max (2023)", "MacBook Pro 16\" M4 Pro (2024)"},
        forbidden_names={"MacBook Air 13\" M3 (2024)"},
    ),
    EvalCase(
        query="дешевий планшет",
        expected_categories={"iPad"},
        preferred_names={"iPad 10 (2022)", "iPad Air 4 (2020)", "iPad 9 (2021)"},
        forbidden_names={"iPad Pro 13\" M4 (2024)"},
    ),
    EvalCase(
        query="дорогий планшет",
        expected_categories={"iPad"},
        preferred_names={"iPad Pro 13\" M4 (2024)", "iPad Pro 11\" M4 (2024)", "iPad Air 13\" M3 (2025)"},
        forbidden_names={"iPad 9 (2021)", "iPad 7 (2019)"},
    ),
    EvalCase(
        query="великий планшет",
        expected_categories={"iPad"},
        preferred_names={"iPad Air 13\" M3 (2025)", "iPad Pro 12.9\" M2 (2022)", "iPad Air 13\" M2 (2024)"},
        forbidden_names={"iPad mini 7 A17 Pro (2024)"},
    ),
    EvalCase(
        query="компактний планшет",
        expected_categories={"iPad"},
        preferred_names={"iPad mini 7 A17 Pro (2024)", "iPad mini 6 (2021)", "iPad mini 5 (2019)"},
        forbidden_names={"iPad Pro 13\" M4 (2024)"},
    ),
    EvalCase(
        query="планшет для навчання",
        expected_categories={"iPad"},
        preferred_names={"iPad Air 11\" M3 (2025)", "iPad Air 13\" M2 (2024)", "iPad Air 11\" M2 (2024)"},
        forbidden_names={"MacBook Pro 16\" M4 Pro (2024)", "iPhone 17"},
    ),
    EvalCase(
        query="планшет для ігор",
        expected_categories={"iPad"},
        preferred_names={"iPad Air 11\" M4 (2026)", "iPad Air 13\" M4 (2026)", "iPad mini 7 A17 Pro (2024)", "iPad Pro 11\" M2 (2022)"},
        forbidden_names={"iPad 7 (2019)"},
    ),
    EvalCase(
        query="планшет для малювання",
        expected_categories={"iPad"},
        preferred_names={"iPad Pro 13\" M4 (2024)", "iPad Air 13\" M3 (2025)", "iPad Air 13\" M2 (2024)"},
        forbidden_names={"iPhone 17", "MacBook Pro 14\" M4 Pro (2024)"},
    ),
]


def evaluate() -> int:
    client = app.test_client()
    passed = 0
    total_accuracy = 0.0
    total_precision_at_3 = 0.0

    print(f"{'Scenario':<40} | {'Accuracy':<10} | {'Precision@3':<12} | {'Status'}")
    print("-" * 80)

    for case in CASES:
        response = client.get("/recommend", query_string={"query": case.query})
        payload = response.get_json()
        results = payload["results"]
        names = [item["name"] for item in results]
        categories = {item["category"] for item in results}

        # Category check
        category_ok = bool(categories) and categories.issubset(case.expected_categories)
        
        # Precision@3 calculation (how many preferred in top 3)
        # Assuming our goal is to have preferred items in the list
        relevant_in_top_3 = [name for name in names if name in case.preferred_names]
        precision_at_3 = len(relevant_in_top_3) / 3.0
        
        # Forbidden check
        forbidden_ok = all(name not in case.forbidden_names for name in names)
        
        # Accuracy for this case (binary: category ok AND no forbidden AND at least one preferred)
        case_passed = category_ok and (len(relevant_in_top_3) > 0) and forbidden_ok
        case_accuracy = 1.0 if case_passed else 0.0

        if case_passed:
            passed += 1
        
        total_accuracy += case_accuracy
        total_precision_at_3 += precision_at_3

        status = "PASS" if case_passed else "FAIL"
        print(f"{case.query:<40} | {case_accuracy:<10.2f} | {precision_at_3:<12.2f} | {status}")

    total = len(CASES)
    avg_accuracy = total_accuracy / total
    avg_precision_at_3 = total_precision_at_3 / total

    print("-" * 80)
    print(f"Final Metrics:")
    print(f"Overall Accuracy: {avg_accuracy:.4f}")
    print(f"Mean Precision@3: {avg_precision_at_3:.4f}")
    print(f"Summary: {passed}/{total} passed")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(evaluate())
