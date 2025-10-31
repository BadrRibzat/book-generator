from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import requests
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)


class GoogleFontsIntegration:
    """Lightweight Google Fonts loader that caches TTF assets locally."""

    FONT_CACHE_DIR = Path("/tmp/book_generator_fonts")

    def __init__(self) -> None:
        self.FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.loaded_fonts: set[str] = set()

    def load_google_font(self, font_family: str, weight: int = 400) -> Optional[str]:
        """Fetch a font from Google Fonts CSS2 API and register it with ReportLab."""
        if not font_family:
            return None

        normalized = font_family.replace(" ", "")
        font_name = f"{normalized}-{weight}"
        if font_name in self.loaded_fonts:
            return font_name

        css_url = (
            "https://fonts.googleapis.com/css2?"
            f"family={font_family.replace(' ', '+')}:wght@{weight}&display=swap"
        )

        try:
            css_response = requests.get(css_url, timeout=10)
            css_response.raise_for_status()
        except Exception as exc:  # pragma: no cover - network failure path
            logger.warning("Failed to fetch CSS for %s: %s", font_family, exc)
            return None

        ttf_url = self._extract_ttf_url(css_response.text)
        if not ttf_url:
            logger.warning("No TTF URL available for %s", font_family)
            return None

        try:
            ttf_response = requests.get(ttf_url, timeout=15)
            ttf_response.raise_for_status()
        except Exception as exc:  # pragma: no cover - network failure path
            logger.warning("Failed to download TTF for %s: %s", font_family, exc)
            return None

        font_file = self.FONT_CACHE_DIR / f"{font_name}.ttf"
        font_file.write_bytes(ttf_response.content)

        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
        except Exception as exc:  # pragma: no cover - registration failure
            logger.error("Could not register font %s: %s", font_name, exc)
            return None

        self.loaded_fonts.add(font_name)
        logger.info("Loaded Google Font: %s", font_name)
        return font_name

    def _extract_ttf_url(self, css_content: str) -> Optional[str]:
        import re

        match = re.search(r"url\((https://[^)]+\.ttf)\)", css_content)
        return match.group(1) if match else None

    def get_fallback_font(self, category: str = "clean_sans") -> str:
        """Provide a safe fallback font bundled with ReportLab."""
        fallbacks = {
            "clean_sans": "Helvetica",
            "modern_sans": "Helvetica",
            "elegant_serif": "Times-Roman",
            "humanist_serif": "Times-Roman",
            "hand_written": "Helvetica",
            "tech_mono": "Courier",
            "modern_geometric": "Helvetica",
            "classic_traditional": "Times-Roman",
        }
        return fallbacks.get(category, "Helvetica")
