"""
Diagnostic script: measure world Z heights of ankle-chain links for g1 and ym1
at flat-foot standing pose (all actuated joints = 0).

Goal: find which ym1 link, when placed at human_ankle_z (~0.15m scaled LAFAN),
naturally results in heel sphere at z=0 (flat-foot contact).

For g1, left_ankle_intermediate_1_link at z=? when flat foot (spheres at z=0)?
"""

import sys
import numpy as np
import mujoco

# ── paths ────────────────────────────────────────────────────────────────────
sys.path.insert(0, "src/holosoma_retargeting/holosoma_retargeting")

G1_XML  = "src/holosoma_retargeting/holosoma_retargeting/models/g1/g1_29dof.xml"
YM1_XML = "src/holosoma_retargeting/holosoma_retargeting/models/ym1/ym1_29dof.xml"

# ── helper ───────────────────────────────────────────────────────────────────
def get_link_z(model, data, link_name):
    try:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, link_name)
        if bid < 0:
            return None
        return data.xpos[bid][2]
    except Exception:
        return None

def analyse(xml_path, label, ankle_chain_links, heel_sphere_link):
    print(f"\n{'='*60}")
    print(f"  Robot: {label}")
    print(f"  XML:   {xml_path}")
    print(f"{'='*60}")

    model = mujoco.MjModel.from_xml_path(xml_path)
    data  = mujoco.MjData(model)

    # set all joints to 0 (flat-foot standing)
    data.qpos[:] = 0
    # identity quaternion for floating base
    data.qpos[3] = 1.0
    mujoco.mj_forward(model, data)

    # measure heel sphere z when all joints = 0
    heel_z = get_link_z(model, data, heel_sphere_link)
    print(f"\n  @ all-joints-zero:  {heel_sphere_link} z = {heel_z:.4f} m")

    # now find what height the floating base must be at for heel to be exactly at z=0
    # (i.e. shift the robot so heel_sphere z = 0)
    if heel_z is not None:
        shift = -heel_z
        data.qpos[2] += shift
        mujoco.mj_forward(model, data)
        print(f"  Shifted base by {shift:.4f} m → heel sphere now at z≈0")
        print(f"\n  Ankle-chain link world Z (flat-foot, heel at z=0):")
        for lname in ankle_chain_links:
            z = get_link_z(model, data, lname)
            tag = " ← Laplacian target" if "intermediate" in lname or "pitch_link" in lname else ""
            print(f"    {lname:45s}  z = {z:.4f} m{tag}")

    # also check what LAFAN ankle height is after scaling (typical)
    lafan_scale = 1.27 / 1.7   # default lafan scale
    human_ankle_z_typical = 0.092 * lafan_scale   # ~0.092m ankle height for 1.7m person
    print(f"\n  LAFAN LeftFoot (ankle) z typical (scaled {lafan_scale:.3f}): {human_ankle_z_typical:.4f} m")
    print()


# ── G1 ───────────────────────────────────────────────────────────────────────
analyse(
    G1_XML, "G1",
    ankle_chain_links=[
        "left_knee_link",
        "left_ankle_intermediate_1_link",    # ← currently mapped to LeftFoot
        "left_ankle_pitch_link",
        "left_ankle_roll_link",
        "left_ankle_roll_sphere_1_link",     # heel contact sphere
        "left_ankle_roll_sphere_5_link",     # toe sphere
    ],
    heel_sphere_link="left_ankle_roll_sphere_1_link",
)

# ── YM1 ──────────────────────────────────────────────────────────────────────
analyse(
    YM1_XML, "YM1",
    ankle_chain_links=[
        "left_knee_pitch_link",
        "left_ankle_pitch_link",             # ← currently mapped to LeftFoot
        "left_ankle_roll_link",
        "left_ankle_roll_sphere_1_link",     # heel contact sphere
        "left_ankle_roll_sphere_5_link",     # toe sphere
    ],
    heel_sphere_link="left_ankle_roll_sphere_1_link",
)
