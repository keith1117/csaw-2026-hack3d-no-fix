"""Render our report source with ReportLab. Only basic Markdown is needed here."""

from pathlib import Path
import html
import re
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 504
font_dir = Path("/System/Library/Fonts/Supplemental")
body_font, title_font, italic_font, mono_font = "Times-Roman", "Helvetica-Bold", "Times-Italic", "Courier"
if (font_dir / "Times New Roman.ttf").exists():
    for name, filename in [("NoFixTimes", "Times New Roman.ttf"), ("NoFixTimesBold", "Times New Roman Bold.ttf"),
                           ("NoFixTimesItalic", "Times New Roman Italic.ttf"),
                           ("NoFixTimesBoldItalic", "Times New Roman Bold Italic.ttf"),
                           ("NoFixArialBold", "Arial Bold.ttf"), ("NoFixMono", "Courier New.ttf")]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily("NoFixTimes", normal="NoFixTimes", bold="NoFixTimesBold",
                                  italic="NoFixTimesItalic", boldItalic="NoFixTimesBoldItalic")
    body_font, title_font, italic_font, mono_font = "NoFixTimes", "NoFixArialBold", "NoFixTimesItalic", "NoFixMono"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportBody", fontName=body_font, fontSize=11,
                          leading=14.5, spaceAfter=8))
styles.add(ParagraphStyle(name="ReportTitle", fontName=title_font, fontSize=22,
                          leading=27, textColor=colors.HexColor("#173f42"), spaceAfter=14))
styles.add(ParagraphStyle(name="ReportHeading", fontName=title_font, fontSize=13,
                          leading=17, spaceBefore=7, spaceAfter=8))
styles.add(ParagraphStyle(name="CaptionSmall", fontName=italic_font, fontSize=9,
                          leading=11, textColor=colors.HexColor("#465557"), spaceAfter=10))
styles.add(ParagraphStyle(name="CellSmall", fontName=body_font, fontSize=9.5, leading=12))


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="#125a70">\1</link>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", lambda m: f'<font name="{mono_font}" size="9">{m.group(1)}</font>', text)
    return text


def page_number(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#667578"))
    canvas.drawString(54, 28, "No Fix - CSAW 2026 Hack3D Final")
    canvas.drawRightString(558, 28, str(doc.page))


def build():
    lines = (ROOT / "docs/report.md").read_text().splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == "<!-- page -->":
            story.append(PageBreak())
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["ReportTitle"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["ReportHeading"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["ReportHeading"]))
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)(?:\{height=(\d+)\})?", line)
            caption, filename, height = match.groups()
            path = ROOT / filename
            with PILImage.open(path) as im:
                width_px, height_px = im.size
            max_height = int(height) if height else 85
            factor = min(WIDTH / width_px, max_height / height_px)
            image = Image(str(path), width_px * factor, height_px * factor)
            image.hAlign = "CENTER"
            story.append(KeepTogether([image, Spacer(1, 4), Paragraph(inline(caption), styles["CaptionSmall"])]))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [s.strip() for s in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", s) for s in cells):
                    rows.append(cells)
                i += 1
            n = len(rows[0])
            widths = [WIDTH/n]*n
            if n == 2:
                widths = [WIDTH*.72, WIDTH*.28]
            data = [[Paragraph(inline(cell), styles["CellSmall"]) for cell in row] for row in rows]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2eae8")),
                ("LINEBELOW", (0, 0), (-1, 0), .5, colors.HexColor("#627a7c")),
                ("LINEBELOW", (0, 1), (-1, -1), .25, colors.HexColor("#d4d9d7")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 9)])
            continue
        elif line.startswith("- "):
            story.append(Paragraph("- " + inline(line[2:]), styles["ReportBody"]))
        else:
            if line.startswith("> "):
                line = line[2:]
            story.append(Paragraph(inline(line), styles["ReportBody"]))
        i += 1
    output = ROOT / "output/pdf/No_Fix_Team_Report.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output), pagesize=(612, 792), rightMargin=54,
                            leftMargin=54, topMargin=45, bottomMargin=48,
                            title="No Fix - CSAW 2026 Hack3D Final Report", author="No Fix")
    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(output)


if __name__ == "__main__":
    build()
