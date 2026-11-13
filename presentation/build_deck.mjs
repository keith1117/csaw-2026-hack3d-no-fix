import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const filename = process.argv[2] ?? 'No_Fix_7_Minute_Final.pptx';
const build = path.join(here, 'build', path.parse(filename).name);
const output = path.join(here, 'output');
await fs.mkdir(build, { recursive: true });
await fs.mkdir(output, { recursive: true });
const notes = JSON.parse(await fs.readFile(path.join(here, 'notes.json'), 'utf8'));
const data = JSON.parse(await fs.readFile(path.join(root, 'results', 'decoded.json'), 'utf8'));
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const font = 'Times New Roman';
const black = '#000000', gray = '#EDEDEB', rule = '#C8C8C5', paleRed = '#E7BDBF';

function text(s, words, x, y, w, h, size = 28, bold = false, align = 'left') {
  const b = s.shapes.add({ geometry: 'textbox', name: words.slice(0, 55),
    position: { left: x, top: y, width: w, height: h },
    fill: 'none', line: { fill: 'none', width: 0 } });
  b.text = words;
  b.text.style = { typeface: font, fontSize: size, color: black, bold,
    alignment: align, verticalAlignment: 'middle', insets: 0 };
  return b;
}

function rect(s, x, y, w, h, fill = gray, stroke = 'none') {
  return s.shapes.add({ geometry: 'rect', position: { left: x, top: y, width: w, height: h },
    fill, line: { fill: stroke, width: stroke === 'none' ? 0 : 1.2 } });
}

function node(s, words, x, y, w, h, size = 25, fill = '#FFFFFF', bold = false) {
  const b = rect(s, x, y, w, h, fill, rule);
  b.text = words;
  b.text.style = { typeface: font, fontSize: size, color: black, bold,
    alignment: 'center', verticalAlignment: 'middle', insets: 3 };
  return b;
}

function connect(s, from, to, kind = 'straight') {
  return s.shapes.connect(from, to, { kind, fromSide: 'right', toSide: 'left',
    line: { fill: black, width: 1.7 }, tail: { type: 'triangle', width: 'sm', length: 'sm' } });
}

async function image(s, name, x, y, w, h, alt) {
  const bytes = await fs.readFile(path.join(root, 'evidence', name));
  s.images.add({ blob: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    contentType: name.endsWith('.jpg') ? 'image/jpeg' : 'image/png', alt, fit: 'contain',
    position: { left: x, top: y, width: w, height: h } });
}

function table(s, values, x, y, w, h, widths, size = 25) {
  const t = s.tables.add({ rows: values.length, columns: values[0].length,
    left: x, top: y, width: w, height: h, values, columnWidths: widths });
  t.borders.assign({ style: 'solid', fill: rule, width: .7 });
  for (let r = 0; r < values.length; r++) {
    t.rows[r].height = h / values.length;
    for (let c = 0; c < values[0].length; c++) {
      const cell = t.getCell(r, c);
      cell.fill = r === 0 ? gray : '#FFFFFF';
      cell.text.style = { typeface: font, fontSize: size, color: black, bold: r === 0,
        verticalAlignment: 'middle', insets: { left: 10, right: 8, top: 3, bottom: 3 } };
    }
  }
  return t;
}

function slide(i, source) {
  const s = deck.slides.add();
  s.background.fill = '#FFFFFF';
  if (i) {
    text(s, notes[i].title, 64, 45, 1150, 74, 43, true);
    rect(s, 64, 126, 1150, 1.2, rule);
  }
  text(s, source, 66, 674, 1050, 25, 17);
  text(s, `${i + 1} / 12`, 1115, 674, 100, 25, 17, false, 'right');
  s.speakerNotes.text = `Speaker ${notes[i].speaker}, ${notes[i].time}, ${notes[i].seconds} seconds\n\nENGLISH\n${notes[i].speech}\n\n中文讲稿\n${notes[i].zh}\n\n翻页与指图提示\n${notes[i].cue_zh}\n\nQ&A backup, not part of the timed speech\n${notes[i].qa}\n\nSources\n${notes[i].sources.join('\n')}`;
  return s;
}

let s = slide(0, 'CSAW 2026 Hack3D Final, November 13, 2026');
text(s, 'A simple game\nof Chess', 68, 183, 570, 180, 66, true);
text(s, 'No Fix', 72, 406, 450, 56, 38, true);
text(s, 'Recovering manufacturing information\nfrom a STEP chess assembly', 72, 495, 570, 100, 29);
await image(s, 'source_assembly.jpg', 650, 160, 565, 445, 'The chess assembly pictured in the supplied statement');

