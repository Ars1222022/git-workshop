# GitHub-workshop: Professionell Code Review & Teamflöde

Workshop (90 minuter) där studenterna arbetar **i par** som AI-utvecklare i ett
gemensamt Python-projekt och lär sig det riktiga flödet:

**Feature branch → Pull Request → Code Review → Feedback → Squash & Merge → pytest**

---

## Snabbstart (studenter)

### 1. Installera verktyg (en gång)

| Verktyg | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Python 3.9+ | python.org (kryssa i *Add to PATH*) | brew install python | sudo apt install python3 |
| Git | git-scm.com/download/win | brew install git | sudo apt install git |
| VS Code | code.visualstudio.com | – | – |

### 2. Skapa GitHub-konto och sätt ditt namn (en gång)

Har du redan konto? Hoppa till steg 3.

1. Gå till **github.com** → **Sign up** (kontot är gratis).
2. Berätta vem du är mot Git – i terminalen i denna mapp:

```bash
git config --global user.name "Ditt Namn"
git config --global user.email "din@epost.se"
```

### 3. Kör setup (ett kommando)

```bash
cd uppgift
python workshop_setup.py
```

Skriptet kontrollerar och **fixar automatiskt**:

- ✔ Python-version
- ✔ Git – ger installationslänk om den saknas
- ✔ pytest – installerar den om den saknas
- ✔ Git-användarnamn – säger till om det inte är satt
- ✔ Skapar `ai-system/`
- ✔ Kör `main.py` och `pytest` för att bevisa att allt fungerar

> Fungerar från **valfri mapp** och på **Windows, macOS och Linux**.

### 4. Följ instruktionerna

Öppna **`workshop_instruktioner.md`** – steg för steg med VAD/VARFÖR/HUR.

---

## Gör så här i ordning

| # | Vad du gör | Var |
|---|-----------|-----|
| 1 | Installera Python, Git, VS Code | Steg 1 ovan |
| 2 | Skapa GitHub-konto | github.com → Sign up |
| 3 | Sätt ditt namn i Git | `git config --global ...` |
| 4 | Hämta ner koden | `cd uppgift` → `python workshop_setup.py` |
| 5 | Skapa repot på GitHub | Instruktioner STEG 1 |
| 6 | Bjud in din partner | Instruktioner STEG 1 |
| 7 | Klona repot lokalt | Instruktioner STEG 2 |
| 8 | Skapa din branch | Instruktioner STEG 2 |
| 9 | Skriv din kod | Instruktioner STEG 3 |
| 10 | Testa lokalt | `python main.py` + `python -m pytest` |
| 11 | Commit & push | Instruktioner STEG 3 |
| 12 | Öppna Pull Request | Instruktioner STEG 4 |
| 13 | Granska varandras kod | Instruktioner STEG 5 |
| 14 | Squash & merge | Instruktioner STEG 5 |
| 15 | Verifiera på `main` | Instruktioner STEG 6 |

**Exakt vilka kommandon** står i `workshop_instruktioner.md`.

---

## Filöversikt

Mappen har **två mappar**: `uppgift/` som studenterna arbetar i och `fasit/`
som bara du behöver.

| Fil | För vem | Beskrivning |
|-----|---------|-------------|
| `0._DevOps_(workshop)-v7.pptx` | Alla | **Huvudpresentationen** – 8 slides, matchar allt annat |
| `README.md` | Alla | Den här filen – starta här |
| `workshop_instruktioner.md` | Studenter | **Steg-för-steg (STEG 0–6)** – det eleven följer |
| `uppgift/` | Studenter | Startkoden + setup-skripten |
| `uppgift/workshop_setup.py` | Studenter | Kontroll + installation + verifiering |
| `uppgift/starter_repo_setup.py` | Alla | Skapar `uppgift/ai-system/` (anropas av setup) |
| `uppgift/ai-system/` | Studenter | Grundprojektet – skapas av setup |
| `fasit/` | Lärare | Lösningar + verifiering (dela inte med studenter) |
| `fasit/lararmaterial_facit.md` | Lärare | Lösningar, mönstergiltiga reviews, tips |

### Projektet `uppgift/ai-system/`

Det här är **grundprojektet** – koden studenterna arbetar i:

```
ai-system/
├── main.py               Huvudmotor – binder ihop modulerna
├── data_loader.py        Dataladdning och sanering     ← Uppgift A
├── model_evaluator.py    Accuracy / Precision / Recall ← Uppgift B
├── requirements.txt      Beroenden (pytest)
├── README.md
└── tests/
    └── test_evaluator.py Enhetstester
```

Det skapas av `python workshop_setup.py` (kör från `uppgift/`), så **du kan
rada bott hela `ai-system/` och skapa om den när som helst**.

**Två uppgifter, ingen konflikt** (de ligger i olika filer):

- **Dev A** – sanera `data_loader.py`: posten `tenure_months: -5` är korrupt.
- **Dev B** – utvidga `model_evaluator.py` med `precision` och `recall`.

---

## Vanliga problem

**"pytest känns inte igen"**
Använd alltid `python -m pytest` (fungerar oavsett PATH). Installera med
`python -m pip install pytest`.

**"pytest: kommandot hittades inte" på Windows**
Kör `python -m pytest` istället. Eller installera om pytest.

**"PowerShell körd inte: Running Scripts is disabled"**
Kör VS Code-terminalen med *Git Bash* istället för PowerShell.

**Git avvisar min branch (rejected)**
Din branch ligger bakom `main`. Kör:
`git fetch origin` → `git rebase origin/main` → `git push --force-with-lease`

**Merge-konflikt**
Se avsnittet *Vad gör jag om en Merge-konflikt uppstår?* i
`workshop_instruktioner.md`, eller slide 5 i presentationen.

**Starta om helt från början**
```bash
cd uppgift
python workshop_setup.py --recreate
```

---

## För läraren

Kör facitkontrollen före lektionen:

```bash
python fasit/facit_verify.py
```

Det kopierar lösningarna till en temporär mapp, kör hela testsviten och
bekräftar att allt är korrekt – utan att röra studenternas filer.

Se `fasit/lararmaterial_facit.md` för lösningar, mönstergiltiga code reviews
och pedagogiska tips.