# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config_loader import AppConfig
from src.i18n import I18n
from src.pdf.styles import (
    BG,
    FONT,
    FONT_BOLD,
    GOLD,
    LINE,
    MUTED,
    NAVY,
    ROW,
    S,
    TEAL,
    TEAL_LT,
    WHITE,
)

MARGIN = 13 * mm


class PageGeom:
    __slots__ = ("w", "h")

    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

    @property
    def usable(self) -> float:
        return self.w - 2 * MARGIN


def resolve_pagesize(orientation: str, paper_size: str = "A4") -> tuple[float, float]:
    base = A3 if (paper_size or "A4").strip().upper() == "A3" else A4
    if (orientation or "portrait").strip().lower() == "landscape":
        return landscape(base)
    return base


def xt(value) -> str:
    """Escape user text for reportlab Paragraph (XML)."""
    return escape(str(value if value is not None else ""), {'"': "&quot;"})


def P(text, style="bd"):
    return Paragraph(str(text), S[style])


def C(text, style="cell"):
    return Paragraph(str(text), S[style])


def CC(text, style="cell_c"):
    return Paragraph(str(text), S[style])


def status_p(i18n: I18n, value):
    label = i18n.status(value)
    key = str(value or "").strip().lower()
    if key in ("yes", "так", "true", "1"):
        style = "yes"
    elif key in ("no", "ні", "false", "0"):
        style = "no"
    else:
        style = "part"
    return Paragraph(label, S[style])


def link_url(url: str | None) -> str:
    if not url:
        return xt("—")
    safe = xt(url)
    return f'<link href="{safe}">{safe}</link>'


def fit_widths(widths: list[float], total: float) -> list[float]:
    if not widths:
        return widths
    out = list(widths)
    out[-1] = max(out[-1] + (total - sum(out)), 12 * mm)
    return out


def table(data, col_widths):
    cmds = [
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.0),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("GRID", (0, 0), (-1, -1), 0.25, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 4.4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4.4),
    ]
    for i in range(1, len(data)):
        cmds.append(("BACKGROUND", (0, i), (-1, i), ROW if i % 2 == 0 else WHITE))
        cmds.append(("BACKGROUND", (0, i), (0, i), TEAL_LT))
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(cmds))
    return t


def kpi_row(page: PageGeom, items):
    n = max(len(items), 1)
    w = page.usable / n
    cells = []
    for v, lab in items:
        inner = Table([[P(v, "kpi_v")], [P(lab, "kpi_l")]], colWidths=[w - 3])
        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), BG),
                    ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        cells.append(inner)
    wrap = Table([cells], colWidths=[w] * n)
    wrap.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 1.2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1.2),
            ]
        )
    )
    return wrap


def banner(page: PageGeom, title, subtitle=""):
    data = [[P(xt(title), "broker_name")]]
    cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (0, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
    ]
    if subtitle:
        data.append([P(xt(subtitle), "broker_tag")])
        cmds.append(("TOPPADDING", (0, 1), (-1, 1), 0))
    t = Table(data, colWidths=[page.usable])
    t.setStyle(TableStyle(cmds))
    return t


def kv_table(page: PageGeom, pairs):
    usable = page.usable
    w_k, w_v = 38 * mm, (usable / 2) - 38 * mm
    rows, row = [], []
    for k, v in pairs:
        row += [C(f"<b>{xt(k)}</b>", "cell_b"), C(v)]
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        while len(row) < 4:
            row += [C(""), C("")]
        rows.append(row)
    t = Table(rows, colWidths=[w_k, w_v, w_k, w_v])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3.0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("BACKGROUND", (0, 0), (0, -1), TEAL_LT),
                ("BACKGROUND", (2, 0), (2, -1), TEAL_LT),
            ]
        )
    )
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(P(x, "blt"), leftIndent=8, bulletColor=TEAL, value="•") for x in items],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        bulletFontName=FONT,
        bulletFontSize=9,
        spaceBefore=1,
        spaceAfter=4,
    )


def names_csv(rows: list[dict], pred) -> str:
    names = [xt(b.get("name") or b["id"]) for b in rows if pred(b)]
    return ", ".join(names)


def name_cell(b: dict):
    return C(f"<b>{xt(b.get('name') or b['id'])}</b>")


