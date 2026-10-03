# 🛠️ Workshop-instruktioner: Professionell Code Review i AI-Projekt (90 min)

Welcome to ML-teamets workshop! I den här övningen kommer ni att arbeta två och två som AI-utvecklare i ett gemensamt Python/ML-projekt (`ai-system`).

---

## 📂 Filöversikt: Vad gör filerna i vårt repo och varför?

Innan ni startar är det viktigt att förstå hur koden i `ai-system/` är uppbyggd:

> **Har ni redan kört STEG 0 nedan? Gör det först** – annars finns
> `ai-system/` inte på er dator.

1. **`main.py` (Systemets Huvudmotor)**
   - **VAD?**: Huvudmanus som binder ihop alla moduler.
   - **VARFÖR?**: I professionell systemdesign vill vi skilja på logik och exekvering (*Separation of Concerns*). `main.py` laddar data, kör simulerade modellförutsägelser och anropar utvärderingsfunktionen.
   - **HUR?**: Körs från terminalen med `python main.py`.

2. **`data_loader.py` (Data Ingestion & Sanering)**
   - **VAD?**: Modul som läser in kunddata för churn-prediktion.
   - **VARFÖR?**: AI-modeller är känsliga för skräpdata (*Garbage in, garbage out*). Denna modul ansvarar för att ladda och filtrera indatan.
   - **HUR?**: Returnerar en lista med kund-dicts. Innehåller från start en korrupt post (`tenure_months: -5`) som Dev A ska sanera.

3. **`model_evaluator.py` (AI-modellens Utvärdering)**
   - **VAD?**: Modul som beräknar prestandamått för AI-modellen.
   - **VARFÖR?**: I klassificeringsproblem (t.ex. churn) räcker inte alltid *Accuracy*. Vi behöver *Precision* och *Recall* för att utvärdera modellen korrekt.
   - **HUR?**: Tar emot `y_true` (facit) och `y_pred` (modellens gissningar) och returnerar en dict med beräknade mätvärden.

4. **`tests/test_evaluator.py` (Automatiserade Pytest-tester)**
   - **VAD?**: Testfil som innehåller automatiska enhetstester (*unit tests*).
   - **VARFÖR?**: Tester garanterar att ny kod inte förstör befintlig funktionalitet (*regressions*) och fungerar som säkerhetsnät inför merge.
   - **HUR?**: Körs från terminalen med kommandot `python -m pytest`.
     *(Alltid `python -m pytest`, inte bara `pytest` – det fungerar på alla operativsystem.)*

5. **`requirements.txt` & `README.md`**
   - **VAD?**: Beroendedefinition (`pytest`) samt projektets dokumentation.
   - **VARFÖR?**: Gör det enkelt för nya utvecklare att komma igång med projektet på under 2 minuter.

---

## ⏱️ Tidsplan & Workshopflöde (90 minuter)

- **10 min**: Genomgång & Systemdesign
- **25 min**: Del 1 — Kodändringar & Första Pull Requesten
- **40 min**: Del 2 — Code Review, Feedback-loop & Merge (2×20 min)
- **15 min**: Del 3 — Integration på `main`, Pytest & Utvärdering

> **Tips för läraren:** Slides och den här filen är i tidsplanen synkade.
> Håll klockan efter Del 2 – den är lätt att dra ut på tiden.

---

## 🚀 Steg-för-steg Instruktioner (VAD? VARFÖR? HUR?)

### STEG 0: Kom igång – gör detta FÖRST (5 min)

> **Det här steget är till för dig som aldrig använt GitHub förut.**
> Gör du detta en gång så fungerar resten av workshopen.
> Den som redan kan GitHub och har konto kan hoppa till STEG 1.

* **VAD?**: Sätta upp GitHub-konto, berätta vem du är mot Git, och hämta ner koden.
* **VARFÖR?**: Git behöver veta ditt namn för att skriva under dina commits.
  Utan konto kan du inte bjuda in din partner eller skapa ett repo.

#### 0.1 Skapa ett GitHub-konto

1. Öppna **github.com** och klicka **Sign up**.
2. Fyll i e-post, lösenord och användarnamn. **Kontot är gratis.**
3. Verifiera din e-post när du får mailet.
4. Logga in.

#### 0.2 Berätta vem du är mot Git

Öppna **terminalen** i mappen `0.1. GitGitHub (workshop)`:

