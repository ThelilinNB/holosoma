import mujoco, numpy as np
m = mujoco.MjModel.from_xml_path("src/holosoma_retargeting/holosoma_retargeting/models/ym1/ym1_29dof.xml")
d = mujoco.MjData(m)
data = np.load("demo_results/ym1/robot_only/lafan/back_standard.npz")
qa = data["q_a"]
qr = data["q_r"]
frame = 200
print(f"qa shape: {qa.shape}")
# print("qr:", qr[frame])
# print("qa:", qa[frame])
d.qpos[:3] = qr[frame][:3]
d.qpos[3:7] = qr[frame][3:] if qr.shape[1]>=7 else [1,0,0,0]
# YM1 has 29 Actuators? Let's check nq
# actuatordata is for actuators. qpos is for joints.
# The retargeter config says how many actuated joints
# Actually just print the xpos of left and right ankle directly from the retargeter outputs
# Wait, interaction mesh retargeter saves q_a. What is the order?
# We can just run it...
d.qpos[7:7+qa.shape[1]] = qa[frame]
mujoco.mj_forward(m, d)
l = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "left_ankle_roll_link")
r = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "right_ankle_roll_link")
print(f"L Y: {d.xpos[l][1]:.4f}")
print(f"R Y: {d.xpos[r][1]:.4f}")
print(f"Diff: {d.xpos[l][1] - d.xpos[r][1]:.4f}")