def cover_page(canvas, doc, cfg: AppConfig, i18n: I18n, page: PageGeom, names: list[str], period: str):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, page.w, page.h, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 8 * mm, page.h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(8 * mm, 0, 1.4 * mm, page.h, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_BOLD, 8.5)
    canvas.drawString(22 * mm, page.h - 26 * mm, i18n.t("cover_kicker"))
    canvas.setFont(FONT_BOLD, 22)
    title = cfg.title
    canvas.drawString(22 * mm, page.h - 42 * mm, title[:48])
    if len(title) > 48:
        canvas.drawString(22 * mm, page.h - 50 * mm, title[48:96])
        y_sub = page.h - 60 * mm
    else:
        y_sub = page.h - 52 * mm
    canvas.setFont(FONT, 11)
    canvas.setFillColor(HexColor("#c9d4e3"))
    canvas.drawString(22 * mm, y_sub, i18n.t("cover_compare", n=len(names), period=period))
    canvas.drawString(22 * mm, y_sub - 6 * mm, i18n.t("cover_topics"))
    y = y_sub - 18 * mm
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(0.8)
    canvas.line(22 * mm, y, 110 * mm, y)
    canvas.setFillColor(GOLD)
    canvas.setFont(FONT_BOLD, 9)
    canvas.drawString(22 * mm, y - 9 * mm, i18n.t("cover_brokers"))
    canvas.setFillColor(WHITE)

    cols = 3 if len(names) > 16 else 2
    font_size = 7.5 if len(names) > 16 else 8.5
    step = 4.4 * mm if len(names) > 16 else 5.2 * mm
    canvas.setFont(FONT, font_size)
    per_col = max((len(names) + cols - 1) // cols, 1)
    yy = y - 17 * mm
    x0 = 22 * mm
    col_w = (page.w - 40 * mm) / cols
    bottom = 34 * mm
    if yy - bottom > 0:
        step = min(step, (yy - bottom) / per_col)
    for i, n in enumerate(names):
        col = i // per_col
        row = i % per_col
        canvas.drawString(x0 + col * col_w, yy - row * step, f"{i + 1:>2}.  {n}")

    canvas.setFillColor(HexColor("#9aabbf"))
    canvas.setFont(FONT, 7.8)
    canvas.drawString(22 * mm, 28 * mm, i18n.t("cover_src1"))
    canvas.drawString(22 * mm, 22 * mm, i18n.t("cover_src2"))
    canvas.restoreState()


def header_footer(canvas, doc, i18n: I18n, page: PageGeom, period: str):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, page.h - 9 * mm, page.w, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT, 7.4)
    canvas.drawString(MARGIN, page.h - 6.1 * mm, i18n.t("header", period=period))
    canvas.drawRightString(page.w - MARGIN, page.h - 6.1 * mm, i18n.t("header_right"))
    canvas.setFillColor(BG)
    canvas.rect(0, 0, page.w, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT, 7.2)
    canvas.drawString(MARGIN, 3.6 * mm, i18n.t("footer"))
    canvas.drawRightString(page.w - MARGIN, 3.6 * mm, f"{doc.page}")
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.6)
    canvas.line(0, page.h - 9 * mm, page.w, page.h - 9 * mm)
    canvas.restoreState()


def ordered(brokers: dict[str, dict], ids: list[str]) -> list[dict]:
    return [brokers[i] for i in ids if i in brokers]


def period_from(override: str | None) -> tuple[str, str]:
    """Return (period YYYY-MM, as_of label for methodology). Default: run date."""
    today = date.today()
    raw = (override or "").strip()
    if raw:
        parts = raw.split("-")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            year, month = int(parts[0]), int(parts[1])
            if 1 <= month <= 12 and year >= 1990:
                period = f"{year:04d}-{month:02d}"
                if len(parts) >= 3 and parts[2].isdigit():
                    day = int(parts[2])
                    if 1 <= day <= 31:
                        return period, f"{year:04d}-{month:02d}-{day:02d}"
                return period, period
    return f"{today.year:04d}-{today.month:02d}", today.isoformat()


def pay_summary(i18n: I18n, block: dict | None) -> str:
    b = block or {}
    note = xt(b.get("note") or "")
    return (
        f"{i18n.t('pay_card')}: {i18n.status(b.get('card'))}. "
        f"{i18n.t('pay_iban')}: {i18n.status(b.get('bank_iban'))}. "
        f"{i18n.t('pay_crypto')}: {i18n.status(b.get('crypto'))}. "
        f"{note}"
    ).strip()


