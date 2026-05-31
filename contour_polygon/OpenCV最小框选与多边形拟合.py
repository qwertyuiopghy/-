import cv2
import numpy as np
from pathlib import Path

# ==========================================
# 1. 工程初始化
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
IMAGE_NAME = "test3.png"
IMAGE_PATH = BASE_DIR / IMAGE_NAME

image = cv2.imread(str(IMAGE_PATH))
if image is None:
    raise FileNotFoundError(f"【FATAL ERROR】图像文件加载失败，请检查路径: {IMAGE_PATH}")

contour_image = image.copy()
final_image = image.copy()
height, width = image.shape[:2]

# ==========================================
# 2. 原生色彩空间重建 (极限抗干扰版)
# ==========================================
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# ① 提取光晕 (Halo)：保持不变
lower_halo = np.array([93, 50, 150])
upper_halo = np.array([102, 142, 255])
mask_halo = cv2.inRange(hsv, lower_halo, upper_halo)

# ② 提取光源内核 (Core)：【核心修正】将亮度 (V) 下限从 200 暴涨到 240！
# 彻底秒杀白纸、灰白布料等环境反光，只保留真正过曝的 LED 发光像素
lower_core = np.array([0, 0, 240])
upper_core = np.array([179, 60, 255])
mask_core = cv2.inRange(hsv, lower_core, upper_core)

mask = cv2.bitwise_or(mask_halo, mask_core)

# ③ ROI 掩膜过滤：【核心修正】
# 将左侧边界往里收 (0.20)，将底部边界往上抬 (0.82)，物理屏蔽左侧布料边缘和左下角主板反光
roi_mask = np.zeros_like(mask)
roi_mask[int(0.08 * height):int(0.82 * height), int(0.20 * width):int(0.85 * width)] = 255
mask = cv2.bitwise_and(mask, roi_mask)

# ==========================================
# 3. 结构化形态学处理
# ==========================================
kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)

# ==========================================
# 4. 几何拟合与严格包裹
# ==========================================
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 10 or area > 5000:
        continue

    epsilon = 0.03 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    vertex_num = len(approx)

    if 4 <= vertex_num <= 12:
        rotated_rect = cv2.minAreaRect(cnt)
        (cx, cy), (rw, rh), angle = rotated_rect

        if rw * rh == 0:
            continue

        # 【核心修正】严格收紧长宽比 (0.4 到 2.5)
        # 拒绝所有细长条的误检目标（比如那块很高的布料侧边）
        aspect_ratio = rw / float(rh)
        if 0.4 <= aspect_ratio <= 2.5:
            box_points = np.int32(cv2.boxPoints(rotated_rect))

            cv2.drawContours(contour_image, [cnt], -1, (0, 255, 0), 1)
            cv2.drawContours(final_image, [box_points], 0, (0, 0, 255), 1)

# ==========================================
# 5. 工业级输出
# ==========================================
cv2.imwrite(str(BASE_DIR / "1_Contours_Pro.png"), contour_image)
cv2.imwrite(str(BASE_DIR / "2_FinalBox_Pro.png"), final_image)

print(">>> [SUCCESS] 已清除布料与金属反光误检。")

stacked_display = np.hstack((contour_image, final_image))
resized_display = cv2.resize(stacked_display, (0, 0), fx=0.7, fy=0.7)

cv2.imshow("PRO MODE | Left: Raw Contours | Right: Clean Bounding", resized_display)
cv2.waitKey(0)
cv2.destroyAllWindows()