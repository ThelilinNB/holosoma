def count_bvh_joints(file_path):
    joints = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('JOINT') or line.startswith('ROOT'):
                # 提取骨骼名称
                joint_name = line.split()[-1]
                joints.append(joint_name)
            if 'CHANNELS' in line:
                print(f"骨骼分量行: {line}")
            if 'MOTION' in line:
                break
    
    print(f"\n文件: {file_path}")
    print(f"检测到的总骨骼数: {len(joints)}")
    print(f"具体骨骼列表: {joints}")

# 替换成你的文件路径
count_bvh_joints("/home/ps/lpl/holosoma/src/holosoma_retargeting/holosoma_retargeting/demo_data/lafan_bvh/back_standard.bvh")