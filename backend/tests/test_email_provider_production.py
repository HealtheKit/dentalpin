"""Console email provider must be loud in production (#614).

`EMAIL_PROVIDER` defaults to `console`, which writes the whole message —
recipient, name, treatment, amount — to the application log and reports
`SUCCESS`, so the outbox marks it sent while the patient receives
nothing. Reaching that state in production is an omission, not a choice,
so it has to say so.
"""

from __future__ import annotations

import logging

from app.core.email.service import EmailService


def _resolve(monkeypatch, caplog, *, environment: str, provider: str = "console"):
    from app.config import settings as app_settings

    monkeypatch.setattr(app_settings, "ENVIRONMENT", environment)
    monkeypatch.setattr(app_settings, "EMAIL_PROVIDER", provider)
    monkeypatch.setattr(app_settings, "EMAIL_ENABLED", True)
    monkeypatch.setattr(app_settings, "TESTING", False)
    service = EmailService()
    with caplog.at_level(logging.INFO, logger="app.core.email.service"):
        service._initialize()
    return caplog.text


def test_console_in_production_logs_an_error(monkeypatch, caplog) -> None:
    text = _resolve(monkeypatch, caplog, environment="production")
    assert "EMAIL_PROVIDER=console in production" in text
    assert any(r.levelno >= logging.ERROR for r in caplog.records)


def test_console_in_development_stays_quiet(monkeypatch, caplog) -> None:
    text = _resolve(monkeypatch, caplog, environment="development")
    assert "in production" not in text
    assert not [r for r in caplog.records if r.levelno >= logging.ERROR]


def test_smtp_in_production_does_not_warn(monkeypatch, caplog) -> None:
    text = _resolve(monkeypatch, caplog, environment="production", provider="smtp")
    assert "EMAIL_PROVIDER=console in production" not in text


def test_env_example_documents_the_setting() -> None:
    """An operator cannot set what the example never mentions."""
    from pathlib import Path

    example = Path(__file__).resolve().parents[2] / ".env.example"
    body = example.read_text(encoding="utf-8")
    for key in ("EMAIL_PROVIDER", "EMAIL_ENABLED", "EMAIL_SMTP_HOST"):
        assert key in body, key
