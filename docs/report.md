# A simple game of Chess
## CSAW 2026 Hack3D Final Report
**Team: No Fix**

Final report | November 13, 2026

We investigated the supplied chess assembly to recover the manufacturing information hidden in its geometry and linked files. We recovered a material specification, six target piece heights, a password-protected Pawn assembly and drawing, King G-code, and an original Knight STEP assembly reached through incomplete Knight G-code.

We used Python and OpenCascade to inspect the STEP assembly, export readable views, sample geometric patterns, and check the recovered files. We read the small inscriptions from enlarged views and recorded those transcriptions as inputs to our scripts. We then checked the calculations against the geometry, opened the recovered CAD assemblies, and verified the archive contents. We preserved the original distribution and recovered manufacturing files.

### The information we recovered

| Starting clue | Recovered information | Check and report section |
| --- | --- | --- |
| Pawn positions and board instructions | Knight G-code link: Hack3d26-2 | 37 occupied squares; six-bit lookup; working redirect. Section 2 |
| Internal board QR pattern | EOS Aluminium AlF357 material sheet | Decode of the reconstructed 25 x 25 pattern. Section 3 |
| Bottom grid, piece labels, and ruler | K 90, Q 80, R 50, B 70, Kn 60, P 50 mm | Binary rows and cm unit. Section 4 |
| Rook inscription | Password Queen; Pawn STEP and exploded drawing | Both ZIP members extracted with matching CRCs. Sections 5-6 |
| King's central body | PI3MK2_King.gcode | Exact inscription link; command and layer checks. Section 7 |
| Note in incomplete Knight G-code | Knight-Full Assm.step | Fresh STEP import: 61 solid instances. Section 8 |

### Our starting files

| Supplied file | Size in bytes |
| --- | --- |
| Chess Board.STEP | 45,768,461 |
| Hack3d 2026 Final Challenge Problem Statement.pdf | 295,304 |
| Pawn Files.zip | 2,845,944 |

We explain the clues, procedures, and unsuccessful attempts below. Section 9 provides checks and reproduction steps. Physical printing and assembly remain untested.

<!-- page -->
# 1. Looking inside the assembly
### 1.1 From a text search to geometry inspection

We began by reading the problem statement and listing the three supplied files. The STEP assembly was the main place to search because the statement said that missing information had hints hidden within the file. The encrypted ZIP gave us a separate question to answer: where could we find its password?

We first searched the STEP file as text. We found product names such as board, Pon, King, Rook Red, and Bishop Red, together with export information. We did not find a plaintext password or a readable hidden message. That search helped us identify parts, but it did not explain the encoded information. We therefore inspected the modeled surfaces and internal bodies.

We loaded the STEP with OpenCascade through the Python OCP package. The importer converted the source units to millimeters and retained the assembly placements. We traversed the placed solids and saved their volumes, centers, and triangulated faces. We found **129 solid instances**. This is a count of placed bodies, including repeated parts and small lettering bodies, rather than a count of unique chess-piece designs.

We identified 37 repeated Pawn instances on the playing area. The assembly also contained pieces below the board and details hidden by exterior surfaces. We inspected those regions by separating solids and selecting faces at particular coordinates.

![Figure 1. Our cutaway view of the supplied king geometry. Removing covering surfaces reveals the lattice and the narrow central body. This is a CAD inspection view.](evidence/solid_89_cut.png){height=225}

### 1.2 Making hidden surfaces readable

For flat inscriptions, we selected triangles lying on the same plane, projected them into a two-dimensional view, and rotated or reflected the view to read the lettering from the appropriate side. We kept the coordinates used for these views in `src/analyze.py`. This let us return to the same source faces instead of relying on an unexplained screenshot.

<!-- page -->
# 1. Board clues and our next steps
### 1.3 The board's instructions

Along an internal board edge, we found the following text:

> Every square has a value, whether occupied or bare. Begin at the highest rank, and read each row with care. Six at a time will reveal what you seek; the knight's missing instructions are hidden in this technique.

> Once the message is revealed, append it to https://tinyurl.com/ to uncover what has been concealed.