def build_pdf(cfg: AppConfig, brokers: dict[str, dict], root: Path, as_of_override: str | None = None) -> Path:
    page = PageGeom(*resolve_pagesize(cfg.orientation, cfg.paper_size))
    i18n = I18n(cfg.language)
    period, as_of = period_from(as_of_override)
    yyyy, month = period.split("-")[:2]
    filename = cfg.filename_pattern.replace("{YYYY}", yyyy).replace("{MM}", month)
    out = root / filename
    rows = ordered(brokers, cfg.broker_ids)
    names = [b.get("name") or b["id"] for b in rows]
    usable = page.usable
    has = cfg.has

    story = [PageBreak()]
    story.append(P(i18n.t("sec_method"), "sec"))
    story.append(P(i18n.t("method_body", as_of=as_of)))
    if has("ukraine"):
        story.append(P(i18n.t("ua_sub"), "sub"))
        story.append(P(i18n.t("ua_body")))
    story.append(P(i18n.t("legend")))
    if i18n.t("corpus_note_en"):
        story.append(P(i18n.t("corpus_note_en"), "caption"))

    ua_yes = sum(1 for b in rows if (b.get("ukraine") or {}).get("status") == "yes")
    ua_no = sum(1 for b in rows if (b.get("ukraine") or {}).get("status") == "no")
    ua_part = sum(1 for b in rows if (b.get("ukraine") or {}).get("status") == "partial")
    raw_n = sum(
        1
        for b in rows
        if "raw" in (b.get("accounts") or "").lower() or "ecn" in (b.get("accounts") or "").lower()
    )
    ct_n = sum(1 for b in rows if (b.get("platforms") or {}).get("ctrader") == "yes")

    story.append(P(i18n.t("sec_findings"), "sec"))
    kpis = [(str(len(rows)), i18n.t("kpi_brokers"))]
    if has("accounts"):
        kpis.append((str(raw_n), i18n.t("kpi_raw")))
    if has("ukraine"):
        kpis.append((f"{ua_yes}", i18n.t("kpi_ua_yes")))
        kpis.append((f"{ua_no}", i18n.t("kpi_ua_no")))
        if ua_part:
            kpis.append((f"{ua_part}", i18n.t("kpi_ua_part")))
    if has("platforms"):
        kpis.append((f"{ct_n}", i18n.t("kpi_ct")))
    story.append(kpi_row(page, kpis))
    story.append(Spacer(1, 3 * mm))

    story.append(P(i18n.t("best_fits"), "sub"))
    recs = []
    if has("deposit"):
        yes_c = names_csv(rows, lambda b: (b.get("deposit") or {}).get("crypto") == "yes")
        no_c = names_csv(rows, lambda b: (b.get("deposit") or {}).get("crypto") == "no")
        part_c = names_csv(rows, lambda b: (b.get("deposit") or {}).get("crypto") == "partial")
        recs.append(
            i18n.t(
                "rec_crypto",
                yes=yes_c or i18n.t("none_listed"),
                no=no_c or i18n.t("none_listed"),
                partial=part_c or i18n.t("none_listed"),
            )
        )
    if has("ukraine"):
        yes_n = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "yes")
        no_n = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "no")
        part_n = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "partial")
        if yes_n:
            recs.append(i18n.t("rec_ua_yes", names=yes_n))
        if no_n:
            recs.append(i18n.t("rec_ua_no", names=no_n))
        if part_n:
            recs.append(i18n.t("rec_ua_part", names=part_n))
    if has("algo") and has("platforms"):
        ct_names = names_csv(rows, lambda b: (b.get("platforms") or {}).get("ctrader") == "yes")
        ct_ua = names_csv(
            rows,
            lambda b: (b.get("platforms") or {}).get("ctrader") == "yes"
            and (b.get("ukraine") or {}).get("status") == "yes",
        )
        if ct_names:
            recs.append(
                i18n.t(
                    "rec_algo_ct",
                    names=ct_names,
                    ua_names=ct_ua or i18n.t("none_listed"),
                )
            )
    if recs:
        story.append(bullets(recs))

    story.append(P(i18n.t("sec_compare"), "sec"))

    if has("homepage") or has("country") or has("regulations"):
        story.append(P(i18n.t("sub_identity"), "sub"))
        hdr = [CC(i18n.t("th_broker"), "th")]
        widths = [28 * mm]
        if has("homepage"):
            hdr.append(CC(i18n.t("th_home"), "th"))
            widths.append(48 * mm)
        if has("country"):
            hdr.append(CC(i18n.t("th_country"), "th"))
            widths.append(40 * mm)
        if has("regulations"):
            hdr.append(CC(i18n.t("th_regs"), "th"))
            widths.append(40 * mm)
        widths = fit_widths(widths, usable)
        body = [hdr]
        for b in rows:
            r = [name_cell(b)]
            if has("homepage"):
                r.append(C(link_url(b.get("homepage"))))
            if has("country"):
                r.append(C(xt(b.get("country") or b.get("hq") or i18n.t("none"))))
            if has("regulations"):
                r.append(C(xt(b.get("regulations") or i18n.t("none"))))
            body.append(r)
        story.append(table(body, widths))
        story.append(Spacer(1, 2 * mm))

    if has("accounts") or has("swaps"):
        story.append(P(i18n.t("sub_accounts"), "sub"))
        hdr = [CC(i18n.t("th_broker"), "th")]
        widths = [26 * mm]
        if has("accounts"):
            hdr.append(CC(i18n.t("th_accounts"), "th"))
            widths.append(90 * mm if has("swaps") else usable - 26 * mm)
        if has("swaps"):
            hdr.append(CC(i18n.t("th_swaps"), "th"))
            widths.append(60 * mm)
        widths = fit_widths(widths, usable)
        body = [hdr]
        for b in rows:
            r = [name_cell(b)]
            if has("accounts"):
                r.append(C(xt(b.get("accounts") or i18n.t("none"))))
            if has("swaps"):
                r.append(C(xt(b.get("swaps") or i18n.t("none"))))
            body.append(r)
        story.append(table(body, widths))
        story.append(P(i18n.t("accounts_caption"), "caption"))

    if has("kyc"):
        story.append(P(i18n.t("sub_kyc"), "sub"))
        kyc_tbl = [[CC(i18n.t("th_broker"), "th"), CC(i18n.t("th_kyc"), "th")]]
        for b in rows:
            kyc_tbl.append([name_cell(b), C(xt(b.get("kyc") or i18n.t("kyc_default")))])
        story.append(table(kyc_tbl, fit_widths([32 * mm, usable - 32 * mm], usable)))
        story.append(Spacer(1, 2 * mm))

    if has("deposit") or has("withdrawal") or has("rts"):
        story.append(P(i18n.t("sub_pay"), "sub"))
        hdr = [CC(i18n.t("th_broker"), "th")]
        widths = [26 * mm]
        cols_pay = []
        if has("deposit"):
            cols_pay += [
                ("d_card", i18n.t("th_dep_card")),
                ("d_bank", i18n.t("th_dep_iban")),
                ("d_crypto", i18n.t("th_dep_crypto")),
            ]
        if has("withdrawal"):
            cols_pay += [
                ("w_card", i18n.t("th_wd_card")),
                ("w_bank", i18n.t("th_wd_iban")),
                ("w_crypto", i18n.t("th_wd_crypto")),
            ]
        if has("rts"):
            cols_pay.append(("rts", i18n.t("th_rts")))
        col_w = (usable - 26 * mm) / max(len(cols_pay), 1)
        for _, lab in cols_pay:
            hdr.append(CC(lab, "th"))
            widths.append(col_w)
        body = [hdr]
        for b in rows:
            dep = b.get("deposit") or {}
            wd = b.get("withdrawal") or {}
            rts = b.get("rts") or {}
            r = [name_cell(b)]
            mapping = {
                "d_card": dep.get("card"),
                "d_bank": dep.get("bank_iban"),
                "d_crypto": dep.get("crypto"),
                "w_card": wd.get("card"),
                "w_bank": wd.get("bank_iban"),
                "w_crypto": wd.get("crypto"),
                "rts": rts.get("status"),
            }
            for key, _ in cols_pay:
                r.append(status_p(i18n, mapping.get(key)))
            body.append(r)
        story.append(table(body, fit_widths(widths, usable)))
        story.append(P(i18n.t("pay_caption"), "caption"))

        notes_tbl = [[CC(i18n.t("th_broker"), "th"), CC(i18n.t("th_pay_details"), "th")]]
        for b in rows:
            bits = []
            if has("deposit"):
                bits.append(f"<b>Dep:</b> {xt((b.get('deposit') or {}).get('note') or i18n.t('none'))}")
            if has("withdrawal"):
                bits.append(f"<b>Wd:</b> {xt((b.get('withdrawal') or {}).get('note') or i18n.t('none'))}")
            if has("rts"):
                bits.append(f"<b>RTS:</b> {xt((b.get('rts') or {}).get('note') or i18n.t('none'))}")
            notes_tbl.append([name_cell(b), C(" ".join(bits))])
        story.append(table(notes_tbl, fit_widths([28 * mm, usable - 28 * mm], usable)))

    if has("ukraine"):
        story.append(P(i18n.t("sub_ukraine_tbl"), "sub"))
        ua_cmp = [[CC(i18n.t("th_broker"), "th"), CC(i18n.t("th_ukraine"), "th")]]
        for b in rows:
            ua = b.get("ukraine") or {}
            ua_cmp.append(
                [
                    name_cell(b),
                    C(f"<b>{i18n.status(ua.get('status'))}.</b> {xt(ua.get('note') or '')}"),
                ]
            )
        story.append(table(ua_cmp, fit_widths([32 * mm, usable - 32 * mm], usable)))
        story.append(P(i18n.t("crimea_note"), "caption"))

    if has("algo") or has("platforms"):
        story.append(P(i18n.t("sub_algo"), "sub"))
        hdr = [CC(i18n.t("th_broker"), "th")]
        widths = [28 * mm]
        if has("platforms"):
            hdr += [CC(i18n.t("th_mt4"), "th"), CC(i18n.t("th_mt5"), "th"), CC(i18n.t("th_ct"), "th")]
            widths += [14 * mm, 14 * mm, 18 * mm]
        if has("algo"):
            hdr.append(CC(i18n.t("th_algo"), "th"))
            widths.append(28 * mm)
        hdr.append(CC(i18n.t("th_comment"), "th"))
        widths.append(40 * mm)
        widths = fit_widths(widths, usable)
        body = [hdr]
        for b in rows:
            plat = b.get("platforms") or {}
            algo = b.get("algo") or {}
            r = [name_cell(b)]
            if has("platforms"):
                r += [
                    status_p(i18n, plat.get("mt4")),
                    status_p(i18n, plat.get("mt5")),
                    status_p(i18n, plat.get("ctrader")),
                ]
            if has("algo"):
                r.append(C(xt(algo.get("rating") or i18n.t("none"))))
            comment = " ".join(
                filter(
                    None,
                    [
                        plat.get("note") if has("platforms") else "",
                        algo.get("note") if has("algo") else "",
                    ],
                )
            )
            r.append(C(xt(comment or i18n.t("none"))))
            body.append(r)
        story.append(table(body, widths))
        story.append(P(i18n.t("algo_caption"), "caption"))

    story.append(PageBreak())
    story.append(P(i18n.t("sec_profiles"), "sec"))
    story.append(P(i18n.t("profiles_intro")))

    renderers = {
        "homepage": lambda b: link_url(b.get("homepage")),
        "country": lambda b: xt(b.get("country") or b.get("hq") or i18n.t("none")),
        "regulations": lambda b: xt(b.get("regulations") or i18n.t("none")),
        "accounts": lambda b: xt(b.get("accounts") or i18n.t("none")),
        "swaps": lambda b: xt(b.get("swaps") or i18n.t("none")),
        "kyc": lambda b: xt(b.get("kyc") or i18n.t("none")),
        "deposit": lambda b: pay_summary(i18n, b.get("deposit")),
        "withdrawal": lambda b: pay_summary(i18n, b.get("withdrawal")),
        "rts": lambda b: xt((b.get("rts") or {}).get("note") or i18n.t("none")),
        "ukraine": lambda b: (
            f"<b>{i18n.status((b.get('ukraine') or {}).get('status'))}.</b> "
            f"{xt((b.get('ukraine') or {}).get('note') or '')}"
        ),
        "platforms": lambda b: (
            f"MT4 — {i18n.status((b.get('platforms') or {}).get('mt4'))}. "
            f"MT5 — {i18n.status((b.get('platforms') or {}).get('mt5'))}. "
            f"cTrader — {i18n.status((b.get('platforms') or {}).get('ctrader'))}. "
            f"{xt((b.get('platforms') or {}).get('note') or '')}"
        ),
        "algo": lambda b: (
            f"<b>{xt((b.get('algo') or {}).get('rating') or '')}.</b> "
            f"{xt((b.get('algo') or {}).get('note') or '')}"
        ),
    }

    for b in rows:
        # Keep banner+meta together; full profile may span pages.
        head = [Spacer(1, 3.2 * mm), banner(page, b.get("name") or b["id"], b.get("tagline") or ""), Spacer(1, 2.2 * mm)]
        meta = []
        if b.get("founded"):
            meta.append((i18n.t("founded"), xt(b.get("founded"))))
        if b.get("hq"):
            meta.append((i18n.t("hq"), xt(b.get("hq"))))
        if has("homepage") and b.get("homepage"):
            meta.append((i18n.t("site"), link_url(b.get("homepage"))))
        if meta:
            head.append(kv_table(page, meta))
        story.append(KeepTogether(head))
        for point in cfg.points:
            fn = renderers.get(point.id)
            if not fn:
                continue
            story.append(P(i18n.point_title(point.id, point.label), "minih"))
            story.append(P(fn(b)))
        if b.get("extra"):
            story.append(P(xt(b["extra"]), "small"))

    story.append(Spacer(1, 4 * mm))
    story.append(P(i18n.t("sec_advice"), "sec"))
    story.append(P(i18n.t("advice_ua") if has("ukraine") else i18n.t("advice_general"), "sub"))
    if has("ukraine"):
        no_names = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "no")
        part_names = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "partial")
        ct_ua = names_csv(
            rows,
            lambda b: (b.get("ukraine") or {}).get("status") == "yes"
            and (b.get("platforms") or {}).get("ctrader") == "yes",
        )
        raw_ua = names_csv(
            rows,
            lambda b: (b.get("ukraine") or {}).get("status") == "yes"
            and (
                "raw" in (b.get("accounts") or "").lower()
                or "ecn" in (b.get("accounts") or "").lower()
            )
            and (b.get("platforms") or {}).get("ctrader") != "yes",
        )
        advice_items = []
        if no_names:
            advice_items.append(i18n.t("advice_avoid", names=no_names))
        advice_items.append(
            i18n.t(
                "advice_shortlist",
                ct=ct_ua or i18n.t("none_listed"),
                raw=raw_ua or i18n.t("none_listed"),
            )
        )
        if part_names:
            advice_items.append(i18n.t("advice_partial", names=part_names))
        advice_items.append(i18n.t("advice_test"))
        advice_items.append(i18n.t("advice_swift"))
        story.append(bullets(advice_items))

    if has("rts"):
        story.append(P(i18n.t("advice_rts"), "sub"))
        story.append(bullets([i18n.t("rts_b1"), i18n.t("rts_b2"), i18n.t("rts_b3")]))

    story.append(P(i18n.t("sec_limits"), "sec"))
    story.append(P(i18n.t("limits_body"), "disc"))
    story.append(P(i18n.t("sec_sources"), "sec"))
    src_items = [i18n.t("src_official")]
    if has("ukraine"):
        yes_n = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "yes")
        no_n = names_csv(rows, lambda b: (b.get("ukraine") or {}).get("status") == "no")
        if yes_n:
            src_items.append(i18n.t("src_ua_yes", names=yes_n))
        if no_n:
            src_items.append(i18n.t("src_ua_no", names=no_n))
    src_items.append(i18n.t("src_extra"))
    story.append(bullets(src_items))
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=TEAL, spaceAfter=6))
    story.append(P(i18n.t("pipeline"), "small"))

    def first(c, d):
        cover_page(c, d, cfg, i18n, page, names, period)

    def later(c, d):
        header_footer(c, d, i18n, page, period)

    doc = SimpleDocTemplate(
        str(out),
        pagesize=(page.w, page.h),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=f"{cfg.title} — {period}",
        author="FX Brokers Research Pipeline",
        subject="config.yml forex broker comparison",
    )
    try:
        doc.build(story, onFirstPage=first, onLaterPages=later)
    except Exception as exc:
        raise ValueError(f"PDF build failed: {exc}") from exc
    return out
