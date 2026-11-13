import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const source = path.resolve(process.argv[2] ?? path.join(here, 'output/No_Fix_7_Minute_Final.pptx'));
const finalPath = path.resolve(process.argv[3] ?? path.join(here, 'output/No_Fix_7_Minute_Transitions.pptx'));
const skill = process.env.PRESENTATIONS_SKILL_DIR;
const python = process.env.ARTIFACT_PYTHON;
if (!skill || !python) throw new Error('Set PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON.');
const build = path.join(root, 'work/notes_transitions');
await fs.mkdir(build, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });

// Work on a snapshot so a PowerPoint save cannot change our input halfway through.
const snapshot = path.join(build, 'input_current.pptx');
const sourceBytes = await fs.readFile(source);
await fs.writeFile(snapshot, sourceBytes);
const sourceHash = createHash('sha256').update(sourceBytes).digest('hex');
const notes = JSON.parse(await fs.readFile(path.join(here, 'notes_transitions.json'), 'utf8'));
const presentation = await PresentationFile.importPptx(await FileBlob.load(snapshot));
if (presentation.slides.items.length !== notes.length) throw new Error('Slide count changed.');
for (let i = 0; i < notes.length; i++) {
  const n = notes[i];
  presentation.slides.items[i].speakerNotes.text =
    `Speaker ${n.speaker}, ${n.time}, ${n.seconds} seconds\n\n` +
    `ENGLISH\n${n.speech}\n\n中文讲稿\n${n.zh}\n\n` +
    `承接逻辑，排练参考，不朗读\n${n.logic_zh}\n\n` +
    `翻页与指图提示\n${n.cue_zh}\n\n` +
    `Q&A backup, not part of the timed speech\n${n.qa}\n\nSources\n${n.sources.join('\n')}`;
}
const authored = path.join(build, 'authored_notes.pptx');
await (await PresentationFile.exportPptx(presentation)).save(authored);

// The imported deck can normalize slide XML. Transfer just its notes paragraphs.
const candidate = path.join(build, 'candidate.pptx');
execFileSync(python, [path.join(root, 'src/merge_presentation_notes.py'), snapshot,
  authored, candidate, path.join(build, 'preservation.json')], { stdio: 'inherit' });
const { finalizePresentation } = await import(pathToFileURL(
  path.join(skill, 'container_tools/artifact_tool_utils.mjs')).href);
const owners = [4, 5, 6, 7, 9, 10, 11, 12];
await finalizePresentation({
  workspaceDir: root, candidatePath: candidate, finalPath,
  pythonExecutable: python,
  integrityValidatorPath: path.join(skill, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skill, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit',
    ...owners.flatMap(n => ['--require-native-table-slide', String(n)])],
  explicitTotalSlideCount: 12,
  requiredNativeTableOwnerSlides: owners,
  requiredNativeChartOwnerSlides: [],
  fontPolicy: { basis: 'reference', families: ['Times New Roman'],
    referencePath: snapshot, referenceSha256: sourceHash },
  verifyArtifactToolImport: true,
  receiptPath: path.join(build, 'finalization.json'),
});
const currentHash = createHash('sha256').update(await fs.readFile(source)).digest('hex');
if (currentHash !== sourceHash) throw new Error('Source changed during editing. Check its latest saved copy.');
console.log(JSON.stringify({ finalPath, sourceSha256: sourceHash, notes: notes.length }));