![Figure 2. The instruction lettering exported from the board's internal geometry. We enlarged this view to transcribe the message.](evidence/board_instruction.png){height=65}

We also found this character sequence:

`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_`

![Figure 3. The engraved character table. Its order supplies the index-to-character mapping used in Section 2.](evidence/alphabet.png){height=55}

The wording gave us a reason to examine occupied and empty squares as two states. It also specified the row order, a group size of six, a link prefix, and the Knight as the expected result. The 64-character table supported that reading: six bits can represent 64 values, from 0 to 63.

We used the engraved rank labels to establish orientation. In the imported coordinate system, the playing area lies in the X-Z plane, and rank 8 lies toward negative Z. We read files A through H within each rank. A camera view alone could reverse that order, so we kept the rank labels as part of the evidence.

![Figure 3a. The rank labels exported from the board edge. We used their order to locate rank 8 in the source coordinate system.](evidence/rank_labels_geometry.png){height=40}

### 1.4 Following the separate clue branches

The board contained several independent clues. We used its Pawn positions for the Knight link, its square internal pattern for the material specification, and its bottom rows for dimensions. We then investigated the rook and king interiors for their own messages. Recovering one result did not automatically establish the others; each branch needed its own decoding and check.

We saved the text we read by eye in `results/transcribed_clues.json`. Our code samples geometry and performs arithmetic. It uses our transcriptions for lettering and does not perform general OCR. We kept these roles explicit so a reviewer can compare the written clues with their source views.

<!-- page -->
# 2. Reading the Pawn positions
### 2.1 Turning the playing area into bits

Following the board instruction, we assigned 1 to occupied squares and 0 to empty squares. We mapped the 37 Pawn centers to their nearest squares. Adjacent centers are 42.8625 mm apart; file A has X = -139.7 mm and rank 8 has Z = -139.7 mm.

All 37 assignments fell inside the grid, with no duplicate squares. The largest center offset on either grid axis was about 5.21 mm, below the 21.43 mm half-spacing. This checked the assignment despite differences between a Pawn's volume center and base center.

![Figure 4. The occupancy grid computed from the placed Pawn centers. We read rank 8 first, from file A to H, then continue down the rows.](evidence/occupancy.png){height=230}

### 2.2 The complete 64-bit record

| Rank | Bits, files A through H |
| --- | --- |
| 8 | 00011101 |
| 7 | 10100111 |
| 6 | 00100100 |
| 5 | 11011101 |
| 4 | 11011101 |
| 3 | 10111010 |
| 2 | 11111011 |
| 1 | 01100000 |

We joined these rows without separators. Their 37 one-bits matched the 37 Pawn instances, providing a second check on the grid transcription.

<!-- page -->
# 2. Decoding the Knight link
### 2.3 Applying the six-bit character table

We divided the bit stream into complete groups of six, as the inscription requested. We converted each group to a decimal value and looked up that value in the engraved alphabet, counting from zero. For example, 000111 equals 7, so it selects H, the eighth character. Starting the count at one would change the message.

| Group | Six bits | Decimal index | Character |
| --- | --- | --- | --- |
| 1 | 000111 | 7 | H |
| 2 | 011010 | 26 | a |
| 3 | 011100 | 28 | c |
| 4 | 100100 | 36 | k |
| 5 | 110111 | 55 | 3 |
| 6 | 011101 | 29 | d |
| 7 | 110110 | 54 | 2 |
| 8 | 111010 | 58 | 6 |
| 9 | 111110 | 62 | - |
| 10 | 110110 | 54 | 2 |

The ten complete groups produced **Hack3d26-2**. We appended that exact, case-sensitive string to the given prefix and opened [https://tinyurl.com/Hack3d26-2](https://tinyurl.com/Hack3d26-2). It redirected to the Drive file `PI3MK2_K14.gcode`. The file type and Knight name agreed with the inscription's reference to missing Knight instructions.

### 2.4 The remaining bits and the failed orientation

Sixty-four board bits do not divide evenly into groups of six. After the ten groups, four bits remained: **0000**. We recorded them separately. Adding two invented zero bits would create an extra 000000 group and append A, but the clue gave us no instruction to add those bits. We used the ten complete groups, and the working destination supported that interpretation. We have not assigned a further meaning to the four remaining bits.

Our first attempt read the positive-Z side first. That order produced `YPu63d0kpx`, with four remaining bits, rather than the recovered Knight link. We returned to the engraved rank labels and corrected the direction to rank 8 first. The combination of source labels, the decoded suffix, and its actual destination gave us stronger evidence than the appearance of the text alone.

The recovered file still needed inspection. We checked its commands and followed its recovery note in Section 8.

<!-- page -->
# 3. Recovering the material link
### 3.1 Recognizing the internal QR pattern

We found another square pattern inside the board on a plane at Y = 3.175 mm. Its three large corner markers suggested a QR code. We first exported that geometry as a flat image and tried to scan it. The scan failed: gaps between the modeled square faces interrupted the continuous modules expected in a normal QR image.

We therefore reconstructed the module grid from the geometry. We identified 25 module positions along each axis, at a pitch of 14.2875 mm. For each position, our script tested whether the module center lay inside a projected face. Sampling centers avoided treating the gaps between neighboring squares as extra white modules.

<!-- pair evidence/qr_geometry.png | evidence/qr_restored.png | height=190 -->

Figure 5. Left: the direct geometry view, with gaps between physical squares. Right: the filled module grid used for decoding. Both represent the same source pattern.

### 3.2 Rebuilding a readable code

We filled one image cell for each sampled module, set the black-and-white polarity so the QR markers had the expected appearance, and added a four-module white border. We enlarged the image with nearest-neighbor sampling to keep the cell edges sharp. These steps changed the presentation of the pattern while retaining its sampled module values.

We passed the restored image to the ZXing decoder. It returned one result: [https://tinyurl.com/Hack3d26](https://tinyurl.com/Hack3d26). This suffix differs from the Pawn-position suffix by the missing `-2`; we kept the two links separate because they lead to different information.

The QR link redirected to an official EOS Aluminium AlF357 material data sheet. This connected the board pattern to a named material and a manufacturing reference. We used that destination, rather than the visual appearance of the chess pieces, to identify the alloy.

<!-- page -->
# 3. Recording the material information
### 3.3 What the linked specification supplies

We read the [EOS Aluminium AlF357 material data sheet](https://www.eos.info/var/assets/03_system-related-assets/material-related-contents/metal-materials-and-examples/metal-material-datasheet/aluminium/material_datasheet_eos_aluminium_alf357_premium_en.pdf), status 02/2020, and recorded the following information. The page references below use the PDF's page order.

| Material item | Value from the linked sheet | PDF page |
| --- | --- | --- |
| Alloy | AlF357, a beryllium-free A357 derivative; AlSi7Mg0.6 | 2 |
| Generic powder size | 20-90 micrometers | 3 |
| Average specimen density | 2.67 g/cm3 | 6 and 11 |

The sheet provides separate system routes. We retained their association with the named machines instead of combining them into one set of settings.

| Process item | EOS M 290 | EOS M 400 |
| --- | --- | --- |
| Layer thickness | 30 micrometers | 60 micrometers |
| Volume rate | 5.8 mm3/s | 17 mm3/s |
| Inert gas | Nitrogen | Nitrogen |
| Powder part number | 9011-0049 | 9011-0049 |
| Source PDF page | 5 | 10 |

The linked heat-treatment cycle specifies 30 minutes at 540 +/- 6 C, measured at the part, followed by immediate room-temperature water quenching. It then specifies 6 hours at 165 +/- 6 C followed by air cooling, with aging started within 40 hours of solution annealing. The sheet gives this cycle on pages 5 and 10.

### 3.4 What we can conclude from the link

We recovered the material identity and the manufacturer's stated process information. These are source specifications. We did not measure alloy composition, powder properties, density, or heat-treatment results on a physical part.

The manufacturer ties its reported properties to the stated systems and conditions. We therefore kept the original official link available for the full composition tables, test conditions, and system requirements. We did not treat the summarized values as a tested recipe for our recovered chess assemblies.

The board's next manufacturing clue addressed size. We read it from the bottom grid and ruler, without using the material link to assume any dimensions.

<!-- page -->
# 4. Recovering the final height table
### 4.1 Reading the rows, bit order, and unit

On the board's bottom, we found six rows labeled K, Q, R, B, Kn, and P, each with eight square positions. The two face levels were Y = -1.905 mm and Y = -3.175 mm. We sampled the centers of the eight positions in each labeled row and assigned shallow positions 1 and deeper positions 0, reading left to right in the upright labeled view.

![Figure 6. The six labeled source rows. We colored shallow positions red and deep positions gray to make the two states visible.](evidence/height_geometry.png){height=160}

| Piece | Eight-bit row | Decimal value in cm | Target height in mm |
| --- | --- | --- | --- |
| King | 00001001 | 9 | 90 |
| Queen | 00001000 | 8 | 80 |
| Rook | 00000101 | 5 | 50 |
| Bishop | 00000111 | 7 | 70 |
| Knight | 00000110 | 6 | 60 |
| Pawn | 00000101 | 5 | 50 |

For example, the King row has one-bits in the 8 and 1 positions, giving 9. The nearby ruler is marked cm, so we converted 9 cm to 90 mm. We also compared the opposite polarity: it gives 246, 247, 250, 248, 249, and 250 cm. The labeled ruler and chess-piece context support the shallow-1 reading above.

<!-- page -->
# 4. Checking units and prototype sizes
### 4.2 Using the ruler and the size note

We checked the nearby ruler before assigning a unit to the decoded numbers. Its cm label supplies the unit; the binary rows alone would only give integers. We used 10 mm per centimeter to convert the six results in the preceding table.

![Figure 6a. The nearby source ruler, including its cm label.](evidence/cm_ruler.png){height=55}

The accompanying note says, **Final sizes may not be reflected in prototype parts**. We therefore kept the decoded target heights as their own result. A recovered STEP envelope or a slicer's maximum Z can describe a different orientation or prototype scale; neither replaces the labeled height table.

![Figure 6b. The size note exported from the source geometry.](evidence/prototype_note.png){height=55}

### 4.3 Handling dimensions that describe different things

We recorded the recovered CAD coordinate envelopes in `results/recovered_cad_checks.json`. Those envelopes describe the imported assemblies in their source frames. A maximum coordinate also depends on the model's position; even a maximum-minus-minimum extent still depends on orientation. We therefore did not use an arbitrary axis value as a substitute for the decoded final piece height.

We preserved the original geometry and hardware dimensions. Uniformly scaling every component would also scale pin holes, magnet seats, and spring spaces, without evidence that the specified hardware would fit. Producing resized working mechanisms would require assembly and fit checks beyond our file analysis.

This gave us a consistent way to report all three kinds of dimensions: the board's target heights, the STEP source geometry, and the G-code's build-coordinate limits. We use the last of these to check a G-code file against its own header in Sections 7 and 8.

<!-- page -->
# 5. Unlocking the Pawn files
### 5.1 Moving from password guesses to a written clue

The board routes gave us links and dimensions, but the supplied `Pawn Files.zip` still required a password. Before reading the rook inscription, we tried `985765`, the six decoded height values joined together, and the recovered strings `Hack3d26`, `Hack3d26-2`, and `AlF357`. None opened the archive. These failures showed that reusing another branch's answer did not resolve the ZIP.

We inspected the rook's interior and found a line of small text near its base. We selected faces at Y = -2.54 mm and rotated the projected view to make the line readable.

![Figure 7. The rook's encrypted sentence. Some letter counters merge in this face projection, so we checked the transcription against the decoded sentence and archive result.](evidence/rook_cipher.png){height=65}

We transcribed the line as:

`Zkdw lv wkh ehvw slhfh iru d sdzq wr wxuq lq wr?`

### 5.2 Decoding the sentence and testing the answer

The spaces and punctuation suggested a substituted sentence. Moving alphabetic characters back three places gave readable English: **What is the best piece for a pawn to turn in to?** For example, Z becomes W, k becomes h, d becomes a, and w becomes t, so `Zkdw` becomes `What`. We preserved spaces and punctuation while shifting the letters.

We interpreted the question as a Pawn-promotion clue and tried **Queen**, with an uppercase Q. We treated that word as a password candidate until the archive accepted it. Python's ZIP reader then extracted both `Pawn Files/Pawn.STEP` and `Pawn Files/Pawn Exploded View.pdf` and checked their CRC values. We also compared the extracted bytes with our delivered recovered files.

This check established the exact password independently of whether Queen is the best promotion in every possible chess position. We needed the answer accepted by this archive, and `Queen` opened both complete members.

The successful extraction gave us geometry and an assembly drawing. We inspected both because an outside Pawn shape alone would not describe its internal parts or purchased hardware.

<!-- page -->
# 6. Understanding the recovered Pawn
### 6.1 Checking the STEP against the exploded drawing

We imported `Pawn.STEP` and found **31 solid instances**. The accompanying PDF is titled **QUEEN-PAWN** and credits **Works by Design**. We kept the recovered filenames and the drawing's title, since those are the source labels.

![Figure 8. Our preview of the recovered Pawn assembly. The colors distinguish bodies for inspection; they do not specify materials.](evidence/pawn_cad.png){height=200}

The drawing labels parts Q1 through Q21. Twenty-one labels do not imply twenty-one physical pieces: Q1 and Q3 each have quantity two, and Q6 and Q13 each have quantity five. The remaining seventeen labels have quantity one. We calculated **2 + 2 + 5 + 5 + 17 = 31** labeled body pieces, matching the STEP instance count. This agreement checked our reading of the repeated quantities.

### 6.2 Hardware recovered from the drawing

| Hardware label as supplied | Quantity |
| --- | --- |
| N52 magnets, 1/4 x 3/16 inch | 2 |
| Springs, 0.3 x 3 x 5 mm | 2 |
| Spring, 0.6 x 8 x 50 mm | 1 |
| Pins, 1.5 x 6 mm | 5 |
| Pins, 1.5 x 18 mm | 2 |

The magnet dimensions convert to 6.35 x 4.7625 mm. We retained the spring dimensions in the drawing's original order because it does not define the dimension convention. The hardware quantities are additional to the 31 labeled body pieces.

We used the exploded drawing to recover the relative part arrangement and hardware locations. Opening the STEP and matching these counts verifies file recovery and the parts list. We have not tested the assembled mechanism's motion, spring action, magnet retention, or fits.

<!-- page -->
# 6. The recovered assembly drawing

We include the complete source drawing here so the part labels, repeated quantities, and hardware locations can be read together. The original one-page PDF is also in the supporting files.

![Figure 9. The recovered Queen-Pawn exploded view, credited to Works by Design in the source drawing.](evidence/pawn_exploded-1.png){height=565}

<!-- page -->
# 7. Reading the King's internal link
### 7.1 Isolating the inscribed central body

The king's lattice and narrow central body gave us another region to inspect. The outer geometry covered the lettering, so we separated the central solid, selected its flat side, and enlarged the projected inscription. The cutaway in Figure 1 shows why the normal outside view was insufficient.

The inscription contained a Drive link and the words **Metal Units produced using this method**. The file ID was small enough that several characters looked ambiguous. Our first transcription returned 404. We enlarged the lettering and checked the ID again before accepting a destination.

![Figure 10. An enlarged portion of the King's geometric lettering used to resolve the Drive file ID.](evidence/king_id.png){height=65}

The corrected link was [the King's embedded Drive file](https://drive.google.com/file/d/1Kk8K4bplqJWDCqiRtARlxXEeBVDJ-CKM/view), with ID:

`1Kk8K4bplqJWDCqiRtARlxXEeBVDJ-CKM`

We retrieved `PI3MK2_King.gcode`, a 6,745,155-byte file. Its contents contained G-code motion and extrusion commands, giving us a concrete file to inspect rather than relying on the inscription's description.

### 7.2 Extracting its saved process settings

The file identifies a Prusa i3 MK2 profile and includes saved Cura settings. We recovered the following values from its header, commands, and settings block:

| Setting | Value stored in the King file |
| --- | --- |
| Nominal layer height | 0.2 mm |
| Extruder / bed temperature | 215 C / 80 C |
| Infill density | 10% |
| Top / bottom layers | 5 / 5 |
| Supports / adhesion | Tree supports / brim |
| Slicer time estimate | 7,105 seconds |
| Filament estimate | 4.34366 m |

We report these as recovered slicer settings and estimates. We did not measure a print time, material use, or finished part from a machine run.

<!-- page -->
# 7. Checking the King file
### 7.3 Comparing metadata with the commands

We read the G-code as text and tracked its motion coordinates, extrusion state, and numbered layer sections. For the inspection image below, we plotted outer-wall moves with increasing extrusion. We used the full command stream for the numerical checks and a subset of segments for the preview.

![Figure 11. Outer-wall extrusion paths from the King file. This plot reconstructs file contents and does not represent a completed print.](evidence/king_toolpath.png){height=245}

The header declares 337 layers. We found 336 numbered sections, labeled 0 through 335. The highest motion Z was 67.15 mm, matching the header's maximum Z. Near the end, we found `M104 S0`, `M140 S0`, fan-off commands, and motor-disable commands. These observations supported a normal ending to the command stream, while leaving the one-layer count discrepancy on record.

We could not establish the cause of that count mismatch from the file alone. We therefore preserved it instead of changing the header or claiming that the file had passed a complete printer simulation. Reaching the stated maximum Z and containing shutdown commands are useful checks, but they do not validate physical print quality or machine compatibility.

### 7.4 Resolving the metal-versus-filament mismatch

The inscription refers to metal production. The retrieved file describes filament extrusion, including an extruder, heated bed, and filament use. We retained both observations. The QR route establishes a linked aluminium material specification; this King file supplies a separate extrusion toolpath and saved settings.

We found no verified metal toolpath in that download. Treating the two sources as interchangeable would hide a gap in the supplied information. Our submission therefore records the mismatch and preserves the file exactly as received.

<!-- page -->
# 8. Investigating the Knight file
### 8.1 Checking the download before using it

The Pawn-position link from Section 2 led to [PI3MK2_K14.gcode](https://drive.google.com/file/d/1vgwSromaUAm5hw45NycKgomDprsVD3Lu/view), a file of 11,371,798 bytes. We applied the same command checks used for the King file so we could compare the header with the actual contents.

| Check | King file | Knight file |
| --- | --- | --- |
| Header layer count | 337 | 177 |
| Numbered layer sections | 336 | 78 |
| Last layer label | 335 | 77 |
| Header maximum Z | 67.15 mm | 34.95 mm |
| Highest motion Z | 67.15 mm | 15.75 mm |
| Extruder and bed shutdown commands | Present | Absent |
| Un-commented non-G-code text lines | 0 | 2 |

The Knight's numbered sections run from 0 through 77 without gaps. Counting them gives 78, leaving 99 of the 177 declared sections absent. The motion stops below the file's own stated maximum Z, and the file lacks the heater-off ending found in the King file. We used these observations together to identify the Knight paths as incomplete.

![Figure 12. The Knight's available outer-wall paths. The numerical truncation check uses its own header and motion data.](evidence/knight_toolpath.png){height=200}

The file still contains an `;End of Gcode` comment and saved settings. Those lines do not add the missing motion. We also kept this diagnosis separate from the 60 mm target Knight height: target dimensions and slicer Z extents describe different records, so their difference alone would not establish truncation.

<!-- page -->
# 8. Recovering the original Knight model
### 8.2 Following the file's explicit recovery note

Near the end of the Knight G-code, we found two lines of ordinary, un-commented text. Line 353917 says **If Corrupted please refer to original model**. The next line provides a Drive link. This was a direct recovery clue inside the downloaded file, so we followed it rather than trying to reconstruct absent upper layers from the partial paths.

The link led to [Knight-Full Assm.step](https://drive.google.com/file/d/1b94MhZaxK8I5xzezqY1e8n1fdASWHZjL/view), a 3,947,243-byte STEP file. We imported it with OpenCascade and found **61 solid instances**. The source contains 24 manifold solid definitions; the larger instance count includes repeated assembly parts.

![Figure 13. Our preview of the recovered original Knight assembly. Colors distinguish bodies and do not identify materials.](evidence/knight_cad.png){height=270}

### 8.3 What the recovery solves

The STEP supplies the original geometry needed for a new slicing attempt. Adding heater-off commands to the downloaded G-code would only add an ending; it would not recreate the missing model surfaces or upper-layer extrusion paths. We therefore delivered the partial G-code beside the recovered STEP, retaining both the evidence and the useful geometry.

The Knight file's saved Cura configuration includes the same 0.2 mm nominal layer height, 215 C extruder, 80 C bed, and 10% infill values found in the King file. Those saved values help describe the source setup. They do not make the incomplete toolpath complete. We have not generated or physically tested a replacement toolpath.

<!-- page -->
# 9. Reviewing the reasoning and results
### 9.1 Problems we encountered and how we handled them

| Attempt or problem | Observation | Our response and check |
| --- | --- | --- |
| Search the STEP as text | Names and export data, but no plaintext password | Inspect internal solids and selected face planes. Sections 1 and 5 |
| Scan the direct QR drawing | No decoded result; gaps interrupted the modules | Sample the 25 x 25 centers, fill cells, and add a white border. One decoded URL. Section 3 |
| Read the positive-Z board side first | YPu63d0kpx instead of the recovered Knight link | Recheck engraved ranks; read rank 8 first. Verify the resulting redirect. Section 2 |
| Try other recovered answers as ZIP passwords | 985765, Hack3d26, Hack3d26-2, and AlF357 all failed | Decode the rook question; Queen opens both members with CRC checks. Section 5 |
| Transcribe the small King file ID | First URL returned 404 | Enlarge the geometric lettering, correct the ID, and retrieve the G-code. Section 7 |
| Compare Knight commands with its header | Only 78 of 177 sections; motion stops at 15.75 mm | Follow its explicit fallback link and import the original STEP. Section 8 |

### 9.2 The checks behind our conclusions

For the final review, we reopened the supplied assembly and both recovered STEP files without using the saved mesh cache. We confirmed 129, 31, and 61 solid instances. The freshly imported source centers matched the saved geometry record, and we independently decoded the Pawn positions again. We also rebuilt the geometry-derived outputs and repeated the G-code and archive checks.

We checked the three original inputs against the supplied distribution and verified SHA-256 hashes for all eight original and recovered files. CRC checks confirmed complete extraction of both encrypted ZIP members. We rechecked both board short links and their destinations. The result tables and `results/final_review_checks.json` record these checks; `results/source_checksums.json` identifies the exact source bytes.

These tests support the decoded information, successful file recovery, and the inconsistencies we describe. They do not establish that a physical mechanism will function. Printing, assembly fit, motion, and manufacturing tolerances remain untested. We also leave the four unused board bits, the King's one-layer count difference, and the metal-versus-filament wording explicit instead of assigning unsupported explanations.

<!-- page -->
# 9. Reproducing the analysis and handoff
### 9.3 Running our scripts

We used Python 3.12 and the pinned packages in `requirements.txt`. From the repository root, create an environment, install those requirements, then run:

`python src/analyze.py`

`python src/check_gcode.py`

`python src/preview_cad.py`

`python src/build_report.py`

`python src/package_submission.py`

`python src/verify_delivery.py`

The first script exports the source views, samples the board patterns, performs the decodes, and extracts the Pawn ZIP. It caches the source meshes under `work/`; removing `work/geometry.json` makes it reimport and mesh the supplied STEP. The second reads G-code and produces the check table and path previews. The third reopens the recovered assemblies. The remaining scripts build and verify the submitted report and packages.

Our code uses solid indices and coordinates for this particular distribution. It also uses the manual inscriptions in `results/transcribed_clues.json`. The original inputs and recovered files are included for offline analysis after dependency installation. The scripts do not need to download the recovered files again.

### 9.4 Recovered files and source references

| Delivered file under recovered/ | Bytes | Origin |
| --- | --- | --- |
| Pawn.STEP | 9,392,435 | Encrypted supplied ZIP; Section 5 |
| Pawn Exploded View.pdf | 4,988,202 | Encrypted supplied ZIP; Works by Design drawing |
| PI3MK2_King.gcode | 6,745,155 | King's embedded Drive link; Section 7 |
| PI3MK2_K14.gcode | 11,371,798 | Pawn-position short link; Sections 2 and 8 |
| Knight-Full Assm.step | 3,947,243 | Recovery link in Knight G-code; Section 8 |

We obtained the distribution from the supplied local files. The [official EOS sheet](https://www.eos.info/var/assets/03_system-related-assets/material-related-contents/metal-materials-and-examples/metal-material-datasheet/aluminium/material_datasheet_eos_aluminium_alf357_premium_en.pdf) is our material reference; we retain its link without republishing the full third-party PDF. The full recovered-link list is in `results/source_registry.json`. Original recovery took place on November 12, with the final checks and report revision on November 13, 2026.

### 9.5 Submission contents

We provide this PDF for Team Report, `No_Fix_Code.zip` for Code Upload, and `No_Fix_Supporting.zip` for supporting files. The code ZIP contains all five recovered files, inputs, scripts, evidence, and results. The supporting ZIP contains the presentation PDF and PowerPoint, recovered CAD and drawing, and selected evidence. Limits are 100 MB for report/code and 10 MB for supporting files; `submission/manifest.json` records sizes and hashes. We also provide `No Fix.zip` and a [public repository](https://github.com/keith1117/csaw-2026-hack3d-no-fix).
