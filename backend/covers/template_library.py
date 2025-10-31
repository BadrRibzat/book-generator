"""Central cover template library for style-specific parameters.

These templates describe layout intent, typography scale, and color palettes.
The actual rendering logic lives in ``layout_engine.CoverLayoutEngine`` which
consumes these templates and produces ReportLab drawings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional
from reportlab.lib.units import inch


@dataclass(frozen=True)
class CoverTemplate:
    """Declarative configuration describing a cover template."""

    key: str
    display_name: str
    renderer: str
    safe_margin: float = 0.75 * inch
    base_font_size: int = 54
    min_font_size: int = 32
    max_lines: int = 3
    title_font: str = "Helvetica-Bold"
    subtitle_font: str = "Helvetica"
    subtitle_text: str = "Professional Guide"
    default_palette: Dict[str, str] = None
    accent_params: Optional[Dict] = None


# Default palettes keep high contrast and may be overridden by AI concepts
DEFAULT_PALETTES: Dict[str, Dict[str, str]] = {
    "glassmorphism": {
        "background": "#EEF2FF",
        "primary": "#1E40AF",
        "secondary": "#475569",
        "accent": "#38BDF8",
    },
    "neomorphism": {
        "background": "#F1F5F9",
        "primary": "#1F2937",
        "secondary": "#4B5563",
        "accent": "#60A5FA",
    },
    "brutalist": {
        "background": "#FFFFFF",
        "primary": "#111827",
        "secondary": "#EF4444",
        "accent": "#F59E0B",
    },
    "organic_shapes": {
        "background": "#ECFDF5",
        "primary": "#047857",
        "secondary": "#10B981",
        "accent": "#34D399",
    },
    "cyberpunk": {
        "background": "#0F172A",
        "primary": "#F472B6",
        "secondary": "#818CF8",
        "accent": "#38BDF8",
    },
    "minimalist_modern": {
        "background": "#F8FAFC",
        "primary": "#0F172A",
        "secondary": "#475569",
        "accent": "#1D4ED8",
    },
    "vintage_modern": {
        "background": "#FEF3C7",
        "primary": "#92400E",
        "secondary": "#F97316",
        "accent": "#F59E0B",
    },
}


COVER_TEMPLATES: Dict[str, CoverTemplate] = {
    "glassmorphism": CoverTemplate(
        key="glassmorphism",
        display_name="Frosted Layers",
        renderer="render_glassmorphism",
        default_palette=DEFAULT_PALETTES["glassmorphism"],
        accent_params={
            "card_width": 5.6 * inch,
            "card_height": 8.4 * inch,
            "title_y_ratio": 0.62,
        },
    ),
    "neomorphism": CoverTemplate(
        key="neomorphism",
        display_name="Soft Depth",
        renderer="render_neomorphism",
        default_palette=DEFAULT_PALETTES["neomorphism"],
        accent_params={
            "corner_radius": 0.6 * inch,
            "title_y_ratio": 0.6,
        },
    ),
    "brutalist": CoverTemplate(
        key="brutalist",
        display_name="Bold Blocks",
        renderer="render_brutalist",
        default_palette=DEFAULT_PALETTES["brutalist"],
        subtitle_font="Helvetica-Bold",
        subtitle_text="GUIDE",
        base_font_size=68,
        min_font_size=36,
        accent_params={
            "title_y_ratio": 0.55,
            "title_alignment": "left",
        },
    ),
    "organic_shapes": CoverTemplate(
        key="organic_shapes",
        display_name="Organic Flow",
        renderer="render_organic",
        default_palette=DEFAULT_PALETTES["organic_shapes"],
        accent_params={"title_y_ratio": 0.6},
    ),
    "cyberpunk": CoverTemplate(
        key="cyberpunk",
        display_name="Neon Grid",
        renderer="render_cyberpunk",
        default_palette=DEFAULT_PALETTES["cyberpunk"],
        base_font_size=60,
        min_font_size=34,
        accent_params={"title_y_ratio": 0.58},
    ),
    "minimalist_modern": CoverTemplate(
        key="minimalist_modern",
        display_name="Modern Minimal",
        renderer="render_minimalist",
        default_palette=DEFAULT_PALETTES["minimalist_modern"],
        accent_params={"title_y_ratio": 0.62},
    ),
    "vintage_modern": CoverTemplate(
        key="vintage_modern",
        display_name="Vintage Modern",
        renderer="render_vintage",
        default_palette=DEFAULT_PALETTES["vintage_modern"],
        title_font="Times-Bold",
        subtitle_font="Helvetica",
        accent_params={"title_y_ratio": 0.61},
    ),
}

DEFAULT_TEMPLATE_KEY = "minimalist_modern"


def resolve_template(key: Optional[str]) -> CoverTemplate:
    """Return a matching cover template or the default fallback."""
    if not key:
        return COVER_TEMPLATES[DEFAULT_TEMPLATE_KEY]

    normalized = key.lower().strip()
    # Map common aliases used by AI prompts to templates
    alias_map = {
        "glass": "glassmorphism",
        "glass_morphism": "glassmorphism",
        "neomorphic": "neomorphism",
        "neo": "neomorphism",
        "brutalism": "brutalist",
        "organic": "organic_shapes",
        "flow": "organic_shapes",
        "cyber": "cyberpunk",
        "futuristic": "cyberpunk",
        "cyberpunk_futuristic": "cyberpunk",
        "minimalist_abstract": "minimalist_modern",
        "professional_minimal": "minimalist_modern",
        "corporate": "minimalist_modern",
        "abstract_art": "organic_shapes",
        "minimalist": "minimalist_modern",
        "minimal": "minimalist_modern",
        "vintage": "vintage_modern",
    }

    normalized = alias_map.get(normalized, normalized)
    return COVER_TEMPLATES.get(normalized, COVER_TEMPLATES[DEFAULT_TEMPLATE_KEY])


__all__ = [
    "CoverTemplate",
    "COVER_TEMPLATES",
    "DEFAULT_TEMPLATE_KEY",
    "resolve_template",
]
