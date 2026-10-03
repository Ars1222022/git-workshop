# FASIT – Fullständiga lösningar

**Till läraren. Dela inte ut den här mappen till studenterna.**

## Innehåll

| Fil | Innehåll |
|-----|----------|
| `facit_dev_a_data_loader.py` | Lösning till uppgift A (datasanering) + testtillägg |
| `facit_dev_b_model_evaluator.py` | Lösning till uppgift B (precision/recall) + testtillägg |
| `facit_verify.py` | Automatisk kontroll av att lösningarna fungerar |

## Verifiera lösningarna

```bash
python facit_verify.py
```

Skriptet:

1. Kopierar `ai-system/` till en temporär mapp
2. Skriver in båda lösningarna
3. Kör `main.py` – visar att integrationen fungerar
4. Kör hela testsviten (11 tester)
5. Bekräftar **PASSERAR** eller **MISSLYCKADES**

Ingenting i `ai-system/` påverkas.

### Visa lösningen i klassen

```bash
python facit_verify.py --kopiera
```

Skriver lösningarna in i `ai-system/`. Återställ startkoden efteråt med:

```bash
python ../uppgift/workshop_setup.py --recreate
```

---

## Varför lösningarna är skrivna så här

**Dev A** filtrerar med en list comprehension:

```python
return [dict(r) for r in RAW_DATA if r["tenure_months"] >= 0]
```

Enkel, tydlig och lätt att granska – precis det vi vill lära ut.
Studenter får gärna hitta på egna lösningar.

**Dev B** innehåller *nolldivisionsskydd*:

```python
precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
```

Detta är exakt den förbättringspunkt som 1+1-regeln pekar på – använd den
i demonstrationen.

---

## Facitets krav (11 tester)

| Test | Krav |
|------|------|
| `test_A_sanerar_korrupt_data` | Inga negativa värden, exakt 4 rader kvar |
| `test_A_behaller_giltiga_kunder` | Giltiga kunder rörs inte |
| `test_B_precision_recall` | precision = 1.0, recall = 0.5 |
| `test_B_nolldivision` | Inga crash när modellen gissar alltid 0 |
| `test_B_tomma_listor` | Tomma listor ger 0.0, inte fel |
| `test_length_mismatch_raises` | ValueError vid olängd |
| `test_regression_accuracy` | Ursprungstestet överlever |
| `test_pipelinen_ger_alla_tre_matten` | A + B integrerar på main |

**Acceptera alternativa studentlösningar** så länge testerna passerar –
det viktiga är att studenterna kan *förklara* sin kod i granskningen.