- **Windows**: högerklicka i mappen → *Open with Git Bash*
- **macOS**: Terminal → `cd` till mappen
- **VS Code**: öppna mappen och tryck `` Ctrl+` `` (eller Terminal → New Terminal)

Kör sedan (byt ut ditt namn och din e-post):

```bash
git config --global user.name "Ditt Namn"
git config --global user.email "din@epost.se"
```

Kontrollera att det fungerade:

```bash
git config --global user.name
```

#### 0.3 Hämta ner projektet

Öppna **terminalen i `uppgift/`-mappen** och kör:

```bash
cd uppgift
python workshop_setup.py
```

Skriptet gör allt åt er:

- ✔ Kontrollerar Python, Git och pytest
- ✔ Installerar pytest om den saknas
- ✔ Skapar mappen `ai-system/` (rakt här bredvid)
- ✔ Kör `main.py` och testerna – så ni ser att allt fungerar

**Klart!** Nu har ni `uppgift/ai-system/` på er dator. Gå vidare till STEG 1.

---

### STEG 1: Skapa Repo & Bjuda in Collaborator (5 min)
* **VAD?**: Skapa ett delat repository på GitHub och ge båda utvecklarna skrivrättigheter.
* **VARFÖR?**: För att två personer ska kunna samarbeta i samma kodbas krävs en gemensam fjärrplats på GitHub.
* **HUR?**:
  1. **Utvecklare A**: Gå till GitHub -> *New Repository* -> Döp till `ai-system` -> Skapa.
  2. **Utvecklare A**: Gå till *Settings* -> *Collaborators* -> *Add people* -> Sök på Utvecklare B:s användarnamn och bjud in.
  3. **Utvecklare B**: Gå till din e-post eller GitHub-notifieringar och tacka JA till inbjudan.

---

### STEG 2: Klona Repot Lokalt (5 min)
* **VAD?**: Ladda ner en kopia av kodbasen till er dator i VS Code.
* **VARFÖR?**: Ni redigerar och kör koden i er lokala utvecklingsmiljö, inte direkt på GitHub.
* **HUR?**:
  1. Kör automatiseringsskriptet eller hämta startkoden: `python starter_repo_setup.py`.
  2. Öppna terminalen i VS Code:
     ```bash
     cd ai-system
     git init
     git add .
     git commit -m "feat: initiera ai-system startkod"
     git branch -M main
     git remote add origin https://github.com/<ANVÄNDARNAMN>/ai-system.git
     git push -u origin main
     ```

     > **Viktigt:** raden `cd ai-system` flyttar dig in i projektmappen. Utan den
     > Initierar Git fel mapp och du får "fatal: not a git repository" senare.
  3. **Utvecklare B**: Kör `git clone https://github.com/<ANVÄNDARNAMN>/ai-system.git` i sin VS Code.

---

### STEG 3: Skapa Feature Branch & Kodändring (15 min)
* **VAD?**: Skapa en isolerad kodgren och göra en specifik förbättring.
* **VARFÖR?**: Arbeta aldrig direkt mot `main`! En feature branch gör att du kan utveckla och testa i lugn och ro utan att störa din kollega.
* **HUR?**:

#### 👨‍💻 Utvecklare A (Indatavalidering):
1. Skapa och växla till branch:
   ```bash
   git checkout -b feature/add-data-validation
   ```
2. Öppna `data_loader.py` och filtrera bort poster där `tenure_months < 0`.
3. Öppna `tests/test_evaluator.py` och lägg till ett test som verifierar att inga negativa värden finns kvar efter laddning:
   ```python
   def test_load_dataset_filters_invalid_tenure():
       data = load_dataset()
       assert all(item["tenure_months"] >= 0 for item in data)
   ```
4. Spara filerna och gör commit & push:
   ```bash
   git add .
   git commit -m "fix: lägg till validering för negativa tenure_months"
   git push origin feature/add-data-validation
   ```

#### 👩‍💻 Utvecklare B (Precision & Recall):
1. Skapa och växla till branch:
   ```bash
   git checkout -b feature/add-precision-recall
   ```
2. Öppna `model_evaluator.py` och utöka `evaluate_predictions()` med beräkning för `precision` och `recall` (inklusive nolldivisionsskydd `if (tp + fp) > 0 else 0.0`).
3. Öppna `tests/test_evaluator.py` och lägg till ett test som verifierar beräkningarna:
   ```python
   def test_evaluate_predictions_precision_recall():
       y_true = [1, 1, 0, 0]
       y_pred = [1, 0, 0, 0]
       metrics = evaluate_predictions(y_true, y_pred)
       assert metrics["precision"] == 1.0
       assert metrics["recall"] == 0.5
   ```
4. Spara filerna och gör commit & push:
   ```bash
   git add .
   git commit -m "feat: utöka utvärdering med precision och recall"
   git push origin feature/add-precision-recall
   ```

