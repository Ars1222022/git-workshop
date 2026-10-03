"""
Modul for att lasa in och forbereda tranings- och utvarderingsdata for AI-modellen.

UPPGIFT A - Utvecklare A
    Arbeta i branchen:  feature/add-data-validation
    Sak som ska goras: filtrera bort posten med tenure_months = -5.
    Testa med:          python main.py  och  python -m pytest
"""

# Dokumentation: har en kund nagon gang haft -5 manader? Nej. Posten ar korrupt
# och ska saneras av Utvecklare A i uppgiften "feature/add-data-validation".
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

    Returnerar: lista med kund-dicts.

    TODO (Utvecklare A): filtrera bort poster med tenure_months < 0.
    """
    return [dict(row) for row in RAW_DATA]
