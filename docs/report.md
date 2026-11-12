# A simple game of Chess
## CSAW 2026 Hack3D Final Report
**Team: No Fix**

November 12, 2026

We worked on the supplied chess assembly to recover the manufacturing information hidden in it. We found clues in the board, the rook, the king, and the positions of the pawns. These led us to a material specification, a table of final piece heights, the encrypted pawn assembly, and manufacturing files for the knight and king.

We used Python to inspect the STEP geometry, draw selected layers, decode the board patterns, and check the recovered files. We kept the original files unchanged. Our report describes the results we could verify from the files. We did not manufacture or test a physical chess set.

### Our recovered information
| Location | What we found | How we checked it |
| --- | --- | --- |
| Inside the board | Material link for AlF357 | Restored and decoded a 25 by 25 QR pattern |
| Bottom of the board | Six final heights in cm | Read the labeled binary rows and cm ruler |
| Pawn positions | Hack3d26-2 | Decoded 60 bits with the engraved character table |
| Inside the rook | Password: Queen | Applied a Caesar shift and extracted both ZIP members |
| Inside the king | King G-code link | Read the inscription and fetched the matching Drive file |
| End of knight G-code | Original knight STEP link | Downloaded and opened the 61-solid assembly |

### Files we started with
| File | Size in bytes |
| --- | --- |
| Chess Board.STEP | 45,768,461 |
| Hack3d 2026 Final Challenge Problem Statement.pdf | 295,304 |
| Pawn Files.zip | 2,845,944 |

The statement asks us to explain the clues, our procedures, and approaches that did not work. We include those steps below, along with the recovered files and scripts. The ZIP in the distribution uses a password, so we treated finding that password as part of the challenge.

<!-- page -->
# 1. Looking inside the assembly

We first checked the STEP file as text. This showed product names such as board, Pon, King, Rook Red, and Bishop Red, but it did not give us a password or a readable hidden message. The file stores much of the interesting information as geometry rather than normal text.

We then loaded the assembly with OpenCascade. Our script applied the assembly placements and converted the surfaces to triangles. It found 129 solid instances. Of these, 37 were repeated pawn shapes on the playing area. Other pieces sat below the board, and many small bodies belonged to the board's lettering.

An ordinary outside view hid several clues. We drew faces at selected coordinates instead. These drawings show actual faces from the model, with the covering geometry removed. They are inspection views rather than photographs of a manufactured part.

### The board's written instructions

We found two lines along the edge of an internal board layer. Our transcription is:

> Every square has a value, whether occupied or bare. Begin at the highest rank, and read each row with care. Six at a time will reveal what you seek; the knight's missing instructions are hidden in this technique.

> Once the message is revealed, append it to https://tinyurl.com/ to uncover what has been concealed.

We also found a 64-character alphabet:

`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_`

![The character table, viewed from the readable side.](evidence/alphabet.png)

The last two characters made a six-bit lookup table a reasonable approach. We recorded our manual transcriptions separately in `results/transcribed_clues.json`. The script does the geometric sampling and arithmetic, but it does not pretend to read every inscription automatically.

We used the engraved rank labels to choose the reading direction. In the imported coordinates, rank 8 is at the negative-Z side. The script then reads files A through H within each rank.

<!-- page -->
# 2. Reading the pawn positions

We assigned 1 to an occupied square and 0 to an empty square. We read rank 8 first, followed by ranks 7 through 1. We found 37 occupied squares, with no two pawn centers assigned to the same square.

![Our occupancy map. The row labels give the chess ranks.](evidence/occupancy.png){height=235}

The eight rows, in that order, are:

`00011101 10100111 00100100 11011101 11011101 10111010 11111011 01100000`

We joined the rows and split the first 60 bits into ten groups of six. We used each group as an index into the character table, starting at index 0.

| Six bits | 000111 | 011010 | 011100 | 100100 | 110111 | 011101 | 110110 | 111010 | 111110 | 110110 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Decimal | 7 | 26 | 28 | 36 | 55 | 29 | 54 | 58 | 62 | 54 |
| Letter | H | a | c | k | 3 | d | 2 | 6 | - | 2 |