s = slide(1, 'Source: final report, overview and Sections 1-8');
text(s, 'Three inputs: Chess Board.STEP, problem statement, Pawn Files.zip', 68, 148, 1140, 44, 27);
const origin = node(s, 'STEP\nassembly', 68, 338, 190, 95, 31, gray, true);
const routes = [
  ['Board QR\nModule sampling', 'AlF357 material sheet'],
  ['Pawn positions\nSix-bit lookup', 'Knight G-code\nOriginal STEP via recovery note'],
  ['Bottom grid\nBinary rows and cm ruler', 'Six target heights'],
  ['Rook inscription\nCaesar shift and promotion clue', 'Pawn CAD and drawing'],
  ['King inscription\nRead the internal file link', 'King G-code']
];
for (let i = 0; i < routes.length; i++) {
  const y = 214 + i * 82;
  const clue = node(s, routes[i][0], 350, y, 330, 65, 24);
  const result = node(s, routes[i][1], 765, y, 445, 65, 25);
  connect(s, origin, clue, 'elbow');
  connect(s, clue, result);
}

s = slide(2, 'Source: final report, Section 1, pp. 2-3');
await image(s, 'solid_89_cut.png', 55, 161, 755, 425, 'King exterior and internal cutaways from the supplied geometry');
const steps = [['Text search', 'Part names, no plaintext answer'], ['Internal face views', 'Separate bodies and reveal inscriptions'],
  ['Manual readings and scripts', 'Read text, then sample and decode']];
for (let i = 0; i < steps.length; i++) {
  text(s, steps[i][0], 840, 180 + i * 133, 370, 44, 29, true);
  text(s, steps[i][1], 840, 229 + i * 133, 365, 65, 25);
}
text(s, '129 solid instances, including 37 placed Pawns', 80, 605, 1140, 43, 30, true);

s = slide(3, 'Source: final report, Section 3, pp. 6-7; official EOS AlF357 sheet');
text(s, 'Source geometry', 80, 150, 235, 40, 25, true);
text(s, 'Restored QR', 367, 150, 235, 40, 25, true);
await image(s, 'qr_geometry.png', 70, 204, 240, 240, 'Gapped physical QR faces before reconstruction');
await image(s, 'qr_restored.png', 360, 204, 240, 240, 'Filled modules with a four-module white border');
s.shapes.add({ geometry: 'rightArrow', position: { left: 318, top: 312, width: 35, height: 20 }, fill: black, line: { fill: 'none', width: 0 } });
text(s, '25 × 25 module centers', 83, 468, 510, 43, 30, true);
text(s, 'Direct scan failed. We filled the gaps\nand added a white border.', 83, 524, 515, 76, 26);
text(s, 'AlF357', 663, 151, 540, 62, 48, true);
text(s, 'A357 derivative, AlSi7Mg0.6', 665, 222, 545, 40, 28);
text(s, 'tinyurl.com/Hack3d26', 665, 270, 545, 35, 25);
table(s, [['EOS system', 'Layer', 'Volume rate'], ['M 290', '30 µm', '5.8 mm³/s'], ['M 400', '60 µm', '17 mm³/s']],
  660, 331, 550, 149, [180, 170, 200], 24);
text(s, 'Nitrogen, 20-90 µm powder\nPart density: 2.67 g/cm³', 665, 503, 545, 67, 24);
text(s, 'Heat treatment: 540 ±6 C for 30 min, water quench, then 165 ±6 C for 6 h.', 70, 613, 1145, 28, 23);
text(s, 'Start aging within 40 h. These are source specifications.', 70, 644, 1145, 25, 21);

