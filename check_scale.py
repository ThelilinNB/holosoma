import os

def check_bvh_scale(file_path):
    print(f"\n{'='*50}")
    print(f"🔍 正在扫描文件: {file_path}")
    print(f"{'='*50}")
    
    if not os.path.exists(file_path):
        print("❌ 文件不存在，请检查路径。")
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 我们来找 'LeftLeg' (小腿) 相对于 'LeftUpLeg' (大腿) 的偏移量，也就是大腿的物理长度
    for i, line in enumerate(lines):
        if "JOINT LeftLeg" in line or "JOINT CC_Base_L_Calf" in line:
            # 找到关节后，往下找两行内必定有 OFFSET
            for j in range(i+1, i+4):
                if "OFFSET" in lines[j]:
                    parts = lines[j].strip().split()
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    # 计算这根骨头的真实长度 (勾股定理)
                    length = (x**2 + y**2 + z**2)**0.5
                    
                    print(f"🦴 找到大腿骨骼数据 -> OFFSET: X={x}, Y={y}, Z={z}")
                    print(f"📏 大腿物理长度: {length:.4f} 个单位")
                    print("-" * 50)
                    
                    if length > 10:
                        print("💡 [终极结论]: 长度几十，单位绝对是 **厘米 (cm)**！")
                        print("   ✅ 在 extract_global_positions.py 中必须使用: / 100")
                    elif length > 0.1 and length < 2:
                        print("💡 [终极结论]: 长度零点几，单位绝对是 **米 (m)**！")
                        print("   🚨 警告：在 extract_global_positions.py 中千万不能 / 100，直接原样保存！")
                    else:
                        print("💡 [终极结论]: 尺度异常，请人工核对。")
                    return

if __name__ == "__main__":
    # 检查 LAFAN 官方参考文件
    lafan_path = "/home/ps/lpl/holosoma/src/holosoma_retargeting/holosoma_retargeting/demo_data/lafan_bvh/aiming1_subject1.bvh"
    check_bvh_scale(lafan_path)
    
    # 检查你自己刚刚烘焙导出的文件
    your_path = "/home/ps/lpl/holosoma/src/holosoma_retargeting/holosoma_retargeting/demo_data/lafan_bvh/back_standard.bvh"
    check_bvh_scale(your_path)