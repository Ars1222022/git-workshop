#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workshop_setup.py - ett kommando for att komma igang med workshopen.

Kors fran VALFRI mapp. Endast standardbiblioteket.

    python workshop_setup.py              # kontrollera + skapa startrepot
    python workshop_setup.py --check      # bara kontrollera (inga andringar)
    python workshop_setup.py --recreate   # skapa om startrepot pa nytt

Vad skriptet gor
----------------
1.  Kontrollerar Python-version.
2.  Kontrollerar att Git ar installerat (och ger instruktion annars).
3.  Kontrollerar/ installerar pytest.
4.  Skapar startrepot ai-system/.
5.  Kor python main.py och pytest for att bevisa att allt fungerar.

Alla fel rapporteras i klartext med en konkret losning - inte en traceback.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJEKT = HERE / "ai-system"

GRON = "[OK]  "
GUL = "[OBS] "
ROD = "[FEL] "


def _rad(t: str = "") -> None:
    try:
        print(t)
    except UnicodeEncodeError:
        print(t.encode("ascii", "replace").decode("ascii"))


def _rubrik(text: str) -> None:
    _rad()
    _rad("-" * 62)
    _rad(f" {text}")
    _rad("-" * 62)


def kontrollera_python() -> bool:
    _rubrik("1. Python")
    if sys.version_info < (3, 9):
        _rad(f"{ROD}Python {sys.version_info.major}.{sys.version_info.minor} "
             "ar for gammal. Behover 3.9 eller nyare.")
        _rad("     Installera: https://www.python.org/downloads/")
        _rad("     Windows: kryssa i 'Add Python to PATH' vid installation.")
        return False
    _rad(f"{GRON}Python {sys.version.split()[0]} pa {sys.executable}")
    return True


def kontrollera_git() -> bool:
    _rubrik("2. Git")
    git = shutil.which("git")
    if not git:
        _rad(f"{ROD}Git ar INTE installerat. Installera:")
        _rad("       Windows: https://git-scm.com/download/win")
        _rad("       macOS:   brew install git")
        _rad("       Linux:   sudo apt install git")
        return False
    try:
        res = subprocess.run([git, "--version"], capture_output=True,
                             text=True, timeout=15)
        version = res.stdout.strip() or "okant version"
    except Exception:  # noqa: BLE001
        version = "okant version"
    _rad(f"{GRON}{version}")
    _rad(f"{GRON}Installerat i: {git}")

    try:
        cfg = subprocess.run([git, "config", "--get", "user.name"],
                             capture_output=True, text=True, timeout=15)
        if not cfg.stdout.strip():
            _rad(f"{GUL}Git anvandarnamn ar INTE sat. Kora:")
            _rad("       git config --global user.name \"Ditt Namn\"")
            _rad("       git config --global user.email \"du@exempel.se\"")
    except Exception:  # noqa: BLE001
        pass
    return True


def hitta_pytest() -> bool:
    _rubrik("3. pytest")
    try:
        koll = subprocess.run([sys.executable, "-m", "pytest", "--version"],
                              capture_output=True, text=True, timeout=60)
        if koll.returncode == 0:
            _rad(f"{GRON}pytest ar installerat: {koll.stdout.strip()}")
            return True
    except Exception:  # noqa: BLE001
        pass

    _rad(f"{GUL}pytest saknas - forsoker installera...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest"],
                       capture_output=True, text=True, timeout=300)
        koll = subprocess.run([sys.executable, "-m", "pytest", "--version"],
                              capture_output=True, text=True, timeout=60)
        if koll.returncode == 0:
            _rad(f"{GRON}pytest installerades: {koll.stdout.strip()}")
            return True
    except Exception as exc:  # noqa: BLE001
        _rad(f"{ROD}Kunde inte installera pytest automatiskt ({exc}).")
    _rad(f"{ROD}Installera manuellt:")
    _rad(f"     {sys.executable} -m pip install pytest")
    return False
def skapa_startrepo(ta_bort: bool = False) -> bool:
    _rubrik("4. Startrepo ai-system/")
    setup = HERE / "starter_repo_setup.py"
    if not setup.exists():
        _rad(f"{ROD}Hittar inte starter_repo_setup.py intill detta skript.")
        return False

    if ta_bort and PROJEKT.exists():
        shutil.rmtree(PROJEKT)
        _rad(f"{GRON}Raderade gammal {PROJEKT.name}/")

    res = subprocess.run([sys.executable, str(setup), "--dir", str(HERE)],
                         capture_output=True, text=True, timeout=120)
    for line in res.stdout.splitlines():
        _rad("  " + line)
    if res.returncode != 0:
        _rad(f"{ROD}startrepo_setup.py misslyckades.")
        if res.stderr.strip():
            _rad("     " + res.stderr.strip().splitlines()[-1])
        return False
    return True


def testa_startrepo() -> bool:
    _rubrik("5. Verifierar att koden fungerar")
    if not (PROJEKT / "main.py").exists():
        _rad(f"{ROD}ai-system/main.py saknas.")
        return False

    res = subprocess.run([sys.executable, "main.py"], cwd=str(PROJEKT),
                         capture_output=True, text=True, timeout=120)
    if res.returncode != 0:
        _rad(f"{ROD}python main.py kraschade.")
        _rad("     " + (res.stderr.strip().splitlines() or ["okant fel"])[-1])
        return False
    _rad(f"{GRON}python main.py fungerar")

    res = subprocess.run([sys.executable, "-m", "pytest", "-q"],
                         cwd=str(PROJEKT), capture_output=True, text=True,
                         timeout=300)
    sista = (res.stdout.strip().splitlines() or ["okant"])[-1]
    if res.returncode != 0:
        _rad(f"{ROD}pytest misslyckades: {sista}")
        return False
    _rad(f"{GRON}pytest: {sista}")
    return True


def sammanfattning(ok: bool) -> None:
    _rad()
    _rad("=" * 62)
    if ok:
        _rad(" ALLT KLART. Du kan borja workshopen.")
        _rad("")
        _rad("  1. Följ workshop_instruktioner.md steg för steg.")
        _rad(f"  2. Projektet ligger i: {PROJEKT}")
        _rad("  3. Verifiera själv:")
        _rad(f"       cd \"{PROJEKT}\"")
        _rad(f"       {sys.executable} main.py")
        _rad(f"       {sys.executable} -m pytest")
    else:
        _rad(" NAGOT GICK INTE. Los problemen ovan och kor om.")
    _rad("=" * 62)


def main() -> int:
    parser = argparse.ArgumentParser(description="Setup for GitGitHub-workshopen.")
    parser.add_argument("--check", action="store_true",
                        help="Kontrollera utan att skapa nagot.")
    parser.add_argument("--recreate", action="store_true",
                        help="Skapa om startrepot pa nytt.")
    args = parser.parse_args()

    _rad("=" * 62)
    _rad(" WORKSHOP-SETUP: Git, GitHub, Code Review & PR")
    _rad("=" * 62)
    _rad(f" Mapp: {HERE}")

    steg = [kontrollera_python(), kontrollera_git(), hitta_pytest()]
    if not args.check:
        steg += [skapa_startrepo(args.recreate), testa_startrepo()]

    ok = all(steg)
    sammanfattning(ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())