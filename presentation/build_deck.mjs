import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const build = path.join(here, 'build');
const output = path.join(here, 'output');
await fs.mkdir(build, { recursive: true });
await fs.mkdir(output, { recursive: true });
const notes = JSON.parse(await fs.readFile(path.join(here, 'notes.json'), 'utf8'));
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const font = 'Arial';
const ink = '#172529', red = '#B52C35', teal = '#1B5E63', paper = '#F7F5F0';

function text(slide, words, x, y, w, h, size = 28, color = ink, bold = false, family = font) {
  const box = slide.shapes.add({ geometry: 'textbox',
    position: { left: x, top: y, width: w, height: h },
    fill: 'none', line: { fill: 'none', width: 0 } });
  box.text = words;
  box.text.style = { typeface: family, fontSize: size, color, bold };
  return box;
}

async function image(slide, name, x, y, w, h, alt) {
  const data = await fs.readFile(path.join(root, 'evidence', name));
  slide.images.add({ blob: data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength),
    contentType: name.endsWith('.jpg') ? 'image/jpeg' : 'image/png',
    alt, fit: 'contain', position: { left: x, top: y, width: w, height: h } });
}

function table(slide, values, x, y, w, h, widths) {
  const tab = slide.tables.add({ rows: values.length, columns: values[0].length,
    left: x, top: y, width: w, height: h, values, columnWidths: widths });
  tab.borders.assign({ style: 'solid', fill: '#D5DDDA', width: 0.7 });
  for (let r = 0; r < values.length; r++) {
    tab.rows[r].height = h / values.length;
    for (let c = 0; c < values[0].length; c++) {
      const cell = tab.getCell(r, c);
      cell.fill = r === 0 ? teal : (r % 2 ? '#FFFFFF' : '#EDF0EB');
      cell.text.style = { typeface: font, fontSize: 24,
        color: r === 0 ? '#FFFFFF' : ink, bold: r === 0 };
    }
  }
  return tab;
}

function slide(index) {
  const s = deck.slides.add();
  s.background.fill = paper;
  if (index) text(s, notes[index].title, 64, 45, 1150, 80, 44, ink, true);
  text(s, 'No Fix', 64, 674, 300, 24, 16, '#687678');
  text(s, String(index + 1), 1160, 674, 65, 24, 16, '#687678');
  s.speakerNotes.text = `${notes[index].time}\n\n${notes[index].speech}\n\n中文提示：${notes[index].zh}\n\nSources:\n${notes[index].sources.join('\n')}`;
  return s;
}

let s = slide(0);
text(s, 'A simple game\nof Chess', 64, 170, 530, 175, 60, ink, true);
text(s, 'No Fix', 68, 402, 430, 56, 36, red, true);
text(s, 'CSAW 2026 Hack3D Final\nNovember 13, 2026', 68, 490, 470, 80, 27, '#465557');
await image(s, 'source_assembly.jpg', 610, 145, 610, 440, 'Chess scene in the supplied problem statement');

s = slide(1);
table(s, [['File', 'Our starting point'], ['Chess Board.STEP', 'Geometry and hidden clues'],
  ['Problem statement PDF', 'Task and submission requirements'], ['Pawn Files.zip', 'Encrypted CAD and drawing']],
  64, 175, 1150, 280, [490, 660]);
text(s, 'Our goal: recover the manufacturing information\nand explain how we found it.', 68, 500, 1100, 95, 32);

s = slide(2);
await image(s, 'solid_89_cut.png', 50, 140, 740, 500, 'Virtual views of the king exterior and clipped interior');
text(s, '129 solid instances\n37 repeated pawns', 825, 190, 380, 110, 32, teal, true);
text(s, 'We inspected internal faces.\n\nWe enlarged geometric text.\n\nWe recorded manual readings.', 825, 345, 370, 235, 27);

s = slide(3);
await image(s, 'qr_restored.png', 70, 160, 440, 440, 'QR pattern reconstructed from the 25 by 25 module centers');
text(s, '25 × 25 modules', 600, 175, 580, 65, 36, teal, true);
text(s, 'Direct scanning failed.\n\nWe sampled the centers and filled the gaps.', 600, 275, 575, 160, 29);
text(s, 'tinyurl.com/Hack3d26', 600, 465, 600, 55, 30, red, true);
text(s, 'AlF357 material specification', 600, 550, 600, 55, 30);

s = slide(4);
await image(s, 'occupancy.png', 52, 135, 590, 520, 'Occupied and empty squares, with rank 8 first');
text(s, 'Occupied = 1\nEmpty = 0', 720, 190, 470, 120, 36, teal, true);
text(s, '37 occupied squares\n27 empty squares', 720, 350, 470, 105, 30);
text(s, 'Rank 8 first\nFiles A through H', 720, 520, 470, 95, 30);

s = slide(5);
table(s, [['Six bits', 'Index', 'Letter'], ['000111', '7', 'H'], ['011010', '26', 'a'],
  ['011100', '28', 'c'], ['100100', '36', 'k']], 64, 190, 410, 300, [175, 115, 120]);
text(s, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789-_',
  540, 155, 670, 145, 28, teal, false, 'Courier New');
text(s, 'Hack3d26-2', 540, 345, 670, 85, 52, red, true);
text(s, 'tinyurl.com/Hack3d26-2', 540, 445, 670, 60, 29);
text(s, '60 message bits\n4 trailing zero bits', 540, 550, 670, 90, 28);