s = slide(4, 'Source: final report, Section 2, pp. 4-5; occupancy computed from placed Pawn centers');
const gridValues = [['', ...'ABCDEFGH'], ...data.occupancy.map((row, i) => [String(8-i), ...row.map(String)])];
const grid = table(s, gridValues, 70, 170, 468, 468, Array(9).fill(52), 26);
grid.borders.assign({ style: 'solid', fill: '#FFFFFF', width: 1.3 });
for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) {
  const cell = grid.getCell(r, c);
  cell.fill = r === 0 || c === 0 ? '#FFFFFF' : (data.occupancy[r-1][c-1] ? paleRed : '#EFEDE7');
  cell.text.style = { typeface: font, fontSize: 26, color: black, bold: r === 0 || c === 0,
    alignment: 'center', verticalAlignment: 'middle', insets: 0 };
}
text(s, 'Occupied = 1, empty = 0', 628, 177, 580, 55, 35, true);
text(s, 'Rank 8 first\nA through H in each row', 628, 273, 575, 105, 33);
text(s, '37 occupied squares\n27 empty squares', 628, 414, 575, 85, 30);
text(s, 'Wrong row order gave YPu63d0kpx.\nThe engraved labels corrected our direction.', 628, 550, 580, 85, 25);

s = slide(5, 'Source: final report, Section 2, pp. 4-5; engraved alphabet and occupancy decode');
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
const chars = data.six_bit_groups.map(bits => alphabet[parseInt(bits, 2)]);
table(s, [['Six bits', 'Index', 'Character'], ...data.six_bit_groups.map((bits,i) => [bits, String(parseInt(bits,2)), chars[i]])],
  67, 151, 480, 474, [195, 135, 150], 25);
