"""Cover layout engine responsible for dynamic styling, wrapping, and validation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from .template_library import CoverTemplate


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
    ) -> None:
        self.canvas = canvas_obj
        self.template = template
        self.page_width, self.page_height = getattr(canvas_obj, "_pagesize", letter)
        self.safe_margin = template.safe_margin
        self.subtitle_text = subtitle_override or template.subtitle_text
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
        font_name = self.template.title_font
        safe_width = self.page_width - (self.safe_margin * 2)
        max_size = self.template.base_font_size
        min_size = self.template.min_font_size
        max_lines = self.template.max_lines

        for font_size in range(max_size, min_size - 1, -2):
            lines = self._wrap_text(title, font_name, font_size, safe_width, max_lines)
            if not lines:
                continue
            if self._validate_lines(lines, font_name, font_size, safe_width):
                return TitleLayout(font_size=font_size, lines=lines, validation=self.validation_report)

        # Last resort: force wrapping at minimum size
        lines = self._wrap_text(title, font_name, min_size, safe_width, max_lines, force=True)
        return TitleLayout(font_size=min_size, lines=lines, validation=self.validation_report)

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
        current: List[str] = []

        for word in words:
            test = " ".join(current + [word])
            width = self.canvas.stringWidth(test, font_name, font_size)
            if width <= max_width:
                current.append(word)
            else:
                if not current:
                    # Single word longer than width -> break characters
                    lines.append(word)
                    current = []
                    continue
                lines.append(" ".join(current))
                current = [word]
                if len(lines) == max_lines and not force:
                    return []

        if current:
            lines.append(" ".join(current))

        if len(lines) > max_lines and not force:
            return []

        return lines[:max_lines]

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

    def _draw_title_block(self, title_layout: TitleLayout) -> None:
        font_name = self.template.title_font
        self.canvas.setFillColor(self._color("primary"))
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
        subtitle_font = self.template.subtitle_font
        font_size = max(int(title_font_size * 0.35), 20)
        self.canvas.setFont(subtitle_font, font_size)
        self.canvas.setFillColor(self._color("secondary"))

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
    def render_minimalist(self) -> None:
        self._fill_background("background")
        accent = self._tint_color("accent", 0.75)
        primary = self._color("primary")

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

    def render_neomorphism(self) -> None:
        self._fill_background("background")
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

    def render_brutalist(self) -> None:
        self._fill_background("primary")
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

    def render_organic(self) -> None:
        self._fill_background("background")
        accent = self._tint_color("accent", 0.3)
        secondary = self._tint_color("secondary", 0.4)

        self.canvas.setFillColor(accent)
        self.canvas.circle(self.page_width * 0.8, self.page_height * 0.82, 2.4 * inch, stroke=0, fill=1)
        self.canvas.setFillColor(secondary)
        self.canvas.circle(self.page_width * 0.25, self.page_height * 0.2, 2.8 * inch, stroke=0, fill=1)

        self.canvas.setFillColor(self._color("accent"))
        self.canvas.circle(self.page_width * 0.2, self.page_height * 0.75, 1.9 * inch, stroke=0, fill=1)

    def render_cyberpunk(self) -> None:
        self._fill_background("primary")
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

    def render_vintage(self) -> None:
        self._fill_background("background")
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
            palette.update(self.template.default_palette)
        if palette_override:
            palette.update({k: v for k, v in palette_override.items() if v})
        return palette

    def _color(self, name: str) -> Color:
        return HexColor(self.palette.get(name, "#000000"))

    def _fill_background(self, key: str) -> None:
        self.canvas.setFillColor(self._color(key))
        self.canvas.rect(0, 0, self.page_width, self.page_height, stroke=0, fill=1)

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


__all__ = ["CoverLayoutEngine", "TitleLayout"]
