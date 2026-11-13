# No Fix - CSAW 2026 Hack3D Final

Our solution to **A simple game of Chess**. We inspected the supplied STEP assembly and recovered its manufacturing clues. The report uses our team's first-person account of the work.

The final report was revised on November 13, 2026. Its 18 pages retain the nine-section structure and explain the clue dependencies, failed attempts, corrections, and verification. The revision includes a fresh source-mesh rebuild, independent STEP imports and Pawn decoding, and another check of the recovered archives and G-code.

The report text and our chart labels use Times New Roman in black. The PDF embeds its fonts. The CAD lettering and recovered source drawing retain their original appearance.

## Submission files

| Google Form field | File |
| --- | --- |
| Team Name | `No Fix` |
| Team Report | [No_Fix_Team_Report.pdf](submission/No_Fix_Team_Report.pdf) |
| Code Upload | [No_Fix_Code.zip](submission/No_Fix_Code.zip) |
| Any additional supporting files | [No_Fix_Supporting.zip](submission/No_Fix_Supporting.zip) |

The [final PowerPoint](presentation/output/No_Fix_7_Minute_Final.pptx) has 12 slides with editable tables and diagrams. It follows the final report and includes a complete English and Chinese script plus Q&A details in each slide's speaker notes. The [PDF backup](presentation/output/No_Fix_7_Minute_Final.pdf) uses the same slide order. The [bilingual speaker scripts](presentation/SPEAKER_SCRIPTS_EN_ZH.md) and [rehearsal guide](presentation/REHEARSAL_ZH.md) match this version. The overall [No Fix.zip](submission/No%20Fix.zip) also follows the single-ZIP wording in the problem statement. See the [upload guide](SUBMISSION_GUIDE_ZH.md) before using the form.

The presentation lasts seven minutes, followed by three minutes of questions. Speakers A, B, C, and D each have 105 seconds and three consecutive slides. English and Chinese are alternative versions of the same timed speech. The slides use Times New Roman and black text.

## Results

- **Material:** the internal 25 x 25 QR pattern resolves to the official AlF357 material sheet.
- **Final heights:** King 90 mm, Queen 80 mm, Rook 50 mm, Bishop 70 mm, Knight 60 mm, Pawn 50 mm.
- **Knight link:** 37 pawn positions decode to `Hack3d26-2`. Four trailing zero bits remain after the 60-bit message.
- **Pawn files:** a Caesar shift of -3 on the rook's inscription gives a promotion question. The case-sensitive password `Queen` opens both ZIP members.
- **King file:** a tiny inscription on its central body supplies the King G-code link.
- **Knight original CAD:** the partial Knight G-code contains a fallback link to a full STEP assembly.

The recovered Pawn STEP has 31 solid instances, and the Knight STEP has 61. The [result JSON](results/decoded.json), [G-code checks](results/gcode_checks.json), and [source registry](results/source_registry.json) record the details. The [report source](docs/report.md) includes the procedures and actual unsuccessful attempts.

## Run the analysis

We used Python 3.12. From this repository's root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/analyze.py
python src/check_gcode.py
python src/preview_cad.py
python src/build_report.py
```

The original distribution is in `inputs/`, so the geometry analysis and ZIP extraction work offline after installing the dependencies. The recovered remote files are already in `recovered/`; the scripts do not need an account, token, or live link. Source URLs remain in the registry for verification. OpenCascade's STEP import converts the inch-based source assembly to millimeters.

`analyze.py` is specific to this supplied assembly. Its solid numbers and sampling coordinates are documented in the code. We manually transcribed the inscriptions into `results/transcribed_clues.json`; the code exports evidence views, then checks the pattern arithmetic and archive extraction. It does not claim to be a general OCR or STEP parser.

To rebuild the source PDF image used in the report, install Poppler and run:

```sh
pdftoppm -scale-to 2000 -png 'recovered/Pawn Exploded View.pdf' 'evidence/pawn_exploded'
```

The presentation source is [build_deck.mjs](presentation/build_deck.mjs). It uses the Artifact Tool runtime bundled with Codex. The exported PPTX is included for normal PowerPoint use; Python is only needed for the analysis and PDF report.

The report renderer loads Times New Roman from `/System/Library/Fonts/Supplemental` on macOS. To rebuild on another system, point `font_dir` in `src/build_report.py` to the installed Times New Roman files and make that family available to Matplotlib. Viewing the delivered PDF does not require installing the fonts.

## What the checks establish

We verified the board decodes, ZIP CRCs, recovered STEP imports, and exact source hashes. We inspected G-code without sending it to hardware. The Knight file has only 78 numbered layers against 177 in its header and includes two non-G-code lines. Its original STEP is the recovery route. The King file has shutdown commands and reaches the header's maximum Z, with a one-layer header mismatch (337 declared versus 336 marked).

The inscriptions, target dimensions, prototype CAD, and filament G-code are separate evidence. The King inscription mentions metal production, but its linked commands describe filament extrusion. We did not test a metal build, validate hardware fits, or manufacture a finished set. We preserved the recovered files without repairing or rescaling them.

## Sources

The three original files come from the challenge distribution. The exploded pawn drawing credits Works by Design. The recovered remote manufacturing files come from the links embedded in that distribution. The material source is the [official EOS datasheet](https://www.eos.info/var/assets/03_system-related-assets/material-related-contents/metal-materials-and-examples/metal-material-datasheet/aluminium/material_datasheet_eos_aluminium_alf357_premium_en.pdf); we link to it instead of republishing the complete third-party PDF. No AI-generated image is used as experimental or CAD evidence.
