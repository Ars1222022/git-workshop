# 🎓 Lärarmaterial & Facit: Code Review & AI-Utvecklingsworkshop

Detta dokument är avsett för läraren och kursansvarig. Det innehåller fullständiga lösningar (facit) för både Utvecklare A och Utvecklare B, pedagogiska tips samt mönstergiltiga exempel på Code Reviews.

---

## 📂 Systemarkitektur & Filförklaringar

Startrepot `ai-system/` representerar ett stiliserat men realistiskt Machine Learning-system:

1. **`main.py`**
   - **Roll**: Huvudprogram. Kopplar samman datainläsning (`data_loader.py`) med modellutvärdering (`model_evaluator.py`).
   - **Pedagogisk poäng**: Visar hur moduler interagerar och varför ändringar i en modul (t.ex. filtrering av korrupt data) direkt påverkar vad som skickas vidare till nästa del av pipelinen.

2. **`data_loader.py`**
   - **Roll**: Dataladdare.
   - **Problem i startkoden**: Innehåller `{"customer_id": 104, "age": 52, "tenure_months": -5, "churned": 1}`. En kund kan inte ha haft ett abonnemang i -5 månader.
   - **Uppgift Dev A**: Rensa korrupt data.

3. **`model_evaluator.py`**
   - **Roll**: Mätvärdesberäknare.
   - **Problem i startkoden**: Beräknar enbart `accuracy`. I obalanserade dataset (t.ex. churn där endast 5% lämnar) ger 95% accuracy noll värde om modellen gissar 0 på allt.
   - **Uppgift Dev B**: Implementera Precision & Recall med nolldivisionsskydd.

4. **`tests/test_evaluator.py`**
   - **Roll**: Automatiserade enhetstester (`pytest`).
   - **Pedagogisk poäng**: Visar hur båda utvecklarna måste skriva tester som täcker deras nya kodingrepp och verifierar edge-cases inför sin Pull Request.

---

## 🔑 Facit & Källkods-lösningar

### 👨‍💻 Dev A Facit: Indatavalidering i `data_loader.py`

#### `data_loader.py` (Lösning)
```python
"""
Modul för att läsa in och förbereda tränings- och utvärderingsdata för AI-modellen.
"""

def load_dataset():
    """
    Läser in kunddata för churn-prediktion.
    Filtrerar bort korrupta poster där tenure_months < 0.
    """
    raw_data = [
        {"customer_id": 101, "age": 34, "tenure_months": 12, "churned": 0},
        {"customer_id": 102, "age": 45, "tenure_months": 2,  "churned": 1},
        {"customer_id": 103, "age": 23, "tenure_months": 24, "churned": 0},
        {"customer_id": 104, "age": 52, "tenure_months": -5, "churned": 1},  # Korrupt post
        {"customer_id": 105, "age": 29, "tenure_months": 18, "churned": 0},
    ]
    
    # Validering: Behåll endast poster med giltig tenure
    valid_data = [item for item in raw_data if item.get("tenure_months", -1) >= 0]
    return valid_data
```

#### `tests/test_evaluator.py` (Dev A Testtillägg)
```python
def test_load_dataset_filters_invalid_tenure():
    data = load_dataset()
    # Verifiera att inga negativa tenure_months finns kvar
    assert all(item["tenure_months"] >= 0 for item in data)
    # Verifiera att den korrupta posten rensats (4 kvar av 5)
    assert len(data) == 4
```

---

### 👩‍💻 Dev B Facit: Precision & Recall i `model_evaluator.py`

#### `model_evaluator.py` (Lösning)
```python
"""
Modul för att utvärdera AI-modellens prediktioner mot facit.
"""

def evaluate_predictions(y_true, y_pred):
    """
    Beräknar accuracy, precision och recall för klassificeringsmodellen.
    Innehåller skydd för division med noll när inga positiva gissningar görs.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true och y_pred måste ha samma längd.")
    
    if len(y_true) == 0:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0}

    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    tp = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 1)
    fp = sum(1 for true, pred in zip(y_true, y_pred) if true == 0 and pred == 1)
    fn = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 0)

    accuracy = correct / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4)
    }
```

#### `tests/test_evaluator.py` (Dev B Testtillägg)
```python
def test_evaluate_predictions_precision_recall():
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 0]  # TP=1, FP=0, FN=1 -> Precision=1.0, Recall=0.5
    metrics = evaluate_predictions(y_true, y_pred)
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 0.5

def test_evaluate_predictions_zero_division():
    # Edge case: Inga positiva prediktioner (TP+FP == 0)
    y_true = [1, 1, 0, 0]
    y_pred = [0, 0, 0, 0]
    metrics = evaluate_predictions(y_true, y_pred)
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0
```

---

## 💬 Exempel på Mönstergiltig 1+1 Code Review

Använd dessa exempel under lektionen för att visa studenterna vad som kännetecknar en konstruktiv review:

### Exempel 1: Review av Dev A:s PR (skriven av Dev B)
> **`[+]` Vad som är bra:**
> *"Snyggt jobbat med list comprehension i `data_loader.py`! Det är väldigt lättläst och gör koden mycket renare."*
>
> **`[!]` Konkret förbättringspunkt:**
> *"Ditt pytest-fall kollar att alla `tenure_months >= 0`, men det vore ännu säkrare om du också lade till `assert len(data) == 4` för att explicit bekräfta att den ogiltiga posten faktiskt sållades bort. Lägg till det så klickar jag Approve direkt!"*

### Exempel 2: Review av Dev B:s PR (skriven av Dev A)
> **`[+]` Vad som är bra:**
> *"Riktigt bra att du lade till Precision och Recall! Det ger oss en mycket bättre bild av hur modulen presterar på churn-data."*
>
> **`[!]` Konkret förbättringspunkt:**
> *"Jag ser att du har `if (tp + fp) > 0 else 0.0` för precision, vilket är jättebra. Kan du lägga till ett enhetstest i `test_evaluator.py` där `y_pred` bara har nollor så att vi säkerställer i pytest att detta nolldivisionsskydd fungerar?"*

---

## 💡 Pedagogiska Tips för Läraren

1. **Tidsdisciplin**: Se till att studenterna inte fastnar i att skriva komplex Python-kod. Om någon tvekar på matematiken för Precision/Recall, ge dem formlerna direkt. Workshopen handlar om **Git, PR och Code Review**, inte linjär algebra.
2. **AI-användning**: Påminn studenterna om att skriva sin PR-text själva i 2-3 meningar innan de ber Copilot/AI förfina språket. AI ska vara en skrivassistent, inte en ersättning för förståelse.
3. **Squash and Merge**: Visa gärna i helklass på projektorn efter workshopen hur git-historiken på `main` ser ut ren och städad med Squash Merge jämfört med en rörig spagettihistorik.
