"""Our geometry checks for the CSAW 2026 Hack3D final. Run from the repo root."""

from pathlib import Path
import hashlib
import json
import os
import zipfile

os.environ.setdefault("MPLCONFIGDIR", "work/mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np
from PIL import Image
import zxingcpp
from OCP.BRep import BRep_Tool
from OCP.BRepGProp import BRepGProp
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.GProp import GProp_GProps
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID, TopAbs_REVERSED
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
for folder in ["work/meshes", "evidence", "results", "recovered"]:
    Path(folder).mkdir(parents=True, exist_ok=True)


def mesh_step(filename, folder):
    """OpenCascade reads STEP units as mm and applies the assembly placements."""
    reader = STEPControl_Reader()
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    reader.ReadFile(str(filename))
    reader.TransferRoots()
    solids = TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    rows = []
    while solids.More():
        solid = solids.Current()
        BRepMesh_IncrementalMesh(solid, 0.025, False, 0.22, True)
        faces = TopExp_Explorer(solid, TopAbs_FACE)
        vertices, triangles = [], []
        while faces.More():
            face = TopoDS.Face_s(faces.Current())
            location = TopLoc_Location()
            mesh = BRep_Tool.Triangulation_s(face, location)
            if mesh:
                offset = len(vertices)
                for i in range(1, mesh.NbNodes() + 1):
                    point = mesh.Node(i).Transformed(location.Transformation())
                    vertices.append([point.X(), point.Y(), point.Z()])
                for i in range(1, mesh.NbTriangles() + 1):
                    ids = list(mesh.Triangle(i).Get())
                    if face.Orientation() == TopAbs_REVERSED:
                        ids.reverse()
                    triangles.append([offset + j - 1 for j in ids])
            faces.Next()
        v, f = np.array(vertices), np.array(triangles)
        number = len(rows)
        np.savez_compressed(folder / f"{number:03}.npz", vertices=v, faces=f)
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(solid, props)
        c = props.CentreOfMass()
        rows.append({"solid": number, "min_mm": v.min(0).tolist(),
                     "max_mm": v.max(0).tolist(), "volume_mm3": props.Mass(),
                     "center_mm": [c.X(), c.Y(), c.Z()]})
        solids.Next()
        if len(rows) % 20 == 0:
            print("Meshed", len(rows), "solids", flush=True)
    return rows


def triangles(number):
    data = np.load(f"work/meshes/{number:03}.npz")
    return data["vertices"][data["faces"]]


def flat_faces(t, axis, level):
    same_plane = np.ptp(t[:, :, axis], axis=1) < 1e-6
    return t[same_plane & (abs(t[:, :, axis].mean(1) - level) < 1e-4)]


def picture(polygons, filename, limits=None, size=(20, 4)):
    fig, ax = plt.subplots(figsize=size)
    ax.add_collection(PolyCollection(polygons, facecolors="black", edgecolors="none",
                                     antialiased=False))
    ax.autoscale()
    if limits:
        ax.set_xlim(*limits[:2])
        ax.set_ylim(*limits[2:])
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig("evidence/" + filename, dpi=160, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def covers(q, x, z):
    """Test a projected point against the flat triangles (including their edges)."""
    a = q[:, 0]
    ab, ac = q[:, 1] - a, q[:, 2] - a
    ap = np.array([x, z]) - a
    den = ab[:, 0] * ac[:, 1] - ab[:, 1] * ac[:, 0]
    good = abs(den) > 1e-10
    u, v = np.zeros(len(q)), np.zeros(len(q))
    u[good] = (ap[good, 0] * ac[good, 1] - ap[good, 1] * ac[good, 0]) / den[good]
    v[good] = (ab[good, 0] * ap[good, 1] - ab[good, 1] * ap[good, 0]) / den[good]
    return good & (u >= -1e-8) & (v >= -1e-8) & (u + v <= 1 + 1e-8)


def caesar(text, shift):
    result = ""
    for char in text:
        base = ord("A") if char.isupper() else ord("a")
        result += chr((ord(char) - base + shift) % 26 + base) if char.isalpha() else char
    return result


def main():
    clues = json.loads(Path("results/transcribed_clues.json").read_text())
    cache = Path("work/geometry.json")
    geometry = json.loads(cache.read_text()) if cache.exists() else mesh_step("inputs/Chess Board.STEP", "work/meshes")
    cache.write_text(json.dumps(geometry, indent=2))
    # These solid numbers refer to this exact supplied assembly, not arbitrary STEP files.
    assert len(geometry) == 129
    board = triangles(0)
    edge = flat_faces(board, 1, 9.525)
    picture(edge[:, :, [2, 0]], "board_instruction.png", (-145, 165, 180, 190))
    alphabet = edge[:, :, [0, 2]].copy()
    alphabet[:, :, 0] *= -1
    picture(alphabet, "alphabet.png", (-95, 80, 184, 189))
    picture(edge[:, :, [2, 0]], "rank_labels_geometry.png", (-170, 190, -175, -165))

    # The highest engraved rank is on the negative-Z side of this assembly.
    occupancy = np.zeros((8, 8), dtype=int)
    pawn_positions = []
    for part in geometry[92:]:
        x, _, z = part["center_mm"]
        col = round((x + 139.7) / 42.8625)
        row = round((z + 139.7) / 42.8625)
        assert 0 <= row < 8 and 0 <= col < 8 and occupancy[row, col] == 0
        occupancy[row, col] = 1
        pawn_positions.append({"solid": part["solid"], "square": f"{chr(65+col)}{8-row}"})
    bits = "".join(str(n) for n in occupancy.ravel())
    groups = [bits[i:i+6] for i in range(0, 60, 6)]
    slug = "".join(clues["alphabet"][int(group, 2)] for group in groups)
    assert slug == "Hack3d26-2" and bits[60:] == "0000"
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(occupancy, cmap=matplotlib.colors.ListedColormap(["#eee9df", "#b52c35"]), vmin=0, vmax=1)
    ax.set_xticks(range(8), list("ABCDEFGH"))
    ax.set_yticks(range(8), list(range(8, 0, -1)))
    for row in range(8):
        for col in range(8):
            ax.text(col, row, str(occupancy[row, col]), ha="center", va="center",
                    color="white" if occupancy[row, col] else "#172529", fontsize=18)
    ax.set_title("Pawn occupancy, rank 8 first")
    fig.savefig("evidence/occupancy.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # The 25 x 25 QR pattern lies inside the board at Y = 3.175 mm.
    qr_faces = flat_faces(board, 1, 3.175)[:, :, [0, 2]]
    picture(qr_faces, "qr_geometry.png", size=(10, 10))
    centers = -157.1625 + np.arange(25) * 14.2875
    grid = np.zeros((25, 25), dtype=np.uint8)
    for row, z in enumerate(centers[::-1]):
        for col, x in enumerate(centers):
            grid[row, col] = np.any(covers(qr_faces, x, z))
    # Fill each physical module to remove the gaps between the machined squares.
    image = Image.fromarray(np.pad(1 - grid, 4, constant_values=1) * 255)
    image = image.resize((990, 990), Image.Resampling.NEAREST)
    image.save("evidence/qr_restored.png")
    decoded = zxingcpp.read_barcodes(image)
    assert len(decoded) == 1
    qr_url = decoded[0].text
    assert qr_url == "https://tinyurl.com/Hack3d26"

    # Six rows of shallow/deep squares form the piece height table.
    xcenters = -74.6125 + np.arange(8) * 30.1625
    zcenters = 171.45 - np.arange(6) * 30.1625
    shallow = flat_faces(board, 1, -1.905)[:, :, [0, 2]]
    height_bits = [[int(np.any(covers(shallow, x, z))) for x in xcenters] for z in zcenters]
    heights = [int("".join(map(str, row)), 2) for row in height_bits]
    assert heights == [9, 8, 5, 7, 6, 5]
    height_rows = [{"piece": label, "binary": "".join(map(str, row)), "height_cm": value,
                    "height_mm": value*10} for label, row, value in zip(clues["height_labels"], height_bits, heights)]
    labels = flat_faces(board, 1, 0.79375)[:, :, [0, 2]]
    picture(labels, "height_labels.png", size=(3, 14))
    fig, ax = plt.subplots(figsize=(12, 7))
    for level, color in [(-3.175, "#cccccc"), (-1.905, "#b52c35"), (0.79375, "black")]:
        q = flat_faces(board, 1, level)[:, :, [0, 2]]
        ax.add_collection(PolyCollection(q, facecolors=color, edgecolors="none", antialiased=False))
    ax.set_xlim(-140, 153)
    ax.set_ylim(5, 190)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig("evidence/height_geometry.png", dpi=180, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    picture(flat_faces(board, 1, 0.3175)[:, :, [0, 2]], "prototype_note.png")
    ruler = flat_faces(board, 1, -2.38125)[:, :, [2, 0]]
    picture(ruler, "cm_ruler.png", size=(20, 3))

    rook = flat_faces(triangles(91), 1, -2.54)[:, :, [0, 2]]
    points = rook.reshape(-1, 2)
    _, directions = np.linalg.eigh(np.cov(points.T))
    rook = (rook - points.mean(0)) @ directions[:, ::-1]
    rook[:, :, 0] *= -1
    picture(rook, "rook_cipher.png")
    question = caesar(clues["rook_cipher"], -3)
    with zipfile.ZipFile("inputs/Pawn Files.zip") as archive:
        for filename in ["Pawn Exploded View.pdf", "Pawn.STEP"]:
            data = archive.read("Pawn Files/" + filename, pwd=clues["pawn_password"].encode())
            Path("recovered", filename).write_bytes(data)  # read() checks the member CRC

    rod = triangles(90)
    front = flat_faces(rod, 2, rod[:, :, 2].min())[:, :, [1, 0]]
    front[:, :, 0] *= -1
    picture(front, "king_inscription.png")
    result = {"assembly_solid_instances": len(geometry), "pawn_count": int(occupancy.sum()),
              "occupancy": occupancy.tolist(), "pawn_squares": pawn_positions,
              "bits": bits, "six_bit_groups": groups, "padding_bits": bits[60:],
              "knight_url": "https://tinyurl.com/" + slug, "material_qr_url": qr_url,
              "heights": height_rows, "rook_decoded_question": question,
              "pawn_password": clues["pawn_password"], "king_inscription": clues["king_inscription"]}
    Path("results/decoded.json").write_text(json.dumps(result, indent=2) + "\n")
    files = sorted(Path("inputs").glob("*")) + sorted(Path("recovered").glob("*"))
    checksums = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in files if path.is_file()}
    Path("results/source_checksums.json").write_text(json.dumps(checksums, indent=2) + "\n")
    print("Decoded:", slug, qr_url, heights, question, "ZIP password:", clues["pawn_password"])


if __name__ == "__main__":
    main()
