# AI-System: Customer Churn Evaluator

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
