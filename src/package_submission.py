"""Build the three upload files and the overall team ZIP."""

from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission"

EVIDENCE = ["alphabet.png", "board_instruction.png", "rank_labels_geometry.png",
            "qr_geometry.png", "qr_restored.png", "occupancy.png", "height_geometry.png",
            "prototype_note.png", "cm_ruler.png", "rook_cipher.png", "king_inscription.png",
            "king_id.png", "pawn_exploded-1.png", "pawn_cad.png", "knight_cad.png",
            "king_toolpath.png", "knight_toolpath.png", "source_assembly.jpg", "solid_89_cut.png"]


def archive(destination, files, prefix=""):
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for relative in sorted(set(files)):
            z.write(ROOT / relative, prefix + relative)
        assert z.testzip() is None


def main():
    OUT.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "output/pdf/No_Fix_Team_Report.pdf", OUT / "No_Fix_Team_Report.pdf")
    results = [str(p.relative_to(ROOT)) for p in (ROOT / "results").glob("*") if p.is_file()]
    recovered = [str(p.relative_to(ROOT)) for p in (ROOT / "recovered").glob("*") if p.is_file()]
    evidence = ["evidence/" + name for name in EVIDENCE]
    # Large previews are already in the report/code bundle. Keep every recovered
    # manufacturing source in this ZIP while meeting the form's 10 MB limit.
    large_previews = {"knight_toolpath.png", "pawn_exploded-1.png", "king_toolpath.png",
                      "solid_89_cut.png", "knight_cad.png", "pawn_cad.png", "source_assembly.jpg"}
    support_files = results + recovered + [name for name in evidence if Path(name).name not in large_previews]
    archive(OUT / "No_Fix_Supporting.zip", support_files)

    code_files = results + recovered + evidence + ["requirements.txt", "SUBMISSION_GUIDE_ZH.md", "docs/report.md",
        "presentation/build_deck.mjs", "presentation/notes.json", "presentation/REHEARSAL_ZH.md"]
    code_files += [str(p.relative_to(ROOT)) for folder in ["inputs", "src"]
                   for p in (ROOT / folder).glob("*") if p.is_file()]
    archive(OUT / "No_Fix_Code.zip", code_files, "NoFix/")
    main_readme = (ROOT / "README.md").read_text()
    code_readme = "# No Fix analysis code\n\nExtract this folder and run the commands below from its root. "
    code_readme += "The original distribution and recovered files are included for offline analysis. "
    code_readme += "The report and presentation binaries are separate submission files.\n\n"
    code_readme += main_readme[main_readme.index("## Run the analysis"):]
    with zipfile.ZipFile(OUT / "No_Fix_Code.zip", "a", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("NoFix/README.md", code_readme)

    files = ["submission/No_Fix_Team_Report.pdf", "submission/No_Fix_Code.zip", "submission/No_Fix_Supporting.zip",
             "presentation/output/No_Fix_10_Minute_Presentation.pptx",
             "presentation/output/No_Fix_10_Minute_Presentation.pdf",
             "presentation/REHEARSAL_ZH.md", "SUBMISSION_GUIDE_ZH.md"]
    archive(OUT / "No Fix.zip", files)
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