---

### STEG 4: Skapa Pull Request (PR) med AI-assistans (10 min)
* **VAD?**: Skapa en begäran på GitHub om att merga din branchens kod till `main`.
* **VARFÖR?**: En PR beskriver *vad* du ändrat och *varför*, vilket gör det enkelt för din kollega att granska koden.
* **HUR?**:
  1. Gå till repot på GitHub. Du ser en gul knapp: *"Compare & pull request"*. Klicka på den.
  2. **Viktigt steg! Skriv PR-beskrivningen själv först!**
     - *Titel*: Tydlig sammanfattning (t.ex. `feat: add data validation for tenure_months`).
     - *Beskrivning*: Förklara med egna ord varför ändringen behövs och vad du testat.
  3. **Använd AI som assistent**:
     - Klistra in din skrivna PR-text i Copilot/ChatGPT och fråga: *"Hur kan jag göra min PR-beskrivning mer professionell och strukturera den i punktform?"*
     - Förfina din text utifrån AI-förslaget och klicka på **"Create Pull Request"**.

---

### STEG 5: 1+1 Code Review & Feedback-loop (40 min)

**WORKSHOPREGEL**: Alla Pull Requests MÅSTE godkännas av en kollega innan merge!

#### 🔄 Runda 1: Utvecklare A granskar Utvecklare B (20 min)
1. **Dev A**: Gå till fliken *Pull Requests* på GitHub och öppna Dev B:s PR.
2. **Dev A**: Klicka på *Files changed* och granska koden utifrån **1+1-regeln**:
   - `[+]` **1 Beröm**: Lämna en positiv kommentar på en rad som är välskriven (t.ex. *"Snyggt nolldivisionsskydd för precision!"*).
   - `[!]` **1 Förbättringspunkt**: Lämna ett konkret konstruktivt förslag (t.ex. *"Vad händer om `y_true` är tom? Kan du lägga till ett pytest-fall för det edge-caset?"*).
   - Välj *Comment* eller *Request changes*.
3. **Dev B (Feedback-loopen)**:
   - Öppna koden lokalt i VS Code och lägg till det efterfrågade testet eller förbättringen.
   - Spara, commit och pusha på **samma feature branch**:
     ```bash
     git add .
     git commit -m "test: lägg till edge-case test för tomma listor"
     git push origin feature/add-precision-recall
     ```
   - **Notera!** GitHub uppdaterar automatiskt PR-sidan med den nya committen!
4. **Dev A**: Se att PR-sidan uppdaterats, klicka på *Review changes* -> Välj **Approve** -> Klicka på **Squash and Merge**!

#### 🔁 Runda 2: Byt roller! Utvecklare B granskar Utvecklare A (20 min)
1. Dev B genomför exakt samma 1+1 Code Review på Dev A:s PR (`feature/add-data-validation`).
2. Dev A åtgärdar koden lokalt i VS Code, gör `commit` och `push`.
3. Dev B verifierar ändringen på GitHub, ger **Approve** och klickar på **Squash and Merge**!

---

### STEG 6: Slutintegration & Pytest på main (15 min)
* **VAD?**: Hämta den färdiga och godkända koden till er lokala `main`-branch och verifiera att hela systemet fungerar.
* **VARFÖR?**: För att säkerställa att båda utvecklarnas ändringar nu är integrerade och fungerar perfekt tillsammans.
* **HUR?**:
  1. Båda utvecklarna kör i terminalen:
     ```bash
     git checkout main
     git pull origin main
     ```
  2. Kör hela AI-pipelinen:
     ```bash
     python main.py
     ```
  3. Kör alla automatiserade enhetstester:
     ```bash
     python -m pytest
     ```
  4. Fira! Båda era funktioner är nu i produktion på `main` med 100% passerande tester! 🎉

---

## ⚡ Vad gör jag om en Merge-konflikt uppstår?

Om båda utvecklarna har ändrat på samma rad i samma fil under workshopen:
1. Växla till `main` och hämta senaste koden: `git checkout main && git pull origin main`.
2. Växla tillbaka till din branch och merga `main`: `git checkout feature/din-branch && git merge main`.
3. VS Code visar konfliktskyltarna (`<<<<<<< HEAD` vs `>>>>>>> main`).
4. Diskutera med din kollega, välj **"Accept Current Change"** eller **"Accept Incoming Change"**, spara filen, och kör:
   ```bash
   git add .
   git commit -m "fix: resolve merge conflict with main"
   git push origin feature/din-branch
   ```
