"""
Huvudmanus som binder ihop dataladdning och utvardering i AI-systemet.

Korrigat: y_true och y_pred byggs nu av SAMMA datamangd, sa att pipelinen
aldrig kastar ValueError. Antalet rader och antalet ogiltiga rader skrivs ut,
sa att du ser effekten av din egen sanering.
"""

from data_loader import load_dataset
from model_evaluator import evaluate_predictions


def hitta_ogiltiga(data):
    """Returnerar de rader som har omojliga (negativa) tenure_months."""
    return [r for r in data if r.get("tenure_months", -1) < 0]


def simulera_modell(data):
    """Deterministisk modell: gissar churn om kunden varit kort tid kund."""
    return [1 if r.get("tenure_months", 0) <= 2 else 0 for r in data]


def run_pipeline():
    print("=== Startar AI-System Pipeline ===")

    # 1. Ladda data
    data = load_dataset()
    print(f"Laddade {len(data)} rader kunddata.")

    # 2. Datakvalitet - synliggjor da saneringen sker
    ogiltiga = hitta_ogiltiga(data)
    if ogiltiga:
        ids = ", ".join(str(r["customer_id"]) for r in ogiltiga)
        print(f"  VARNING: {len(ogiltiga)} rad(er) med ogiltigt "
              f"tenure_months (customer_id: {ids})")
        print("  -> Utvecklare A: filtrera bort dessa i data_loader.py")
    else:
        print("  OK: inga ogiltiga rader kvar.")

    # 3. Facit och prediktioner - alltid samma langd
    y_true = [r["churned"] for r in data]
    y_pred = simulera_modell(data)

    # 4. Utvardera
    metrics = evaluate_predictions(y_true, y_pred)
    print()
    print("--- Utvarderingsresultat ---")
    for namn, varde in metrics.items():
        print(f"{namn.capitalize()}: {varde}")


if __name__ == "__main__":
    run_pipeline()
