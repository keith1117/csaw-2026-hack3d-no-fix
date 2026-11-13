"""Read the recovered G-code as text. This script never sends commands to a printer."""

from pathlib import Path
import json
import os
import re

os.environ.setdefault("MPLCONFIGDIR", "work/mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "Times New Roman", "text.color": "black",
                     "axes.labelcolor": "black", "axes.titlecolor": "black",
                     "xtick.color": "black", "ytick.color": "black"})
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)


def read_file(path):
    text = path.read_text()
    position = dict(X=0.0, Y=0.0, Z=0.0, E=0.0)
    absolute_xyz, absolute_e = True, True
    kind = ""
    outer_walls, layers, motion_z, invalid = [], [], [], []
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith(";TYPE:"):
            kind = line[6:]
        if line.startswith(";LAYER:"):
            layers.append(int(line[7:]))
        code = line.split(";")[0].strip()
        if not code:
            continue
        command = code.split()[0]
        values = {key: float(value) for key, value in re.findall(r"([XYZEFST])(-?\d+(?:\.\d+)?)", code)}
        if command == "G90":
            absolute_xyz = True
        elif command == "G91":
            absolute_xyz = False
        elif command == "M82":
            absolute_e = True
        elif command == "M83":
            absolute_e = False
        elif command == "G92":
            position.update({k: v for k, v in values.items() if k in position})
        elif command in ["G0", "G1"]:
            previous = position.copy()
            for axis in position:
                if axis in values:
                    absolute = absolute_e if axis == "E" else absolute_xyz
                    position[axis] = values[axis] if absolute else position[axis] + values[axis]
            motion_z.append(position["Z"])
            if (command == "G1" and position["E"] > previous["E"]
                    and kind == "WALL-OUTER"
                    and (position["X"], position["Y"]) != (previous["X"], previous["Y"])):
                outer_walls.append([[previous[k] for k in "XYZ"], [position[k] for k in "XYZ"]])
        elif not re.fullmatch(r"[GMT]\d+", command):
            invalid.append({"line": number, "text": line})

    def header(name):
        match = re.search(r"^;" + name + r":([^\n]+)", text, re.M)
        return match.group(1) if match else None

    settings_text = "".join(re.findall(r"^;SETTING_3 (.*)$", text, re.M))
    settings = json.loads(settings_text) if settings_text else {}
    summary = {
        "filename": path.name, "header_layer_count": int(header("LAYER_COUNT")),
        "observed_layer_count": len(layers), "first_layer": min(layers), "last_layer": max(layers),
        "header_max_z_mm": float(header("MAXZ")), "observed_motion_max_z_mm": max(motion_z),
        "nominal_layer_height_mm": float(header("Layer height")),
        "slicer_time_seconds": int(header("TIME")), "header_filament_m": header("Filament used"),
        "extruder_setpoints_c": sorted(set(map(float, re.findall(r"^M10[49] S(\d+)", text, re.M)))),
        "bed_setpoints_c": sorted(set(map(float, re.findall(r"^M1[49]0 S(\d+)", text, re.M)))),
        "extruder_shutdown_present": bool(re.search(r"^M104 S0\b", text, re.M)),
        "bed_shutdown_present": bool(re.search(r"^M140 S0\b", text, re.M)),
        "non_gcode_lines": invalid, "embedded_links": re.findall(r"https?://\S+", text),
        "cura_settings": settings,
    }
    return summary, np.array(outer_walls)


def preview(segments, label):
    # Rendering a subset keeps the preview small. The summary uses the whole file.
    step = max(1, len(segments) // 45000)
    shown = segments[::step]
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(projection="3d")
    colors = plt.cm.viridis(shown[:, :, 2].mean(1) / max(segments[:, :, 2].max(), 1))
    ax.add_collection3d(Line3DCollection(shown, colors=colors, linewidths=0.35))
    bounds = segments.reshape(-1, 3)
    low, high = bounds.min(0), bounds.max(0)
    ax.set_xlim(low[0], high[0])
    ax.set_ylim(low[1], high[1])
    ax.set_zlim(0, high[2])
    ax.set_box_aspect(high - np.minimum(low, [low[0], low[1], 0]))
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.view_init(elev=24, azim=-58)
    ax.set_title(label + " outer-wall extrusion paths")
    fig.savefig("evidence/" + label.lower() + "_toolpath.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    summaries = []
    for filename, label in [("PI3MK2_King.gcode", "King"), ("PI3MK2_K14.gcode", "Knight")]:
        summary, segments = read_file(Path("recovered") / filename)
        summaries.append(summary)
        preview(segments, label)
        print(filename, "layers:", summary["observed_layer_count"], "max motion Z:",
              summary["observed_motion_max_z_mm"], "non-code lines:", len(summary["non_gcode_lines"]))
    Path("results/gcode_checks.json").write_text(json.dumps(summaries, indent=2) + "\n")
