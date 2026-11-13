"""Check our delivered files, independently of the geometry cache."""

from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def check():
    hashes = json.loads((ROOT / "results/source_checksums.json").read_text())
    for name, expected in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    decoded = json.loads((ROOT / "results/decoded.json").read_text())
    assert sum(map(sum, decoded["occupancy"])) == 37
    assert decoded["knight_url"] == "https://tinyurl.com/Hack3d26-2"
    assert decoded["material_qr_url"] == "https://tinyurl.com/Hack3d26"
    assert [r["height_mm"] for r in decoded["heights"]] == [90, 80, 50, 70, 60, 50]
    with (ROOT / "results/final_heights.csv").open() as f:
        assert [int(row["height_mm"]) for row in csv.DictReader(f)] == [90, 80, 50, 70, 60, 50]
    with zipfile.ZipFile(ROOT / "inputs/Pawn Files.zip") as z:
        for name in ["Pawn.STEP", "Pawn Exploded View.pdf"]:
            assert z.read("Pawn Files/" + name, pwd=b"Queen") == (ROOT / "recovered" / name).read_bytes()

    pdf = ROOT / "submission/No_Fix_Team_Report.pdf"
    report = PdfReader(pdf)
    assert len(report.pages) == 18
    assert len(report.outline) == 9
    for page in report.pages:
        for font in page["/Resources"]["/Font"].values():
            font = font.get_object()
            assert "TimesNewRoman" in str(font["/BaseFont"]), font["/BaseFont"]
            assert "/FontFile2" in font["/FontDescriptor"].get_object()
    report_text = "\n".join(p.extract_text() for p in report.pages)
    for required in ["November 13, 2026", "Hack3d26-2", "Queen", "15.75", "61 solid instances"]:
        assert required in report_text, required
    assert pdf.read_bytes() == (ROOT / "output/pdf/No_Fix_Team_Report.pdf").read_bytes()
    pptx = ROOT / "presentation/output/No_Fix_10_Minute_Presentation.pptx"
    with zipfile.ZipFile(pptx) as z:
        assert z.testzip() is None
        slides = [n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+.xml", n)]
        notes = [n for n in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+.xml", n)]
        assert len(slides) == len(notes) == 12
        ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        assert sum(len(ET.fromstring(z.read(n)).findall(".//a:tbl", ns)) for n in slides) == 8
    timings = json.loads((ROOT / "presentation/notes.json").read_text())
    assert len(timings) == 12 and sum(n["seconds"] for n in timings) == 600
    assert len(PdfReader(ROOT / "presentation/output/No_Fix_10_Minute_Presentation.pdf").pages) == 12

    manifest = json.loads((ROOT / "submission/manifest.json").read_text())
    for row in manifest["files"]:
        path = ROOT / "submission" / row["file"]
        assert path.stat().st_size == row["bytes"] < row["limit_bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
                assert not any(n.startswith("/") or ".." in Path(n).parts for n in z.namelist())
    with zipfile.ZipFile(ROOT / "submission/No_Fix_Supporting.zip") as z:
        for name, digest in hashes.items():
            if name.startswith("recovered/"):
                assert hashlib.sha256(z.read(name)).hexdigest() == digest
    with zipfile.ZipFile(ROOT / "submission/No_Fix_Code.zip") as z:
        for name in ["docs/report.md", "src/build_report.py", "src/verify_delivery.py", "results/final_review_checks.json", "results/report_typography.json"]:
            assert z.read("NoFix/" + name) == (ROOT / name).read_bytes(), name
    with zipfile.ZipFile(ROOT / "submission/No Fix.zip") as z:
        for name in ["submission/No_Fix_Team_Report.pdf", "submission/No_Fix_Code.zip", "submission/No_Fix_Supporting.zip"]:
            assert z.read(name) == (ROOT / name).read_bytes(), name
    print("PASS: source hashes, decodes, current ZIP contents, 18 report pages/9 sections, 12 slides/notes, upload limits")


if __name__ == "__main__":
    check()