This gave us **Hack3d26-2**. The remaining four board bits were 0000. Padding those to a sixth bit group would add an A, so we kept the ten-character message and recorded the four unused bits explicitly. The resulting link, [tinyurl.com/Hack3d26-2](https://tinyurl.com/Hack3d26-2), successfully redirected to `PI3MK2_K14.gcode`. That redirect checked our choice of reading order and message length.

<!-- page -->
# 3. Material specification

We found a square pattern inside the board at Y = 3.175 mm. Its three corner patterns suggested a QR code. Scanning the direct geometry drawing did not work because the physical squares had gaps between them.

We sampled the centers of its 25 by 25 modules. Their pitch was 14.2875 mm. We filled each sampled module, chose the readable polarity, and added a white border. A QR decoder then returned [tinyurl.com/Hack3d26](https://tinyurl.com/Hack3d26).

![The QR pattern after sampling the physical module centers.](evidence/qr_restored.png){height=220}

That link redirected to the official [AlF357 material data sheet](https://www.eos.info/var/assets/03_system-related-assets/material-related-contents/metal-materials-and-examples/metal-material-datasheet/aluminium/material_datasheet_eos_aluminium_alf357_premium_en.pdf). We identified the alloy as a beryllium-free A357 derivative, AlSi7Mg0.6. The sheet gives a powder size range of 20-90 um and a part density of 2.67 g/cm3.

| Item from the linked sheet | M 290 route | M 400 route |
| --- | --- | --- |
| Layer thickness | 30 um | 60 um |
| Volume rate | 5.8 mm3/s | 17 mm3/s |
| Atmosphere | Nitrogen | Nitrogen |
| Powder part number | 9011-0049 | 9011-0049 |

We also recorded its heat treatment: solution anneal at 540 +/- 6 C for 30 minutes, water quench, then age at 165 +/- 6 C for 6 hours and air cool. Aging starts within 40 hours. These are the linked sheet's process conditions, not settings we tested. We retain the official source link so its composition tables and system-specific conditions can be checked directly (pages 3, 5, 6 and 10).

<!-- page -->
# 4. Final height table

On the bottom of the board we found six rows labeled K, Q, R, B, Kn, and P. Each row had eight square positions. The two bottom levels were Y = -3.175 mm and Y = -1.905 mm. We treated the shallow positions as 1 and the deeper positions as 0.

| Piece | Eight-bit row | Value in cm | Height in mm |
| --- | --- | --- | --- |
| King | 00001001 | 9 | 90 |
| Queen | 00001000 | 8 | 80 |
| Rook | 00000101 | 5 | 50 |
| Bishop | 00000111 | 7 | 70 |
| Knight | 00000110 | 6 | 60 |
| Pawn | 00000101 | 5 | 50 |

We used the nearby ruler's cm label to interpret the values as heights in centimeters. The six row labels establish the piece order.

![The source geometry's labeled rows. We colored the shallow positions red for readability.](evidence/height_geometry.png){height=185}

We found another note below the diagram:

![The size note drawn directly from the model.](evidence/prototype_note.png)

This note matters because the supplied CAD and recovered toolpaths describe prototype parts. We therefore report the decoded heights separately from the files' current coordinate envelopes. Rotating an assembly also changes its bounding box, so a raw X, Y, or Z extent alone is not enough to identify a final piece height.

We did not assign new tolerances or resize the mechanism's pins, springs, and magnets. The files do not give us a tested way to apply all target sizes while preserving those fits. Our submission preserves the source geometry and provides the recovered target dimensions for that later manufacturing step.

<!-- page -->
# 5. Unlocking the pawn files

We found small lettering inside the rook near its base. We isolated the plane at Y = -2.54 mm and rotated the geometry view to make the line readable.

![The rook's encrypted line. Some letter counters merge in this flat face view.](evidence/rook_cipher.png)

Our transcription was:

`Zkdw lv wkh ehvw slhfh iru d sdzq wr wxuq lq wr?`

Moving each alphabetic character back three places gave us: **What is the best piece for a pawn to turn in to?** For example, Zkdw becomes What. We tried the answer **Queen**, with an uppercase Q. That exact password extracted both members of `Pawn Files.zip`, and Python's ZIP reader verified their CRC values.

We recovered `Pawn.STEP` and `Pawn Exploded View.pdf`. The STEP opened as 31 solid instances. The drawing is labeled QUEEN-PAWN and uses part labels Q1 through Q21. Its repeated part quantities add up to 31 printed pieces: Q1 and Q3 appear twice, and Q6 and Q13 appear five times. The other labels appear once.

### Hardware shown in the recovered drawing
| Item, as labeled | Quantity |
| --- | --- |
| N52 magnets, 1/4 x 3/16 inch | 2 |
| Springs, 0.3 x 3 x 5 mm | 2 |
| Spring, 0.6 x 8 x 50 mm | 1 |
| Pins, 1.5 x 6 mm | 5 |
| Pins, 1.5 x 18 mm | 2 |

The inch dimensions convert to 6.35 x 4.7625 mm for the magnets. We kept the drawing's original labels for the springs because it does not spell out the dimension convention. The next page shows the complete recovered exploded view. It supplies the assembly order and part positions that a simple outside pawn shape would leave out.

<!-- page -->
# 6. Recovered pawn assembly drawing

We kept the original PDF in the supporting files. This page reproduces its single page for reference. The source drawing credits Works by Design.

![The full Queen-Pawn exploded view from the decrypted archive.](evidence/pawn_exploded-1.png){height=555}

<!-- page -->
# 7. King internal inscription

The king contained a lattice and a narrow central body. Looking only at the outside hid the text on that body. We separated the central solid and drew its flat side, then enlarged the inscription to read its Drive file ID.

The inscription linked to [PI3MK2_King.gcode](https://drive.google.com/file/d/1Kk8K4bplqJWDCqiRtARlxXEeBVDJ-CKM/view). It also said: Metal Units produced using this method.

![Part of the enlarged inscription on the king's central body.](evidence/king_id.png)

We downloaded the file and read its commands as text. Our preview below uses its outer-wall extrusion moves. We reconstructed these lines for inspection and did not run them on a printer.

![Outer-wall paths in the recovered King G-code.](evidence/king_toolpath.png){height=285}

The file identifies a Prusa i3 MK2 profile and Cura settings. We found 0.2 mm nominal layers, a 215 C extruder setting, an 80 C bed setting, 10% infill, five top and bottom layers, and tree supports. Its header estimates 7,105 seconds and 4.34366 m of filament. These are slicer values, not measurements from a print.

The metal wording and the filament-style commands do not establish the same production process. We kept that distinction in our results. The board's QR supplies the alloy specification; this file supplies a prototype extrusion toolpath. We found normal heater-off commands at the end. We also found a small count mismatch: the header declares 337 layers, while the file contains 336 numbered layer sections, 0 through 335.

<!-- page -->
# 8. Original Knight model

The occupancy link led us to [PI3MK2_K14.gcode](https://drive.google.com/file/d/1vgwSromaUAm5hw45NycKgomDprsVD3Lu/view). We checked its actual commands against its header and found that the file stopped early.

| Check | King file | Knight file |
| --- | --- | --- |
| Header layer count | 337 | 177 |
| Numbered layer sections found | 336 | 78 |
| Last layer label | 335 | 77 |
| Header maximum Z | 67.15 mm | 34.95 mm |
| Highest motion Z found | 67.15 mm | 15.75 mm |
| Heater-off commands present | Yes | No |
| Non-G-code lines | 0 | 2 |

The knight file ends with a note, If Corrupted please refer to original model, followed by a [Drive link to Knight-Full Assm.step](https://drive.google.com/file/d/1b94MhZaxK8I5xzezqY1e8n1fdASWHZjL/view). We downloaded that model and opened all 61 solid instances. Its 24 STEP solid definitions include repeated assembly parts.

![The original Knight assembly recovered through the file's fallback link. Colors distinguish bodies in our preview.](evidence/knight_cad.png){height=265}

The original STEP is the useful recovery route here. Appending an ending to the partial G-code would not recover the missing shape in the upper layers. We include the G-code exactly as received, alongside the STEP and a machine-readable check summary. The same 0.2 mm, 215 C, 80 C and 10% infill settings appear in its saved Cura configuration, but they do not make the truncated paths complete.

<!-- page -->
# 9. Attempts, checks, and handoff

### Approaches that did not work

- Searching ordinary STEP strings found names and export information but no plaintext password. We switched to geometry inspection.
- Scanning the direct QR geometry image failed. Sampling module centers and filling the gaps produced a readable QR code.
- Our first row order read the positive-Z side first and produced YPu63d0kpx with four leftover bits. Checking the rank labels gave us the successful negative-Z-first order.
- Before finding the rook text, we tried 985765, Hack3d26, Hack3d26-2, and AlF357 as ZIP passwords. None worked. The rook clue led to Queen and a successful CRC check.
- Our first transcription of the king's long Drive ID had ambiguous letters and returned 404. We enlarged the geometric lettering and corrected the ID before downloading it.

These checks helped us avoid treating a readable-looking guess as a result. We verified each URL through its actual destination and each recovered CAD file by opening it.

### Repeating our analysis

We used Python 3.12 with the versions in `requirements.txt`. From the repository root, install the requirements and run:

`python src/analyze.py`

`python src/check_gcode.py`

`python src/preview_cad.py`

The first script recreates the geometry views, occupancy decode, QR decode, size rows, and pawn extraction. The second reads both G-code files and creates the check table and previews. The third reopens and previews the recovered assemblies. Our scripts use the supplied coordinate layout, so they are specific to this challenge. The manual inscriptions are inputs in a clearly labeled JSON file.

### What we are submitting

We provide this report, a code ZIP with the three original distribution files, and a supporting ZIP with the recovered manufacturing files, evidence images, and result tables. We also provide our 10-minute presentation and an overall `No Fix.zip` to match the wording in the problem statement. The upload guide maps these to the separate fields shown in the Google Form.

We checked hashes for the original and recovered files, opened the recovered STEP assemblies, and checked both ZIP members. We did not physically assemble, print, or measure a finished set. The target heights, prototype geometry, and supplied G-code should therefore remain separate records. Our source registry lists every recovered link, and `results/source_checksums.json` identifies the exact files we examined.
