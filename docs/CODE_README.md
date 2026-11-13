# No Fix analysis code

This folder contains our solution to the CSAW 2026 Hack3D final challenge, "A simple game of Chess".

## Contents

- `src/`: geometry analysis, G-code checks, CAD previews, report generation, packaging, and delivery checks.
- `inputs/`: the three original distribution files.
- `recovered/`: all five recovered manufacturing files, including both original G-code files.
- `results/`: decoded clues, height and hardware tables, source links, hashes, and analysis checks.
- `evidence/`: views exported from the geometry and recovered files.
- `docs/report.md`: the English report source.

## Run the analysis

We used Python 3.12. From this folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/analyze.py
python src/check_gcode.py
python src/preview_cad.py
python src/build_report.py
```

The original inputs and recovered files are included, so the analysis works offline after installing the dependencies. OpenCascade converts the STEP source units to millimeters. We manually read the small inscriptions from enlarged views and recorded them in `results/transcribed_clues.json`; the scripts perform geometry sampling, decoding, and archive checks.

`analyze.py` uses solid indices and coordinates specific to this distribution. Its first run imports and meshes the source STEP, then caches that geometry under `work/`. The other scripts inspect G-code and recovered assemblies and build the report.

The report renderer uses Times New Roman from `/System/Library/Fonts/Supplemental` on macOS. On another system, set `font_dir` in `src/build_report.py` to the installed Times New Roman files and make that family available to Matplotlib. The recovered drawing preview is already included. To rebuild it, install Poppler and run:

```sh
pdftoppm -scale-to 2000 -png 'recovered/Pawn Exploded View.pdf' 'evidence/pawn_exploded'
```

## Submission files

The separate supporting ZIP contains the presentation PDF, recovered CAD and assembly drawing, and selected evidence. Both G-code originals remain in this code ZIP to keep the supporting upload below 10 MB.

To rebuild or check the complete submission, extract the supporting ZIP into this folder, keeping its directory structure, and run the analysis/report commands first. Then run `python src/package_submission.py` and `python src/verify_delivery.py`. The full submission is also available from the team's public repository.

We checked file recovery, decoding, hashes, and archive extraction. Printing, assembly fit, and mechanism motion remain untested. The original G-code files are preserved, including the incomplete Knight paths and the King header discrepancy.
