import cv2
import numpy as np
import math
from pathlib import Path


def nothing(x): pass


# 计算矩形真实的倾斜角度（相对于垂直方向）
def get_tilt_angle(rect):
    (w, h) = rect[1]
    angle = rect[2]
    if w > h:
        angle += 90
    return angle % 180


# ==========================================
# 1. 视频与调试控制台初始化
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
VIDEO_NAME = "实验测试原视频.mp4"
VIDEO_PATH = BASE_DIR / VIDEO_NAME

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    raise FileNotFoundError(f"【FATAL ERROR】视频加载失败: {VIDEO_PATH}")

# 获取原视频的帧率和尺寸 (因为要做逆时针旋转，所以宽和高互换)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or math.isnan(fps): fps = 30.0
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
rotated_size = (original_height, original_width)

# 初始化视频写入器 (保存成品视频)
OUTPUT_PATH = str(BASE_DIR / "Result_Output.mp4")
out = cv2.VideoWriter(OUTPUT_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, rotated_size)

cv2.namedWindow('Debugger Panel', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Debugger Panel', 450, 400)

# 核心参数滑动条
cv2.createTrackbar('Halo Brightness', 'Debugger Panel', 130, 255, nothing)
cv2.createTrackbar('Halo Saturation', 'Debugger Panel', 100, 255, nothing)
cv2.createTrackbar('Min Area', 'Debugger Panel', 30, 1000, nothing)
cv2.createTrackbar('Min Aspect Ratio', 'Debugger Panel', 12, 50, nothing)
cv2.createTrackbar('Max Aspect Ratio', 'Debugger Panel', 80, 150, nothing)
cv2.createTrackbar('Armor Max Width', 'Debugger Panel', 50, 100, nothing)

print(">>> [操作说明]")
print(">>> 1. 刚开始请按【空格键】暂停画面。")
print(">>> 2. 调节滑动条，直到右侧杂光消失，且红框稳定。")
print(">>> 3. 按【空格键】继续播放，播放过程中会自动录制并保存结果！")
print(f">>> 4. 按 'q' 键退出，成品视频将保存在: {OUTPUT_PATH}")

paused = False

# 预先读取第一帧作为启动时的底图
ret, current_frame = cap.read()
if ret:
    current_frame = cv2.rotate(current_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
else:
    raise ValueError("无法读取视频的第一帧。")

# ==========================================
# 2. 视频流循环处理
# ==========================================
while True:
    if not paused:
        ret, frame_read = cap.read()
        if not ret:
            print(">>> [INFO] 视频处理完毕，正在保存...")
            break
        # 【核心修复】：物理正骨必须放在这里！只在新画面进来时旋转一次！
        current_frame = cv2.rotate(frame_read, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # 每一帧的计算和绘画，都基于干净的 current_frame 副本
    final_image = current_frame.copy()
    hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

    # 获取实时参数
    halo_v_min = cv2.getTrackbarPos('Halo Brightness', 'Debugger Panel')
    halo_s_min = cv2.getTrackbarPos('Halo Saturation', 'Debugger Panel')
    min_area = cv2.getTrackbarPos('Min Area', 'Debugger Panel')
    min_ratio = cv2.getTrackbarPos('Min Aspect Ratio', 'Debugger Panel') / 10.0
    max_ratio = cv2.getTrackbarPos('Max Aspect Ratio', 'Debugger Panel') / 10.0
    armor_max_width = cv2.getTrackbarPos('Armor Max Width', 'Debugger Panel') / 10.0

    # ==========================================
    # === 图像预处理 (色彩净化) ===
    # ==========================================
    lower_halo = np.array([90, halo_s_min, halo_v_min])
    upper_halo = np.array([130, 255, 255])
    mask_halo = cv2.inRange(hsv, lower_halo, upper_halo)

    lower_core = np.array([90, 20, 230])
    upper_core = np.array([130, 255, 255])
    mask_core = cv2.inRange(hsv, lower_core, upper_core)

    mask = cv2.bitwise_or(mask_halo, mask_core)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # ==========================================
    # === 第一阶段：寻找独立灯条候选人 (绿框) ===
    # ==========================================
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    light_bars = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area or area > 5000:
            continue

        rect = cv2.minAreaRect(cnt)
        (cx, cy), (w, h), angle = rect
        if w == 0 or h == 0: continue

        light_length = max(w, h)
        light_width = min(w, h)
        aspect_ratio = light_length / light_width

        box = np.int32(cv2.boxPoints(rect))

        if min_ratio < aspect_ratio < max_ratio:
            light_bars.append({'center': (cx, cy), 'length': light_length, 'rect': rect})
            cv2.drawContours(final_image, [box], 0, (0, 255, 0), 2)

    # ==========================================
    # === 第二阶段：灯条严格配对 (大红框) ===
    # ==========================================
    num_bars = len(light_bars)
    for i in range(num_bars):
        for j in range(i + 1, num_bars):
            bar1 = light_bars[i]
            bar2 = light_bars[j]

            dy = abs(bar1['center'][1] - bar2['center'][1])
            dx = abs(bar1['center'][0] - bar2['center'][0])
            distance = math.sqrt(dx ** 2 + dy ** 2)
            avg_length = (bar1['length'] + bar2['length']) / 2.0

            angle1 = get_tilt_angle(bar1['rect'])
            angle2 = get_tilt_angle(bar2['rect'])
            angle_diff = abs(angle1 - angle2)
            if 15 < angle_diff < 165:
                continue

            if dy > avg_length * 0.8: continue
            if abs(bar1['length'] - bar2['length']) / avg_length > 0.6: continue

            if 1.0 < (distance / avg_length) < armor_max_width:
                box1 = np.int32(cv2.boxPoints(bar1['rect']))
                box2 = np.int32(cv2.boxPoints(bar2['rect']))
                combined_points = np.vstack((box1, box2))

                armor_rect = cv2.minAreaRect(combined_points)
                armor_box = np.int32(cv2.boxPoints(armor_rect))

                cv2.drawContours(final_image, [armor_box], 0, (0, 0, 255), 3)

                armor_cx = int((bar1['center'][0] + bar2['center'][0]) / 2)
                armor_cy = int((bar1['center'][1] + bar2['center'][1]) / 2)
                cv2.circle(final_image, (armor_cx, armor_cy), 5, (0, 255, 255), -1)

    # ==========================================
    # === 录制与显示 ===
    # ==========================================
    # 核心：仅在正常播放状态下，将最终处理后的帧存入视频文件
    if not paused:
        out.write(final_image)

    scale = 0.6
    display_frame = cv2.resize(final_image, (0, 0), fx=scale, fy=scale)
    display_mask = cv2.cvtColor(cv2.resize(mask, (0, 0), fx=scale, fy=scale), cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((display_frame, display_mask))

    # 左上角显示当前状态（方便你确认是暂停还是正在录制）
    status_text = "PAUSED (Tune parameters!)" if paused else "RECORDING..."
    color = (0, 0, 255) if paused else (0, 255, 0)
    cv2.putText(stacked, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("PRO Armor Debugger | SPACE to Pause/Play", stacked)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'): break
    if key == ord(' '): paused = not paused

# 释放资源并保存视频
cap.release()
out.release()
cv2.destroyAllWindows()
print(f">>> [SUCCESS] 视频处理完成，成品已保存至: {OUTPUT_PATH}")