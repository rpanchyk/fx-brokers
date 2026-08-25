# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

NAVY = HexColor("#152238")
NAVY2 = HexColor("#1e3354")
TEAL = HexColor("#156b66")
TEAL_LT = HexColor("#e6f3f2")
GOLD = HexColor("#b0892e")
MUTED = HexColor("#5b6777")
LINE = HexColor("#d5dbe3")
BG = HexColor("#f6f8fb")
ROW = HexColor("#eef2f6")
GREEN = HexColor("#0f6b45")
RED = HexColor("#9b1c1c")
AMBER = HexColor("#8a5a00")
WHITE = white

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"


def _register_fonts() -> None:
    global FONT, FONT_BOLD, FONT_ITALIC
    candidates = [
        (
            "Calibri",
            r"C:\Windows\Fonts\calibri.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
            r"C:\Windows\Fonts\calibrii.ttf",
        ),
        (
            "Arial",
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\ariali.ttf",
        ),
        (
            "SegoeUI",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\segoeuii.ttf",
        ),
        (
            "DejaVu",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        ),
    ]
    for family, regular, bold, italic in candidates:
        if not (Path(regular).exists() and Path(bold).exists()):
            continue
        try:
            pdfmetrics.registerFont(TTFont(family, regular))
            pdfmetrics.registerFont(TTFont(f"{family}-Bold", bold))
            if Path(italic).exists():
                pdfmetrics.registerFont(TTFont(f"{family}-Italic", italic))
                FONT_ITALIC = f"{family}-Italic"
            else:
                FONT_ITALIC = family
            FONT = family
            FONT_BOLD = f"{family}-Bold"
            return
        except Exception:
            continue
    raise ValueError(
        "No Unicode font found (need Calibri, Arial, Segoe UI, or DejaVuSans). "
        "Ukrainian PDF text cannot be built with Helvetica."
    )


_register_fonts()

S = getSampleStyleSheet()


def _add(name: str, **kw) -> None:
    kw.setdefault("fontName", FONT)
    S.add(ParagraphStyle(name=name, **kw))


_add("sec", fontName=FONT_BOLD, fontSize=16, leading=20, textColor=NAVY, spaceBefore=2, spaceAfter=8)
_add("sub", fontName=FONT_BOLD, fontSize=12.5, leading=16, textColor=NAVY2, spaceBefore=10, spaceAfter=5)
_add("minih", fontName=FONT_BOLD, fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=7, spaceAfter=3)
_add("bd", fontName=FONT, fontSize=9.2, leading=13.2, textColor=HexColor("#243040"), alignment=TA_JUSTIFY, spaceAfter=5)
_add("small", fontName=FONT, fontSize=8, leading=11, textColor=MUTED, alignment=TA_LEFT, spaceAfter=3)
_add("caption", fontName=FONT_ITALIC, fontSize=7.5, leading=10, textColor=MUTED, spaceAfter=8, spaceBefore=2)
_add("cell", fontName=FONT, fontSize=7.0, leading=9.3, textColor=HexColor("#1d2a3a"), alignment=TA_LEFT)
_add("cell_c", fontName=FONT, fontSize=7.0, leading=9.3, textColor=HexColor("#1d2a3a"), alignment=TA_CENTER)
_add("cell_b", fontName=FONT_BOLD, fontSize=7.0, leading=9.3, textColor=NAVY, alignment=TA_LEFT)
_add("th", fontName=FONT_BOLD, fontSize=6.8, leading=9.0, textColor=WHITE, alignment=TA_CENTER)
_add("kpi_v", fontName=FONT_BOLD, fontSize=11, leading=14, textColor=NAVY, alignment=TA_CENTER)
_add("kpi_l", fontName=FONT, fontSize=7.2, leading=9.5, textColor=MUTED, alignment=TA_CENTER)
_add("disc", fontName=FONT, fontSize=8, leading=11.2, textColor=MUTED, alignment=TA_JUSTIFY, spaceAfter=4)
_add("broker_name", fontName=FONT_BOLD, fontSize=14, leading=17, textColor=WHITE, alignment=TA_LEFT)
_add("broker_tag", fontName=FONT, fontSize=8.3, leading=11, textColor=HexColor("#d5e8e6"))
_add("yes", fontName=FONT_BOLD, fontSize=7.1, leading=9.3, textColor=GREEN, alignment=TA_CENTER)
_add("no", fontName=FONT_BOLD, fontSize=7.1, leading=9.3, textColor=RED, alignment=TA_CENTER)
_add("part", fontName=FONT_BOLD, fontSize=6.9, leading=9.1, textColor=AMBER, alignment=TA_CENTER)
_add("blt", fontName=FONT, fontSize=9, leading=12.6, textColor=HexColor("#243040"), leftIndent=8)
