"""Make two geometry previews and check the recovered assemblies."""

from pathlib import Path
import json
import numpy as np
from analyze import mesh_step, triangles
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def king_cutaways():
    t = triangles(89)
    center = (t.reshape(-1, 3).min(0) + t.reshape(-1, 3).max(0)) / 2
    fig, axes = plt.subplots(1, 3, figsize=(18, 12))
    for j, (ax, clip) in enumerate(zip(axes, [None, 2, 0])):
        q = t if clip is None else t[np.all(t[:, :, clip] < center[clip] + 1e-4, axis=1)]
        a, b, c = (0, 1, 2) if j < 2 else (2, 1, 0)
        q = q[np.argsort(np.round(q[:, :, c].mean(1), 4), kind="stable")]
        normals = np.cross(q[:, 1] - q[:, 0], q[:, 2] - q[:, 0])
        normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-12)
        shade = np.clip(.82 * (.25 + .75 * np.abs(normals @ np.array([.3, .4, .8]))), .05, 1)
        ax.add_collection(PolyCollection(q[:, :, [a, b]], facecolors=np.repeat(shade[:, None], 3, axis=1),
                                        edgecolors="none", antialiased=False))
        ax.autoscale()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"solid 89, clip {clip}", color="black")
    fig.savefig("evidence/solid_89_cut.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def preview(filename, label, expected):
    folder = Path("work") / label.lower()
    parts = mesh_step(Path("recovered") / filename, folder)
    assert len(parts) == expected
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(projection="3d")
    all_points = []
    for i, part in enumerate(parts):
        data = np.load(folder / f"{i:03}.npz")
        v, f = data["vertices"], data["faces"]
        # The supplied assemblies use Z as their vertical axis.
        all_points.append(v)
        color = (0.70, 0.72, 0.73) if i % 4 else (0.71, 0.23, 0.26)
        ax.add_collection3d(Poly3DCollection(v[f], facecolors=[color], linewidth=0,
                                            edgecolor="none", shade=True,
                                            antialiased=False))
    points = np.concatenate(all_points)
    low, high = points.min(0), points.max(0)
    ax.set_xlim(low[0], high[0])
    ax.set_ylim(low[1], high[1])
    ax.set_zlim(low[2], high[2])
    ax.set_box_aspect(high-low)
    ax.view_init(elev=18, azim=-55)
    ax.set_axis_off()
    ax.set_title(label + f" recovered assembly ({len(parts)} solid instances)")
    fig.savefig(f"evidence/{label.lower()}_cad.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return {"file": filename, "solid_instances": len(parts),
            "mesh_min_mm": low.tolist(), "mesh_max_mm": high.tolist(),
            "note": "Mesh envelope in the source coordinate frame, not a final piece height."}


if __name__ == "__main__":
    king_cutaways()
    summaries = [preview("Pawn.STEP", "Pawn", 31),
                 preview("Knight-Full Assm.step", "Knight", 61)]
    Path("results/recovered_cad_checks.json").write_text(json.dumps(summaries, indent=2) + "\n")
