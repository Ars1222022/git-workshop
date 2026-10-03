# -*- coding: utf-8 -*-
"""
FASIT - Dev A: losning for data_loader.py

Kopiera innehallet over ai-system/data_loader.py (eller jämfor).
Syftet med workshopuppgiften ar INTE att skriva korrekt kod - utan att
gora en liten, isolerad andring i en egen feature branch och fa den
granskad. Behover inte vara snyggast losning, bara korrekt och testad.
"""

RAW_DATA = [
    {"customer_id": 101, "age": 34, "tenure_months": 12, "churned": 0},
    {"customer_id": 102, "age": 45, "tenure_months": 2, "churned": 1},
    {"customer_id": 103, "age": 23, "tenure_months": 24, "churned": 0},
    {"customer_id": 104, "age": 52, "tenure_months": -5, "churned": 1},  # KORRUPT
    {"customer_id": 105, "age": 29, "tenure_months": 18, "churned": 0},
]


def load_dataset():
    """
    Laser in kunddata for churn-prediktion.

    LOSNING: poster med negativ tenure_months ar korrupta och filtreras bort.
    En kund kan inte ha haft ett abonnemang i -5 manader.
    """
    return [dict(row) for row in RAW_DATA if row["tenure_months"] >= 0]


# ---------------------------------------------------------------------------
# Testtillagg - kopiera detta in i tests/test_evaluator.py
# ---------------------------------------------------------------------------
TEST_DEV_A = '''
def test_load_dataset_filters_invalid_tenure():
    """Kontrollera att den korrupta posten (tenure_months = -5) ar borttagen."""
    data = load_dataset()
    assert all(item["tenure_months"] >= 0 for item in data)
    # Detta extra assert ar det som reviewern begar i 1+1-regeln!
    assert len(data) == 4


def test_load_dataset_keeps_valid_customers():
    """Kontrollera att giltiga kunder INTE roras."""
    data = load_dataset()
    ids = {item["customer_id"] for item in data}
    assert ids == {101, 102, 103, 105}
'''


if __name__ == "__main__":
    print("Dev A losning - foregående facit:")
    for rad in load_dataset():
        print(f"  customer {rad['customer_id']}: "
              f"tenure={rad['tenure_months']}")
    print(f"\nAntal giltiga rader: {len(load_dataset())} (av 5)")
    print("\nTesttillagg att kopiera in i tests/test_evaluator.py:")
    print(TEST_DEV_A)