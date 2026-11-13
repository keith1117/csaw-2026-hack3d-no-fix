"""Build the three upload files and the overall team ZIP."""

from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission"

RESULTS = ["decoded.json", "final_heights.csv", "pawn_hardware.csv",
           "transcribed_clues.json", "source_registry.json", "source_checksums.json",
           "gcode_checks.json", "recovered_cad_checks.json", "final_review_checks.json"]
SCRIPTS = ["analyze.py", "check_gcode.py", "preview_cad.py", "build_report.py",
           "package_submission.py", "verify_delivery.py"]
PRESENTATIONS = ["presentation/output/No_Fix_presentation.pdf",
                 "presentation/output/No_Fix_presentation.pptx"]
EVIDENCE = ["alphabet.png", "board_instruction.png", "rank_labels_geometry.png",
            "qr_geometry.png", "qr_restored.png", "occupancy.png", "height_geometry.png",
            "prototype_note.png", "cm_ruler.png", "rook_cipher.png", "king_inscription.png",
            "king_id.png", "pawn_exploded-1.png", "pawn_cad.png", "knight_cad.png",
            "king_toolpath.png", "knight_toolpath.png", "source_assembly.jpg", "solid_89_cut.png"]


def archive(destination, files, prefix="", readme=None):
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for relative in sorted(set(files)):
            z.write(ROOT / relative, prefix + relative)
        if readme is not None:
            z.writestr(prefix + "README.md", readme)
        assert z.testzip() is None


def main():
    OUT.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "output/pdf/No_Fix_Team_Report.pdf", OUT / "No_Fix_Team_Report.pdf")
    results = ["results/" + name for name in RESULTS]
    recovered = [str(p.relative_to(ROOT)) for p in (ROOT / "recovered").glob("*") if p.is_file()]
    evidence = ["evidence/" + name for name in EVIDENCE]

    # Keep G-code in the code ZIP to leave room for both presentation formats.
    large_previews = {"knight_toolpath.png", "pawn_exploded-1.png", "king_toolpath.png",
                      "solid_89_cut.png", "knight_cad.png", "pawn_cad.png", "source_assembly.jpg"}
    support_files = results + PRESENTATIONS
    support_files += [name for name in recovered if not name.endswith(".gcode")]
    support_files += [name for name in evidence if Path(name).name not in large_previews]
    archive(OUT / "No_Fix_Supporting.zip", support_files,
            readme=(ROOT / "docs/SUPPORTING_README.md").read_text())

    # A fixed list excludes local guides, rehearsal notes, and authoring checks.
    code_files = results + recovered + evidence + ["requirements.txt", "docs/report.md",
                 "docs/CODE_README.md", "docs/SUPPORTING_README.md"]
    code_files += ["src/" + name for name in SCRIPTS]
    code_files += [str(p.relative_to(ROOT)) for p in (ROOT / "inputs").glob("*") if p.is_file()]
    archive(OUT / "No_Fix_Code.zip", code_files, "NoFix/",
            readme=(ROOT / "docs/CODE_README.md").read_text())

    files = ["submission/No_Fix_Team_Report.pdf", "submission/No_Fix_Code.zip",
             "submission/No_Fix_Supporting.zip"] + PRESENTATIONS
    overall_readme = "# No Fix submission\n\n"
    overall_readme += "The submission folder contains the report PDF, code ZIP, and supporting ZIP.\n\n"
    overall_readme += "The presentation folder contains the PDF and native PowerPoint. "
    overall_readme += "Both are also included in the supporting ZIP. "
    overall_readme += "All five recovered manufacturing files are in the code ZIP.\n"
    archive(OUT / "No Fix.zip", files, readme=overall_readme)

    limits = {"No_Fix_Team_Report.pdf": 100_000_000, "No_Fix_Code.zip": 100_000_000,
              "No_Fix_Supporting.zip": 10_000_000, "No Fix.zip": 100_000_000}
    records = []
    for name, limit in limits.items():
        path = OUT / name
        size = path.stat().st_size
        assert size < limit, (name, size, limit)
        records.append({"file": name, "bytes": size, "limit_bytes": limit,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        print(name, f"{size/1_000_000:.2f} MB")
    (OUT / "manifest.json").write_text(json.dumps({"team": "No Fix", "files": records}, indent=2) + "\n")


if __name__ == "__main__":
    main()
