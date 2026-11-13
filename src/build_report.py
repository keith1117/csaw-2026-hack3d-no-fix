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
for name, filename in [("NoFixTimes", "Times New Roman.ttf"), ("NoFixTimesBold", "Times New Roman Bold.ttf"),
                       ("NoFixTimesItalic", "Times New Roman Italic.ttf"),
                       ("NoFixTimesBoldItalic", "Times New Roman Bold Italic.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
pdfmetrics.registerFontFamily("NoFixTimes", normal="NoFixTimes", bold="NoFixTimesBold",
                              italic="NoFixTimesItalic", boldItalic="NoFixTimesBoldItalic")
body_font, title_font, italic_font = "NoFixTimes", "NoFixTimesBold", "NoFixTimesItalic"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportBody", fontName=body_font, fontSize=11,
                          leading=14.5, textColor=colors.black, spaceAfter=8))
styles.add(ParagraphStyle(name="ReportTitle", fontName=title_font, fontSize=22,
                          leading=27, textColor=colors.black, spaceAfter=14,
                          keepWithNext=True))
styles.add(ParagraphStyle(name="ReportHeading", fontName=title_font, fontSize=13,
                          leading=17, textColor=colors.black, spaceBefore=7, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name="CaptionSmall", fontName=italic_font, fontSize=9,
                          leading=11, textColor=colors.black, spaceAfter=10))
styles.add(ParagraphStyle(name="CellSmall", fontName=body_font, fontSize=9.5, leading=12,
                          textColor=colors.black))


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="black">\1</link>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", lambda m: f'<font name="{body_font}" size="9">{m.group(1)}</font>', text)
    return text


def page_number(canvas, doc):
    canvas.setFont(body_font, 9)
    canvas.setFillColor(colors.black)
    canvas.drawString(54, 28, "No Fix - CSAW 2026 Hack3D Final")
    canvas.drawRightString(558, 28, str(doc.page))


class ReportDocument(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "ReportTitle":
            title = flowable.getPlainText()
            match = re.match(r"^([1-9])\.", title)
            if match:
                key = "section" + match[1]
                if not hasattr(self, "section_keys"):
                    self.section_keys = set()
                if key not in self.section_keys:
                    self.canv.bookmarkPage(key)
                    self.canv.addOutlineEntry(title, key, level=0)
                    self.section_keys.add(key)


def report_image(filename, max_width, max_height):
    path = ROOT / filename
    with PILImage.open(path) as im:
        width_px, height_px = im.size
    factor = min(max_width / width_px, max_height / height_px)
    return Image(str(path), width_px * factor, height_px * factor)


def table_widths(rows):
    header = rows[0]
    if header[0] == "Rank":
        ratios = [.22, .78]
    elif header[0] == "Starting clue":
        ratios = [.26, .34, .40]
    elif header[0] == "Material item":
        ratios = [.34, .47, .19]
    elif header[0].startswith("Delivered file"):
        ratios = [.37, .17, .46]
    elif header[0] == "Attempt or problem":
        ratios = [.25, .28, .47]
    elif header[0] == "Group":
        ratios = [.15, .30, .30, .25]
    elif len(header) == 2:
        ratios = [.65, .35]
    elif len(header) == 3:
        ratios = [.38, .31, .31]
    else:
        ratios = [1 / len(header)] * len(header)
    return [WIDTH * value for value in ratios]


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
        elif line.startswith("<!-- pair "):
            match = re.fullmatch(r"<!-- pair (.*?) \| (.*?) \| height=(\d+) -->", line)
            left, right, height = match.groups()
            images = [report_image(name, WIDTH / 2 - 12, int(height)) for name in (left, right)]
            pair = Table([[images[0], images[1]]], colWidths=[WIDTH / 2] * 2)
            pair.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), body_font),
                                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                     ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
            story.append(KeepTogether([pair, Spacer(1, 7)]))
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["ReportTitle"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["ReportHeading"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["ReportHeading"]))
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)(?:\{height=(\d+)\})?", line)
            caption, filename, height = match.groups()
            max_height = int(height) if height else 85
            image = report_image(filename, WIDTH, max_height)
            image.hAlign = "CENTER"
            story.append(KeepTogether([image, Spacer(1, 4), Paragraph(inline(caption), styles["CaptionSmall"])]))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [s.strip() for s in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", s) for s in cells):
                    rows.append(cells)
                i += 1
            widths = table_widths(rows)
            padding = 3 if rows[0][0] == "Rank" else 5
            data = [[Paragraph(inline(cell), styles["CellSmall"]) for cell in row] for row in rows]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), body_font),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2eae8")),
                ("LINEBELOW", (0, 0), (-1, 0), .5, colors.HexColor("#627a7c")),
                ("LINEBELOW", (0, 1), (-1, -1), .25, colors.HexColor("#d4d9d7")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), padding),
                ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
            ]))
            story.extend([table, Spacer(1, 9)])
            continue
        elif line.startswith("- "):
            story.append(Paragraph("- " + inline(line[2:]), styles["ReportBody"]))
        elif line.startswith("Figure "):
            story.append(Paragraph(inline(line), styles["CaptionSmall"]))
        else:
            if line.startswith("> "):
                line = line[2:]
            story.append(Paragraph(inline(line), styles["ReportBody"]))
        i += 1
    output = ROOT / "output/pdf/No_Fix_Team_Report.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDocument(str(output), pagesize=(612, 792), rightMargin=54,
                            leftMargin=54, topMargin=45, bottomMargin=48,
                            initialFontName=body_font,
                            title="No Fix - CSAW 2026 Hack3D Final Report", author="No Fix",
                            subject="Final report: clue recovery, decoding, file checks, and limitations")
    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(output)


if __name__ == "__main__":
    build()
