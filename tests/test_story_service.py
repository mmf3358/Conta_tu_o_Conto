"""Lightweight tests with model pipelines replaced by stubs."""
from project.app import conta_app


def test_generates_three_choices(monkeypatch):
    monkeypatch.setattr(conta_app, "TRANSLATOR_PT_EN", "mock-pt-en")
    monkeypatch.setattr(conta_app, "TRANSLATOR_EN_PT", "mock-en-pt")
    monkeypatch.setattr(conta_app, "translator", lambda text, model, **kwargs: [{"translation_text": text}])
    monkeypatch.setattr(conta_app, "generate_text", lambda text: [{"generated_text": text + " next chapter"}])
    monkeypatch.setattr(conta_app, "summarizer", lambda text, **kwargs: [{"summary_text": "chapter"}])
    outputs, summaries = conta_app.generate_outputs("Era uma vez")
    assert len(outputs) == len(summaries) == 3
    assert all("next chapter" in output for output in outputs)


def test_rejects_empty_context():
    import pytest
    with pytest.raises(ValueError):
        conta_app.generate_outputs("  ")
