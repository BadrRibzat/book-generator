"""Cover layout engine responsible for dynamic styling, wrapping, and validation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics

from backend.utils.fonts import GoogleFontsIntegration
from .template_library import (
    CoverTemplate,
    get_domain_typography,
    resolve_domain_palette,
)


@dataclass
class TitleLayout:
    font_size: int
    lines: List[str]
    validation: Dict[str, float]


class CoverLayoutEngine:
    """High-level layout orchestrator for cover compositions."""

    def __init__(
        self,
        canvas_obj,
        template: CoverTemplate,
        palette_override: Optional[Dict[str, str]] = None,
        subtitle_override: Optional[str] = None,
        domain_slug: Optional[str] = None,
    ) -> None:
        self.canvas = canvas_obj
        self.template = template
        self.page_width, self.page_height = getattr(canvas_obj, "_pagesize", letter)
        self.safe_margin = template.safe_margin
        self.subtitle_text = subtitle_override or template.subtitle_text
        self.domain_slug = (domain_slug or "").strip().lower()
        self.typography = get_domain_typography(self.domain_slug)
        self.font_loader = GoogleFontsIntegration()
        self.cover_title_font = self._resolve_font(
            "cover_title_font_family",
            "cover_title_weight",
            template.title_font,
            self.typography.get("title_category", "modern_sans"),
        )
        self.subtitle_font_name = self._resolve_font(
            "cover_subtitle_font_family",
            "cover_subtitle_weight",
            template.subtitle_font,
            self.typography.get("body_category", "modern_sans"),
        )
        self.palette = self._compose_palette(palette_override)
        self.validation_report: Dict[str, List[Dict[str, float]]] = {"title_lines": []}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def render_cover(self, title: str) -> Dict[str, List[Dict[str, float]]]:
        """Render a full cover and return validation metrics."""
        title_layout = self._prepare_title_layout(title)

        # Render style-specific accents first
        renderer = getattr(self, self.template.renderer, self.render_minimalist)
        renderer()

        # Draw the title and subtitle after accent layers so text stays above
        self._draw_title_block(title_layout)
        self._draw_subtitle(title_layout.font_size)

        return self.validation_report

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------
    def _prepare_title_layout(self, title: str) -> TitleLayout:
        font_name = self.cover_title_font
        safe_width = self.page_width - (self.safe_margin * 2)
        max_size = self.template.base_font_size
        min_size = self.template.min_font_size
        max_lines = self.template.max_lines

        for font_size in range(max_size, min_size - 1, -2):
            lines = self._wrap_text_intelligent(title, font_name, font_size, safe_width, max_lines)
            if not lines:
                continue
            if self._validate_lines(lines, font_name, font_size, safe_width):
                adjusted_size = self._scale_font_for_lines(font_size, len(lines))
                return TitleLayout(font_size=adjusted_size, lines=lines, validation=self.validation_report)

        # Last resort: force wrapping at minimum size
        lines = self._wrap_text_intelligent(title, font_name, min_size, safe_width, max_lines)
        adjusted_size = self._scale_font_for_lines(min_size, len(lines))
        return TitleLayout(font_size=adjusted_size, lines=lines, validation=self.validation_report)

    def _wrap_text(
        self,
        text: str,
        font_name: str,
        font_size: int,
        max_width: float,
        max_lines: int,
        force: bool = False,
    ) -> List[str]:
        words = text.split()
        if not words:
            return []

        lines: List[str] = []
        remaining = words

        while remaining:
            line, rest = self._consume_line(remaining, font_name, font_size, max_width)
            if not line or rest is remaining:
                break
            lines.append(line)
            if self._should_abort_wrap(lines, rest, max_lines, force):
                return []
            remaining = rest

        return lines if force or len(lines) <= max_lines else []

    def _should_abort_wrap(
        self,
        lines: List[str],
        remaining_words: List[str],
        max_lines: int,
        force: bool,
    ) -> bool:
        if force or max_lines <= 0:
            return False
        if len(lines) < max_lines:
            return False
        return bool(remaining_words)

    def _consume_line(
        self,
        words: List[str],
        font_name: str,
        font_size: int,
        max_width: float,
    ) -> Tuple[str, List[str]]:
        if not words:
            return "", []

        current: List[str] = []
        for idx, word in enumerate(words):
            candidate = current + [word]
            text = " ".join(candidate)
            width = self.canvas.stringWidth(text, font_name, font_size)
            if width <= max_width or not current:
                current.append(word)
                continue
            return " ".join(current), words[idx:]

        return " ".join(current), []

    def _wrap_text_intelligent(
        self,
        text: str,
        font_name: str,
        font_size: int,
        max_width: float,
        max_lines: int,
    ) -> List[str]:
        """Intelligent wrapping that prefers natural punctuation breaks."""

        break_points = [": ", " – ", " — ", "; ", " - "]
        for bp in break_points:
            if bp in text:
                parts = text.split(bp, 1)
                line1 = parts[0].strip()
                line2 = parts[1].strip() if len(parts) > 1 else ""
                if not line2:
                    continue

                width1 = self.canvas.stringWidth(line1, font_name, font_size)
                width2 = self.canvas.stringWidth(line2, font_name, int(font_size * 0.92))
                if width1 <= max_width and width2 <= max_width:
                    return [line1, line2]

        wrapped = self._wrap_text(text, font_name, font_size, max_width, max_lines)
        if wrapped:
            return wrapped
        return self._wrap_text(text, font_name, font_size, max_width, max_lines, force=True)

    def _validate_lines(self, lines: List[str], font_name: str, font_size: int, max_width: float) -> bool:
        valid = True
        for idx, line in enumerate(lines):
            width = self.canvas.stringWidth(line, font_name, font_size)
            ratio = width / max_width if max_width else 0
            self.validation_report["title_lines"].append({
                "line_index": idx,
                "width": width,
                "max_width": max_width,
                "ratio": round(ratio, 3),
            })
            if width > max_width:
                valid = False
        return valid

    def _scale_font_for_lines(self, font_size: int, line_count: int) -> int:
        if line_count <= 0:
            return font_size
        if line_count == 1:
            return min(max(font_size, 48), self.template.base_font_size)
        if line_count == 2:
            return min(max(font_size, 38), 42)
        return min(max(font_size, 32), 36)

    def _draw_title_block(self, title_layout: TitleLayout) -> None:
        font_name = self.cover_title_font
        primary_hex = self._ensure_contrast_wcag_aaa(
            self.palette.get("primary", "#111827"),
            self.palette.get("background", "#ffffff"),
        )
        self.canvas.setFillColor(HexColor(primary_hex))
        self.canvas.setFont(font_name, title_layout.font_size)

        line_spacing = title_layout.font_size * 1.05
        block_height = line_spacing * (len(title_layout.lines) - 1) if title_layout.lines else 0
        title_y_ratio = (self.template.accent_params or {}).get("title_y_ratio", 0.62)
        center_y = self.page_height * title_y_ratio
        start_y = center_y + block_height / 2

        alignment = (self.template.accent_params or {}).get("title_alignment", "center")
        safe_left = self.safe_margin
        safe_right = self.page_width - self.safe_margin
        center_x = self.page_width / 2

        for index, line in enumerate(title_layout.lines):
            y = start_y - (index * line_spacing)
            if alignment == "left":
                self.canvas.drawString(safe_left, y, line)
            elif alignment == "right":
                self.canvas.drawRightString(safe_right, y, line)
            else:
                self.canvas.drawCentredString(center_x, y, line)

    def _draw_subtitle(self, title_font_size: int) -> None:
        if not self.subtitle_text:
            return
        subtitle_font = self.subtitle_font_name
        font_size = max(int(title_font_size * 0.35), 20)
        self.canvas.setFont(subtitle_font, font_size)
        subtitle_hex = self._ensure_contrast_wcag_aaa(
            self.palette.get("secondary", "#4B5563"),
            self.palette.get("background", "#ffffff"),
        )
        self.canvas.setFillColor(HexColor(subtitle_hex))

        alignment = (self.template.accent_params or {}).get("title_alignment", "center")
        safe_left = self.safe_margin
        safe_right = self.page_width - self.safe_margin
        center_x = self.page_width / 2
        subtitle_y = self.page_height * 0.3

        if alignment == "left":
            self.canvas.drawString(safe_left, subtitle_y, self.subtitle_text)
        elif alignment == "right":
            self.canvas.drawRightString(safe_right, subtitle_y, self.subtitle_text)
        else:
            self.canvas.drawCentredString(center_x, subtitle_y, self.subtitle_text)

    # ------------------------------------------------------------------
    # Style renderers
    # ------------------------------------------------------------------
    def _draw_corner_frames(self, stroke_color: Color, line_width: float, margin_scale: float = 0.5) -> None:
        margin = self.safe_margin * margin_scale
        corner_size = 1.2 * inch
        self.canvas.setStrokeColor(stroke_color)
        self.canvas.setLineWidth(line_width)
        self.canvas.line(
            margin,
            self.page_height - margin,
            margin + corner_size,
            self.page_height - margin,
        )
        self.canvas.line(
            margin,
            self.page_height - margin,
            margin,
            self.page_height - margin - corner_size,
        )
        self.canvas.line(
            self.page_width - margin - corner_size,
            margin,
            self.page_width - margin,
            margin,
        )
        self.canvas.line(
            self.page_width - margin,
            margin,
            self.page_width - margin,
            margin + corner_size,
        )

    def render_minimalist(self) -> None:
        self._fill_background("background")
        self._add_gradient_overlay(self.palette.get("accent", "#3B82F6"))
        accent = self._tint_color("accent", 0.75)
        primary = self._color("primary")

        self._draw_corner_frames(primary, 4)

        # Accent band behind title
        band_height = 1.6 * inch
        y = self.page_height * 0.55
        self.canvas.setFillColor(accent)
        self.canvas.roundRect(
            self.safe_margin,
            y - band_height / 2,
            self.page_width - (self.safe_margin * 2),
            band_height,
            0.35 * inch,
            stroke=0,
            fill=1,
        )
        self.canvas.setStrokeColor(primary)
        self.canvas.setLineWidth(6)
        self.canvas.line(
            self.safe_margin,
            self.page_height * 0.18,
            self.page_width - self.safe_margin,
            self.page_height * 0.18,
        )

    def render_glassmorphism(self) -> None:
        self._fill_background("background")
        self._add_gradient_overlay(self.palette.get("accent", "#38BDF8"))
        params = self.template.accent_params or {}
        card_width = params.get("card_width", 5.6 * inch)
        card_height = params.get("card_height", 8.4 * inch)

        # Soft halo
        halo_color = self._tint_color("accent", 0.5)
        self.canvas.setFillColor(halo_color)
        self.canvas.circle(self.page_width * 0.78, self.page_height * 0.78, 2.8 * inch, stroke=0, fill=1)

        glass_color = self._tint_color("background", 0.25)
        self.canvas.setFillColor(glass_color)
        x = (self.page_width - card_width) / 2
        y = (self.page_height - card_height) / 2
        self.canvas.roundRect(x, y, card_width, card_height, 0.5 * inch, stroke=0, fill=1)

        border_color = self._color("accent")
        self.canvas.setStrokeColor(border_color)
        self.canvas.setLineWidth(4)
        self.canvas.roundRect(x, y, card_width, card_height, 0.5 * inch, stroke=1, fill=0)

        # Geometric accent bars
        bar_color = self._shade_color("accent", 0.6)
        self.canvas.setFillColor(bar_color)
        bar_height = 0.3 * inch
        self.canvas.rect(x + card_width * 0.1, y + card_height * 0.15, card_width * 0.8, bar_height, stroke=0, fill=1)
        self.canvas.rect(x + card_width * 0.1, y + card_height * 0.75, card_width * 0.3, bar_height, stroke=0, fill=1)

    def render_neomorphism(self) -> None:
        self._fill_background("background")
        self._add_gradient_overlay(self.palette.get("secondary", "#4B5563"))
        params = self.template.accent_params or {}
        radius = params.get("corner_radius", 0.6 * inch)
        block_width = self.page_width - (self.safe_margin * 1.1)
        block_height = self.page_height - (self.safe_margin * 1.6)
        x = (self.page_width - block_width) / 2
        y = (self.page_height - block_height) / 2

        base = self._color("background")
        highlight = self._tint_color("background", 0.92)
        shadow = self._shade_color("background", 0.65)

        # Shadow and highlight to simulate extrusion
        self.canvas.setFillColor(shadow)
        self.canvas.roundRect(x + 12, y - 12, block_width, block_height, radius, stroke=0, fill=1)
        self.canvas.setFillColor(highlight)
        self.canvas.roundRect(x - 12, y + 12, block_width, block_height, radius, stroke=0, fill=1)

        self.canvas.setFillColor(base)
        self.canvas.roundRect(x, y, block_width, block_height, radius, stroke=0, fill=1)

        # Subtle divider lines for depth
        divider_color = self._shade_color("secondary", 0.7)
        self.canvas.setStrokeColor(divider_color)
        self.canvas.setLineWidth(2)
        self.canvas.line(x + block_width * 0.15, y + block_height * 0.35, x + block_width * 0.85, y + block_height * 0.35)
        self.canvas.line(x + block_width * 0.15, y + block_height * 0.65, x + block_width * 0.85, y + block_height * 0.65)

    def render_brutalist(self) -> None:
        self._fill_background("primary")
        self._add_gradient_overlay(self.palette.get("background", "#FFFFFF"))
        block_width = self.page_width - (self.safe_margin * 1.2)
        block_height = self.page_height * 0.65
        x = self.safe_margin * 0.9
        y = self.page_height * 0.48

        self.canvas.setFillColor(self._color("background"))
        self.canvas.rect(x, y - block_height / 2, block_width, block_height, stroke=0, fill=1)

        self.canvas.setStrokeColor(self._color("accent"))
        self.canvas.setLineWidth(14)
        self.canvas.rect(x, y - block_height / 2, block_width, block_height, stroke=1, fill=0)

        # Accent bar
        self.canvas.setFillColor(self._color("secondary"))
        self.canvas.rect(self.safe_margin * 0.9, self.page_height * 0.18, block_width, 0.4 * inch, stroke=0, fill=1)

        # Diagonal accent lines
        accent = self._color("accent")
        self.canvas.setStrokeColor(accent)
        self.canvas.setLineWidth(8)
        self.canvas.line(x, y + block_height / 2, x + block_width * 0.35, y + block_height * 0.95)
        self.canvas.line(x + block_width, y - block_height / 2, x + block_width * 0.65, y - block_height * 0.95)

    def render_organic(self) -> None:
        self._fill_background("background")
        self._add_gradient_overlay(self.palette.get("secondary", "#10B981"))
        accent = self._tint_color("accent", 0.3)
        secondary = self._tint_color("secondary", 0.4)

        self.canvas.setFillColor(accent)
        self.canvas.circle(self.page_width * 0.8, self.page_height * 0.82, 2.4 * inch, stroke=0, fill=1)
        self.canvas.setFillColor(secondary)
        self.canvas.circle(self.page_width * 0.25, self.page_height * 0.2, 2.8 * inch, stroke=0, fill=1)

        self.canvas.setFillColor(self._color("accent"))
        self.canvas.circle(self.page_width * 0.2, self.page_height * 0.75, 1.9 * inch, stroke=0, fill=1)

        # Flowing divider ribbon
        ribbon_color = self._shade_color("accent", 0.8)
        self.canvas.setFillColor(ribbon_color)
        self.canvas.setStrokeColor(ribbon_color)
        self.canvas.setLineWidth(12)
        self.canvas.line(
            self.safe_margin,
            self.page_height * 0.35,
            self.page_width - self.safe_margin,
            self.page_height * 0.28,
        )

    def render_cyberpunk(self) -> None:
        self._fill_background("primary")
        self._add_gradient_overlay(self.palette.get("secondary", "#818CF8"))
        self.canvas.setStrokeColor(self._color("secondary"))
        self.canvas.setLineWidth(1)
        cell_size = 0.5 * inch
        cols = int(self.page_width / cell_size) + 2
        rows = int(self.page_height / cell_size) + 2
        for col in range(cols):
            x = col * cell_size
            self.canvas.line(x, 0, x, self.page_height)
        for row in range(rows):
            y = row * cell_size
            self.canvas.line(0, y, self.page_width, y)

        # Neon glow rectangle
        self.canvas.setFillColor(self._tint_color("accent", 0.4))
        glow_w = self.page_width * 0.7
        glow_h = self.page_height * 0.55
        x = (self.page_width - glow_w) / 2
        y = (self.page_height - glow_h) / 2
        self.canvas.rect(x, y, glow_w, glow_h, stroke=0, fill=1)

        # Futuristic corner nodes
        node_color = self._color("accent")
        self.canvas.setFillColor(node_color)
        node_radius = 0.15 * inch
        positions = [
            (self.safe_margin * 0.8, self.page_height - self.safe_margin * 0.8),
            (self.page_width - self.safe_margin * 0.8, self.safe_margin * 0.8),
            (self.page_width * 0.5, self.page_height * 0.88),
        ]
        for px, py in positions:
            self.canvas.circle(px, py, node_radius, stroke=0, fill=1)

    def render_vintage(self) -> None:
        self._fill_background("background")
        self._add_gradient_overlay(self.palette.get("accent", "#F59E0B"))
        border_color = self._color("secondary")
        inner_margin = self.safe_margin * 0.8
        self.canvas.setStrokeColor(border_color)
        self.canvas.setLineWidth(8)
        self.canvas.rect(
            inner_margin,
            inner_margin,
            self.page_width - (inner_margin * 2),
            self.page_height - (inner_margin * 2),
            stroke=1,
            fill=0,
        )

        self.canvas.setFillColor(self._tint_color("accent", 0.35))
        self.canvas.rect(
            inner_margin,
            self.page_height * 0.15,
            self.page_width - (inner_margin * 2),
            0.45 * inch,
            stroke=0,
            fill=1,
        )

        # Corner ornaments
        ornament_color = self._shade_color("secondary", 0.6)
        self.canvas.setStrokeColor(ornament_color)
        self.canvas.setLineWidth(5)
        self.canvas.arc(
            inner_margin,
            self.page_height - inner_margin - 1.2 * inch,
            inner_margin + 1.2 * inch,
            self.page_height - inner_margin,
            0,
            90,
        )
        self.canvas.arc(
            self.page_width - inner_margin - 1.2 * inch,
            inner_margin,
            self.page_width - inner_margin,
            inner_margin + 1.2 * inch,
            180,
            270,
        )

    # ------------------------------------------------------------------
    # Color utilities
    # ------------------------------------------------------------------
    def _compose_palette(self, palette_override: Optional[Dict[str, str]]) -> Dict[str, str]:
        palette = {
            "background": "#F8FAFC",
            "primary": "#111827",
            "secondary": "#4B5563",
            "accent": "#3B82F6",
        }
        if self.template.default_palette:
            palette.update({k: v for k, v in self.template.default_palette.items() if v})
        domain_palette = resolve_domain_palette(self.domain_slug, self.template.key)
        palette.update(domain_palette)
        if palette_override:
            palette.update({k: v for k, v in palette_override.items() if v})
        return palette

    def _color(self, name: str) -> Color:
        return HexColor(self.palette.get(name, "#000000"))

    def _font_available(self, font_name: str) -> bool:
        try:
            pdfmetrics.getFont(font_name)
            return True
        except KeyError:
            return False

    def _resolve_font(
        self,
        family_key: str,
        weight_key: str,
        fallback: Optional[str],
        category: str,
    ) -> str:
        family = self.typography.get(family_key)
        weight_value = self.typography.get(weight_key, 400)

        try:
            weight = int(weight_value)
        except (TypeError, ValueError):
            weight = 400

        if family:
            loaded = self.font_loader.load_google_font(family, weight)
            if loaded:
                return loaded

        if fallback and self._font_available(fallback):
            return fallback

        return self.font_loader.get_fallback_font(category)

    def _fill_background(self, key: str) -> None:
        self.canvas.setFillColor(self._color(key))
        self.canvas.rect(0, 0, self.page_width, self.page_height, stroke=0, fill=1)

    def _add_gradient_overlay(self, base_color: Optional[str], opacity: float = 0.15) -> None:
        if not base_color:
            return
        base_rgb = self._hex_to_rgb_tuple(base_color)
        top_rgb = self._interpolate_rgb(base_rgb, (1.0, 1.0, 1.0), opacity)
        bottom_rgb = self._interpolate_rgb(base_rgb, (0.0, 0.0, 0.0), opacity * 0.8)

        self.canvas.saveState()
        self.canvas.setFillColor(Color(*top_rgb))
        self.canvas.rect(0, self.page_height * 0.65, self.page_width, self.page_height * 0.35, stroke=0, fill=1)
        mid_rgb = self._interpolate_rgb(base_rgb, (1.0, 1.0, 1.0), opacity * 0.4)
        self.canvas.setFillColor(Color(*mid_rgb))
        self.canvas.rect(0, self.page_height * 0.35, self.page_width, self.page_height * 0.3, stroke=0, fill=1)
        self.canvas.setFillColor(Color(*bottom_rgb))
        self.canvas.rect(0, 0, self.page_width, self.page_height * 0.35, stroke=0, fill=1)
        self.canvas.restoreState()

    def _tint_color(self, key: str, amount: float) -> Color:
        base = self._color(key)
        amount = max(0.0, min(1.0, amount))
        r = base.red + (1 - base.red) * amount
        g = base.green + (1 - base.green) * amount
        b = base.blue + (1 - base.blue) * amount
        return Color(r, g, b)

    def _shade_color(self, key: str, amount: float) -> Color:
        base = self._color(key)
        amount = max(0.0, min(1.0, amount))
        r = base.red * amount
        g = base.green * amount
        b = base.blue * amount
        return Color(r, g, b)

    def _hex_to_rgb_tuple(self, value: str) -> Tuple[float, float, float]:
        value = value.lstrip("#")
        if len(value) != 6:
            return (0.0, 0.0, 0.0)
        r = int(value[0:2], 16) / 255.0
        g = int(value[2:4], 16) / 255.0
        b = int(value[4:6], 16) / 255.0
        return (r, g, b)

    def _rgb_tuple_to_hex(self, rgb: Tuple[float, float, float]) -> str:
        r, g, b = [max(0, min(255, int(round(component * 255)))) for component in rgb]
        return f"#{r:02x}{g:02x}{b:02x}"

    def _interpolate_rgb(
        self, source: Tuple[float, float, float], target: Tuple[float, float, float], factor: float
    ) -> Tuple[float, float, float]:
        factor = max(0.0, min(1.0, factor))
        return tuple(s + (t - s) * factor for s, t in zip(source, target))

    def _luminance(self, rgb: Tuple[float, float, float]) -> float:
        def f(channel: float) -> float:
            return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

        r, g, b = rgb
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

    def _contrast_ratio(self, color_a: str, color_b: str) -> float:
        rgb_a = self._hex_to_rgb_tuple(color_a)
        rgb_b = self._hex_to_rgb_tuple(color_b)
        lum_a = self._luminance(rgb_a)
        lum_b = self._luminance(rgb_b)
        lighter, darker = (lum_a, lum_b) if lum_a >= lum_b else (lum_b, lum_a)
        return (lighter + 0.05) / (darker + 0.05)

    def _ensure_contrast_wcag_aaa(self, primary: str, background: str) -> str:
        ratio = self._contrast_ratio(primary, background)
        if ratio >= 7.0:
            return primary
        bg_luminance = self._luminance(self._hex_to_rgb_tuple(background))
        fallback = "#0a0a0a" if bg_luminance > 0.5 else "#f8f9fa"
        return fallback


__all__ = ["CoverLayoutEngine", "TitleLayout"]
