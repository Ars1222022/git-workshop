"""Automatiska enhetstester for AI-systemet (kors med pytest)."""

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
