"""Copy authored notes into an existing PPTX without changing its slides."""

from pathlib import Path
import argparse
import copy
import json
import posixpath
from xml.dom import minidom
from zipfile import ZipFile

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def targets(z, part):
    parent, name = posixpath.split(part)
    rel = posixpath.join(parent, "_rels", name + ".rels")
    doc = minidom.parseString(z.read(rel))
    return {n.getAttribute("Id"): (
        n.getAttribute("Type"),
        posixpath.normpath(posixpath.join(parent, n.getAttribute("Target"))).lstrip("/")
    ) for n in doc.getElementsByTagName("Relationship")}


def ordered_notes(z):
    part = "ppt/presentation.xml"
    rels = targets(z, part)
    doc = minidom.parseString(z.read(part))
    result = []
    for slide in doc.getElementsByTagNameNS(P, "sldId"):
        slide_part = rels[slide.getAttributeNS(R, "id")][1]
        matches = [dest for kind, dest in targets(z, slide_part).values()
                   if kind.endswith("/notesSlide")]
        assert len(matches) == 1, slide_part
        result.append(matches[0])
    return result


def note_body(doc):
    for shape in doc.getElementsByTagNameNS(P, "sp"):
        placeholders = shape.getElementsByTagNameNS(P, "ph")
        if any(p.getAttribute("type") == "body" for p in placeholders):
            return shape.getElementsByTagNameNS(P, "txBody")[0]
    raise ValueError("Notes body placeholder was not found")


def merge(source, authored, output, record):
    with ZipFile(source) as original, ZipFile(authored) as updated:
        before, after = ordered_notes(original), ordered_notes(updated)
        assert len(before) == len(after) == 12
        replacements = {}
        for dest, src in zip(before, after):
            doc = minidom.parseString(original.read(dest))
            body = note_body(doc)
            new_body = note_body(minidom.parseString(updated.read(src)))
            for node in list(body.childNodes):
                if node.namespaceURI == A and node.localName == "p":
                    body.removeChild(node)
            for node in new_body.childNodes:
                if node.namespaceURI == A and node.localName == "p":
                    body.appendChild(doc.importNode(node, deep=True))
            replacements[dest] = doc.toxml(encoding="UTF-8")
        with ZipFile(output, "w") as out:
            out.comment = original.comment
            for info in original.infolist():
                out.writestr(copy.copy(info), replacements.get(info.filename, original.read(info)))
        with ZipFile(output) as result:
            changed = [n for n in original.namelist()
                       if original.read(n) != result.read(n)]
            assert set(changed) == set(before), changed
            assert result.testzip() is None
        Path(record).write_text(json.dumps({
            "changed_parts": changed,
            "unchanged_parts": len(original.namelist()) - len(changed),
            "all_non_notes_parts_identical": True
        }, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ("source", "authored", "output", "record"):
        parser.add_argument(name)
    args = parser.parse_args()
    merge(args.source, args.authored, args.output, args.record)
