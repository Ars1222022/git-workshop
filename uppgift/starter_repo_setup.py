#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starter_repo_setup.py - skapar startrepot "ai-system/" for workshopen.

Kors fran VALFRI mapp: alla sokvargar utgar fran den har filens placering.

    python starter_repo_setup.py                  # skapar ./ai-system intill filen
    python starter_repo_setup.py --dir C:\\temp   # skapar i valfri mapp
    python starter_repo_setup.py --force          # skriver over

Endast standardbiblioteket. Inget anpassat till operativsystem.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJEKT = "ai-system"
SLUT_UT = "[KLART]"


def _rad(text: str = "") -> None:
    """Skriver en rad. Tolerant mot konsoler som inte klarar UTF-8."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def _skriv(svag: Path, innehall: str) -> None:
    """Skriver fil med UTF-8 och Unix-radbrytningar (git-vanligt)."""
    svag.parent.mkdir(parents=True, exist_ok=True)
    svag.write_text(innehall, encoding="utf-8", newline="\n")


REQUIREMENTS = """pytest>=7.0.0
"""

DATA_LOADER = '''"""
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
'''

MODEL_EVALUATOR = '''"""
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
'''
MAIN = '''"""
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
'''


TESTS = '''"""Automatiska enhetstester for AI-systemet (kors med pytest)."""

from data_loader import load_dataset
from model_evaluator import evaluate_predictions


def test_load_dataset_returns_list():
    data = load_dataset()
    assert isinstance(data, list)
    assert len(data) > 0


def test_evaluate_predictions_accuracy():
    y_true = [1, 1, 0, 0]
    y_pred = [1, 1, 0, 1]  # 3 av 4 ratt = 0.75
    results = evaluate_predictions(y_true, y_pred)
    assert results["accuracy"] == 0.75


def test_evaluate_predictions_empty():
    results = evaluate_predictions([], [])
    assert results["accuracy"] == 0.0
'''

GITIGNORE = """__pycache__/
*.py[cod]
.pytest_cache/
.venv/
venv/
env/
.env
.DS_Store
Thumbs.db
"""

README = """# AI-System: Customer Churn Evaluator

Startkod for workshopen om professionell Code Review och Pull Requests.

## Snabbstart

```bash
pip install -r requirements.txt
python main.py
pytest
```

## Projektstruktur

    ai-system/
    |-- main.py               Huvudmotor - binder ihop modulerna
    |-- data_loader.py        Dataladdning och sanering    (Uppgift: Dev A)
    |-- model_evaluator.py    Accuracy/Precision/Recall    (Uppgift: Dev B)
    |-- requirements.txt      Beroenden
    `-- tests/
        `-- test_evaluator.py Enhetstester (pytest)

## Workshopregler

1. Arbeta ALDRIG direkt pa `main` - skapa alltid en `feature/`-branch.
2. Ingen kod mergas utan godkannande fraan en kollega.
3. Anvand **1+1-regeln** vid review: en berom `[+]` och en konkret
   forbattringspunkt `[!]`.

## Ditt ansvar

* **Utvecklare A** - sanera `data_loader.py` (posten med `tenure_months: -5`)
  och skriv ett pytest-fall som bevisar att den forsvann.
* **Utvecklare B** - utvidga `model_evaluator.py` med `precision` och `recall`
  inklusive nolldivisionsskydd, och skriv pytest-fall for bada.

Fullstandiga losningar finns i `../../fasit/` (for lararen).
"""


def bygg(mal: Path, tvinga: bool = False) -> bool:
    """Skapar hela startrepot. Returnerar True vid framgang."""
    tests = mal / "tests"

    # Safety: krocka inte med en beintlig branch-mapp.
    if (mal / ".git").exists() and not tvinga:
        print(f"  {SLUT_UT} {mal} ar redan ett git-repo.")
        print("       Anvand --force for att skriva over (danner historiken!).")
        return False

    mal.mkdir(parents=True, exist_ok=True)
    tests.mkdir(parents=True, exist_ok=True)

    filer = {
        mal / "requirements.txt": REQUIREMENTS,
        mal / "data_loader.py": DATA_LOADER,
        mal / "model_evaluator.py": MODEL_EVALUATOR,
        mal / "main.py": MAIN,
        tests / "test_evaluator.py": TESTS,
        mal / ".gitignore": GITIGNORE,
        mal / "README.md": README,
    }

    for svag, innehall in filer.items():
        _skriv(svag, innehall)
        print(f"  skrev {svag.relative_to(mal.parent)}")

    # Verifiera att genererad kod faktiskt kan tolkas av Python.
    fel = []
    for svag in filer:
        if svag.suffix == ".py":
            try:
                compile(svag.read_text(encoding="utf-8"), str(svag), "exec")
            except SyntaxError as exc:
                fel.append(f"{svag}: {exc}")

    if fel:
        print("  FEL - genererad kod har syntaxfel:")
        for f in fel:
            print(f"    {f}")
        return False

    print(f"  {SLUT_UT} Startrepot skapat: {mal.resolve()}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Skapa startrepot ai-system/ for Code Review-workshopen.")
    parser.add_argument("--dir", default=None,
                        help="Var startrepot ska skapas "
                             "(standard: intill denna fil).")
    parser.add_argument("--force", action="store_true",
                        help="Skriv over even om .git redan finns.")
    args = parser.parse_args()

    # Allt utgar harifran -> fungerar oavsett vilken mapp du star i.
    bas = (Path(args.dir).expanduser().resolve() if args.dir
           else Path(__file__).resolve().parent)
    mal = bas / PROJEKT

    _rad("=" * 62)
    _rad(" STARTER REPO - ai-system/")
    _rad("=" * 62)

    if sys.version_info < (3, 9):
        _rad(f"  FEL: Python {sys.version_info.major}.{sys.version_info.minor} "
             "ar for gammal. Behover 3.9 eller nyare.")
        _rad("       Installera fran https://www.python.org/downloads/")
        return 1

    _rad(f"  Python {sys.version.split()[0]} OK")
    _rad(f"  Mal: {mal}")
    _rad("")
    return 0 if bygg(mal, args.force) else 1


if __name__ == "__main__":
    sys.exit(main())
