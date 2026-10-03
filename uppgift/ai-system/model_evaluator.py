"""
Modul for att utvardera AI-modellens prediktioner mot facit.

UPPGIFT B - Utvecklare B
    Arbeta i branchen:  feature/add-precision-recall
    Sak som ska goras: lagg till "precision" och "recall" i retur-dicten.
    Kom ihag:            skydda mot division by zero (tomma listor).
    Testa med:           python main.py  och  python -m pytest
"""

# Formlerna for precision och recall finns i ../../fasit/lararmaterial_facit.md.
# TODO (Utvecklare B): utvidga med precision och recall i uppgiften
# "feature/add-precision-recall", inklusive nolldivisionsskydd.


def evaluate_predictions(y_true, y_pred):
    """
    Beraknar utvarderingsmatt for klassificeringsmodellen.

    Returnerar: dict med "accuracy" (och efter Dev B: "precision", "recall").
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true och y_pred maste ha samma langd.")

    if len(y_true) == 0:
        return {"accuracy": 0.0}

    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    accuracy = correct / len(y_true)

    return {"accuracy": round(accuracy, 4)}
