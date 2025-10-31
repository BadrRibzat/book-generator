"""Central cover template library for style-specific parameters.

These templates describe layout intent, typography scale, and color palettes.
The actual rendering logic lives in ``layout_engine.CoverLayoutEngine`` which
consumes these templates and produces ReportLab drawings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
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


# Domain-specific typography mapping
DOMAIN_TYPOGRAPHY = {
    "ai_ml": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Space Grotesk",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "IBM Plex Sans",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Space Grotesk",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "IBM Plex Sans",
        "interior_body_weight": 400,
        "title_category": "modern_geometric",
        "body_category": "modern_sans",
        "accent_color": "#2563eb",
        "personality": "modern, tech-forward, precise",
    },
    "web3_blockchain": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Sora",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Inter",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Sora",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Inter",
        "interior_body_weight": 400,
        "title_category": "modern_geometric",
        "body_category": "modern_sans",
        "accent_color": "#7c3aed",
        "personality": "futuristic, innovative, bold",
    },
    "health_wellness_tech": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Playfair Display",
        "cover_title_weight": 600,
        "cover_subtitle_font_family": "Source Sans 3",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Playfair Display",
        "interior_title_weight": 600,
        "interior_body_font": "Times-Roman",
        "interior_body_font_family": "Source Sans 3",
        "interior_body_weight": 400,
        "title_category": "humanist_serif",
        "body_category": "clean_sans",
        "accent_color": "#10b981",
        "personality": "trustworthy, calming, professional",
    },
    "edtech_online_learning": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Manrope",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Manrope",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Manrope",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Manrope",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#f59e0b",
        "personality": "friendly, approachable, clear",
    },
    "sustainable_tech": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Work Sans",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Work Sans",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Work Sans",
        "interior_title_weight": 700,
        "interior_body_font": "Times-Roman",
        "interior_body_font_family": "Work Sans",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#0ea5e9",
        "personality": "purposeful, resilient, impact-driven",
    },
    "remote_work": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Montserrat",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Inter",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Montserrat",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Inter",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#14b8a6",
        "personality": "collaborative, flexible, streamlined",
    },
    "cybersecurity": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Orbitron",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Poppins",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Orbitron",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Poppins",
        "interior_body_weight": 400,
        "title_category": "modern_geometric",
        "body_category": "modern_sans",
        "accent_color": "#9333ea",
        "personality": "secure, vigilant, confident",
    },
    "creator_economy": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Poppins",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Source Sans 3",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Poppins",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Source Sans 3",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "clean_sans",
        "accent_color": "#ec4899",
        "personality": "expressive, dynamic, community-first",
    },
    "ecommerce_retail": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Montserrat",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Lato",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Montserrat",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Lato",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "clean_sans",
        "accent_color": "#f97316",
        "personality": "energetic, conversion-focused, polished",
    },
    "fintech": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Raleway",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Inter",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Raleway",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Inter",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#0f172a",
        "personality": "trustworthy, analytical, modern",
    },
    "data_analytics": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "IBM Plex Sans",
        "cover_title_weight": 600,
        "cover_subtitle_font_family": "IBM Plex Sans",
        "cover_subtitle_weight": 400,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "IBM Plex Sans",
        "interior_title_weight": 600,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "IBM Plex Sans",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#2563eb",
        "personality": "insightful, structured, clear",
    },
    "gaming": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Chakra Petch",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Rubik",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Chakra Petch",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Rubik",
        "interior_body_weight": 400,
        "title_category": "modern_geometric",
        "body_category": "modern_sans",
        "accent_color": "#f43f5e",
        "personality": "immersive, bold, high-energy",
    },
    "automation": {
        "cover_title_font": "Helvetica-Bold",
        "cover_title_font_family": "Barlow",
        "cover_title_weight": 700,
        "cover_subtitle_font_family": "Barlow",
        "cover_subtitle_weight": 500,
        "interior_title_font": "Helvetica-Bold",
        "interior_title_font_family": "Barlow",
        "interior_title_weight": 700,
        "interior_body_font": "Helvetica",
        "interior_body_font_family": "Barlow",
        "interior_body_weight": 400,
        "title_category": "modern_sans",
        "body_category": "modern_sans",
        "accent_color": "#38bdf8",
        "personality": "systematic, efficient, scalable",
    },
}

_TYPOGRAPHY_ALIASES = {
    "artificial_intelligence_machine_learning": "ai_ml",
    "health_wellness_technology": "health_wellness_tech",
    "sustainable_tech_green_energy": "sustainable_tech",
    "remote_work_digital_collaboration": "remote_work",
    "creator_economy_digital_content": "creator_economy",
    "ecommerce_retail_tech": "ecommerce_retail",
    "data_analytics_business_intelligence": "data_analytics",
    "gaming_interactive_entertainment": "gaming",
}


def get_domain_typography(domain_slug: str) -> dict:
    """Return typography settings for a domain, with fallback."""
    if not domain_slug:
        return DOMAIN_TYPOGRAPHY["ai_ml"]

    normalized = domain_slug.strip().lower()
    mapped = _TYPOGRAPHY_ALIASES.get(normalized, normalized)
    return DOMAIN_TYPOGRAPHY.get(mapped, DOMAIN_TYPOGRAPHY["ai_ml"])


DOMAIN_PALETTES = {
    "ai_ml": {
        "background": "#EEF2FF",
        "primary": "#1E40AF",
        "secondary": "#475569",
        "accent": "#3B82F6",
    },
    "web3_blockchain": {
        "background": "#F5F3FF",
        "primary": "#5B21B6",
        "secondary": "#6B7280",
        "accent": "#7C3AED",
    },
    "health_wellness_tech": {
        "background": "#ECFDF5",
        "primary": "#065F46",
        "secondary": "#4B5563",
        "accent": "#10B981",
    },
    "edtech_online_learning": {
        "background": "#FFFBEB",
        "primary": "#92400E",
        "secondary": "#6B7280",
        "accent": "#F59E0B",
    },
    "sustainable_tech": {
        "background": "#F0FDFA",
        "primary": "#0F766E",
        "secondary": "#134E4A",
        "accent": "#14B8A6",
    },
    "remote_work": {
        "background": "#F8FAFC",
        "primary": "#0F172A",
        "secondary": "#475569",
        "accent": "#22D3EE",
    },
    "cybersecurity": {
        "background": "#0F172A",
        "primary": "#1E293B",
        "secondary": "#38BDF8",
        "accent": "#9333EA",
    },
    "creator_economy": {
        "background": "#FFF1F2",
        "primary": "#BE123C",
        "secondary": "#86198F",
        "accent": "#F472B6",
    },
    "ecommerce_retail": {
        "background": "#FFF7ED",
        "primary": "#9A3412",
        "secondary": "#78350F",
        "accent": "#F97316",
    },
    "fintech": {
        "background": "#F7FBFF",
        "primary": "#0B4F6C",
        "secondary": "#274060",
        "accent": "#06B6D4",
    },
    "data_analytics": {
        "background": "#EFF6FF",
        "primary": "#1D4ED8",
        "secondary": "#1E3A8A",
        "accent": "#2563EB",
    },
    "gaming": {
        "background": "#111827",
        "primary": "#312E81",
        "secondary": "#F59E0B",
        "accent": "#F43F5E",
    },
    "automation": {
        "background": "#ECFEFF",
        "primary": "#0E7490",
        "secondary": "#155E75",
        "accent": "#38BDF8",
    },
}

_PALETTE_ALIASES = {
    "artificial_intelligence_machine_learning": "ai_ml",
    "health_wellness_technology": "health_wellness_tech",
    "sustainable_tech_green_energy": "sustainable_tech",
    "remote_work_digital_collaboration": "remote_work",
    "creator_economy_digital_content": "creator_economy",
    "ecommerce_retail_tech": "ecommerce_retail",
    "data_analytics_business_intelligence": "data_analytics",
    "gaming_interactive_entertainment": "gaming",
}


def resolve_domain_palette(domain_slug: str, template_key: str) -> dict:
    """Merge domain palette with template defaults."""
    template_colors = DEFAULT_PALETTES.get(template_key, {})
    if not domain_slug:
        return {**template_colors, **DOMAIN_PALETTES["ai_ml"]}

    normalized = domain_slug.strip().lower()
    mapped = _PALETTE_ALIASES.get(normalized, normalized)
    domain_colors = DOMAIN_PALETTES.get(mapped, DOMAIN_PALETTES["ai_ml"])
    return {**template_colors, **domain_colors}


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
    "DOMAIN_TYPOGRAPHY",
    "DOMAIN_PALETTES",
    "get_domain_typography",
    "resolve_domain_palette",
    "resolve_template",
]
