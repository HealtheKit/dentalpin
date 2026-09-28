"""The PDF locale list must cover every language the app ships (#422, #441).

A locale the host offers but the PDF endpoints reject turns "Download PDF"
into a 422 with no message, which is how #422 and #441 were found in
production rather than in review.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from app.config import settings
from app.core.pdf_locales import LOCALE_BY_LANG, PDF_LOCALE_PATTERN, PDF_LOCALES


def _host_locales() -> set[str]:
    # CI checks out the whole repo; the dev container mounts the host
    # frontend at DENTALPIN_FRONTEND_ROOT instead.
    candidates = (
        Path(settings.DENTALPIN_FRONTEND_ROOT) / "nuxt.config.ts",
        Path(__file__).resolve().parents[2] / "frontend" / "nuxt.config.ts",
    )
    nuxt_config = next((c for c in candidates if c.is_file()), None)
    if nuxt_config is None:
        pytest.skip("host frontend not reachable from here")
    i18n_block = nuxt_config.read_text().split("i18n: {", 1)[1].split("defaultLocale", 1)[0]
    # Accept both two-letter codes (`pt`) and region overlays (`pt-BR`).
    return set(re.findall(r"code: '([a-z]{2}(?:-[A-Z]{2})?)'", i18n_block))


def test_every_host_language_is_an_accepted_pdf_locale() -> None:
    ui_locales = _host_locales()
    assert ui_locales, "could not read the host locales from nuxt.config.ts"
    assert ui_locales <= set(PDF_LOCALES), ui_locales - set(PDF_LOCALES)


def test_every_accepted_locale_has_a_babel_locale_and_matches_the_pattern() -> None:
    for locale in PDF_LOCALES:
        assert re.match(PDF_LOCALE_PATTERN, locale), locale
        assert locale in LOCALE_BY_LANG, locale
    assert not re.match(PDF_LOCALE_PATTERN, "xx")


def test_pt_br_overlay_reuses_pt_labels_and_babel_pt_br() -> None:
    """pt-BR is an overlay (#509): Babel pt_BR, labels from pt."""
    from app.core.pdf_locales import labels_locale

    assert LOCALE_BY_LANG["pt-BR"] == "pt_BR"
    assert labels_locale("pt-BR") == "pt"
    assert labels_locale("pt") == "pt"
    assert labels_locale("es") == "es"
