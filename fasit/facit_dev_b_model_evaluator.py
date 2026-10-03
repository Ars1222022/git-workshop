# -*- coding: utf-8 -*-
"""
FASIT - Dev B: losning for model_evaluator.py

Kopiera innehallet over ai-system/model_evaluator.py (eller jamfor).

Varfor overhuvudtaget precision och recall?
I churn-data slutar kanske 5 av 100 kunder. En modell som alltid gissar
"ingen lamnar" far accuracy = 95 % - och ar fullstendigt oanvandbar.
Precision och recall fangar just den farligheten.
"""


def evaluate_predictions(y_true, y_pred):
    """
    Beraknar accuracy, precision och recall for klassificeringsmodellen.

    Innehaller skydd for division med noll nar modellen inte gissar
    nagra positiva fall alls (TP + FP = 0).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true och y_pred maste ha samma langd.")

    if len(y_true) == 0:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0}

    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)

    accuracy = correct / len(y_true)
    # Nolldivisionsskydd - detta ar det reviewern begar i steg 2.
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
    }


# ---------------------------------------------------------------------------
# Testtillagg - kopiera in i tests/test_evaluator.py
# ---------------------------------------------------------------------------
TEST_DEV_B = '''
def test_evaluate_predictions_precision_recall():
    """TP=1, FP=0, FN=1 -> Precision=1.0, Recall=0.5"""
    metrics = evaluate_predictions([1, 1, 0, 0], [1, 0, 0, 0])
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 0.5


def test_evaluate_predictions_zero_division():
    """Edge case: modellen gissar aldrig 1 -> precision ska vara 0.0, inte crash."""
    metrics = evaluate_predictions([1, 1, 0, 0], [0, 0, 0, 0])
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0


def test_evaluate_predictions_empty_lists():
    metrics = evaluate_predictions([], [])
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0
'''


if __name__ == "__main__":
    m = evaluate_predictions([1, 1, 0, 0], [1, 0, 0, 0])
    print("Dev B losning - testfall 1:")
    for k, v in m.items():
        print(f"  {k}: {v}")
    print("\nTesttillagg att kopiera in i tests/test_evaluator.py:")
    print(TEST_DEV_B)