text(s, 'The engraved alphabet has 64 characters', 610, 165, 600, 52, 28, true);
text(s, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789-_', 610, 232, 595, 112, 27);
text(s, '000111 = 7, selecting H at index 7', 610, 367, 600, 46, 27);
text(s, 'Hack3d26-2', 610, 434, 600, 72, 52, true);
text(s, 'tinyurl.com/Hack3d26-2', 610, 517, 600, 42, 29);
text(s, '60 bits decoded. Four remaining zeros recorded.\nThe destination opened the Knight G-code.', 610, 584, 600, 65, 25);

s = slide(6, 'Source: final report, Section 4, pp. 8-9');
text(s, 'Shallow = 1, deep = 0', 68, 151, 650, 44, 30, true);
table(s, [['Piece', 'Binary row', 'cm', 'mm'], ...data.heights.map(h => [h.piece, h.binary, String(h.height_cm), String(h.height_mm)])],
  66, 216, 652, 350, [182, 230, 110, 130], 25);
await image(s, 'height_geometry.png', 765, 173, 445, 305, 'The six labeled shallow/deep source rows');
text(s, 'Ruler unit: cm', 775, 485, 435, 33, 26, true);
await image(s, 'cm_ruler.png', 772, 522, 435, 35, 'The source ruler supplies centimeters');
text(s, 'King: 8 + 1 = 9 cm = 90 mm', 68, 591, 660, 48, 30, true);
text(s, 'The prototype note keeps target heights\nseparate from the current CAD size.', 770, 575, 440, 74, 26);

s = slide(7, 'Source: final report, Section 5, p. 10; the supplied encrypted Pawn ZIP');
await image(s, 'rook_cipher.png', 70, 157, 1134, 83, 'The source ciphertext from inside the rook');
const before = node(s, 'Zkdw', 76, 291, 220, 76, 37);
const after = node(s, 'What', 448, 291, 220, 76, 37);
connect(s, before, after);
text(s, 'Shift -3', 316, 250, 120, 40, 26, true, 'center');
text(s, 'What is the best piece for a pawn\nto turn in to?', 75, 415, 690, 104, 34);
text(s, 'Queen', 833, 306, 355, 90, 62, true);
text(s, 'Case-sensitive password', 839, 413, 356, 42, 25);
text(s, 'Earlier guesses failed. The rook clue supplied the answer.', 78, 566, 1120, 45, 27);
text(s, 'Both archive members extracted and passed CRC checks.', 78, 617, 1120, 39, 30, true);

s = slide(8, 'Source: final report, Section 6, pp. 11-12; recovered drawing credited to Works by Design');
text(s, '31 solid instances', 70, 151, 650, 65, 42, true);
text(s, '21 labels with repeated quantities', 72, 227, 665, 43, 30);
table(s, [['Additional hardware', 'Qty'], ['N52 magnets, 1/4 × 3/16 inch', '2'], ['Springs, 0.3 × 3 × 5 mm', '2'],
  ['Spring, 0.6 × 8 × 50 mm', '1'], ['Pins, 1.5 × 6 mm', '5'], ['Pins, 1.5 × 18 mm', '2']],
  70, 314, 660, 283, [555, 105], 25);
text(s, 'Body count: 2 + 2 + 5 + 5 + 17 = 31', 73, 616, 660, 40, 27, true);
await image(s, 'pawn_exploded-1.png', 790, 143, 405, 506, 'The original Queen-Pawn exploded assembly drawing');

s = slide(9, 'Source: final report, Section 7, pp. 13-14; PI3MK2_King.gcode');
await image(s, 'king_id.png', 69, 150, 455, 65, 'Enlarged lettering used to correct an ambiguous Drive ID');
await image(s, 'king_toolpath.png', 60, 228, 477, 375, 'King outer-wall extrusion paths reconstructed from commands');
text(s, 'The enlarged ID corrected our first 404.', 70, 619, 490, 33, 24);
table(s, [['Command check', 'Observed result'], ['Layer sections', '336, header 337'], ['Maximum motion Z', '67.15 mm, matches header'],
  ['Heater-off commands', 'Present']], 586, 159, 625, 244, [280, 345], 25);
text(s, '0.2 mm layers, 215 C extruder, 80 C bed\n10% infill, tree supports, brim', 593, 438, 615, 86, 27);
rect(s, 588, 554, 621, 95, gray);
text(s, 'Inscription: metal production\nLinked file: filament extrusion commands', 604, 563, 590, 76, 28, true);

s = slide(10, 'Source: final report, Section 8, pp. 15-16; original model link inside Knight G-code');
table(s, [['Knight check', 'Header', 'Observed'], ['Layer sections', '177', '78'], ['Maximum Z', '34.95 mm', '15.75 mm']],
  67, 165, 590, 199, [260, 165, 165], 25);
text(s, 'No heater-off commands.\nAn ending comment did not restore missing paths.', 72, 386, 585, 85, 27);
const recovery = node(s, 'Recovery note\n“If Corrupted please refer\nto original model”', 74, 505, 548, 119, 28, gray);
const model = node(s, 'Original Knight STEP', 811, 587, 390, 52, 28);
connect(s, recovery, model, 'elbow');
await image(s, 'knight_cad.png', 758, 158, 455, 386, 'The recovered original Knight assembly');
text(s, '61 solid instances', 806, 531, 400, 46, 33, true);

s = slide(11, 'Source: final report, Section 9, pp. 17-18; decoded results and file checks');
table(s, [['Clue', 'Recovered information', 'Verification'], ['Board QR', 'AlF357 specification', 'Restored QR and destination'],
  ['Bottom grid', 'Six target heights', 'Labeled rows and cm ruler'], ['Pawn positions', 'Knight G-code', 'Six-bit decode and destination'],
  ['Rook inscription', 'Pawn CAD and drawing', 'Queen opens both ZIP members'], ['King inscription', 'King G-code', 'Header and command checks'],
  ['Knight recovery note', 'Original Knight STEP', '61 imported solid instances']],
  65, 157, 1148, 350, [290, 405, 453], 25);
text(s, 'We verified file hashes, decodes, archive contents, and CAD imports.', 72, 540, 1136, 46, 29, true);
text(s, 'Open points: four unused bits, the King count mismatch, and the metal wording.', 73, 596, 1136, 35, 24);
text(s, 'Physical printing, fit, and motion remain untested.', 73, 633, 1136, 31, 25);

for (const [i, item] of deck.slides.items.entries()) {
  const png = await deck.export({ slide: item, format: 'png', scale: 1 });
  await fs.writeFile(path.join(build, `slide-${String(i + 1).padStart(2, '0')}.png`), new Uint8Array(await png.arrayBuffer()));
  console.log('Rendered slide', i + 1);
}
const candidate = path.join(build, 'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
const skillDir = process.env.PRESENTATIONS_SKILL_DIR;
const python = process.env.ARTIFACT_PYTHON;
if (!skillDir || !python) throw new Error('Set PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON.');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const finalPath = path.join(output, filename);
const owners = [4, 5, 6, 7, 9, 10, 11, 12];
const receipt = await finalizePresentation({ workspaceDir: root, candidatePath: candidate, finalPath,
  pythonExecutable: python,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit',
    ...owners.flatMap(n => ['--require-native-table-slide', String(n)])],
  explicitTotalSlideCount: 12, requiredNativeTableOwnerSlides: owners, requiredNativeChartOwnerSlides: [],
  fontPolicy: { basis: 'design', families: [font] }, verifyArtifactToolImport: true,
  receiptPath: path.join(build, path.basename(finalPath) + '.validation.json') });
console.log(JSON.stringify(receipt));