s = slide(6);
table(s, [['Piece', 'Binary row', 'Height (cm)'], ['King', '00001001', '9'],
  ['Queen', '00001000', '8'], ['Rook', '00000101', '5'], ['Bishop', '00000111', '7'],
  ['Knight', '00000110', '6'], ['Pawn', '00000101', '5']], 64, 165, 680, 385, [210, 260, 210]);
await image(s, 'height_geometry.png', 790, 160, 420, 290, 'Actual underside depth pattern and row labels');
text(s, 'The ruler gives cm.\n\nThe size note identifies\nthe CAD as prototype parts.', 800, 470, 400, 150, 27);

s = slide(7);
await image(s, 'rook_cipher.png', 64, 145, 1150, 95, 'Geometric ciphertext from inside the rook');
table(s, [['Shift -3', 'Result'], ['Zkdw', 'What']], 64, 300, 390, 125, [195, 195]);
text(s, 'What is the best piece for a pawn\nto turn in to?', 525, 295, 680, 110, 31);
text(s, 'Queen', 525, 450, 650, 85, 60, red, true);
text(s, 'Both archive members passed their CRC checks.', 68, 590, 1110, 65, 29);

s = slide(8);
text(s, '31 solid instances\n21 part labels', 64, 155, 620, 100, 35, teal, true);
table(s, [['Hardware label', 'Qty'], ['N52 magnets 1/4 × 3/16 in', '2'],
  ['Springs 0.3 × 3 × 5 mm', '2'], ['Spring 0.6 × 8 × 50 mm', '1'],
  ['Pins 1.5 × 6 mm', '5'], ['Pins 1.5 × 18 mm', '2']],
  64, 300, 620, 300, [525, 95]);
await image(s, 'pawn_exploded-1.png', 735, 130, 470, 510, 'Recovered Queen-Pawn exploded drawing, credited to Works by Design');

s = slide(9);
await image(s, 'king_toolpath.png', 50, 130, 575, 520, 'King outer-wall extrusion toolpath reconstructed from G-code');
text(s, 'PI3MK2_King.gcode', 670, 150, 540, 60, 34, teal, true);
table(s, [['Setting', 'Value'], ['Nominal layer', '0.2 mm'], ['Extruder', '215 C'], ['Bed', '80 C']],
  670, 250, 540, 205, [310, 230]);
text(s, '336 marked layers\n337 declared in the header', 670, 490, 540, 85, 28);
text(s, 'The inscription mentions metal.\nThe file contains filament commands.', 670, 590, 540, 65, 24);

s = slide(10);
await image(s, 'knight_cad.png', 45, 160, 470, 440, 'Recovered original Knight STEP assembly');
table(s, [['Check', 'King', 'Knight'], ['Header layers', '337', '177'],
  ['Marked sections', '336', '78'], ['Highest motion Z', '67.15 mm', '15.75 mm'],
  ['Heater-off ending', 'Present', 'Missing']], 535, 175, 680, 290, [285, 195, 200]);
text(s, 'The file ending supplies an original-model link.', 535, 510, 680, 75, 28);
text(s, 'Recovered STEP: 61 solid instances', 535, 600, 680, 55, 30, red, true);

s = slide(11);
table(s, [['Clue', 'Recovered result', 'Check'], ['Board QR', 'AlF357 specification', 'Valid redirect'],
  ['Bottom diagram', 'Six target heights', 'Rows and cm ruler'], ['Pawn positions', 'Knight G-code', '60-bit message'],
  ['Rook cipher', 'Pawn CAD and drawing', 'Queen opens ZIP'], ['King inscription', 'King G-code', 'Commands inspected'],
  ['Knight file ending', 'Original Knight STEP', '61 solid instances']],
  64, 155, 1150, 360, [340, 460, 350]);
text(s, 'Original files, analysis code, report, and evidence are included.', 68, 565, 1130, 65, 31);
text(s, 'Physical manufacturing and fit remain untested.', 68, 635, 1130, 35, 24, '#465557');

for (const [i, item] of deck.slides.items.entries()) {
  const png = await deck.export({ slide: item, format: 'png', scale: 1 });
  await fs.writeFile(path.join(build, `slide-${String(i + 1).padStart(2, '0')}.png`), new Uint8Array(await png.arrayBuffer()));
  console.log('Rendered slide', i + 1);
}
const candidate = path.join(build, 'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);

const skillDir = process.env.PRESENTATIONS_SKILL_DIR;
const runtimePython = process.env.ARTIFACT_PYTHON;
if (!skillDir || !runtimePython) throw new Error('Set PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON to the bundled runtime paths.');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const finalPath = path.join(output, process.argv[2] ?? 'No_Fix_10_Minute_Presentation.pptx');
const result = await finalizePresentation({ workspaceDir: root, candidatePath: candidate, finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit',
    ...[2, 6, 7, 8, 9, 10, 11, 12].flatMap(number => ['--require-native-table-slide', String(number)])],
  explicitTotalSlideCount: 12,
  requiredNativeTableOwnerSlides: [2, 6, 7, 8, 9, 10, 11, 12],
  requiredNativeChartOwnerSlides: [],
  fontPolicy: { basis: 'design', families: ['Arial', 'Courier New'] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(build, 'presentation.validation.json') });
console.log(JSON.stringify(result));
