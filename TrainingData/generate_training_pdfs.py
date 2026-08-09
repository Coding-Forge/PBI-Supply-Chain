from html import escape
from pathlib import Path
import re
import shutil

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
DOCUMENTS = (
    "INSTRUCTIONS",
    "POWER_QUERY_TRANSFORMATIONS",
    "REPORT_BUILDING_GUIDE",
)


def register_fonts():
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Arial", fonts / "arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", fonts / "arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Consolas", fonts / "consola.ttf"))


def inline(text):
    text = escape(text.strip())
    text = re.sub(r"\[([^]]+)]\(([^)]+)\)", r'<link href="\2" color="#006D77">\1</link>', text)
    text = re.sub(r"`([^`]+)`", r'<font name="Consolas" color="#7A2838">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    return text


def styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#24323D"),
            spaceAfter=6,
        ),
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Arial-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#12343B"),
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Arial-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#12343B"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName="Arial-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#006D77"),
            spaceBefore=8,
            spaceAfter=4,
        ),
        "h4": ParagraphStyle(
            "Heading4",
            parent=base["Heading4"],
            fontName="Arial-Bold",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#7A2838"),
            spaceBefore=6,
            spaceAfter=3,
        ),
        "list": ParagraphStyle(
            "List",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=9.5,
            leading=13,
            leftIndent=18,
            firstLineIndent=-9,
            spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=9,
            leading=13,
            leftIndent=14,
            rightIndent=8,
            borderColor=colors.HexColor("#E9C46A"),
            borderWidth=1,
            borderPadding=7,
            backColor=colors.HexColor("#FFF9E8"),
            spaceAfter=7,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Consolas",
            fontSize=7.5,
            leading=10,
            leftIndent=7,
            rightIndent=7,
            borderPadding=7,
            borderColor=colors.HexColor("#C8D5D8"),
            borderWidth=0.5,
            backColor=colors.HexColor("#F3F7F7"),
            spaceAfter=7,
        ),
        "cell": ParagraphStyle(
            "Cell",
            fontName="Arial",
            fontSize=7.2,
            leading=9,
            textColor=colors.HexColor("#24323D"),
        ),
        "cell_header": ParagraphStyle(
            "CellHeader",
            fontName="Arial-Bold",
            fontSize=7.2,
            leading=9,
            textColor=colors.white,
        ),
    }


def is_structure(line):
    stripped = line.strip()
    return (
        not stripped
        or stripped.startswith(("#", "```", ">", "|"))
        or stripped == "---"
        or re.match(r"^\s*(?:[-*]|\d+\.)\s+", line)
    )


def table_flowable(lines, style, width):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        row_style = style["cell_header"] if not rows else style["cell"]
        rows.append([Paragraph(inline(cell), row_style) for cell in cells])
    columns = max(len(row) for row in rows)
    for row in rows:
        row.extend(Paragraph("", style["cell"]) for _ in range(columns - len(row)))
    table = Table(rows, colWidths=[width / columns] * columns, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#006D77")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAB9BC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7F7")]),
            ]
        )
    )
    return table


def markdown_story(text, width):
    style = styles()
    story = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("```"):
            language = stripped[3:].strip()
            index += 1
            code = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            label = f"{language.upper()}\n" if language else ""
            story.append(Preformatted(label + "\n".join(code), style["code"], maxLineLength=100))
            index += 1
            continue
        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.extend([table_flowable(table_lines, style, width), Spacer(1, 7)])
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            key = "title" if level == 1 else f"h{level}"
            story.append(Paragraph(inline(heading.group(2)), style[key]))
            index += 1
            continue
        if stripped == "---":
            story.extend([HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#94A7AA")), Spacer(1, 6)])
            index += 1
            continue
        if stripped.startswith(">"):
            story.append(Paragraph(inline(stripped.lstrip("> ")), style["quote"]))
            index += 1
            continue
        item = re.match(r"^\s*(?:([-*])|(\d+)\.)\s+(.+)$", line)
        if item:
            marker = "•" if item.group(1) else f"{item.group(2)}."
            story.append(Paragraph(f"{marker}&nbsp;&nbsp;{inline(item.group(3))}", style["list"]))
            index += 1
            continue
        paragraph = [stripped]
        index += 1
        while index < len(lines) and not is_structure(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        story.append(Paragraph(inline(" ".join(paragraph)), style["body"]))
    return story


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C8D5D8"))
    canvas.line(0.65 * inch, 0.48 * inch, 7.85 * inch, 0.48 * inch)
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(colors.HexColor("#52656B"))
    canvas.drawString(0.65 * inch, 0.3 * inch, "Coding-Forge Power BI Training")
    canvas.drawRightString(7.85 * inch, 0.3 * inch, f"Page {document.page}")
    canvas.restoreState()


def build(source, destination):
    document = SimpleDocTemplate(
        str(destination),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.65 * inch,
        title=source.stem.replace("_", " ").title(),
        author="Coding-Forge",
        subject="Power BI training material",
    )
    story = markdown_story(source.read_text(encoding="utf-8"), document.width)
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    register_fonts()
    copy_directories = (PROJECT / "placeholder", PROJECT / "Coding-Forge_Data")
    for directory in copy_directories:
        directory.mkdir(exist_ok=True)
    for name in DOCUMENTS:
        source = ROOT / f"{name}.md"
        destination = ROOT / f"{name}.pdf"
        build(source, destination)
        for directory in copy_directories:
            shutil.copy2(destination, directory / destination.name)
    generic_pdf = ROOT / "POWER_QUERY_M_CODE.pdf"
    for directory in copy_directories:
        shutil.copy2(generic_pdf, directory / generic_pdf.name)


if __name__ == "__main__":
    main()