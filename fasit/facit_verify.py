#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fasit_verify.py - lararens facitkontroll.

Kopierar in Dev A:s och Dev B:s losningar i en temporar kopia av
startrepot, kor hela testsviten och skriver ut ett meddelande till klassen.
Anvands INTE av studenterna.

Losningarna hardas INTE in i detta skript - de hamtas fran
facit_dev_a_data_loader.py och facit_dev_b_model_evaluator.py via
inspect.getsource(). Da finns det bara en kalla pa varje losning.

    python fasit_verify.py
    python fasit_verify.py --kopiera   # losningarna skrivs in i ai-system/
"""

from __future__ import annotations

import argparse
import inspect
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HAR = Path(__file__).resolve().parent
ROT = HAR.parent
# Startprojektet ligger i uppgift/ (inte direkt i workshoproten).
KALLA = ROT / "uppgift" / "ai-system"

sys.path.insert(0, str(HAR))
import facit_dev_a_data_loader as FA  # noqa: E402
import facit_dev_b_model_evaluator as FB  # noqa: E402


def _rad(t: str = "") -> None:
    try:
        print(t)
    except UnicodeEncodeError:
        print(t.encode("ascii", "replace").decode("ascii"))


def _kalla(modul) -> str:
    """Returnerar hela modulens kalla - det ar losningen for filen."""
    return Path(modul.__file__).read_text(encoding="utf-8")


def bygg_testkopia(mal: Path) -> Path:
    """Kopierar startrepot och skriver in bada losningarna."""
    shutil.copytree(KALLA, mal / "ai-system")
    repo = mal / "ai-system"
    (repo / "data_loader.py").write_text(_kalla(FA), encoding="utf-8",
                                        newline="\n")
    (repo / "model_evaluator.py").write_text(_kalla(FB), encoding="utf-8",
                                             newline="\n")

    # Facitets tester - samma krav som i lararmaterial_facit.md
    tester = (
        "from data_loader import load_dataset\n"
        "from model_evaluator import evaluate_predictions\n\n\n"
        "def test_A_sanerar_korrupt_data():\n"
        "    data = load_dataset()\n"
        "    assert all(r['tenure_months'] >= 0 for r in data)\n"
        "    assert len(data) == 4\n\n\n"
        "def test_A_behaller_giltiga_kunder():\n"
        "    ids = {r['customer_id'] for r in load_dataset()}\n"
        "    assert ids == {101, 102, 103, 105}\n\n\n"
        "def test_B_precision_recall():\n"
        "    m = evaluate_predictions([1, 1, 0, 0], [1, 0, 0, 0])\n"
        "    assert m['precision'] == 1.0\n"
        "    assert m['recall'] == 0.5\n\n\n"
        "def test_B_nolldivision():\n"
        "    m = evaluate_predictions([1, 1, 0, 0], [0, 0, 0, 0])\n"
        "    assert m['precision'] == 0.0\n"
        "    assert m['recall'] == 0.0\n\n\n"
        "def test_B_tomma_listor():\n"
        "    assert evaluate_predictions([], [])['accuracy'] == 0.0\n\n\n"
        "def test_length_mismatch_raises():\n"
        "    import pytest\n"
        "    with pytest.raises(ValueError):\n"
        "        evaluate_predictions([1, 0], [1])\n\n\n"
        "def test_regression_accuracy():\n"
        "    m = evaluate_predictions([1, 1, 0, 0], [1, 1, 0, 1])\n"
        "    assert m['accuracy'] == 0.75\n\n\n"
        "def test_pipelinen_ger_alla_tre_matten():\n"
        "    data = load_dataset()\n"
        "    y_true = [r['churned'] for r in data]\n"
        "    y_pred = [1 if r.get('tenure_months', 0) <= 2 else 0 "
        "for r in data]\n"
        "    m = evaluate_predictions(y_true, y_pred)\n"
        "    assert set(m) >= {'accuracy', 'precision', 'recall'}\n"
        "    assert len(data) == 4\n"
    )
    (repo / "tests" / "test_facit.py").write_text(tester, encoding="utf-8",
                                                 newline="\n")
    return repo


def main() -> int:
    p = argparse.ArgumentParser(description="Verifiera workshopens facit.")
    p.add_argument("--kopiera", action="store_true",
                   help="Skriv losningarna in i ai-system/ (for demo)")
    args = p.parse_args()

    _rad("=" * 62)
    _rad(" FASITVERIFIERING - lararens kontroll")
    _rad("=" * 62)

    if not KALLA.exists():
        _rad("[FEL] uppgift/ai-system/ saknas. Kors uppgift/workshop_setup.py forst.")
        return 1

    klar = False
    with tempfile.TemporaryDirectory(prefix="facit_") as tmp:
        repo = bygg_testkopia(Path(tmp))

        _rad("")
        _rad("--- main.py med Dev A + Dev B ---")
        r = subprocess.run([sys.executable, "main.py"], cwd=str(repo),
                           capture_output=True, text=True, timeout=120)
        for line in r.stdout.splitlines():
            _rad("  " + line)
        if r.returncode != 0:
            _rad("  [FEL] main.py kraschade:")
            _rad("  " + (r.stderr.strip().splitlines() or ["?"])[-1])

        _rad("")
        _rad("--- pytest ---")
        r = subprocess.run([sys.executable, "-m", "pytest", "-v"],
                           cwd=str(repo), capture_output=True, text=True,
                           timeout=300)
        for line in r.stdout.strip().splitlines():
            _rad("  " + line)
        klar = r.returncode == 0

    _rad("")
    _rad("=" * 62)
    if klar:
        _rad(" FACIT: ALLA TESTER PASSERAR - losningarna ar korrekta.")
    else:
        _rad(" FACIT: TESTER MISSLYCKADES - se outputen ovan.")
    _rad("=" * 62)

    if args.kopiera:
        _rad("")
        _rad("Skriver losningarna in i ai-system/ ...")
        (KALLA / "data_loader.py").write_text(_kalla(FA), encoding="utf-8",
                                              newline="\n")
        (KALLA / "model_evaluator.py").write_text(_kalla(FB), encoding="utf-8",
                                                 newline="\n")
        _rad("[KLART] Atterstall startkoden med:")
        _rad("   python workshop_setup.py --recreate")

    return 0 if klar else 1


if __name__ == "__main__":
    sys.exit(main())